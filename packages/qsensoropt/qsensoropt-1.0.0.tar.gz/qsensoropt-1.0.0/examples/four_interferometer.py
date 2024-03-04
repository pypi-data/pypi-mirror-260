#!/usr/bin/env python3
from typing import Callable, List, Optional, \
    Tuple

from tensorflow import cast, \
    gather, concat, reshape, expand_dims, \
        squeeze, print, zeros, argsort,  ones, \
            tensor_scatter_nd_update, gather_nd, \
                Variable, Tensor
from tensorflow.math import exp, log, abs, minimum, \
    reciprocal_no_nan, round, floormod
from tensorflow.random import stateless_categorical, \
    Generator, uniform
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import get_memory_info
from numpy import ceil, sqrt, zeros, savetxt, pi
from numpy.random import rand
from math import floor as mfloor
from argparse import ArgumentParser
from os.path import join

from qsensoropt import StatelessPhysicalModel, \
    StatelessMetrology, InverseSqrtDecay, ParticleFilter, \
        Parameter, Control, SimulationParameters, PhysicalModel
from qsensoropt.utils import train, \
    performance_evaluation, get_seed, store_input_control, \
        standard_model, denormalize, get_seed, random_uniform


def true_model(angles: Tensor):
    r"""Returns the true outcome probabilities for
    a batch of angles :math:`\vec{\varphi} = (\varphi_1,
    \varphi_2, \varphi_3)`.

    Parameters
    ----------
    angles: Tensor
        `Tensor` of shape (`bs`, 3) containing
        the values of the angles in the interferometer.
    
    Returns
    -------
    prob: Tensor
        `Tensor` of shape (`bs`, 10) containing
        the probabilities of the 10 possible
        photon counting measurement outcomes.
    """
    phi1 = cast(angles[:, 0:1], dtype="complex64")
    phi2 = cast(angles[:, 1:2], dtype="complex64")
    phi3 = cast(angles[:, 2:3], dtype="complex64")
    prob0 = abs(exp(2j*phi1)+exp(2j*phi2)-exp(2j*phi3)+\
                2*exp(1j*phi3)-2*exp(1j*(phi1+phi2))-1)**2/128
    prob1 = abs(exp(2j*phi1)+exp(2j*phi2)+exp(2j*phi3)-\
                2*exp(1j*phi3)-2*exp(1j*(phi1+phi2))+1)**2/64
    prob2 = abs(exp(2j*phi1)+exp(2j*phi2)-exp(2j*phi3)+\
                2*exp(1j*phi3)-2*exp(1j*(phi1+phi2))-1)**2/128
    prob3 = abs(exp(2j*phi1)-exp(2j*phi2)-exp(2j*phi3)+1)**2/64
    prob4 = abs(exp(2j*phi1)-exp(2j*phi2)+exp(2j*phi3)-1)**2/64
    prob5 = abs(exp(2j*phi1)+exp(2j*phi2)-exp(2j*phi3)-\
                2*exp(1j*phi3)+2*exp(1j*(phi1+phi2))-1)**2/128
    prob6 = abs(exp(2j*phi1)-exp(2j*phi2)+exp(2j*phi3)-1)**2/64
    prob7 = abs(exp(2j*phi1)-exp(2j*phi2)-exp(2j*phi3)+1)**2/64
    prob8 = abs(exp(2j*phi1)+exp(2j*phi2)+exp(2j*phi3)+\
                2*exp(1j*phi3)+2*exp(1j*(phi1+phi2))+1)**2/64
    prob9 = abs(exp(2j*phi1)+exp(2j*phi2)-exp(2j*phi3)-\
                2*exp(1j*phi3)+2*exp(1j*(phi1+phi2))-1)**2/128
    return concat([
        prob0, prob1, prob2, prob3, prob4, prob5, prob6,
        prob7, prob8, prob9], 1,
        )

class FourArmsInterferometer(StatelessPhysicalModel):
    """Physical model for a four arm interferometer
    with three controllable phases and two
    photon inputted in the first two modes.
    """
    def __init__(
            self, batchsize: int,
            params: List[Parameter],
            prec: str = "float64",
            ):
        controls = [
            Control(name="c1"),
            Control(name="c2"),
            Control(name="c3"),
        ]
        super().__init__(
            batchsize, controls, params, prec=prec,
        )

        self.phys_model_network = true_model

    def perform_measurement(
            self, controls: Tensor,
            parameters: Tensor,
            meas_step: Tensor,
            rangen: Generator,
            ) -> Tuple[Tensor, Tensor]:
        logprob = log(
            self.phys_model_network(
                squeeze(parameters-controls),
            )+1e-33,
        )
        outcomes = reshape(stateless_categorical(
            logprob, 1, get_seed(rangen), dtype="int32",
        ), (self.bs, 1, 1), )
        loglikelihood_outcomes = gather_nd(
            logprob, outcomes, batch_dims=1,
        )
        return cast(outcomes, dtype=self.prec), \
            loglikelihood_outcomes

    def model(
            self, outcomes: Tensor, controls: Tensor,
            parameters: Tensor, meas_step: Tensor,
            num_systems: int = 1,
            ) -> Tensor:
        angles_reshaped = reshape(
            parameters-controls,
             (self.bs*num_systems, 3),
        )
        outcomes_reshaped = reshape(
            outcomes, (self.bs*num_systems, 1, 1))
        prob = gather_nd(
            self.phys_model_network(angles_reshaped),
            cast(round(outcomes_reshaped), dtype="int32"),
            batch_dims=1,
        )
        return reshape(prob, (self.bs, num_systems, ))
    
    def count_resources(
            self, resources: Tensor, controls: Tensor,
            true_values: Tensor, meas_step: Tensor,
            ) -> Tensor:
        return resources+1.0
    

class FourArmsSimulation(StatelessMetrology):
    r"""Simulation object for the four
    arms interferometer with 
    input state :math:`|1100\rangle`."""
    def __init__(
            self, particle_filter: ParticleFilter,
            phys_model: PhysicalModel,
            control_strategy: Callable,
            simpars: SimulationParameters,
            cov_weight_matrix: Optional[List] = None,
            median: bool = False,
            random: bool = False,
            loss_normalization: bool = False,
            ):
        super().__init__(
            particle_filter, phys_model,
            control_strategy,
            simpars, cov_weight_matrix,
            )
        
        self.median = median
        self.random = random
        self.loss_normalization = loss_normalization

        if self.random:
            self.input_size += 3
            self.input_name += ["c1r", "c2r", "c3r", ]

    def generate_input(
            self, weights: Tensor, particles: Tensor,
            meas_step: Tensor, used_resources: Tensor,
            rangen: Generator,
            ) -> Tensor:
        old_input = super().generate_input(
            weights, particles, meas_step,
            used_resources, rangen,
            )
        if self.random:
            first_control = expand_dims(random_uniform(
                self.bs, self.simpars.prec, 0, 2*pi,
                get_seed(rangen),
                ), axis=1,
            )
            second_control = expand_dims(random_uniform(
                self.bs, self.simpars.prec, 0, 2*pi,
                get_seed(rangen),
                ), axis=1,
            )
            third_control = expand_dims(random_uniform(
                self.bs, self.simpars.prec, 0, 2*pi,
                get_seed(rangen),
                ), axis=1,
            )
            return concat(
                [old_input, first_control,
                 second_control, third_control], 1,
                )
        else:
            return old_input

    def loss_function(
            self, weights: Tensor, particles: Tensor,
            true_values: Tensor, used_resources: Tensor,
            meas_step: Tensor
            ):
        pars = self.simpars
        old_losses = super().loss_function(
            weights, particles, true_values,
            used_resources, meas_step,
        )
        if self.loss_normalization:
            init_var = 0
            for param in self.pf.phys_model.params:
                bounds = param.bounds
                init_var += 1/12*(bounds[1]-bounds[0])**2
            eta = minimum(
                2.5*reciprocal_no_nan(used_resources),
                init_var*ones((self.bs, 1), dtype=pars.prec),
            )
            old_losses = old_losses/eta
        if self.median:
            losses =  squeeze(old_losses)
            indices = argsort(losses)
            median_index = reshape(
                indices[mfloor(self.bs/2)], (1, 1),
            )
            mask = tensor_scatter_nd_update(
                zeros((self.bs, ), dtype=pars.prec),
                median_index,
                ones((1, ), dtype=pars.prec),
                name = "median_loss_mask"
            )
            return expand_dims(self.bs*mask*losses, axis=1)
        else:
            return old_losses

        
def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir", type=str,
                        default="./four_interferometer/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./four_interferometer/data")
    parser.add_argument("--prec", type=str, default="float32")
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument("--num-steps", type=int, default=100)
    parser.add_argument("--iterations", type=int, default=2048)

    return parser.parse_args()

def three_phase_estimation(
    args, batchsize: int,
    num_particles: int,
    learning_rate: float = 1e-2,
    gradient_accumulation: int = 1,
    cumulative_loss: bool = True,
    cov_weight_matrix: Optional[List] = None,
    phase_bounds: Tuple[float, float] = (0.0, pi),
    static: bool = True,
    neural_network: bool = True,
):
    """Estimation of the three phases in the interferometer.
    """

    four_interferometer = FourArmsInterferometer(
        batchsize=batchsize,
        params=[
            Parameter(bounds=phase_bounds, name="phi1"),
            Parameter(bounds=phase_bounds, name="phi2"),
            Parameter(bounds=phase_bounds, name="phi3"),
        ],
        prec=args.prec,
    )
 
    particle_filter = ParticleFilter(
        num_particles=num_particles,
        phys_model=four_interferometer,
        resample_fraction=0.98,
        prec=args.prec,
    )

    name = f"four_interferometer_num_part_{num_particles}"

    # NN strategy
    # ----------------------------------------------

    if neural_network:
        input_size = 17
        control_size = 3

        network = standard_model(
            input_size=input_size,
            controls_size=control_size,
            neurons_per_layer=args.n,
            prec=args.prec,
        )
        network.compile()

        simpars_nn = SimulationParameters(
            sim_name=f"{name}_mean",
            num_steps=args.num_steps,
            max_resources=args.num_steps,
            prec=args.prec,
            cumulative_loss=cumulative_loss,
        )

        sim_nn = FourArmsSimulation(
            particle_filter=particle_filter,
            simpars=simpars_nn,
            phys_model=four_interferometer,
            control_strategy=lambda x: 2*pi*network(x),
            median=False,
            random=False,
            loss_normalization=True,
        )

        decaying_learning_rate = InverseSqrtDecay(
            learning_rate, args.prec,
        )

        train(
        sim_nn, Adam(
            learning_rate=decaying_learning_rate),
        args.iterations, args.scratch_dir,
        gradient_accumulation=gradient_accumulation,
        network=network,
        xla_compile=False,
        )

        network.save(
            join(args.trained_models_dir, str(sim_nn)),
        )
        # network=load_model(
        #     join(args.trained_models_dir, str(sim_nn)),
        #     )

        simpars_median = SimulationParameters(
            sim_name=f"{name}_median",
            num_steps=args.num_steps,
            max_resources=args.num_steps,
            prec=args.prec,
            cumulative_loss=cumulative_loss,
        )

        sim_median = FourArmsSimulation(
            particle_filter=particle_filter,
            simpars=simpars_median,
            phys_model=four_interferometer,
            control_strategy=lambda x: floormod(network(x), 2*pi),
            median=True,
            random=False,
            loss_normalization=False,
            cov_weight_matrix=cov_weight_matrix
        )

        simpars_mean = SimulationParameters(
            sim_name=f"{name}_mean",
            num_steps=args.num_steps,
            max_resources=args.num_steps,
            prec=args.prec,
            cumulative_loss=cumulative_loss,
        )

        sim_mean = FourArmsSimulation(
            particle_filter=particle_filter,
            simpars=simpars_mean,
            phys_model=four_interferometer,
            control_strategy=lambda x: floormod(network(x), 2*pi),
            median=False,
            random=False,
            loss_normalization=False,
            cov_weight_matrix=cov_weight_matrix
        )

        performance_evaluation(
        sim_median, args.iterations, args.data_dir,
        delta_resources=1.0,
        y_label='MedianSE',
        xla_compile=True
        )

        store_input_control(
        sim_median, args.data_dir, 5,
        xla_compile=True
        )

        performance_evaluation(
        sim_mean, args.iterations, args.data_dir,
        delta_resources=1.0,
        y_label='MSE',
        xla_compile=True
        )

        store_input_control(
        sim_mean, args.data_dir, 5,
        xla_compile=True
        )

    # Random strategy
    #----------------------------------------------------

    simpars_random = SimulationParameters(
        sim_name=f"{name}_random_mean",
        num_steps=args.num_steps,
        max_resources=args.num_steps,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
    )

    sim_random = FourArmsSimulation(
        particle_filter=particle_filter,
        simpars=simpars_random,
        phys_model=four_interferometer,
        control_strategy=lambda x: x[:, -3:],
        median=False,
        random=True,
        loss_normalization=False,
        cov_weight_matrix=cov_weight_matrix
    )

    simpars_random_median = SimulationParameters(
        sim_name=f"{name}_random_median",
        num_steps=args.num_steps,
        max_resources=args.num_steps,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
    )

    sim_random_median = FourArmsSimulation(
        particle_filter=particle_filter,
        simpars=simpars_random_median,
        phys_model=four_interferometer,
        control_strategy=lambda x: x[:, -3:],
        median=True,
        random=True,
        loss_normalization=False,
        cov_weight_matrix=cov_weight_matrix
    )

    performance_evaluation(
       sim_random, args.iterations, args.data_dir,
       delta_resources=1.0,
       y_label='MSE',
       xla_compile=True
    )

    store_input_control(
       sim_random, args.data_dir, 5,
       xla_compile=True
    )

    performance_evaluation(
       sim_random_median, args.iterations, args.data_dir,
       delta_resources=1.0,
       y_label='MedianSE',
       xla_compile=True
    )

    store_input_control(
       sim_random_median, args.data_dir, 5,
       xla_compile=True
    )

    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)

    # Static simulation
    # --------------------------------------------------

    if static:
        # Initial value of the controls
        # in the static optimization
        initial_state = zeros((int(args.num_steps), 3))
        for i in range(int(args.num_steps)):
            initial_state[i, :] = rand()
            
        static_variables = Variable(
            initial_state, dtype=args.prec,
            )

        def static_control(input_tensor: Tensor):
            return gather(
                    params=2*pi*static_variables,
                    indices=cast(
                round(denormalize(input_tensor[:, -1],
                                  (0, args.num_steps))),
                dtype="int32"),
                )
        
        simpars_static = SimulationParameters(
            sim_name=f"{name}_static_mean",
            num_steps=args.num_steps,
            max_resources=args.num_steps,
            prec=args.prec,
            cumulative_loss=cumulative_loss,
        )
        
        sim_static = FourArmsSimulation(
            particle_filter=particle_filter,
            simpars=simpars_static,
            # True model for the extraction of the outcomes
            phys_model=four_interferometer,
            control_strategy=static_control,
            median=False,
            random=False,
            loss_normalization=True,
            cov_weight_matrix=cov_weight_matrix
        )

        decaying_learning_rate = InverseSqrtDecay(
            1e-2, args.prec
        )

        train(
            sim_static,
            Adam(learning_rate=decaying_learning_rate),
            args.iterations, args.scratch_dir,
            custom_controls=static_variables,
            xla_compile=True,
            gradient_accumulation=gradient_accumulation,
        )
        
        # print(get_memory_info('GPU:0')['peak']/1024**3)

        savetxt(
            join(args.trained_models_dir, str(sim_static)),
                static_variables.numpy()
                )
        
        simpars_static_mean = SimulationParameters(
            sim_name=f"{name}_static_mean",
            num_steps=args.num_steps,
            max_resources=args.num_steps,
            prec=args.prec,
            cumulative_loss=cumulative_loss,
        )
        
        sim_static_mean = FourArmsSimulation(
            particle_filter=particle_filter,
            simpars=simpars_static_mean,
            # True model for the extraction of the outcomes
            phys_model=four_interferometer,
            control_strategy=static_control,
            median=False,
            random=False,
            loss_normalization=False,
            cov_weight_matrix=cov_weight_matrix
        )

        simpars_static_median = SimulationParameters(
            sim_name=f"{name}_static_median",
            num_steps=args.num_steps,
            max_resources=args.num_steps,
            prec=args.prec,
            cumulative_loss=cumulative_loss,
        )
        
        sim_static_median = FourArmsSimulation(
            particle_filter=particle_filter,
            simpars=simpars_static_median,
            # True model for the extraction of the outcomes
            phys_model=four_interferometer,
            control_strategy=static_control,
            median=True,
            random=False,
            loss_normalization=False,
            cov_weight_matrix=cov_weight_matrix
        )

        performance_evaluation(
        sim_static_median, args.iterations, args.data_dir,
        delta_resources=1.0,
        y_label='MedianSE',
        xla_compile=True
        )

        store_input_control(
        sim_static_median, args.data_dir, 5,
        xla_compile=True
        )

        performance_evaluation(
        sim_static_mean, args.iterations, args.data_dir,
        delta_resources=1.0,
        y_label='MSE',
        xla_compile=True
        )

        store_input_control(
        sim_static_mean, args.data_dir, 5,
        xla_compile=True
        )

def main():

    args = parse_args()

    three_phase_estimation(
        args, 256, 2048,
        learning_rate=1e-2,
        gradient_accumulation=1,
        cumulative_loss=True,
        phase_bounds=(0.0, pi),
    )

    three_phase_estimation(
        args, 64, 4096,
        learning_rate=1e-2,
        gradient_accumulation=4,
        cumulative_loss=True,
        phase_bounds=(0.0, pi),
        static=True,
        neural_network=True,
    )

    three_phase_estimation(
        args, 32, 8192,
        learning_rate=1e-2,
        gradient_accumulation=4,
        cumulative_loss=True,
        phase_bounds=(0.0, pi),
        static=True,
        neural_network=True,
    )

    three_phase_estimation(
        args, 32, 16384,
        learning_rate=1e-2,
        gradient_accumulation=4,
        cumulative_loss=True,
        phase_bounds=(0.0, pi),
        static=False,
        neural_network=False,
    )

    three_phase_estimation(
        args, 32, 24000,
        learning_rate=1e-2,
        gradient_accumulation=4,
        cumulative_loss=True,
        phase_bounds=(0.0, pi),
        static=False,
        neural_network=False,
    )

    three_phase_estimation(
        args, 32, 32768,
        learning_rate=1e-2,
        gradient_accumulation=4,
        cumulative_loss=True,
        phase_bounds=(0.0, pi),
        static=False,
        neural_network=False,
    )
    
if __name__ == "__main__":
    main()