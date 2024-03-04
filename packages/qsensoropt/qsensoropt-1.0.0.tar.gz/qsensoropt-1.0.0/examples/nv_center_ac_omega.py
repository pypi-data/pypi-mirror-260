#!/usr/bin/env python3
from typing import Callable, Literal, \
    List, Tuple

from tensorflow import cast, ones, \
    gather, reshape, norm, expand_dims, \
        concat, where, broadcast_to, \
            Variable, stop_gradient, Tensor
from tensorflow.math import exp, cos, sin, \
    abs, round, log, equal, reduce_sum, \
        reciprocal_no_nan, sqrt, argmax, cumsum
from tensorflow.random import Generator, stateless_uniform
from tensorflow.linalg import trace, diag_part
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import \
    get_memory_info
from numpy import zeros, savetxt
from numpy.random import rand
from argparse import ArgumentParser
from itertools import product
from os.path import join
from math import pi

from qsensoropt import InverseSqrtDecay, \
    ParticleFilter, Parameter, SimulationParameters, \
    StatelessSimulation, StatelessPhysicalModel, Control
from qsensoropt.utils import train, \
    performance_evaluation, store_input_control, \
        denormalize, standard_model, normalize, get_seed

class NVCenterPiPulse(StatelessPhysicalModel):
    r"""The optimal time interval between the
    application of two pi-pulses is independent
    of the magnetic field. The intensity of the field
    enters only in the total duration of the measurement,
    i.e. how much it takes to accumulate 2pi phase.
    """
    def __init__(
        self, batchsize: int, params: List[Parameter],
        prec: Literal["float64", "float32"] = "float64",
        res: Literal["meas", "time"] = "meas",
        max_pulse_number: int = 50,
        ):
        r"""Constructor
        of the :py:obj:`~.NVCenter` class.

        Parameters
        ----------
        batchsize: int
            Batchsize of the simulation, i.e. number of
            estimations executed simultaneously.
        params: List[:py:obj:`~.Parameter`]
            List of unknown parameters to estimate in
            the NV center experiment, with their
            respective bounds. 
        prec : {"float64", "float32"}
            Precision of the floating point operations in the 
            simulation.
        res: {"meas", "time"}
            Resource type for the present metrological task, 
            can be either the total evolution time, i.e. `time`,
            or the total number of Ramsey measurement on
            the spin, i.e. `meas`.
        max_pulse_number: int = 50
            Maximum number of pi-pulses applied.
        """
        self.max_pulse_number = max_pulse_number
        controls = [
            Control(name=f"EvolutionTime{i}") \
                for i in range(max_pulse_number)
        ]
        controls += [Control(name="Phase"), ]

        assert res=="meas" or res=="time"
        
        super().__init__(
            batchsize, controls, params,
            prec=prec,
        )

        self.res = res

    def perform_measurement(
        self, controls: Tensor, parameters: Tensor,
        meas_step: Tensor,
        rangen: Generator,
        ):
        r"""Ramsey measurement on the NV center.
        
        The spin is measured after having evolved in the
        magnetic field for a time specified by the parameter
        `control`. The possible outcomes
        are :math:`+1` and :math:`-1`,
        selected stochastically according to the probabilities
        :math:`p(\pm 1| \vec{\theta}, \tau)`, where :math:`\tau` is the
        evolution time (the control) and :math:`\vec{\theta}`
        the parameters to estimate (the magnetic field
        or the magnetic field and the decoherence time,
        typically). It returns the outcomes
        and the log-likelihood of the observed outcomes.
        The probability :math:`p(\pm 1| \vec{\theta}, \tau)`
        must be returned by the :py:meth:`model` method.
        """
        list_plus = ones((self.bs, 1, 1), dtype=self.prec)
        prob_plus = self.model(
            list_plus, controls, parameters, meas_step,
            )
        # Extraction of the actual outcomes
        seed = get_seed(rangen)
        outcomes = 2*cast((stateless_uniform((self.bs, 1),
                        seed, dtype=self.prec) <
                        stop_gradient(abs(prob_plus))),
                        dtype="int8") - 1
        outcomes = cast(
            expand_dims(outcomes, axis=1),
            dtype=self.prec, name="outcomes",
            )
        prob_outcomes = self.model(
            outcomes, controls, parameters, meas_step,
            )
        log_prob = cast(
            log(prob_outcomes),
            dtype=self.prec, name="log_prob",
            )
        return outcomes, log_prob

    def count_resources(
        self, resources: Tensor, controls: Tensor,
        true_values: Tensor, meas_step: Tensor,
        ):
        """The resources can be either the
        number of measurements, or the total
        evolution time, according to the
        attribute `res` of the :py:obj:`NVCenter`
        class.
        """
        if self.res == "time":
            return resources+reduce_sum(
                    abs(controls[:, 0:self.max_pulse_number]),
                    axis=1, keepdims=True,
                )
        return resources+1.0

class NVCenterACMagnetometryOmega(NVCenterPiPulse):
    """Hypothesis testing for the frequency with
    magnetic field intensity as nuisance parameter
    inspired by
    https://www.nature.com/articles/s41534-021-00391-5.

    The study of this model may have
    applications in the search for dark matter
    (axions and dark photons) with NV center
    magnetometry http://arxiv.org/abs/2302.12756.

    The parameter structure of this problem
    is that of the Dolinar receiver.
    """
    def __init__(
        self, batchsize: int, params: List[Parameter],
        prec: Literal["float64", "float32"] = "float64",
        res: Literal["meas", "time"] = "meas",
        invT2: float = 0.0,
        max_pulse_number: int = 50,
        ):
        r"""Constructor of the
        :py:obj:`~.NVCenterACMagnetometryOmega` class.

        Parameters
        ----------
        batchsize: int
            Batchsize of the simulation, i.e. number of estimations
            executed simultaneously.
        params: List[:py:obj:`~.Parameter`]
            List of unknown parameters to estimate in
            the NV center experiment, with their
            respective bounds. It should contain the intensity of the
            magnetic field `B` and the frequency `omega`, with they
            respective admissible bounds.
        prec : {"float64", "float32"}
            Precision of the floating point operations in the 
            simulation.
        res: {"meas", "time"}
            Resource type for the present metrological task, 
            can be either the total evolution time, i.e. `time`,
            or the total number of Ramsey measurements on
            the spin, i.e. `meas`.
        invT2: float = 0.0
            Inverse of the transverse relaxation time
            of the NV center.
        """
        super().__init__(
            batchsize, params, prec=prec, res=res,
            max_pulse_number=max_pulse_number,
        )

        self.invT2 = invT2

    def model(
        self, outcomes: Tensor, controls: Tensor,
        parameters: Tensor, meas_step: Tensor,
        num_systems: int = 1,
        ):
        r"""Model for the outcomes of a Ramsey measurement
        on a spin that has been precessing in an
        oscillating magnetic field of unknown intensity
        :math:`B` and unknown frequency
        :math:`omega`. The probability of getting the
        outcome :math:`+1` is

        .. math::

            p(+1|\omega, B, \tau) := e^{-\frac{\tau}{T_2}}
            \cos^2 \left[ \frac{B}{2 \omega} \sin( \omega \tau) 
            \right] + \frac{1-e^{-\frac{\tau}{T_2}}}{2} \; .

        The evolution time :math:`\tau` is controlled
        by the trainable agent.
        The parameter :math:`T_2` is the attribute `invT2`
        of the :py:obj:`NVCenterACMagnetometryOmega` class.
        """
        evolution_time = cumsum(
            controls[:, :, 0:self.max_pulse_number], axis=2,
            )
        phase_control = controls[:, :, -1]
        B_field = parameters[:, :, 0]
        omega = parameters[:, :, 1]
        invT2 = self.invT2
        exp_decay = exp(-evolution_time[:, :, -1]*invT2)
        ramsey_out = outcomes[:, :, 0]
        # Phase accumulation
        acc_phase =  sin(omega*evolution_time[:, :, 0])
        for i in range(1, self.max_pulse_number):
            acc_phase += ((-1)**i)*(sin(omega*evolution_time[:, :, i])-\
                sin(omega*evolution_time[:, :, i-1]))
        noise_less = (1.0-ramsey_out*cos( \
            B_field/omega*acc_phase+phase_control))/2.0
        return exp_decay*noise_less + (1.0-exp_decay)/2.0
        
class FrequencyTesting(StatelessSimulation):
    """ 
    """
    def __init__(
            self, particle_filter: ParticleFilter,
            phys_model: NVCenterACMagnetometryOmega,
            control_strategy: Callable,
            simpars: SimulationParameters,
            extraction_flag: bool = False,
            cov_flag: bool = False,
            ):
        r"""Constructor
        of the :py:obj:`~.FrequencyTesting` class.

        Parameters
        ----------
        particle_filter: :py:obj:`~.ParticleFilter`
            Particle filter responsible for the update
            of the Bayesian posterior on the parameters
            and on the state of the probe.
        phys_model: :py:obj:`~.NVCenterACMagnetometryOmega`
            Abstract description of the parameter
            encoding and of the measurement on the
            spin.
        control_strategy: Callable
            Callable object (normally a
            function or a lambda function) that
            computes the values of the controls
            for the next measurement from
            the `Tensor` `input_strategy`.
        simpars: :py:obj:`~.SimulationParameters`
            Contains the flags and parameters
            that regulate the stopping
            condition of the measurement loop
            and modify the loss function used in the
            training.
        extraction_flag: bool = False
            If `extraction_flag=True` a couple of
            particles are sampled from the posterior
            and added to the `input_strategy` `Tensor`.
            This is useful to simulate the PGH control for
            the evolution time, which prescribes the
            evolution time of :eq:`PGH_tau`.
        cov_flag: bool = False
            If `cov_flag=True` a flattened version of the
            covariance matrix of the particle filter
            ensemble is added to the `input_strategy` `Tensor`.
            This is useful to simulate the :math:`\sigma^{-1}`
            control strategy and its variant that accounts
            for a finite transversal relaxation time.
            The control times prescribed by these
            strategies is described in the documentation of
            the :py:obj:`~.Magnetometry` class, in :eq:`cov_1`
            and :eq:`cov_2`.
        """
        self.extraction_flag = extraction_flag
        self.cov_flag = cov_flag
        # Set the input size
        d = particle_filter.d
        input_size = 8
        # Set the name of each column of the input
        input_name = ["Mean0", "Log_Dev_0", "Prob_0", 
                "Mean1", "Log_Dev_1", "Prob_1",
                "StepOverMaxStep", "ResOverMaxRes", ]

        if self.extraction_flag:
            self.input_size += 2*d
            self.input_name +=  [f"Ext1_{par.name}" \
                                 for par in self.pf.phys_model.params] + \
                [f"Ext2_{par.name}" for par in self.pf.phys_model.params]
        if self.cov_flag:
            self.input_size += d**2
            self.input_name += [f"Cov_{par1.name}_{par2.name}" \
                                for par1, par2 \
                    in product(self.pf.phys_model.params,
                               self.pf.phys_model.params)]

        super().__init__(
            particle_filter, phys_model,
            control_strategy,
            input_size, input_name,
            simpars,
        )

    def _select_hypothesis(
            self, particles: Tensor,
            weights: Tensor,
            omega_hyp: float,
    ) -> Tuple[Tensor, Tensor]:
        """Returns the posterior
        probability distribution conditioned
        on the frequency.
        """
        pars = self.simpars
        zeros_tensor = zeros(
            (self.bs, self.pf.np), dtype=pars.prec,
            )
        ones_tensor = ones(
            (self.bs, self.pf.np), dtype=pars.prec,
            )
        selected_weights = where(
            equal(particles[:, :, 1],
                  omega_hyp*ones_tensor),
            weights, zeros_tensor,
        )
        prob_hypothesis = reduce_sum(
            selected_weights, axis=1, keepdims=True,
            )
        normalized_weights = selected_weights*\
            reciprocal_no_nan(
            broadcast_to(
                prob_hypothesis, (self.bs, self.pf.np)),
        )
        return normalized_weights, prob_hypothesis

    def _compute_partial_input(
            self, weights: Tensor,
            particles: Tensor,
    ) -> Tuple[Tensor, Tensor]:
        """
        """
        mean_field = normalize(self.pf.compute_mean(
            weights, particles[:, :, 0:1], dims=1,
        ), [0, 1], )
        sigma_alpha = self.pf.compute_covariance(
            weights, particles[:, :, 0:1], dims=1,
        )
        logdev_field = normalize(
            log(sqrt(diag_part(sigma_alpha))+1e-33),
            [-10.0, 0.0],
            )
        return mean_field, logdev_field
    
    def generate_input(
            self, weights: Tensor, particles: Tensor,
            meas_step: Tensor, used_resources: Tensor,
            rangen: Generator,
            ):
        r"""
        """
        # Divide the particles according to the
        # two possble value for omega.
        d = self.pf.d
        weights0, prob0 = self._select_hypothesis(
            particles, weights,
            self.phys_model.params[1].values[0],
        )
        weights1, prob1 = self._select_hypothesis(
            particles, weights,
            self.phys_model.params[1].values[1],
        )
        mean_0, sigma_0 = self._compute_partial_input(
            weights0, particles,
            )
        mean_1, sigma_1 = self._compute_partial_input(
                weights1, particles,
                )
        scaled_step = normalize(
            meas_step, (0, self.simpars.num_steps),
            )
        scaled_resources = normalize(
            used_resources, (0, self.simpars.max_resources),
            )
        input_tensor = concat([
            mean_0, sigma_0, prob0,
            mean_1, sigma_1, prob1,
            scaled_step, scaled_resources,
        ], 1, name="input_tensor", )

        if self.extraction_flag:
            two_particles = self.pf.extract_particles(
                weights, particles, 2, rangen,
                )
            input_tensor = concat(
                [input_tensor, reshape(two_particles,
                                       (self.bs, 2*d))], 1,
                )
        if self.cov_flag:
            cov = self.pf.compute_covariance(weights, particles)
            input_tensor = concat(
                [input_tensor, reshape(cov, (self.bs, d**2))], 1,
            )
        return input_tensor

    def loss_function(
        self, weights: Tensor, particles: Tensor,
        true_values: Tensor, used_resources: Tensor,
        meas_step: Tensor,
    ):
        r"""Loss function.
        """
        pars = self.simpars
        hyp0 = self.phys_model.params[1].values[0]
        hyp1 = self.phys_model.params[1].values[1]
        zeros_tensor = zeros(
            (self.bs, 1), dtype=pars.prec,)
        ones_tensor = ones(
            (self.bs, 1), dtype=pars.prec,
            )
        _, prob0 = self._select_hypothesis(
            particles, weights, hyp0, 
        )
        _, prob1 = self._select_hypothesis(
            particles, weights, hyp1,
        )
        prob = concat([prob0, prob1, ], 1)
        choice = cast(expand_dims(
            argmax(prob, axis=1, output_type="int32"),
            axis=1,
            ), dtype=pars.prec,
        )
        choice_omega = where(
            equal(choice, zeros_tensor),
            hyp0*ones_tensor, zeros_tensor,
        )
        choice_omega = where(
            equal(choice, ones_tensor),
            hyp1*ones_tensor, choice_omega,
        )
        loss_values = where(
            equal(
                choice_omega, true_values[:, :, 1],
            ), zeros_tensor, ones_tensor,
        )
        return loss_values

def parse_args():
    """Arguments
    ---------
    scratch_dir: str, required
        Directory in which the
        intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./nv_center_ac_omega/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./nv_center_ac_omega/data"
        Directory containing the csv files
        produced by the
        :py:func:`~.utils.performance_evaluation`
        and the
        :py:func:`~.utils.store_input_control` functions.
    prec: str = "float32"
        Floating point precision of the
        whole simulation.
    n: int = 64
        Number of neurons per layer in the neural network.
    num_particles: int = 1024
        Number of particles in the ensemble representing
        the posterior.
    iterations: int = 16392
        Number of training steps.
    scatter_points: int = 32
        Number of points in the Resources/Precision
        csv produced by
        :py:func:`~.utils.performance_evaluation`
    """
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir", type=str,
                        default="./nv_center_ac_omega/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./nv_center_ac_omega/data")
    parser.add_argument("--prec", type=str, default="float32")
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument("--num-particles", type=int, default=1024)
    parser.add_argument("--iterations", type=int, default=16392)
    parser.add_argument("--scatter-points", type=int, default=32)

    return parser.parse_args()

def simple_frequency_testing(
    args, batchsize: int, max_res: float,
    learning_rate: float = 1e-2,
    gradient_accumulation: int = 1,
    cumulative_loss: bool = False,
    log_loss: bool = False,
    res: Literal["meas", "time"] ="meas",
    B_bounds: Tuple[float, float] = (0.9, 1.0),
    omega_values: Tuple[float, float] = (1.000, 1.002),
    invT2: float = 0.0,
    ):
    r"""Simulate a Bayesian estimation of the intensity
    of an oscillating magnetic field of unknown frequency
    and unknown intensity with an NV center spin,
    for a neural network
    controlling the evolution time,
    a static strategy, two variations of the
    :math:`\sigma^{-1}` strategy, and the
    particle guess heuristic (PGH).

    Parameters
    ----------
    args:
        Arguments passed to the Python script.
    batchsize: int
        Batchsize of the simulation, i.e. number of
        estimations executed simultaneously.
    max_res: float
        Maximum amount of resources allowed to
        be consumed in the estimation.
    learning_rate: float = 1e-2
        Initial learning rate for the neural
        network. The initial learning rate of the
        static strategy is fixed to `1e-2`.
        They both decay with
        :py:obj:`~.InverseSqrtDecay`.
    gradient_accumulation: int = 1
        Flag of the :py:func:`~.utils.train` function.
    cumulative_loss: bool = False
        Flag :py:obj:`~.SimulationParameters.cumulative_loss`.
    log_loss: bool = False
        Flag :py:obj:`~.SimulationParameters.log_loss`.
    res: {"meas", "time"}
        Type of resource for the simulation. It can
        be either the number of Ramsey
        measurements or the total evolution time.
    B_bounds: Tuple[float, float] = (1.0, 2.0)
        Extrema of admissible values for
        the intensity of the magnetic field.
    omega_values: Tuple[float, float] = (1.0, 1.1)
        Admissible values for
        the frequency of the magnetic field.
    invT2: float = 0.0
        Inverse of the transversal relaxation time.
        It is a known parameter of the estimation.
    """
    input_size = 8
    max_pulse = 12
    control_size = max_pulse+1

    name = "nv_center_ac_omega_" + res
    name += f"_invT2_{invT2:.2f}"
    name += f"_lr_{learning_rate}"

    network = standard_model(
        input_size=input_size,
        controls_size=control_size,
        neurons_per_layer=args.n,
        prec=args.prec,
        )

    nv_center = NVCenterACMagnetometryOmega(
        batchsize=batchsize,
        params=[
            Parameter(bounds=B_bounds,
                      name="B"),
            Parameter(values=omega_values,
                      name="omega"),
        ],
        prec=args.prec,
        res=res, invT2=invT2,
        max_pulse_number=max_pulse,
        )
        
    pf = ParticleFilter(
        num_particles=args.num_particles,
        phys_model=nv_center,
        resample_fraction=0.98, prec=args.prec,
    )

    prefact = (1/(omega_values[1]-omega_values[0]))/max_pulse
    if res=="time":
        num_steps = 128
    else:
        num_steps = max_res
    
    simpars = SimulationParameters(
        sim_name=name,
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    def control_nn(input_tensor: Tensor):
        tau = prefact*abs(
            network(input_tensor)[:, 0:max_pulse])
        phase = pi*network(input_tensor)[:, 1:2]
        return concat([tau, phase], 1)

    sim_nn = FrequencyTesting(
        particle_filter=pf,
        simpars=simpars,
        phys_model=nv_center,
        control_strategy=control_nn,
    )

    decaying_learning_rate = InverseSqrtDecay(
        learning_rate, args.prec
    )

    # train_nn_graph(
    #     sim_nn,
    #     Adam(learning_rate=decaying_learning_rate),
    #     network,
    # )

    # train_nn_profiler(
    #     sim_nn, Adam(
    #     learning_rate=decaying_learning_rate,
    #     ),
    #     network, xla_compile=True,
    # )

    print(sim_nn)
  
    train(
        sim_nn, Adam(learning_rate=decaying_learning_rate),
        args.iterations, args.scratch_dir,
        network=network,
        xla_compile=True,
        gradient_accumulation=gradient_accumulation,
    )

    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)

    network.save(
        join(args.trained_models_dir, str(sim_nn)),
        )
    # network=load_model(
    #     join(args.trained_models_dir, str(sim_nn)),
    #     )

    if res=="time" and max_res>128:
        precision_fit = None
        delta_resources = 50
    else:
        precision_fit = None if res=="meas" else \
            {'num_points': args.scatter_points,
                'batchsize': 16384,
                'epochs': 8,
                'direct_func': lambda res, prec: res*prec,
                'inverse_func': lambda res, c: c/res}
        delta_resources = 1.0 if res=="meas" else None

    performance_evaluation(
        sim_nn,
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='ProbErr',
    )

    store_input_control(
        sim_nn, args.data_dir, 5,
        xla_compile=True,
    )

    # Static simulation

    simpars_static = SimulationParameters(
        sim_name=name+"_static",
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    #Initial value of the controls in the static
    # optimization
    initial_state = zeros((int(max_res), 51))
    for i in range(int(max_res)):
        for j in range(nv_center.max_pulse_number):
            initial_state[i, j] = rand()
        initial_state[i, nv_center.max_pulse_number] = rand()

    static_variables = Variable(
        initial_state, dtype=args.prec,
        )

    def control_static(input_tensor: Tensor):
        var = abs(gather(
                params=static_variables,
                indices=cast(
        round(denormalize(input_tensor[:, input_size-2],
                          (0, max_res))), dtype="int32"),
            ))
        return concat(
            [prefact*var[:, 0:max_pulse], pi*var[:, (max_pulse-1):max_pulse]], 1,
        )

    sim_static = FrequencyTesting(
        particle_filter=pf,
        simpars=simpars_static,
        phys_model=nv_center,
        control_strategy=control_static,
    )

    decaying_learning_rate = InverseSqrtDecay(
        1e-1, args.prec
    )

    train(
        sim_static, Adam(
        learning_rate=decaying_learning_rate,
        ),
        args.iterations, args.scratch_dir,
        custom_controls=static_variables,
        xla_compile=True,
        gradient_accumulation=gradient_accumulation,
    )
    
    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)

    savetxt(join(args.trained_models_dir, str(sim_static)),
            static_variables.numpy())

    performance_evaluation(
        sim_static,
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='ProbErr',
    )

    store_input_control(
        sim_static, args.data_dir, 5,
        xla_compile=True,
    )

    # PGH simulation

    simpars_pgh = SimulationParameters(
        sim_name=name+"_PGH",
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    def control_pgh(input_tensor):
        extracted_particles = reshape(
            input_tensor[:, \
                input_size:(input_size+4)],
            (batchsize, 2, 2),
            )
        return 1.0/(norm(
            extracted_particles[:, 0, :]-\
                extracted_particles[:, 1, :],
            axis=1, keepdims=True)+1e-5)

    sim_pgh = FrequencyTesting(
        particle_filter=pf,
        simpars=simpars_pgh,
        phys_model=nv_center,
        control_strategy=control_pgh,
        extraction_flag=True,
    )

    performance_evaluation(
        sim_pgh,
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='ProbErr',
    )

    # Sigma strategy

    simpars_sigma = SimulationParameters(
        sim_name=name+"_Sigma",
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    def control_sigma(input_tensor):
        mean_invT2 = invT2*ones((batchsize, ), dtype=args.prec)
        cov = reshape(input_tensor[:, input_size:\
                                   (input_size+4)],
                                   (batchsize, 2, 2))
        return expand_dims(
            ((trace(cov))**(1/2)+mean_invT2)**(-1),
            axis=1,
            )

    sim_sigma = FrequencyTesting(
        particle_filter=pf,
        simpars=simpars_sigma,
        phys_model=nv_center,
        control_strategy=control_sigma,
        cov_flag = True,
    )

    performance_evaluation(
        sim_sigma,
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='ProbErr',
    )

    # Sigma simplified

    simpars_sigmah = SimulationParameters(
        sim_name=name+"_SigmaH",
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    def control_sigmah(input_tensor):
        cov = reshape(input_tensor[:, input_size:\
                                   (input_size+4)],
                                   (batchsize, 2, 2))
        return expand_dims(((trace(cov))**(-1/2)), axis=1)

    sim_sigmah = FrequencyTesting(
        particle_filter=pf,
        simpars=simpars_sigmah,
        phys_model=nv_center,
        control_strategy=control_sigmah,
        cov_flag=True,
    )

    performance_evaluation(
        sim_sigmah,
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='ProbErr',
    )

    # Sigma 2Pi

    simpars_sigmapi = SimulationParameters(
        sim_name=name+"_SigmaPi",
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    def control_sigmapi(input_tensor):
        cov = reshape(input_tensor[:, input_size:\
                                   (input_size+2**2)],
                                   (batchsize, 2, 2))
        return expand_dims(((4*pi**2*trace(cov))**(-1/2)), axis=1)

    sim_sigmapi = FrequencyTesting(
        particle_filter=pf,
        simpars=simpars_sigmapi,
        phys_model=nv_center,
        control_strategy=control_sigmapi,
        cov_flag=True,
    )

    performance_evaluation(
        sim_sigmapi,
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='ProbErr',
    )
    
    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)


def main():
    r"""
    """
    args = parse_args()

    simple_frequency_testing(
        args, 128, 5120, learning_rate=1e-2, res='time',
        cumulative_loss=True,
        invT2=0.0,
        )

    simple_frequency_testing(
        args, 32, 2560*4, learning_rate=1e-2, res='time',
        cumulative_loss=True,
        invT2 = 0.001,
        )

if __name__ == "__main__":
    main()