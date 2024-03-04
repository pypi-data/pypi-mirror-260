#!/usr/bin/env python3
from typing import Literal, List, Optional, \
    Tuple

from tensorflow import cast, ones, \
    gather, reshape, norm, expand_dims, \
        Variable, Tensor
from tensorflow.math import exp, cos, sin, abs, round
from tensorflow.linalg import trace
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import get_memory_info
from numpy import zeros, savetxt, loadtxt
from argparse import ArgumentParser
from os.path import join

from qsensoropt import InverseSqrtDecay, \
    ParticleFilter, Parameter, SimulationParameters
from qsensoropt.utils import train, \
    performance_evaluation, store_input_control, \
        denormalize, standard_model

from nv_center_dc import NVCenter, Magnetometry

class NVCenterACMagnetometry(NVCenter):
    r"""This model describes the estimation of the intensity of
    oscillating magnetic field of known frequency with
    an NV center used as magnetometer.
    The transversal relaxation time :math:`T_2` can
    be either known, or be a parameter to
    estimate.
    """
    def __init__(
        self, batchsize: int, params: List[Parameter],
        omega: float = 0.2,
        prec: Literal["float64", "float32"] = "float64",
        res: Literal["meas", "time"] = "meas",
        invT2: Optional[float] = None,
        ):
        r"""Constructor
        of the :py:obj:`~.NVCenterACMagnetometry` class.

        Parameters
        ----------
        batchsize: int
            Batchsize of the simulation, i.e. number of estimations
            executed simultaneously.
        params: List[:py:obj:`~.Parameter`]
            List of unknown parameters to estimate in
            the NV center experiment, with their
            respective bounds. This contains either
            the field intensity :math:`B` only or
            :math:`B` and the inverse coherence time :math:`T_2^{-1}`.
        omega: float = 0.2
            Frequency of the oscillating magnetic field to
            be estimated.
        prec : {"float64", "float32"}
            Precision of the floating point operations in the 
            simulation.
        res: {"meas", "time"}
            Resource type for the present metrological task, 
            can be either the total evolution time, i.e. `time`,
            or the total number of measurements on
            the spin, i.e. `meas`.
        invT2: float, optional
            If this parameter is specified
            the estimation is performed only for the
            field intensity :math:`B` while the inverse of the
            transverse relaxation time :math:`T_2^{-1}` is fixed
            to the value `invT2`. In this case the list `params`
            must contain a single parameter.
            If no `invT2` is specified,
            it is assumed that it is an unknown parameter that
            will be estimated along :math:`B` by the Bayesian
            procedure. In this case `params` must contain two
            objects, the second of them should be the inverse of the
            transversal relaxation time.
        """
        super().__init__(
            batchsize, params, prec=prec, res=res,
        )       
        self.invT2 = invT2
        self.omega = omega

    def model(
        self, outcomes: Tensor, controls: Tensor,
        parameters: Tensor, meas_step: Tensor,
        num_systems: int = 1,
        ):
        r"""Model for the outcome of a measurement
        on a spin that has been precessing in an
        oscillating magnetic field of intensity
        :math:`B` and known frequency
        `omega`. The probability of getting the
        outcome :math:`+1` is

        .. math::

            p(+1|B, T_2, \tau) := e^{-\frac{\tau}{T_2}}
            \cos^2 \left[ \frac{B}{2 \omega} \sin( \omega \tau) 
            \right] + \frac{1-e^{-\frac{\tau}{T_2}}}{2} \; .

        The evolution time :math:`\tau` is controlled
        by the trainable agent, and :math:`B`
        is the unknown magnetic field.
        The parameter :math:`T_2`
        may or may not be an unknown in the estimation,
        according to the value of the attribute `invT2`
        of the :py:obj:`NVCenterACMagnetometry` class.
        """
        evolution_time = controls[:, :, 0]
        B_field = parameters[:, :, 0]
        if self.invT2 is not None:
            invT2 = self.invT2
        else:
            invT2 = parameters[:, :, 1]
        exp_decay = exp(-evolution_time*invT2)
        ramsey_out = outcomes[:, :, 0]
        noise_less = (1.0-ramsey_out*cos( \
            B_field/self.omega*sin(self.omega*evolution_time)))/2.0
        return exp_decay*noise_less + (1.0-exp_decay)/2.0


def parse_args():
    """Arguments
    ---------
    scratch_dir: str, required
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./nv_center_ac/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./nv_center_ac/data"
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
                        default="./nv_center_ac/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./nv_center_ac/data")
    parser.add_argument("--prec", type=str, default="float32")
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument("--num-particles", type=int, default=480)
    parser.add_argument("--iterations", type=int, default=32768)
    parser.add_argument("--scatter-points", type=int, default=32)

    return parser.parse_args()

def alternate_field_estimation(
    args, batchsize: int, max_res: float,
    learning_rate: float = 1e-2,
    gradient_accumulation: int = 1,
    cumulative_loss: bool = False,
    log_loss: bool = False,
    res: Literal["meas", "time"] ="meas",
    omega: float = 0.2,
    invT2: Optional[float] = None,
    invT2_bound: Optional[Tuple] = None,
    cov_weight_matrix: Optional[List] = None,
    B_bounds: Tuple[float, float] = (0.0, 1.0),
    ):
    r"""Simulates the Bayesian estimation of the intensity
    of an oscillating magnetic field of known frequency
    with an NV center sensor, for a neural network
    controlling the evolution time,
    a static strategy, two variations of the
    :math:`\sigma^{-1}` strategy, and the
    particle guess heuristic (PGH).

    The measurement loop is showed in the following
    picture.

    .. image:: ../docs/_static/nv_center_ac_execute.png
        :width: 700
        :alt: nv_center_ac_execute

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
        be either the number of
        measurements or the total evolution time.
    omega: float = 0.2
        Known frequency of the oscillating magnetic
        field.
    invT2: float, optional
        Inverse of the transversal relaxation time.
        If it is infinity or it is unknown and must
        be estimated, this parameter should not
        be passed.
    invT2_bound: Tuple[float, float], optional
        Extrema of admissible values of
        the inverse of the transversal
        relaxation time, whose precise
        value is not known
        before the estimation.
    cov_weight_matrix: List, optional
        Weight matrix for the mean square error
        on the field intensity and on the decoherence
        parameter.
    B_bounds: Tuple[float, float] = (0.0, 1.0)
        Extrema of admissible values for
        the intensity of the magnetic field.
    """
    if invT2 is None and invT2_bound is None:
        raise ValueError("At least one of the two optional \
                         parameter invT2 and invT2_bound \
                         must be passed to the call of the \
                         simple_Bfield_estimation function.")

    d = 2 if invT2 is None else 1
    input_size_original = d**2+2*d+2
    input_size = input_size_original
    control_size = 1

    name = "nv_center_ac_" + res
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

    nv_center = NVCenterACMagnetometry(
        batchsize=batchsize,
        params=[Parameter(bounds=B_bounds, \
                          name="B_field"),] if invT2 is not None else
            [Parameter(bounds=B_bounds, name="B_field"),
            Parameter(bounds=invT2_bound, name="invT2"),],
        omega=omega,
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

    prefact = 1.0

    sim_nn = Magnetometry(
        particle_filter=pf,
        simpars=simpars,
        phys_model=nv_center,
        control_strategy=lambda input_tensor: \
            prefact*abs(network(input_tensor))+1.0,
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

    if res=="time" and max_res>512:
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

    # Initial value of the controls
    # in the static optimization
    initial_state = zeros((int(max_res), 1))
    for i in range(int(max_res)):
        initial_state[i, :] = i/max_res
        #initial_state[i, :] = prefact*rand()
        
    static_variables = Variable(
        initial_state, dtype=args.prec,
        )

    sim_static = Magnetometry(
        particle_filter=pf,
        simpars=simpars_static,
        phys_model=nv_center,
        control_strategy=lambda input_tensor:
            abs(gather(
                params=prefact*static_variables+1.0,
                indices=cast(
            round(denormalize(input_tensor[:, input_size_original-2],
                              (0, max_res))),
            dtype="int32"),
            )),
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
        return 1.0/(norm(
            extracted_particles[:, 0, :]-extracted_particles[:, 1, :], 
            axis=1, keepdims=True)+1e-5)

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
        if invT2_bound is not None:
            mean_invT2 = denormalize(input_tensor[:, 1], invT2_bound)
        else:
            mean_invT2 = invT2*ones((batchsize, ), dtype=args.prec)
        cov = reshape(input_tensor[:, input_size_original:\
                                   (input_size_original+d**2)],
                                   (batchsize, d, d))
        return expand_dims(((trace(cov))**(1/2)+\
                            mean_invT2)**(-1), axis=1)

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
        return expand_dims(((trace(cov))**(-1/2)), axis=1)

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

def main():
    r"""Runs the simulations
    for the estimation of the intensity
    of an oscillating magnetic field of
    known frequency, for the same parameters
    of the simulations 
    done by Fiderer, Schuff and Braun [1]_,

    The performances of the optimized
    neural network and static strategies
    are reported in the following plots,
    together with the simulated :math:`\sigma^{-1}`
    and PGH strategies, for a range of resources
    and coherence times. The resource can be either
    the total evolution time or the total
    number of measurements.

    .. list-table::

        * - .. figure:: ../examples/nv_center_ac/images/
                          nv_center_ac_meas_invT2_0.0100_lr_0.001_batchsize_
                          1024_num_steps_128_max_resources_128.00_ll_
                          True_cl_True/plot_MeasStep_MSE.png

                invT2=0.01, Meas=128

          - .. figure:: ../examples/nv_center_ac/images/
                          nv_center_ac_meas_invT2_0.1000_lr_0.001_batchsize_
                          1024_num_steps_128_max_resources_128.00_ll_
                          True_cl_True/plot_MeasStep_MSE.png

                invT2=0.1, Meas=128

        * - .. figure:: ../examples/nv_center_ac/images/
                          nv_center_ac_meas_invT2_min_0.0900_invT2_max_0.1100_
                          lr_0.001_batchsize_256_num_steps_512_max_resources_
                          512.00_ll_True_cl_True/plot_MeasStep_MSE.png

               invT2 in (0.09, 0.11), Meas=512

          - .. figure:: ../examples/nv_center_ac/images/
                           nv_center_ac_meas_lr_0.0001_batchsize_1536_
                           num_steps_24_max_resources_24.00_ll_True_
                           cl_True/plot_MeasStep_MSE.png

                invT2=0, Meas=24

        * - .. figure:: ../examples/nv_center_ac/images/
                          nv_center_ac_time_invT2_0.0100_lr_0.01_batchsize_
                          128_num_steps_2560_max_resources_
                          2560.00_ll_False_cl_True/plot_Time_MSE.png
                
                invT2=0.01, Time=2560

          - .. figure:: ../examples/nv_center_ac/images/
                          nv_center_ac_time_invT2_0.1000_lr_0.01_batchsize_
                          128_num_steps_2560_max_resources_2560.00_
                          ll_False_cl_True/plot_Time_MSE.png
                
                invT2=0.1, Time=2560
        
        * - .. figure:: ../examples/nv_center_ac/images/
                          nv_center_ac_time_invT2_min_0.0900_invT2_
                          max_0.1100_lr_0.01_batchsize_128_num_steps_
                          1024_max_resources_1024.00_ll_False_cl_
                          True/plot_Time_MSE.png

                invT2 in (0.09, 0.11), Time=1024

          - .. figure:: ../examples/nv_center_ac/images/
                          nv_center_ac_time_lr_0.01_batchsize_2048_
                          num_steps_128_max_resources_128.00_
                          ll_False_cl_True/plot_Time_MSE.png

                invT2=0, Time=128

    The shaded grey areas in the above plot indicate
    the Bayesian Cramér-Rao bound, which is the
    the ultimate precision bound computed from
    the Fisher information.
    
    In all simulations we see that an
    "adaptivity-gap" opens between the
    precision of the static and the NN
    strategies as the resources grow.

    Notes
    -----
    The model used in this example is
    formally equivalent to that of
    the :py:mod:`nv_center_dc` module,
    where the adaptive strategy gives only small
    advantages, at difference with the results
    obtained hare for AC-magnetometry.
    This is because the AC model maps
    to the DC one in a very different region
    of parameters with respect to the
    region we have explored
    in :py:mod:`nv_center_dc`.

    In AC magnetometry the technique of
    dynamical decoupling (DD) is often used to
    improve the sensitivity with respect to
    :math:`B` and to increase the coherence
    time :math:`T_2`. This consists in series
    of :math:`\pi`-pulses that reverse the
    sign of the accumulated phase.
    Given :math:`t_i, \, 0<i<N+1` the times
    at which the instantaneous :math:`\pi`-pulse
    are applied, the outcome probability for
    a noiseless estimation is given by

    .. math::
        p(0|B, T_2, \lbrace t_i \rbrace) = \cos^2 \left[ \frac{B}{2 \omega}
        \sum_{i=1}^{N+1} (-1)^i \left[ \sin(\omega t_{i})-
        \sin(\omega t_{i-1}) \right] \right] \; ,
    
    with :math:`N` being the number of pulses,
    and :math:`t_0` and :math:`t_{N+1}` being respectively
    the initialization and the measurement times.
    
    In the simulations done we have used
    no :math:`\pi`-pulse,
    but optimizing their application is the natural
    extension of this example, left
    for future works. For controlling the pulses
    there are possibilities:

    * the interval between the pulses is fixed
      to :math:`\tau = t_{i+1}-t_i`, which is
      produced by a NN together with the
      number of pulses `N`,

    * the controls are the :math:`N` time
      intervals :math:`\tau_i = t_{i}-t_{i-1}`.
      The number of pulses is fixed but they
      can be made ineffective with :math:`\tau_i = 0`,
      
    * the control is the free evolution time :math:`\tau`
      together with a boolean variable, that tells
      whether a pulse or a measurement has to be applied after
      the free evolution. This would require a stateful model
      for the NV center, where the current phase is
      the state.
     
    The problem of estimating :math:`B` knowing
    the frequency is complementary to the
    protocol for the optimal discrimination of
    frequencies presented in [3]_, which is used
    to distinguish chemical species in a sample.
    In this work
    the authors put forward an optimal strategy
    for the discrimination of two frequencies
    :math:`\omega` and :math:`\omega+\Delta \omega`,
    knowing the intensity :math:`B`.
    If :math:`\Delta \omega \ll \omega` and
    the field intensity is unknown a two stage approach
    to the problem is possible.
    We can estimate :math:`B` as done in this example,
    i.e. by considering the frequency fixed to
    :math:`\omega`, and then proceed with the optimal
    frequency discrimination based on the intensity
    just estimated. The error probability of the second
    stage depends on the precision
    of the first. Given a fixed total time for the discrimination,
    the time assigned to the first and the
    second stage can be optimized to minimize the
    final error. For close frequencies we
    expect this two stage protocol to be
    close to optimality. A small improvement would
    be to simulate the estimation of :math:`B`
    with the frequency as a nuisance parameters.
    It is important for the first stage, the estimation
    of the field intensity, to have low sensitivity
    to variations in the frequency.
    For optimizing frequency discrimination
    with :math:`B` as a nuisance parameter
    in a fully integrated protocol the introduction
    of :math:`\pi`-pulses is necessary, just like
    for dynamical decoupling.
    The natural extension of hypothesis testing
    on the frequency is the
    estimation of both the intensity and the frequency
    of the magnetic field optimally, both starting from
    a broad prior. All these improvements are left
    for future work.

    All the training of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.
    
    .. [3] Schmitt, S., Gefen, T., Louzon, D. et al.
        npj Quantum Inf 7, 55 (2021).
    """
    args = parse_args()
    
    alternate_field_estimation(
        args, 1536, 24, learning_rate=1e-4, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2=0.0,
        )

    alternate_field_estimation(
        args, 1024, 128, learning_rate=1e-3, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2=0.01,
        )

    alternate_field_estimation(
        args, 1024, 128, learning_rate=1e-3, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2=0.1,
        )
    
    alternate_field_estimation(
        args, 256, 512, learning_rate=1e-3, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2_bound=(0.09, 0.11),
        cov_weight_matrix=[[1, 0], [0, 1]],
    )
    
    alternate_field_estimation(
        args, 2048, 128, learning_rate=1e-2, res='time',
        cumulative_loss=True, invT2=0.0,
        )

    alternate_field_estimation(
        args, 128, 2560, learning_rate=1e-2, res='time',
        cumulative_loss=True, invT2 = 0.01,
        )

    alternate_field_estimation(
        args, 128, 2560, learning_rate=1e-2, res='time',
        cumulative_loss=True, invT2=0.1,
        )

    alternate_field_estimation(
        args, 128, 1024, learning_rate=1e-2, res='time',
        cumulative_loss=True,
        invT2_bound=(0.09, 0.11),
        cov_weight_matrix=[[1, 0], [0, 1]],
        )

if __name__ == "__main__":
    main()
