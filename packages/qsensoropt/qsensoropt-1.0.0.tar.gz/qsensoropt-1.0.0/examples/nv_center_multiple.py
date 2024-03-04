#!/usr/bin/env python3
from typing import Literal, List, Optional, \
    Tuple

from tensorflow import cast, ones, \
    gather, reshape, norm, expand_dims, \
        concat, print, Variable, Tensor
from tensorflow.math import exp, cos, abs, round
from tensorflow.linalg import trace
from tensorflow.random import uniform
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import get_memory_info
from numpy import zeros, savetxt, loadtxt
from numpy.random import rand
from argparse import ArgumentParser
from math import floor as mfloor
from os.path import join
from math import pi

from qsensoropt import InverseSqrtDecay, ParticleFilter, \
        Parameter, SimulationParameters, StatelessMetrology
from qsensoropt.utils import train, \
    performance_evaluation, store_input_control, \
        standard_model, denormalize, normalize

from nv_center_dc import NVCenter, Magnetometry

class NVCenterHyperfine(NVCenter):
    r"""This class models the measurement of
    an NV center strongly coupled to a 13C
    nuclear spin in the diamond lattice. Such
    nuclear spin is not hidden in the spin bath
    of nuclei, that causes the dephasing noise,
    instead it splits the
    energy levels of the NV center, according
    to the hyperfine interaction strength.
    The precession frequency of the NV center
    in a magnetic field is determined by
    the state of the nuclear spin. In the work
    of T. Joas et al. [4]_ multiple incoherent
    nuclear spin flips happen during the read out,
    so that the nuclear spin is in each eigenstate
    approximately half of the time.
    This motivates the choice for
    the outcome probability of Ramsey
    measure on the NV center:

    .. math::
        \begin{aligned}
        p(+1|\omega_0, \omega_1, T_2, \tau) :=
        \frac{e^{-\frac{\tau}{T_2}}}{2}
        & \left[ \cos^2 \left( \frac{\omega_0 \tau}{2} +
        \phi \right) \right. \\
        & \left. + \cos^2 \left( \frac{\omega_1 \tau}{2} +
        \phi\right) \right] +
        \frac{1-e^{-\frac{\tau}{T_2}}}{2} \; .
        \end{aligned}
        :label: nv_double_model

    In such model :math:`\omega_0` and :math:`\omega_1`
    are the two precession frequencies of the sensor to
    be estimated,
    splitted by the hyperfine interaction, :math:`T_2` is
    the coherence time, :math:`\tau` and :math:`\phi`
    are the controls, being respectively
    the evolution time and the
    phase.

    Notes
    -----
    This models is completely symmetric under
    permutation of the two precession frequencies.
    In these cases the flag
    :py:attr:`~.SimulationParameters.permutation_invariant`
    must be activated. Only those weight matrices that
    are permutationally invariant should be considered for
    the estimation.

    All the training of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.

    .. [4] Joas, T., Schmitt, S., Santagati, R. et al.
       npj Quantum Inf 7, 56 (2021).
    """
    def __init__(
        self, batchsize: int, params: List[Parameter],
        prec: Literal["float64", "float32"] = "float64",
        res: Literal["meas", "time"] = "meas",
        invT2: float = 0.0,
        ):
        r"""Constructor
        of the :py:obj:`~.NVCenterHyperfine` class.

        Parameters
        ----------
        batchsize: int
            Batchsize of the simulation, i.e.
            number of estimations
            executed simultaneously.
        params: List[:py:obj:`~.Parameter`]
            List of unknown parameters to estimate in
            the NV center experiment, with their
            respective bounds. These are the two
            precession frequencies
            :math:`\omega_0` and
            :math:`\omega_1`.
        prec : {"float64", "float32"}
            Precision of the floating point operations in the 
            simulation.
        res: {"meas", "time"}
            Resource type for the present metrological task, 
            can be either the total evolution time, i.e. `time`,
            or the total number of measurements on
            the NV center, i.e. `meas`.
        invT2: float = 0.0
            The inverse of the
            transverse relaxation time
            :math:`T_2^{-1}` is fixed
            to the value `invT2`.
        """
        super().__init__(
            batchsize, params, prec=prec, res=res,
            control_phase=True,
        )       
        self.invT2 = invT2

    def model(
        self, outcomes: Tensor, controls: Tensor,
        parameters: Tensor, meas_step: Tensor,
        num_systems: int = 1,
        ) -> Tensor:
        r"""Model for the outcome probability
        of the NV center subject to the hyperfine
        interaction with the carbon nucleus and
        measured through photoluminescence after
        a Ramsey sequence.
        The probability of getting `+1`
        in the majority voting following the
        photon counting is given by
        :eq:`nv_double_model`.

        Notes
        -----
        There is also another way of expressing
        the outcome probability of the measurement.
        Instead of defining the model in terms of
        :math:`\omega_0` and :math:`\omega_1` we
        could define it in terms of the frequency sum
        :math:`\Sigma = \omega_0 + \omega_1` and
        frequency difference
        :math:`\Delta = \omega_1 - \omega_0`, thus writing

        .. math::
            \begin{aligned}
            p(+1|\Sigma, \Delta, T_2, \tau) :=
            \frac{e^{-\frac{\tau}{T_2}}}{2}
            & \left[ \cos^2 \left( \frac{\Sigma+\Delta}{4} \tau +
            \phi \right) \right. \\
            & \left. + \cos^2 \left( \frac{\Sigma-\Delta}{4} \tau +
            \phi\right) \right] +
            \frac{1-e^{-\frac{\tau}{T_2}}}{2} \; .
            \end{aligned}
            :label: alt_double

        In this form there is no permutational invariance in
        :math:`\Sigma` and :math:`\Delta`, instead the model
        is invariant under the transformation
        :math:`\Delta \rightarrow - \Delta`. We should
        choose a prior having :math:`\Delta>0`,
        which means :math:`\omega_1>\omega_0`.
        We could impose the positivity of the frequencies
        by requiring :math:`\Sigma>\Delta` in the prior.
        """
        evolution_time = controls[:, :, 0]
        phase = controls[:, :, 1]
        omega0, omega1, omega2, omega3, omega4, omega5, \
        omega6, omega7, omega8, omega9 = \
            parameters[:, :, 0], parameters[:, :, 1], \
            parameters[:, :, 2], parameters[:, :, 3], \
            parameters[:, :, 4], parameters[:, :, 5], \
            parameters[:, :, 6], parameters[:, :, 7], \
            parameters[:, :, 8], parameters[:, :, 9]
        if self.invT2 is not None:
            invT2 = self.invT2
        else:
            invT2 = parameters[:, :, 10]
        exp_decay = exp(-evolution_time*invT2)
        ramsey_out = outcomes[:, :, 0]
        noise_less = \
            (1.0-ramsey_out*cos(omega0*evolution_time+phase))/20.0+\
            (1.0-ramsey_out*cos(omega1*evolution_time+phase))/20.0+\
            (1.0-ramsey_out*cos(omega2*evolution_time+phase))/20.0+\
            (1.0-ramsey_out*cos(omega3*evolution_time+phase))/20.0+\
            (1.0-ramsey_out*cos(omega4*evolution_time+phase))/20.0+\
            (1.0-ramsey_out*cos(omega5*evolution_time+phase))/20.0+\
            (1.0-ramsey_out*cos(omega6*evolution_time+phase))/20.0+\
            (1.0-ramsey_out*cos(omega7*evolution_time+phase))/20.0+\
            (1.0-ramsey_out*cos(omega8*evolution_time+phase))/20.0+\
            (1.0-ramsey_out*cos(omega9*evolution_time+phase))/20.0
        return exp_decay*noise_less + (1.0-exp_decay)/2.0

def parse_args():
    """Arguments
    ---------
    scratch_dir: str
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./nv_center_double/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./nv_center_double/data"
        Directory containing the csv files
        produced by the :py:func:`~.utils.performance_evaluation`
        and the :py:func:`~.utils.store_input_control` functions.
    prec: str = "float32"
        Floating point precision of the
        whole simulation.
    n: int = 64
        Number of neurons per layer in the neural network.
    num_particles: int = 4096
        Number of particles in the ensemble representing
        the posterior.
    iterations: int = 4096
        Number of training steps.
    """
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir", type=str,
                        default="./nv_center_multiple/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./nv_center_multiple/data")
    parser.add_argument("--prec", type=str, default="float32")
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument("--num-particles", type=int, default=1024)
    parser.add_argument("--iterations", type=int, default=4096)

    return parser.parse_args()

def hyperfine_parallel_estimation(
    args, batchsize: int, max_res: float,
    learning_rate: float = 1e-2,
    gradient_accumulation: int = 1,
    cumulative_loss: bool = False,
    log_loss: bool = False,
    res: Literal["meas", "time"] ="meas",
    invT2: Optional[float] = None,
    cov_weight_matrix: Optional[List] = None,
    omega_bounds: Tuple[float, float] = (0.0, 1.0),
    ):
    r"""Estimation of the frequencies of
    two hyperfine lines in the
    spectrum of an NV center
    strongly interacting with a 13C
    nuclear spin. The mean square
    errors of the two parameters are
    weighted equally with :math:`G=\text{Id}`.
    The frequency difference
    is the component of
    the hyperfine interaction parallel
    to the NV center quantization
    axis, i.e. :math:`A_{||} = | \omega_1 - \omega_0 |`.
    The priors for :math:`\omega_0` and :math:`\omega_1` are
    both uniform in `(0, 1)`, and they are symmetrized.
    Beside the NN and the static strategies,
    the performances of the particle guess heuristic (PGH),
    and of the :math:`\sigma^{-1}` strategies are reported
    in the plots. These other strategies are explained
    in the documentation of the :py:obj:`~.Magnetometry`
    class. The picture represent a schematic of the
    estimation of the hyperfine coupling controlled
    by the NN.

    .. image:: ../docs/_static/nv_center_double.png
        :width: 700
        :alt: nv_center_double  
    """
    d = 10
    input_size_original = d**2+2*d+2
    input_size = input_size_original
    control_size = 2

    name = "nv_center_double_" + res
    if invT2:
        name += f"_invT2_{invT2:.4f}"
    
    name += f"_lr_{learning_rate}"

    network = standard_model(
        input_size=input_size,
        controls_size=control_size,
        neurons_per_layer=args.n,
        prec=args.prec,
    )
    
    # Preconditioning of the network
    input_tensor = 2*uniform((16384, input_size),
                             dtype=args.prec)-1
    output_tensor_tau = ((input_tensor[:, (input_size_original-1):\
                    input_size_original]+1)/2)
    output_tensor_phase = 2*uniform((16384, 1), 
                             dtype=args.prec)-1
    output_tensor = concat(
        [output_tensor_tau, output_tensor_phase], 1,
        )
    network.compile(loss='mean_squared_error',
                    optimizer='adam')
    network.fit(
        input_tensor, output_tensor,
        epochs=12, batch_size=1024, verbose=0,
        )

    nv_center = NVCenterHyperfine(
        batchsize=batchsize,
        params=[Parameter(bounds=omega_bounds, name="omega0"),
                Parameter(bounds=omega_bounds, name="omega1"),
                Parameter(bounds=omega_bounds, name="omega2"),
                Parameter(bounds=omega_bounds, name="omega3"),
                Parameter(bounds=omega_bounds, name="omega4"),
                Parameter(bounds=omega_bounds, name="omega5"),
                Parameter(bounds=omega_bounds, name="omega6"),
                Parameter(bounds=omega_bounds, name="omega7"),
                Parameter(bounds=omega_bounds, name="omega8"),
                Parameter(bounds=omega_bounds, name="omega9")],
        prec=args.prec,
        res=res, invT2=invT2,
        )
        
    pf = ParticleFilter(
        num_particles=args.num_particles,
        phys_model=nv_center,
        resample_fraction=0.98, prec=args.prec,
    )

    num_steps = max_res if res=="meas" else 512

    if invT2>=0.1 and res=="time":
        num_steps *= 2

    simpars = SimulationParameters(
        sim_name=name,
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
        permutation_invariant=True,
    )

    # Computation of the prefactor
    invT2_tmp = 1e-4 if invT2==0 else invT2
    prefact = min(40.0, (1.0/invT2_tmp)/2)
    
    prefact = 3.0

    def control_nn(input_tensor: Tensor):
        nn_out = network(input_tensor)
        tau = prefact*abs(nn_out[:, 0:1])+1.0
        phase = pi*nn_out[:, 1:2]
        return concat([tau, phase], 1)

    sim_nn = Magnetometry(
        particle_filter=pf,
        simpars=simpars,
        phys_model=nv_center,
        control_strategy=control_nn,
        cov_weight_matrix=cov_weight_matrix,
        eta_flag=res=="time",
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
    #     sim_nn, Adam(learning_rate=decaying_learning_rate),
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

    sim_nn.eta_flag = False

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
        args.iterations,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
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
        permutation_invariant=True,
    )

    #Initial value of the controls in the static
    # optimization
    initial_state = zeros((int(num_steps), 2))
    for i in range(int(num_steps)):
        initial_state[i, 0] = i/(num_steps)
        # initial_state[i, 0] = rand()
        initial_state[i, 1] = rand()

    static_variables = Variable(
        initial_state, dtype=args.prec,
        )

    def control_static(input_tensor: Tensor):
        var = gather(
                params=static_variables,
                indices=cast(
        round(denormalize(input_tensor[:, input_size_original-2],
                          (0, num_steps))), dtype="int32"),
            )
        return concat(
            [prefact*abs(var[:, 0:1])+1.0, pi*var[:, 1:2]], 1,
        )

    sim_static = Magnetometry(
        particle_filter=pf,
        simpars=simpars_static,
        phys_model=nv_center,
        control_strategy=control_static,
        cov_weight_matrix=cov_weight_matrix,
        eta_flag=res=="time",
    )
    
    decaying_learning_rate = InverseSqrtDecay(
        1e-1, args.prec
    )

    train(
        sim_static, Adam(learning_rate=decaying_learning_rate),
        args.iterations, args.scratch_dir,
        custom_controls=static_variables,
        xla_compile=True,
        gradient_accumulation=gradient_accumulation,
    )
    
    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)

    savetxt(
        join(args.trained_models_dir, str(sim_static)),
            static_variables.numpy(),
            )
    # static_variables = Variable(loadtxt(
    #     join(args.trained_models_dir, str(sim_static)),
    #     )[:, None], dtype=args.prec,
    # )

    sim_static.eta_flag = False

    performance_evaluation(
        sim_static,
        args.iterations,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
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
        permutation_invariant=True,
    )

    def control_pgh(input_tensor):
        extracted_particles = reshape(
            input_tensor[:, input_size_original:\
                         (input_size_original+2*d)],
            (batchsize, 2, d),
            )
        tau = 1.0/(norm(
            extracted_particles[:, 0, :]-extracted_particles[:, 1, :],
            axis=1, keepdims=True)+1e-8)
        zeros_tensor = zeros(
            (batchsize, 1), dtype=args.prec,
            )
        return concat([tau, zeros_tensor], 1)

    sim_pgh = Magnetometry(
        particle_filter=pf,
        simpars=simpars_pgh,
        phys_model=nv_center,
        control_strategy=control_pgh,
        cov_weight_matrix=cov_weight_matrix,
        extraction_flag=True,
    )

    performance_evaluation(
        sim_pgh,
        args.iterations,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
    )
    
    store_input_control(
        sim_pgh, args.data_dir, 5,
        xla_compile=True,
    )

    # Sigma strategy

    simpars_sigma = SimulationParameters(
        sim_name=name+"_Sigma",
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
        permutation_invariant=True,
    )

    def control_sigma(input_tensor):
        mean_invT2 = invT2*ones((batchsize, ), dtype=args.prec)
        cov = reshape(input_tensor[:, input_size_original:\
                                   (input_size_original+d**2)],
                                   (batchsize, d, d))
        tau = expand_dims(((trace(cov))**(1/2)+\
                            mean_invT2)**(-1), axis=1)
        zeros_tensor = zeros(
            (batchsize, 1), dtype=args.prec,
            )
        return concat([tau, zeros_tensor], 1)

    sim_sigma = Magnetometry(
        particle_filter=pf,
        simpars=simpars_sigma,
        phys_model=nv_center,
        control_strategy=control_sigma,
        cov_weight_matrix=cov_weight_matrix,
        cov_flag=True,
    )

    performance_evaluation(
        sim_sigma,
        args.iterations,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
    )

    # Sigma simplified

    simpars_sigmah = SimulationParameters(
        sim_name=name+"_SigmaH",
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
        permutation_invariant=True,
    )

    def control_sigmah(input_tensor):
        cov = reshape(input_tensor[:, input_size_original:\
                                   (input_size_original+d**2)],
                                   (batchsize, d, d))
        tau = expand_dims(((trace(cov))**(-1/2)), axis=1)
        zeros_tensor = zeros(
            (batchsize, 1), dtype=args.prec,
            )
        return concat([tau, zeros_tensor], 1)

    sim_sigmah = Magnetometry(
        particle_filter=pf,
        simpars=simpars_sigmah,
        phys_model=nv_center,
        control_strategy=control_sigmah,
        cov_weight_matrix=cov_weight_matrix,
        cov_flag=True,
    )

    performance_evaluation(
        sim_sigmah,
        args.iterations,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
    )

    # Sigma 2Pi

    simpars_sigmapi = SimulationParameters(
        sim_name=name+"_SigmaPi",
        num_steps=num_steps,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
        permutation_invariant=True,
    )

    def control_sigmapi(input_tensor):
        cov = reshape(input_tensor[:, input_size_original:\
                                   (input_size_original+d**2)],
                                   (batchsize, d, d))
        tau = expand_dims(((4*pi**2*trace(cov))**(-1/2)), axis=1)
        zeros_tensor = zeros(
            (batchsize, 1), dtype=args.prec,
            )
        return concat([tau, zeros_tensor], 1)

    sim_sigmapi = Magnetometry(
        particle_filter=pf,
        simpars=simpars_sigmapi,
        phys_model=nv_center,
        control_strategy=control_sigmapi,
        cov_weight_matrix=cov_weight_matrix,
        cov_flag=True,
    )

    performance_evaluation(
        sim_sigmapi,
        args.iterations,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
    )

def main():
    r"""In the following we report
    the mean square error on the
    Bayesian estimators for the two
    frequencies for different strategies
    and different
    coherence times :math:`T_2`. The resource is
    either the total evolution time
    or the number of measurements on the
    NV center.

    .. list-table::

        * - .. figure:: ../examples/nv_center_double/images/
                          nv_center_double_meas_lr_0.001_batchsize_
                          256_num_steps_128_max_resources_128.00_ll_
                          True_cl_True/plot_MeasStep_MSE.png

                invT2=0, Meas=128

          - .. figure:: ../examples/nv_center_double/images/
                          nv_center_double_time_lr_0.0001_batchsize_
                          64_num_steps_512_max_resources_2048.00_ll_
                          False_cl_True/plot_Time_MSE.png

                invT2=0, Time=2048

        * - .. figure:: ../examples/nv_center_double/images/
                          nv_center_double_meas_invT2_0.0100_
                          lr_0.001_batchsize_256_num_steps_128_
                          max_resources_128.00_ll_True_cl_True
                          /plot_MeasStep_MSE.png

               invT2=0.01, Meas=128

          - .. figure:: ../examples/nv_center_double/images/
                          nv_center_double_time_invT2_0.0100_lr_
                          0.001_batchsize_64_num_steps_512_max_resources_
                          2048.00_ll_False_cl_True/plot_Time_MSE.png

                invT2=0.01, Time=2048

        * - .. figure:: ../examples/nv_center_double/images/
                          nv_center_double_meas_invT2_0.1000_
                          lr_0.01_batchsize_128_num_steps_256_
                          max_resources_128.00_ll_True_cl_True/
                          plot_MeasStep_MSE.png
                
                invT2=0.1, Meas=128

          - .. figure:: ../examples/nv_center_double/images/
                          nv_center_double_time_invT2_0.1000_
                          lr_0.01_batchsize_32_num_steps_1024_
                          max_resources_2048.00_ll_False_cl_True/
                          plot_Time_MSE.png
                
                invT2=0.1, Time=2048

    The shaded grey areas in the above plot indicate
    the Bayesian Cramér-Rao bound, which is the
    the ultimate precision bound computed from
    the Fisher information.
    
    From these simulations there seems to
    be no significant advantage in using
    an adaptive strategy for the simultaneous
    estimation of the two precession frequencies.
    Neither for large nor for
    small coherence times :math:`T_2`.
    
    Notes
    -----
    In a future work the alternative model
    of :eq:`alt_double` should be implemented.
    Being interested in the difference
    :math:`\Delta`, the sum of the frequencies
    would be treated as a nuisance parameter.

    The absence on an advantage of the adaptive
    strategy over the non-adaptive one is probably
    also due to the hyper-simplified information passed
    to the neural network. We are in fact approximating
    a complex 2D posterior, with many peaks and
    valleys with a Gaussian. A better approach would be
    to train an autoencoder to compress the information
    contained in the posterior and pass it to the NN.
    The autoencoder will be trained to compress that
    class of distribution which are produced by the
    likelihood of the double precession frequency model.

    All the simulations of this module
    have been done on a
    GPU NVIDIA GeForce RTX-4090-24GB.
    """
    args = parse_args()

    hyperfine_parallel_estimation(
        args, 32, 1024, learning_rate=1e-3, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2=0.0,
        )

if __name__ == "__main__":
    main()
