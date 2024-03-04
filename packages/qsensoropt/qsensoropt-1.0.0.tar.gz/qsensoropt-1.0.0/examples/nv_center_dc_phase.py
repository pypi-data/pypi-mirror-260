#!/usr/bin/env python3
from typing import Literal, List, Optional, Tuple

from tensorflow import cast, ones, \
    gather, concat, reshape, norm, expand_dims, \
        Variable, Tensor
from tensorflow.math import exp, cos, abs, round
from tensorflow.linalg import trace
from tensorflow.random import uniform
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import get_memory_info
from numpy import ceil, sqrt, zeros, savetxt, loadtxt
from numpy.random import rand
from argparse import ArgumentParser
from os.path import join
from math import pi

from qsensoropt import InverseSqrtDecay, \
    ParticleFilter, Parameter, \
        SimulationParameters
from qsensoropt.utils import train, \
    performance_evaluation, store_input_control, \
        standard_model, denormalize

from nv_center_dc import NVCenter, Magnetometry

class NVCenterDCMagnPhase(NVCenter):
    r"""Model describing the estimation of a
    static magnetic field with an NV center
    used as magnetometer.
    The transversal relaxation time :math:`T_2^{-1}` can
    be either known, or be a parameter to
    estimate. The estimation will be
    formulated in terms of the precession
    frequency :math:`\omega` of the NV center, which
    is proportional to the magnetic
    field :math:`B`.
    With respect to the :py:mod:`nv_center_dc` module
    we add here the possibility
    of imprinting an arbitrary phase on the NV-center
    state before the photon counting measurement.
    """
    def __init__(
        self, batchsize: int, params: List[Parameter],
        prec: Literal["float64", "float32"] = "float64",
        res: Literal["meas", "time"] = "meas",
        invT2: Optional[float] = None,
        ):
        r"""Constructor
        of the :py:obj:`~.NVCenterDCMagnPhase` class.

        Parameters
        ----------
        batchsize: int
            Batchsize of the simulation, i.e. number of estimations
            executed simultaneously.
        params: List[:py:obj:`~.Parameter`]
            List of unknown parameters to estimate in
            the NV center experiment, with their
            respective bounds. This contains either
            the precession frequency only or
            the frequency and the inverse coherence time.
        prec : {"float64", "float32"}
            Precision of the floating point operations in the 
            simulation.
        res: {"meas", "time"}
            Resource type for the present metrological task, 
            can be either the total evolution time, i.e. `time`,
            or the total number of measurements on
            the NV center, i.e. `meas`.
        invT2: float, optional
            If this parameter is specified only the precession
            frequency :math:`\omega` is considered as an unknown
            parameter, while the inverse of the
            transverse relaxation time :math:`T_2^{-1}` is fixed
            to the value `invT2`. In this case the list `params`
            must contain a single parameter, i.e. `omega`.
            If no `invT2` is specified,
            it is assumed that it is an unknown parameter that
            will be estimated along the frequency in the Bayesian
            procedure. In this case `params` must contain two
            objects, the second of them should be the inverse of the
            transversal relaxation time.
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
        r"""Model for the outcome of a measurement
        on a NV center that has been precessing in a static
        magnetic field.  The probability of getting the
        outcome :math:`+1` is

        .. math::

            p(+1|\omega, T_2, \tau) := e^{-\frac{\tau}{T_2}}
            \cos^2 \left( \frac{\omega}{2} \tau + \phi \right) +
            \frac{1-e^{-\frac{\tau}{T_2}}}{2} \; .

        The evolution time :math:`\tau` and
        the phase :math:`\phi` are controlled
        by the trainable agent, and :math:`\omega`
        is the unknown precession frequency, which is
        proportional to the magnetic field.
        The parameter :math:`T_2`
        may or may not be an unknown in the estimation,
        according to the value of the attribute `invT2`
        of the :py:obj:`NVCenterDCMagnPhase` class.
        """
        evolution_time = controls[:, :, 0]
        phase = controls[:, :, 1]
        omega = parameters[:, :, 0]
        if self.invT2 is not None:
            invT2 = self.invT2
        else:
            invT2 = parameters[:, :, 1]
        exp_decay = exp(-evolution_time*invT2)
        ramsey_out = outcomes[:, :, 0]
        noise_less = (1.0-ramsey_out*\
            cos(omega*evolution_time+phase))/2.0
        return exp_decay*noise_less + (1.0-exp_decay)/2.0

def parse_args():
    """Arguments
    ---------
    scratch_dir: str
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./nv_center_dc_phase/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./nv_center_dc_phase/data"
        Directory containing the csv files
        produced by the :py:func:`~.utils.performance_evaluation`
        and the :py:func:`~.utils.store_input_control` functions.
    prec: str = "float32"
        Floating point precision of the
        whole simulation.
    n: int = 64
        Number of neurons per layer in the neural network.
    num_particles: int = 480
        Number of particles in the ensemble representing
        the posterior.
    iterations: int = 32768
        Number of training steps.
    scatter_points: int = 32
        Number of points in the Resources/Precision
        csv produced by
        :py:func:`~.utils.performance_evaluation`.
    """
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir", type=str,
                        default="./nv_center_dc_phase/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./nv_center_dc_phase/data")
    parser.add_argument("--prec", type=str, default="float32")
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument("--num-particles", type=int, default=480)
    parser.add_argument("--iterations", type=int, default=32768)
    parser.add_argument("--scatter-points", type=int, default=32)

    return parser.parse_args()

def static_field_estimation(
    args, batchsize: int, max_res: float,
    learning_rate: float = 1e-2,
    gradient_accumulation: int = 1,
    cumulative_loss: bool = False,
    log_loss: bool = False,
    res: Literal["meas", "time"] ="meas",
    invT2: Optional[float] = None,
    invT2_bound: Optional[Tuple] = None,
    cov_weight_matrix: Optional[List] = None,
    omega_bounds: Tuple[float, float] = (0.0, 1.0),
    ):
    r"""Simulates the Bayesian estimation of a static
    magnetic field with an NV center,
    for a neural network controlling the sensor,
    a static strategy, two variations of the
    :math:`\sigma^{-1}` strategy, and the
    particle guess heuristic (PGH). Beside
    the evolution time also the phase
    is be controlled by the agent.

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
        static strategy is fixed to `1e-1`.
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
    invT2: float, optional
        Inverse of the transversal relaxation time.
        If :math:`T_2 = \infty` or it is unknown and must
        be estimated, this parameter should not
        be passed.
    invT2_bound: Tuple[float, float], optional
        Extrema of the uniform prior for the
        Bayesian estimation of the
        inverse of the transversal
        relaxation time.
    cov_weight_matrix: List, optional
        Weight matrix for the mean square error
        on the frequency and on the inverse of the
        coherence time :math:`T_2`.
    omega_bounds: Tuple[float, float] = (0.0, 1.0)
        Extrema of admissible values for
        the precession frequency.
    """
    if invT2 is None and invT2_bound is None:
        raise ValueError("At least one between invT2 and" \
            "invT2_bound must be passed to static_field_estimation")

    d = 2 if invT2 is None else 1
    input_size_original = d**2+2*d+2
    input_size = input_size_original
    control_size = 2

    name = "nv_center_" + res
    if invT2:
        name += f"_invT2_{invT2:.4f}"
    if invT2_bound:
        name += f"_invT2_min_{invT2_bound[0]:.4f}_" \
            f"invT2_max_{invT2_bound[1]:.4f}"
    
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
    output_tensor_tau = (input_tensor[:, -1:]+1)/2
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

    nv_center = NVCenterDCMagnPhase(
        batchsize=batchsize,
        params=[Parameter(bounds=omega_bounds, \
                          name="omega"),] if invT2 is not None else
            [Parameter(bounds=omega_bounds, name="omega"),
            Parameter(bounds=invT2_bound, name="invT2"),],
        prec=args.prec,
        res=res, invT2=invT2,
        )
        
    pf = ParticleFilter(
        num_particles=args.num_particles,
        phys_model=nv_center,
        resample_fraction=0.98, prec=args.prec,
    )
    
    simpars = SimulationParameters(
        sim_name=name,
        num_steps=max_res,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    # Computation of the prefactor
    prefact = max_res/20 if res=="time" \
        else ceil(2**(sqrt(max_res)))
    invT2_min = invT2 if invT2 is not None \
        else invT2_bound[0]
    if invT2_min > 0.0:
        prefact = min(prefact, 1.0/invT2_min)

    def control_nn(input_tensor: Tensor):
        tau = prefact*abs(
            network(input_tensor)[:, 0:1])+1.0
        phase = pi*network(input_tensor)[:, 1:2]
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

    print(get_memory_info('GPU:0')['peak']/1024**3)

    network.save(
        join(args.trained_models_dir, str(sim_nn)),
        )
    # network=load_model(
    #     join(args.trained_models_dir, str(sim_nn)),
    #     )

    sim_nn.eta_flag = False

    if res=="time":
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
        y_label='MSE',
    )

    store_input_control(
        sim_nn, args.data_dir, 5,
        xla_compile=True,
    )

    # Static simulation

    simpars_static = SimulationParameters(
        sim_name=name+"_static",
        num_steps=max_res,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    #Initial value of the controls in the static
    # optimization
    initial_state = zeros((int(max_res), 2))
    for i in range(int(max_res)):
        initial_state[i, 0] = i/(max_res)
        # initial_state[i, 0] = rand()
        initial_state[i, 1] = rand()

    static_variables = Variable(
        initial_state, dtype=args.prec,
        )

    def control_static(input_tensor: Tensor):
        var = abs(gather(
                params=static_variables,
                indices=cast(
        round(denormalize(input_tensor[:, input_size_original-2],
                          (0, max_res))), dtype="int32"),
            ))
        return concat(
            [prefact*var[:, 0:1]+1.0, pi*var[:, 1:2]], 1,
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
            static_variables.numpy(),
            )
    # static_variables = Variable(loadtxt(
    #     join(args.trained_models_dir, str(sim_static)),
    #     ), dtype=args.prec,
    # )

    sim_static.eta_flag = False

    performance_evaluation(
        sim_static,
        gradient_accumulation*4096,
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
        num_steps=max_res,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    def control_pgh(input_tensor):
        extracted_particles = reshape(
            input_tensor[:, input_size_original:\
                         (input_size_original+2*d)],
            (batchsize, 2, d),
            )
        tau = 1.0/(norm(
            extracted_particles[:, 0, :]-extracted_particles[:, 1, :],
            axis=1, keepdims=True)+1e-5)
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
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
    )

    # Sigma strategy

    simpars_sigma = SimulationParameters(
        sim_name=name+"_Sigma",
        num_steps=max_res,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    def control_sigma(input_tensor):
        if invT2_bound is None:
            mean_invT2 = invT2*ones((batchsize, ),
                                    dtype=args.prec)
        else:
            mean_invT2 = denormalize(input_tensor[:, 1],
                                     invT2_bound)
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
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
    )

    # Sigma simplified

    simpars_sigmah = SimulationParameters(
        sim_name=name+"_SigmaH",
        num_steps=max_res,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
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
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
    )

    # Sigma 2Pi

    simpars_sigmapi = SimulationParameters(
        sim_name=name+"_SigmaPi",
        num_steps=max_res,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
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
        gradient_accumulation*4096,
        args.data_dir,
        xla_compile=True,
        precision_fit=precision_fit,
        delta_resources=delta_resources,
        y_label='MSE',
    )

def main():
    r"""Runs the same simulations
    done by Fiderer, Schuff and Braun [1]_
    but with the possibility of controlling the
    phase of the NV center before the Ramsey
    measurement.
    
    The performances of the optimized
    neural network and the static strategy
    are reported in the following plots,
    together with other strategies commonly used
    in the literature. The resource can be either
    the total number of measurements or the total
    evolution time. Beside the NN
    optimized to control :math:`\tau` and
    :math:`\phi`, the
    performances of the NN trained to control
    only the evolution time :math:`\tau` are reported in
    brown.

    .. list-table::

        * - .. figure:: ../examples/nv_center_dc_phase/images/
                          nv_center_meas_invT2_0.1000_lr_0.001_
                          batchsize_1024_num_steps_128_max_resources_
                          128.00_ll_True_cl_True/plot_MeasStep_MSE.png

                invT2=0.1, Meas=128

          - .. figure:: ../examples/nv_center_dc_phase/images/
                          nv_center_time_invT2_0.1000_lr_0.01_
                          batchsize_128_num_steps_2560_max_resources_
                          2560.00_ll_False_cl_True/plot_Time_MSE.png

                invT2=0.1, Time=2560

        * - .. figure:: ../examples/nv_center_dc_phase/images/
                          nv_center_meas_invT2_min_0.0900_invT2_max_0.1100_
                          lr_0.001_batchsize_256_num_steps_512_max_resources_
                          512.00_ll_True_cl_True/plot_MeasStep_MSE.png

                invT2 in (0.09, 0.11), Meas=512

          - .. figure:: ../examples/nv_center_dc_phase/images/
                          nv_center_time_invT2_min_0.0900_invT2_
                          max_0.1100_lr_0.01_batchsize_128_num_steps_
                          1024_max_resources_1024.00_ll_False_cl_
                          True/plot_Time_MSE.png

                invT2 in (0.09, 0.11), Time=1024

        * - .. figure:: ../examples/nv_center_dc_phase/images/
                          nv_center_meas_invT2_0.2000_lr_0.001_
                          batchsize_1024_num_steps_128_max_resources_
                          128.00_ll_True_cl_True/plot_MeasStep_MSE.png
                
                invT2=0.2, Meas=128

          - .. figure:: ../examples/nv_center_dc_phase/images/
                          nv_center_time_invT2_0.2000_lr_0.01_batchsize_
                          128_num_steps_2560_max_resources_2560.00_
                          ll_False_cl_True/plot_Time_MSE.png
                
                invT2=0.2, Time=2560
        
    The shaded grey areas in the above plot indicate
    the Bayesian Cramér-Rao bound, which is the
    the ultimate precision bound computed from
    the Fisher information.
    
    There is only a very small advantage in controlling
    the phase for :math:`T_2^{-1} = 0.1`, if there is any at all.
    Similarly, with :math:`T_2^{-1} = 0, 0.01` no advantage has
    been found. For :math:`T_2^{-1} = 0.1` and `Time=2560` the
    phase control had converged to :math:`\phi=\pi`, and
    more training could not take it out of this minimum.
    For :math:`T_2^{-1} = 0.2` the advantage in introducing
    also the phase control becomes more consistent.

    Notes
    -----
    For the phase control be advantageous, the phase
    :math:`\omega \tau` must be known to some extent.
    While the error on :math:`\omega` goes down, the
    evolution time increases, so that the error on
    :math:`\omega \tau` doesn't go to zero. This limits
    the utility of controlling the phase in
    DC magnetometry.

    All the training of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.
    """
    args = parse_args()

    static_field_estimation(
        args, 1024, 128, learning_rate=1e-3, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2=0.1,
        )
    
    static_field_estimation(
        args, 1024, 128, learning_rate=1e-3, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2=0.2,
        )

    static_field_estimation(
        args, 256, 512, learning_rate=2e-2, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2_bound=(0.09, 0.11),
        cov_weight_matrix=[[1, 0], [0, 1]],
    )

    static_field_estimation(
        args, 128, 2560, learning_rate=1e-2, res='time',
        cumulative_loss=True, invT2=0.1,
        )
    
    static_field_estimation(
        args, 128, 2560, learning_rate=1e-2, res='time',
        cumulative_loss=True, invT2=0.2,
        )

    static_field_estimation(
        args, 128, 1024, learning_rate=1e-2, res='time',
        cumulative_loss=True,
        invT2_bound=(0.09, 0.11),
        cov_weight_matrix=[[1, 0], [0, 1]],
        )

if __name__ == "__main__":
    main()
