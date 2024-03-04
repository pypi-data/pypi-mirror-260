#!/usr/bin/env python3
from typing import Literal, Callable, List, Optional, \
    Tuple

from tensorflow import cast, stop_gradient, ones, \
    gather, concat, reshape, norm, expand_dims, \
        broadcast_to, constant, \
            Variable, Tensor
from tensorflow.math import exp, log, cos, abs, minimum, \
    reciprocal_no_nan, round
from tensorflow.linalg import trace, tensor_diag, matmul
from tensorflow.random import stateless_uniform, uniform, \
    Generator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import get_memory_info
from numpy import ceil, sqrt, zeros, savetxt, loadtxt
from numpy.random import rand
from itertools import product
from argparse import ArgumentParser
from os.path import join
from math import pi

from qsensoropt import StatelessPhysicalModel, \
    StatelessMetrology, InverseSqrtDecay, ParticleFilter, \
        Parameter, Control, SimulationParameters
from qsensoropt.utils import train, \
    performance_evaluation, get_seed, store_input_control, \
        standard_model, denormalize

class NVCenter(StatelessPhysicalModel):
    r"""Model for the negatively charged NV center in
    diamond used for various quantum metrological
    task. A single measurement on the NV center
    consists in multiple Ramsey sequencies of the same
    controllable duration applied to the NV center,
    followed by photon counting of the photoluminescent
    photon and a majority voting to decide the
    binary outcome. The NV center is reinitialized
    after each photon counting.
    During the free evolution in the Ramsey sequence
    the NV center precesses freely in the external
    magnetic field, thereby encoding its value
    in its state. The two possible controls we
    have on the system are the duration of the
    free evolution :math:`\tau` and the phase
    :math:`\phi` applied before
    the photon counting.
    The resource of the estimation task
    can be either the total number of measurements or
    the total evolution time.

    **Achtung!** The :py:meth:`~.StatelessPhysicalModel.model`
    method must still be implemented in this class. It
    should describe the probability of getting
    :math:`+1` in the measurement after the majority voting
    from the collected photons.
    """
    def __init__(
        self, batchsize: int, params: List[Parameter],
        prec: Literal["float64", "float32"] = "float64",
        res: Literal["meas", "time"] = "meas",
        control_phase: bool = False,
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
            or the total number of measurements on
            the NV center, i.e. `meas`.
        control_phase: bool = False
            If this flag is `True`, beside the free evolution time,
            also the phase applied
            before the photon counting is controlled by
            the agent.
        """
        self.control_phase = control_phase

        if not res in ("meas", "time"):
            raise ValueError("The allowed values of \
                             res are time and res.")
        
        if self.control_phase:
            # Controls the time and the phase.
            controls=[
                Control(name="EvolutionTime"),
                Control(name="Phase"),
            ]
        else:
            # The only control is the free precession
            # time of the NV center
            # in the magnetic field, between the two pi/2-pulses.
            controls=[
                Control(name="EvolutionTime"),
            ]
        
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
        r"""Measurement on the NV center.
        
        The NV center is measured after having evolved freely in the
        magnetic field for a time specified by the parameter
        `control`. The possible outcomes
        are :math:`+1` and :math:`-1`,
        selected stochastically according to the probabilities
        :math:`p(\pm 1| \vec{\theta}, \tau)`, where :math:`\tau` is the
        evolution time (the control) and :math:`\vec{\theta}`
        the parameters to estimate. This method
        returns the observed outcomes
        and their log-likelihood.

        **Achtung!** The :py:meth:`model` method must return
        the probability :math:`p(\pm 1| \vec{\theta}, \tau)`
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
        total number of measurements, or the total
        evolution time, according to the
        attribute `res` of the :py:obj:`NVCenter`
        class.
        """
        if self.res == "time":
            return resources+abs(controls[:, 0:1])
        return resources+1.0


class NVCenterDCMagnetometry(NVCenter):
    r"""Model describing the estimation of a
    static magnetic field with an NV center
    used as magnetometer.
    The spin-spin relaxation time :math:`T_2^{-1}` can
    be either known, or be a parameter to
    estimate. The estimation will be
    formulated in terms of the precession
    frequency :math:`\omega` of the NV center, which
    is proportional to the magnetic
    field :math:`B`.

    This physical model and the application of 
    Reinforcement Learning to the estimation
    of a static magnetic fields have been also studied in the
    seminal work of Fiderer, Schuff and Braun [1]_.

    .. [1] Lukas J. Fiderer, Jonas Schuff, and Daniel Braun
        PRX Quantum 2, 020303 (2021).
    """
    def __init__(
        self, batchsize: int, params: List[Parameter],
        prec: Literal["float64", "float32"] = "float64",
        res: Literal["meas", "time"] = "meas",
        invT2: Optional[float] = None,
        ):
        r"""Constructor
        of the :py:obj:`~.NVCenterDCMagnetometry` class.

        Parameters
        ----------
        batchsize: int
            Batchsize of the simulation, i.e. number of estimations
            executed simultaneously.
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
        )

        self.invT2 = invT2

    def model(
        self, outcomes: Tensor, controls: Tensor,
        parameters: Tensor, meas_step: Tensor,
        num_systems: int = 1,
        ) -> Tensor:
        r"""Model for the outcome of a measurement
        on a NV center subject to free precession in a static
        magnetic field.  The probability of getting the
        outcome :math:`+1` is

        .. math::

            p(+1|\omega, T_2, \tau) := e^{-\frac{\tau}{T_2}}
            \cos^2 \left( \frac{\omega}{2} \tau \right) +
            \frac{1-e^{-\frac{\tau}{T_2}}}{2} \; .

        The evolution time :math:`\tau` is controlled
        by the trainable agent, and :math:`\omega`
        is the unknown precession frequency, which is
        proportional to the magnetic field.
        The parameter :math:`T_2`
        may or may not be an unknown in the estimation,
        according to the value of the attribute `invT2`
        of the :py:obj:`~.NVCenterDCMagnetometry` class.
        """
        evolution_time = controls[:, :, 0]
        omega = parameters[:, :, 0]
        if self.invT2 is not None:
            invT2 = self.invT2
        else:
            invT2 = parameters[:, :, 1]
        exp_decay = exp(-evolution_time*invT2)
        ramsey_out = outcomes[:, :, 0]
        noise_less = (1.0-ramsey_out*cos(omega*evolution_time))/2.0
        return exp_decay*noise_less + (1.0-exp_decay)/2.0
    
class Magnetometry(StatelessMetrology):
    r"""Simulates the estimation of a magnetic field
    with a mean square error loss. This class is suitable
    for a neural network agent, for a static strategy,
    and for other simple controls known in
    the literature, like the :math:`\sigma^{-1}` strategy
    and the particle guess heuristic (PGH).
    It works both for static and for oscillating
    magnetic fields.
    """
    def __init__(
            self, particle_filter: ParticleFilter,
            phys_model: NVCenter,
            control_strategy: Callable,
            simpars: SimulationParameters,
            cov_weight_matrix=None,
            eta_flag: bool = False,
            extraction_flag: bool = False,
            cov_flag: bool = False,
    ):
        r"""Constructor of the 
        :py:obj:`Magnetometry` class.

        Parameters
        ----------
        particle_filter: :py:obj:`~.ParticleFilter`
            Particle filter responsible for the update
            of the Bayesian posterior on the parameters
            and on the state of the probe. It
            contains the methods for applying the Bayes
            rule and computing Bayesian estimators
            from the posterior.
        phys_model: :py:obj:`~.NVCenter`
            Abstract description of the parameters
            encoding and of the measurement on the
            NV center.
        control_strategy: Callable
            Callable object (normally a
            function or a lambda function) that
            computes the values of the controls
            for the next measurement from
            the `Tensor` `input_strategy`.
            This class expects a callable
            with the following
            header

            ``controls = 
            control_strategy(input_strategy)``

            It is typically a wrapper for the
            neural network or a vector of
            static controls.
        simpars: :py:obj:`~.SimulationParameters`
            Contains the flags and parameters
            that regulate the stopping
            condition of the measurement loop
            and modify the loss function used in the
            training.
        cov_weight_matrix: List, optional
            Weight matrix that determines the relative
            contribution to the total error of the
            parameters in `phys_model.params`.
            It is list of `float` representing
            a positive semidefinite matrix.
            If this parameter is not passed then the
            default weight matrix is the identity, i.e.
            :math:`G=\text{Id}`.
        eta_flag: bool = False
            This flag
            controls the addition of a normalization factor
            to the MSE loss.

            If `eta_flag` is True, the MSE loss is divided by the
            normalization factor
            
            .. math::
                \eta = \min \left( \sum_{i=1}^d G_{ii}
                \frac{(b_i-a_i)}{12}, \frac{1}{T} \right) \; ,

            where :math:`(a_i, b_i)` are the bounds
            of the `i`-th parameter in `phys_model.params`
            and :math:`G_{ii}` are the diagonal entries of
            `cov_weight_matrix`. :math:`T` is the total
            elapsed evolution time, which can be different
            for each estimation in the batch.

            **Achtung!** This flag should be used only
            if the resource is the total estimation time.
        extraction_flag: bool = False
            If `extraction_flag=True` a couple of
            particles are sampled from the posterior
            and added to the `input_strategy` `Tensor`.
            This is useful to simulate the PGH control for
            the evolution time, according to which the `k-th`
            control should be

            .. math::
                \tau_k = \frac{1}{||\vec{x}_1 - \vec{x}_2||
                + \epsilon} \; ,
                :label: PGH_tau

            with :math:`\epsilon \ll 1`,
            where :math:`\vec{x}_1` and :math:`\vec{x}_2` are
            respectively the first and the second particle
            extracted from the ensemble and :math:`||\cdot||`
            is the cartesian norm.
        cov_flag: bool = False
            If `cov_flag=True` a flattened version of the
            covariance matrix of the particle filter
            ensemble is added to the `input_strategy` `Tensor`.
            This is useful to simulate the :math:`\sigma^{-1}`
            control strategy and its variant that accounts
            for a finite
            transversal relaxation time. They prescribe
            respectively for the `k-th` control

            .. math::
                \tau_k = \frac{1}{\left[ \text{tr} 
                (\Sigma) \right]^{\frac{1}{2}} } \; ,
                :label: cov_1
            
            and

            .. math::
                \tau_k = \frac{1}{\left[ \text{tr} 
                (\Sigma) \right]^{\frac{1}{2}} +
                \widehat{T_2^{-1}}} \; ,
                :label: cov_2
            
            being :math:`\Sigma` the covariance matrix
            of the posterior computed with the
            :py:meth:`~.ParticleFilter.compute_covariance`
            method.
        """
        super().__init__(
            particle_filter, phys_model, control_strategy,
            simpars, cov_weight_matrix,
            )

        d = self.pf.d
        self.eta_flag = eta_flag
        self.extraction_flag = extraction_flag
        self.cov_flag = cov_flag

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

    def generate_input(
        self, weights: Tensor,
        particles: Tensor,
        meas_step: Tensor,
        used_resources: Tensor,
        rangen: Generator,
        ):
        """Generates the `input_strategy` `Tensor`
        of the :py:meth:`~.StatelessMetrology.generate_input`
        method.  The returned `Tensor` is influenced
        by the parameters `extract_flag` and
        `cov_flag` of the constructor.
        """
        d = self.pf.d
        input_tensor = super().generate_input(
            weights, particles, meas_step, used_resources,
            rangen,
            )

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
        """Mean square error on the parameters,
        as computed in :py:meth:`~.StatelessMetrology.loss_function`.
        The behavior of this
        method is influence by the flag `eta_flag` passed to the
        constructor of the class.
        """
        pars = self.simpars
        loss_values = super().loss_function(
                weights, particles, true_values,
                used_resources, meas_step,
            )
        d = len(self.pf.phys_model.params)
        if self.eta_flag:
            init_var = []
            for param in self.pf.phys_model.params:
                bounds = param.bounds
                init_var.append(1/12*(bounds[1]-bounds[0])**2)
            initial_loss = broadcast_to(reshape(
                tensor_diag(constant(init_var, dtype=pars.prec)),
                (1, d, d),
                ), (self.bs, d, d),
            )
            initial_loss_scalar = expand_dims(
                trace(matmul(
                    self.cov_weight_matrix_tensor, initial_loss),
                    ), axis=1,
                    )
            eta = minimum(
                reciprocal_no_nan(used_resources),
                initial_loss_scalar,
            )
            loss_values = loss_values/eta
        return loss_values

def parse_args():
    """Arguments
    ---------
    scratch_dir: str
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./nv_center_dc/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./nv_center_dc/data"
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
                        default="./nv_center_dc/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./nv_center_dc/data")
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
    magnetic field with an NV center, for a neural network
    controlling the evolution time,
    a static strategy, two variations of the
    :math:`\sigma^{-1}` strategy, and the
    particle guess heuristic (PGH).

    The measurement loop is showed in the following
    picture.

    .. image:: ../docs/_static/nv_center_execute.png
        :width: 700
        :alt: nv_center_execute

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
    control_size = 1

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
    output_tensor = (input_tensor[:, -1:]+1)/2
    network.compile(loss='mean_squared_error',
                    optimizer='adam')
    network.fit(
        input_tensor, output_tensor,
        epochs=12, batch_size=1024, verbose=0,
        )

    nv_center = NVCenterDCMagnetometry(
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

    sim_nn = Magnetometry(
        particle_filter=pf,
        simpars=simpars,
        phys_model=nv_center,
        control_strategy=lambda input_tensor: \
            prefact*abs(network(input_tensor))+1,
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

    pf_eval = ParticleFilter(
        num_particles=args.num_particles,
        phys_model=nv_center,
        resample_fraction=0.98, prec=args.prec,
    )

    sim_nn_eval = Magnetometry(
        particle_filter=pf_eval,
        simpars=simpars,
        phys_model=nv_center,
        control_strategy=lambda input_tensor: \
            prefact*abs(network(input_tensor))+1,
        cov_weight_matrix=cov_weight_matrix,
        eta_flag=False,
    )

    performance_evaluation(
        sim_nn_eval,
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
    initial_state = zeros((int(max_res), 1))
    for i in range(int(max_res)):
        initial_state[i, :] = i/(max_res)
        # initial_state[i, :] = prefact*rand()

    static_variables = Variable(
        initial_state, dtype=args.prec,
        )

    sim_static = Magnetometry(
        particle_filter=pf,
        simpars=simpars_static,
        phys_model=nv_center,
        control_strategy=lambda input_tensor:
            abs(gather(
                params=prefact*static_variables+1,
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
        sim_static, Adam(learning_rate=decaying_learning_rate),
        args.iterations, args.scratch_dir,
        custom_controls=static_variables,
        xla_compile=True,
        gradient_accumulation=gradient_accumulation,
    )
    
    print(get_memory_info('GPU:0')['peak']/1024**3)

    savetxt(
        join(args.trained_models_dir, str(sim_static)),
            static_variables.numpy(),
            )
    # static_variables = Variable(loadtxt(
    #     join(args.trained_models_dir, str(sim_static)),
    #     )[:, None], dtype=args.prec,
    # )

    sim_static_eval = Magnetometry(
        particle_filter=pf_eval,
        simpars=simpars_static,
        phys_model=nv_center,
        control_strategy=lambda input_tensor:
            abs(gather(
                params=prefact*static_variables+1,
                indices=cast(
        round(denormalize(input_tensor[:, input_size_original-2],
                          (0, max_res))),
        dtype="int32"),
            )),
        cov_weight_matrix=cov_weight_matrix,
    )
    
    performance_evaluation(
        sim_static_eval,
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
            axis=1, keepdims=True, ord=1)+1e-5)

    sim_pgh = Magnetometry(
        particle_filter=pf_eval,
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
        return expand_dims(((trace(cov))**(1/2)+\
                            mean_invT2)**(-1), axis=1)

    sim_sigma = Magnetometry(
        particle_filter=pf_eval,
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
        particle_filter=pf_eval,
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
        return expand_dims(((4*pi**2*trace(cov))**(-1/2)), axis=1)

    sim_sigmapi = Magnetometry(
        particle_filter=pf_eval,
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
    done by Fiderer, Schuff and Braun [1]_.
    
    The performances of the optimized
    neural network and static strategies
    are reported in the following plot,
    together with other strategies commonly used
    in the literature. The resources can be
    the number of measurements or the total
    evolution time.

    .. list-table::

        * - .. figure:: ../examples/nv_center_dc/images/
                          nv_center_meas_invT2_0.0100_lr_0.001_batchsize_
                          1024_num_steps_128_max_resources_128.00_ll_
                          True_cl_True/plot_MeasStep_MSE.png

                invT2=0.01, Meas=128

          - .. figure:: ../examples/nv_center_dc/images/
                          nv_center_meas_invT2_0.1000_lr_0.001_batchsize_
                          1024_num_steps_128_max_resources_128.00_ll_
                          True_cl_True/plot_MeasStep_MSE.png

                invT2=0.1, Meas=128

        * - .. figure:: ../examples/nv_center_dc/images/
                          nv_center_meas_invT2_min_0.0900_invT2_max_0.1100_
                          lr_0.001_batchsize_256_num_steps_512_max_resources_
                          512.00_ll_True_cl_True/plot_MeasStep_MSE.png

               invT2 in (0.09, 0.11), Meas=512

          - .. figure:: ../examples/nv_center_dc/images/
                           nv_center_meas_lr_0.0001_batchsize_2048_
                           num_steps_24_max_resources_24.00_ll_True_
                           cl_True/plot_MeasStep_MSE.png

                invT2=0, Meas=24

        * - .. figure:: ../examples/nv_center_dc/images/
                          nv_center_time_invT2_0.0100_lr_0.001_batchsize_
                          64_num_steps_2560_max_resources_
                          2560.00_ll_False_cl_True/plot_Time_MSE.png
                
                invT2=0.01, Time=2560

          - .. figure:: ../examples/nv_center_dc/images/
                          nv_center_time_invT2_0.1000_lr_0.01_batchsize_
                          128_num_steps_2560_max_resources_2560.00_
                          ll_False_cl_True/plot_Time_MSE.png
                
                invT2=0.1, Time=2560
        
        * - .. figure:: ../examples/nv_center_dc/images/
                          nv_center_time_invT2_min_0.0900_invT2_
                          max_0.1100_lr_0.01_batchsize_128_num_steps_
                          1024_max_resources_1024.00_ll_False_cl_
                          True/plot_Time_MSE.png

                invT2 in (0.09, 0.11), Time=1024

          - .. figure:: ../examples/nv_center_dc/images/
                          nv_center_time_lr_0.01_batchsize_2048_
                          num_steps_128_max_resources_128.00_
                          ll_False_cl_True/plot_Time_MSE.png

                invT2=0, Time=128

    For the plot referring to the estimation of
    `omega` only the green line is the best
    performance found in the literature so far, obtained
    in [1]_ with model-free RL. In the plot corresponding
    to the simultaneous estimation of both the frequency
    and the decoherence time we din't compare our
    results with [1]_ and the green line in simply the
    :math:`\sigma^{-1}`.
    
    The shaded grey areas in the above plot indicate
    the Bayesian Cramér-Rao bound, which is the
    the ultimate precision bound computed from
    the Fisher information.
    
    From the above plots we can conclude
    that the adaptive strategy offers
    no advantage with respect to the
    optimal static strategy for those
    experiments limited in the number
    of measurements and for all
    those with a sufficiently high
    coherence time. For :math:`T_2=10` we
    see some small advantage of the adaptive
    strategy in the time limited experiments.
    This observation is in accordance with
    the analysis based only on the Fisher information.
    For :math:`T_2=0` the Fisher information
    of a single measurement is :math:`\tau^2` and is
    independent on :math:`\omega`. For :math:`T_2>0`
    the Fisher information manifests a dependence
    on :math:`\omega`, which could indicate
    the possibility of an adaptive strategy
    being useful, which is confirmed in
    these simulations.

    Notes
    -----
    The results of the simulations with `invT2 in (0.09, 0.11)`
    are very similar to that with `invT2=0.1` because
    of the relatively narrow prior on `invT2`.

    For an NV center used as a magnetometer the
    actual decoherence model is given by
    :math:`e^{-\left( \frac{\tau}{T_2} \right)^2}`
    instead of
    :math:`e^{-\frac{\tau}{T_2}}`

    **Achtung!** The performances of the time limited
    estimations with the :math:`\sigma^{-1}`
    and the PGH strategies are not in accordance
    with the results of
    Fiderer, Schuff and Braun [1]_. Also the simulations
    with `invT2 in (0.09, 0.11)` do not agree with the results
    reported in this paper.

    Normally in the applications the meaningful
    resource is the total time required for the
    estimation. This doesn't coincide however with
    the total evolution time that we considered,
    because the initialization of the NV center,
    the read-out the and
    the data processing all take time.
    This overhead time is
    proportional to the number of measurements,
    so that in a real experiment we expect the
    actual resource to be a combination of the
    evolution time and the number of
    measurements.

    In a future work the role of the higher moments
    of the posterior distribution in the
    determination of the controls should be
    explored. In particular it should be understood if
    with

    .. math::
        \tau = NN(\hat{\omega}, \hat{\sigma},
        \hat{\gamma}_1, \frac{\hat{\mu}_4}{\hat{\sigma}^4},
        \frac{\hat{\mu}_5}{\hat{\sigma}^5}, \cdots) \; ,
    
    more advantage from the adaptivity could be extracted.

    In room-temperature magnetometry it is impossible
    to do single-shot readout of the NV center state
    (SSR). We should train the control strategy to
    work with non-SSR, as done by Zohar et al [2]_

    All the trainings of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.

    .. [2] I Zohar et al, Quantum Sci. Technol. 8 035017 (2023).
    """
    args = parse_args()

    static_field_estimation(
        args, 2048, 24, learning_rate=1e-4, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2=0.0,
        )

    # num_particles = 1536
    static_field_estimation(
       args, 1024, 128, learning_rate=1e-3, res='meas',
       log_loss=True, cumulative_loss=True,
       invT2=0.01,
       )

    static_field_estimation(
        args, 1024, 128, learning_rate=1e-3, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2=0.1,
        )

    static_field_estimation(
        args, 256, 512, learning_rate=1e-3, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2_bound=(0.09, 0.11),
        cov_weight_matrix=[[1, 0], [0, 1]],
    )

    static_field_estimation(
        args, 2048, 128, learning_rate=1e-2, res='time',
        cumulative_loss=True, invT2=0.0,
        )
    
    # num_particles_training = 1024
    # num_particles_eval = 4096
    static_field_estimation(
        args, 64, 2560, learning_rate=1e-3, res='time',
        cumulative_loss=True, invT2 = 0.01,
        )

    static_field_estimation(
        args, 128, 2560, learning_rate=1e-2, res='time',
        cumulative_loss=True, invT2=0.1,
        )
    
    static_field_estimation(
        args, 128, 1024, learning_rate=1e-2, res='time',
        cumulative_loss=True,
        invT2_bound=(0.09, 0.11),
        cov_weight_matrix=[[1, 0], [0, 1]],
        )

    static_field_estimation(
        args, 1024, 128, learning_rate=1e-3, res='meas',
        log_loss=True, cumulative_loss=True,
        invT2=0.2,
        )
    
    static_field_estimation(
        args, 128, 2560, learning_rate=1e-2, res='time',
        cumulative_loss=True, invT2=0.2,
        )
    

if __name__ == "__main__":
    main()
