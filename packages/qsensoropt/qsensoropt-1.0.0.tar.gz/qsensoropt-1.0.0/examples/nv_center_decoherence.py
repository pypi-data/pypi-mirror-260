#!/usr/bin/env python3
from typing import Callable, Literal, List, Optional

from tensorflow import expand_dims, concat, \
    squeeze, tensor_scatter_nd_update, \
        reshape, argsort, ones, constant, \
            broadcast_to, Tensor
from tensorflow.math import exp, abs, pow, minimum, \
                reciprocal_no_nan
from tensorflow.linalg import tensor_diag, trace, matmul
from tensorflow.random import uniform, Generator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import \
    get_memory_info
from numpy import zeros
from numpy.random import rand
from argparse import ArgumentParser
from os.path import join
from math import floor as mfloor

from qsensoropt import InverseSqrtDecay, \
    ParticleFilter, Parameter, SimulationParameters, \
        StatelessMetrology
from qsensoropt.utils import train, \
    performance_evaluation, store_input_control, \
        denormalize, standard_model, random_uniform, \
        get_seed

from nv_center_dc import NVCenter

class NVCenterDecoherence(NVCenter):
    """Model describing an NV center subject
    to a variable amount of decoherence.
    The dephasing rate
    encodes some useful information about the
    environment, which
    can be recovered by estimating
    the transverse relaxation time and
    the decaying exponent.
    """
    def __init__(
        self, batchsize: int,
        params: List[Parameter],
        prec: Literal["float64", "float32"] = "float64",
        res: Literal["meas", "time"] = "meas",
        ):
        r"""Constructor
        of the :py:obj:`~.NVCenterDecoherence` class.

        Parameters
        ----------
        batchsize: int
            Batchsize of the simulation, i.e.
            number of estimations
            executed simultaneously.
        params: List[:py:obj:`~.Parameter`]
            List of unknown parameters to estimate in
            the NV center experiment, with their priors.
            It should contain the inverse
            of the characteristic time
            of the dephasing process, indicated with
            the symbol :math:`T^{-1}`
            and the exponent :math:`\beta`
            of the decay. This last parameter carries
            information on the spectral density
            of the noise.
        prec : {"float64", "float32"}
            Precision of the floating point operations in the 
            simulation.
        res: {"meas", "time"}
            Resource type for the present metrological task.
            It can be either the total evolution time, i.e. `time`,
            or the total number of measurements on
            the NV center, i.e. `meas`.
        """
        super().__init__(
            batchsize, params, prec=prec, res=res,
        )       

    def model(
        self, outcomes: Tensor, controls: Tensor,
        parameters: Tensor, meas_step: Tensor,
        num_systems: int = 1,
        ):
        r"""Model for the outcome of a photon counting
        measurement following a Ramsey sequence
        on the NV center sensor subject to dephasing noise.
        The probability of getting the
        outcome :math:`+1` is

        .. math::
            p(+1|T, \beta, \tau) := \frac{1 + e^{-\left(
                \frac{\tau}{T}\right)^{ 20 \beta}}}{2} \; .

        The evolution time :math:`\tau` is controlled
        by the trainable agent and :math:`T` and :math:`\beta`
        are the two unknown characteristic parameters
        of the noise. The factor `20` appearing
        at the exponent is just the
        normalization factor we used for :math:`\beta`.
        """
        evolution_time = controls[:, :, 0]
        decay_time_inv = parameters[:, :, 0]
        decay_exponent = parameters[:, :, 1]

        exp_decay = pow(
            evolution_time*decay_time_inv, 20*decay_exponent,
            )
        ramsey_out = outcomes[:, :, 0]
        return (1.0-ramsey_out*exp(-exp_decay))/2.0
    
class DecoherenceSimulation(StatelessMetrology):
    r"""This class does the same job of
    :py:obj:`~.StatelessMetrology`, but it can
    append a randomly generated control time to the
    `input_strategy` Tensor produced by the
    :py:meth:`~.generate_input` method
    and it can compute the median square error
    (MedianSE) instead of the mean square error
    (MSE) in the :py:meth:`~.loss_function` method.
    """
    def __init__(
            self, particle_filter: ParticleFilter,
            phys_model: NVCenterDecoherence,
            control_strategy: Callable,
            simpars: SimulationParameters,
            cov_weight_matrix: Optional[List] = None,
            random: bool = False,
            median: bool = False,
            loss_normalization: bool = False,
            ):
        r"""Parameters passed to the constructor of
        the :py:obj:`~.DecoherenceSimulation` class.

        Parameters
        ----------
        particle_filter: :py:obj:`~.ParticleFilter`
            Particle filter responsible for the update
            of the Bayesian posterior on the parameters.
        phys_model: :py:obj:`~.NVCenterDecoherence`
            Abstract description of the
            NC center for the characterization
            of the dephasing noise.
        control_strategy: Callable
            Callable object (normally a
            function or a lambda function) that
            computes the values of the controls
            for the next measurement from
            the `Tensor` `input_strategy`, which is
            produced by the method
            :py:meth:`~.StatelessSimulation.generate_input`.
        simpars: :py:obj:`~.SimulationParameters`
            Contains the flags and parameters
            that regulate the stopping
            condition of the measurement loop
            and modify the loss function used in the
            training.
        cov_weight_matrix: List, optional
            Positive semidefinite weight matrix.
            If this parameter is not passed then the
            default weight matrix is the identity, i.e.
            :math:`G=\text{Id}`.
        random: bool = False
            If this flag is `True` then a randomly chosen
            evolution time :math:`\tau_r`
            is added to the `input_strategy`
            Tensor produced by :py:meth:`~.generate_input`.
        median: bool = False
            If this flag is `True`, then instead of
            computing the mean square error (MSE) from a
            batch of simulation the median square error
            (MedianSE) is computed. See the documentation
            of the :py:meth:`~.loss_function` method.

            **Achtung!** The median **can** be used in the
            training, however it means throwing away all the
            simulations in the batch except to the one
            that realizes the median. This is not an efficient
            use of the simulations in the training. When used
            the median should be always confined to
            the performances evaluation, while the training
            is to be carried out with the mean square error.
        loss_normalization: bool = False
            If `loss_normalization` is True,
            then the loss is divided by the
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
        """
        super().__init__(
            particle_filter, phys_model,
            control_strategy, simpars,
            cov_weight_matrix,
            )
        
        self.random = random
        self.median = median
        self.loss_normalization = loss_normalization
        if self.median:
            simpars.sim_name += "_median"
        if self.random:
            self.input_size += 1
            self.input_name += ["RandomTime", ]
        
    def generate_input(
        self, weights: Tensor,
        particles: Tensor,
        meas_step: Tensor,
        used_resources: Tensor,
        rangen: Generator,
        ):
        r"""This method returns the same `input_strategy`
        Tensor of the
        :py:meth:`~.StatelessMetrology.generate_input`
        method, but, if the attribute `random` is `True`,
        an extra column is appended to this `Tensor`
        containing the randomly generated
        evolution time :math:`\tau_r`.
        The value of :math:`\tau_r^{-1}` is
        uniformly extracted in the interval
        of the admissible values for the inverse of the
        coherence time :math:`T^{-1}`.
        """
        input_tensor = super().generate_input(
            weights, particles,
            meas_step, used_resources,
            rangen,
            )
        if self.random:
            invT_bounds = self.pf.phys_model.params[0].bounds
            random_invT_control = \
                expand_dims(random_uniform(
                self.bs, self.simpars.prec,
                invT_bounds[0], invT_bounds[1],
                get_seed(rangen),
                ), axis=1,
            )
            return concat(
                [input_tensor, 1.0/random_invT_control], 1,
                )
        else:
            return input_tensor
        
    def loss_function(
            self, weights: Tensor, particles: Tensor,
            true_values: Tensor, used_resources: Tensor,
            meas_step: Tensor):
        r"""Computes the loss for each estimation in the
        batch.
        
        If `median` is `False`, then it returns
        the same loss of the
        :py:obj:`~.StatelessMetrology.loss_function`
        method,
        i.e. the square error for each simulation
        in the batch, called
        :math:`\ell (\omega_k, \vec{\lambda})`,
        where :math:`k` runs from :math:`0` to :math:`B`,
        with :math:`B` the batchsize. If
        the flag `median` is `True`, this method
        returns the median square error of the batch, 
        in symbols
        :math:`\text{Median} [ \ell (\omega_k, \vec{\lambda})]`.
        In order to compute it, the vector of
        losses :math:`\ell (\omega_k, \vec{\lambda})` is
        sorted, the element at position
        :math:`\lfloor B/2 \rfloor`
        is then the median of the losses in the batch.
        Calling :math:`k_0` the
        position in the unsorted batch of the simulation
        realizing the median, the outcome of this method
        is the vector

        .. math::
            \ell' (\omega_k, \vec{\lambda}) = 
            B \delta_{k, k_0} \text{Median} 
            [ \ell (\omega_k, \vec{\lambda})] \; .

        The advantage of using the median error is the
        reduced sensitivity to outliers with respect to
        the mean erro.

        **Achtung!** Even if the performances evaluation
        can be performed with the median square error,
        the training should always minimize
        the mean square error.
        """
        pars = self.simpars
        old_losses = super().loss_function(
            weights, particles,
            true_values, used_resources, meas_step,
            )
        if self.loss_normalization:
            init_var = []
            for param in self.pf.phys_model.params:
                bounds = param.bounds
                init_var.append(1/12*(bounds[1]-bounds[0])**2)
            initial_loss = broadcast_to(reshape(
                tensor_diag(constant(init_var, dtype=pars.prec)),
                (1, 2, 2),
                ), (self.bs, 2, 2),
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
            old_losses = old_losses/eta
        if self.median:
            losses = squeeze(old_losses)
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
        return old_losses

def parse_args():
    """Arguments
    ---------
    scratch_dir: str, required
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./nv_center_decoherence/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./nv_center_decoherence/data"
        Directory containing the csv files
        produced by the :py:func:`~.utils.performance_evaluation`
        and the :py:func:`~.utils.store_input_control` functions.
    prec: str = "float32"
        Floating point precision of the
        whole simulation.
    n: int = 64
        Number of neurons per layer in the neural network.
    num_particles: int = 2048
        Number of particles in the ensemble representing
        the posterior.
    iterations: int = 4096
        Number of training steps.
    scatter_points: int = 32
        Number of points in the Resources/Precision
        csv produced by
        :py:func:`~.utils.performance_evaluation`.
    """
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir", type=str,
                        default="./nv_center_decoherence/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./nv_center_decoherence/data")
    parser.add_argument("--prec", type=str, default="float32")
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument("--num-particles", type=int, default=2048)
    parser.add_argument("--iterations", type=int, default=4096)
    parser.add_argument("--scatter-points", type=int, default=32)

    return parser.parse_args()

def decoherence_estimation(
    args, batchsize: int, max_res: float,
    learning_rate: float = 1e-3,
    gradient_accumulation: int = 1,
    cumulative_loss: bool = True,
    log_loss: bool = False,
    res: Literal["meas", "time"] ="meas",
    loss_normalization: bool = False,
    beta_nuisance: bool = False,
    fixed_beta: bool = False,
    ):
    r"""Simulates the Bayesian estimation of the decoherence
    parameters of a dephasing noise acting on an NV center.
    The control parameter is the free evolution time
    of the system during the Ramsey sequence.
    We have implement four strategies for the
    control of the evolution time:

    * Adaptive strategy with a trained neural network
      on the basis of the
      state of the particle filter (adaptive strategy).

    * Static strategy implemented with a neural network
      that receives in input the amount of already
      consumed resources (time or measurements)

    * Random strategy, with an evolution time
      chosen in the admissible interval for the
      values of :math:`T^{-1}`.
    
    * Inverse time strategy. The evolution time is
      is :math:`\tau = \alpha_M^{\frac{1}{\widehat{\beta}}}
      \widehat{T^{-1}}` for the measurement-limited
      estimation and
      :math:`\tau = \alpha_T^{\frac{1}{\widehat{\beta}}}
      \widehat{T^{-1}}` for the time-limited estimations,
      where :math:`\alpha_M = 0.79681` and
      :math:`\alpha_M = 0.43711`.
      These numerical coefficients come from
      the optimization of the Fisher information.
      For the simulations where :math:`\beta` is a nuisance
      parameter :math:`\alpha_M` is used also for the
      time-limited estimation.

    This function trains
    the static and the adaptive strategies,
    and evaluates the error for all these
    four possibilities, in this
    order.

    **Achtung!** In this example the static strategy is
    not implemented as a `Tensor` of controls
    for each individual measurement,
    like in the other examples. On the contrary it
    is implemented as a neural network that
    takes in input only the value of the consumed
    resources up to that point.

    The measurement cycle is represented in the
    picture below.

    .. image:: ../docs/_static/nv_dec_center_execute.png
        :width: 700
        :alt: nv_dec_center_execute 

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
    learning_rate: float = 1e-3
        Initial learning rate for the neural
        networks, for both the adaptive and
        static strategies. The learning rate
        decays with
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
    loss_normalization: bool = False
        Parameter `loss_normalization` passed
        to the constructor of the
        :obj:`~.NVCenterDecoherence` class.
    beta_nuisance: bool = False
        If this flag is `True`, the loss is
        computed only from the error on the
        inverse decay time :math:`T^{-1}`.
    fixed_beta: bool = False
        If this flag is `True` the
        decay exponent is set
        to :math:`\beta=0.1`.
    """
    input_size = 10
    control_size = 1

    if fixed_beta:
        beta_bounds = (0.1, 0.1+1e-6)
    else:
        beta_bounds = (0.075, 0.2)

    if beta_nuisance or fixed_beta:
        cov_weight_matrix = [[1, 0], [0, 0]]
    else:
        cov_weight_matrix = [[1, 0], [0, 1/2]]

    name = "nv_center_decoherence_" + res
    name += f"_lr_{learning_rate}"

    if beta_nuisance:
        name += "_G"
    if fixed_beta:
        name += "_fixbeta"

    # NN simulation
    # --------------

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

    nv_center = NVCenterDecoherence(
        batchsize=batchsize,
        params=[Parameter(bounds=(0.01, 0.1), name="T"),
                Parameter(bounds=beta_bounds, name="beta")],
        prec=args.prec,
        res=res,
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

    sim_nn = DecoherenceSimulation(
        particle_filter=pf,
        simpars=simpars,
        phys_model=nv_center,
        control_strategy=lambda input_tensor: \
            100*abs(network(input_tensor))+1.0,
        cov_weight_matrix=cov_weight_matrix,
        loss_normalization=loss_normalization,
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
    #     sim_nn,
    #     Adam(learning_rate=decaying_learning_rate),
    #     network, xla_compile=True,
    # )

    print(sim_nn)
  
    # train(
    #     sim_nn,
    #     Adam(learning_rate=decaying_learning_rate),
    #     args.iterations, args.scratch_dir,
    #     network=network,
    #     xla_compile=True,
    #     gradient_accumulation=gradient_accumulation,
    # )

    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)

    # network.save(
    #     join(args.trained_models_dir, str(sim_nn)),
    #     )
    # network=load_model(
    #     join(args.trained_models_dir, str(sim_nn)),
    #     )

    delta_resources = 1.0 if res=="meas" else 50.0

    sim_nn.loss_normalization = False

    # performance_evaluation(
    #     sim_nn, min(4096, args.iterations),
    #     args.data_dir,
    #     xla_compile=True,
    #     delta_resources=delta_resources,
    #     y_label='MSE',
    # )

    # store_input_control(
    #     sim_nn, args.data_dir, 5,
    #     xla_compile=True,
    # )

    # Static simulation
    # -----------------

    simpars_static = SimulationParameters(
        sim_name=name+"_static",
        num_steps=max_res,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    network_static = standard_model(
        input_size=1,
        controls_size=control_size,
        neurons_per_layer=args.n,
        prec=args.prec,
        )
    
    # Preconditioning of the network
    input_tensor = 2*uniform((16384, 1),
                             dtype=args.prec)-1
    output_tensor = (input_tensor[:, -1:]+1)/2
    network_static.compile(loss='mean_squared_error',
                           optimizer='adam')
    network_static.fit(
        input_tensor, output_tensor,
        epochs=12, batch_size=1024, verbose=0,
       )

    sim_static = DecoherenceSimulation(
        particle_filter=pf,
        simpars=simpars_static,
        phys_model=nv_center,
        control_strategy=lambda input_tensor: \
            100*abs(network_static(input_tensor[:, -1:]))+1.0,
        cov_weight_matrix=cov_weight_matrix,
        loss_normalization=loss_normalization,
    )

    decaying_learning_rate = InverseSqrtDecay(
        learning_rate, args.prec,
    )

    # train(
    #     sim_static,
    #     Adam(learning_rate=decaying_learning_rate),
    #     args.iterations, args.scratch_dir,
    #     network=network_static,
    #     xla_compile=True,
    #     gradient_accumulation=gradient_accumulation,
    # )
    
    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)

    # network_static.save(
    #     join(args.trained_models_dir, str(sim_static)),
    # )
    # network_static=load_model(
    #     join(args.trained_models_dir, str(sim_static)),
    #     )

    sim_static.loss_normalization = False
    
    # performance_evaluation(
    #     sim_static, min(4096, args.iterations),
    #     args.data_dir,
    #     xla_compile=True,
    #     delta_resources=delta_resources,
    #     y_label='MSE',
    # )

    # store_input_control(
    #     sim_static, args.data_dir, 5,
    #     xla_compile=True,
    # )

    # Random strategy
    # ----------------
    
    simpars_random = SimulationParameters(
        sim_name=name+"_random",
        num_steps=max_res,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )

    sim_random = DecoherenceSimulation(
        particle_filter=pf,
        simpars=simpars_random,
        phys_model=nv_center,
        control_strategy=lambda input_tensor: \
            input_tensor[:, -1:],
        random=True,
        cov_weight_matrix=cov_weight_matrix,
    )

    # performance_evaluation(
    #     sim_random, min(4096, args.iterations),
    #     args.data_dir,
    #     xla_compile=True,
    #     delta_resources=delta_resources,
    #     y_label='MSE',
    # )

    # store_input_control(
    #     sim_random, args.data_dir, 5,
    #     xla_compile=True,
    # )

    # Inverse T strategy
    # ----------------
    
    simpars_inverse = SimulationParameters(
        sim_name=name+"_inverse",
        num_steps=max_res,
        max_resources=max_res,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
        log_loss=log_loss,
    )
    
    strat_const = 0.22713902 if (res=="meas" or beta_nuisance is True) \
        else 0.82757039
    sim_inverse = DecoherenceSimulation(
            particle_filter=pf,
            simpars=simpars_inverse,
            phys_model=nv_center,
            control_strategy=lambda input_tensor: \
                exp(-strat_const/(20*denormalize(
                    input_tensor[:, 1:2], [0.075, 0.2])))/\
                    denormalize(input_tensor[:, 0:1],
                                (0.01, 0.1)),
            cov_weight_matrix=cov_weight_matrix,
        )

    performance_evaluation(
        sim_inverse, min(4096, args.iterations),
        args.data_dir,
        xla_compile=True,
        delta_resources=delta_resources,
        y_label='MSE',
    )

    store_input_control(
        sim_inverse, args.data_dir, 5,
        xla_compile=True,
    )

def main():
    r"""In this example we characterize
    the dephasing process of an NV center.
    We study three
    cases. In the first one the decaying exponent
    :math:`\beta` is unknown and it is treated as
    a nuisance parameter. Therefore, only the
    precision on the inverse decay time appears
    in the loss (the MSE). In the second case
    :math:`\beta` is known and fixed 
    (:math:`20 \beta = 2`), and only :math:`T^{-1}`
    is estimated. In the third case
    both  :math:`\beta` and :math:`T^{-1}`
    are unknown and are parameters of interest,
    but their MSE are not evenly weighted:
    the error :math:`\Delta^2 \hat{\beta}` weights
    half of :math:`\Delta^2 \hat{T_2}^{-1}`. This
    is done t equilibrate the different priors on
    the parameters and consider them on an equal
    footage.
    
    The prior on :math:`T^{-1}` is uniform
    in `(0.01, 0.1)`, and that of :math:`\beta`
    is uniform in `(0.075, 0.2)` (when it is not
    fixed), so that the interval
    for the actual exponent, which is :math:`20 \beta`
    (see :py:meth:`~.NVCenterDecoherence.model`)
    is `(1.5, 4)` [5]_.

    In the following we report the estimator error
    (MSE) for a bounded 
    number of measurement (on the left),
    and for a bounded total evolution time
    (on the right).
    These simulations are done by calling the
    function
    :py:func:`~.decoherence_estimation`.

    The adaptive and static strategies are compared with
    two simple choices for the controls. The first is
    a randomize strategy, according to which the inverse of the
    evolution time is randomly selected uniformly in 
    (`0.01`, `0.1`), while the second is a
    :math:`\widehat{T^{-1}}` strategy, according to which the
    inverse of the evolution time is chosen to be the current
    estimator for the inverse of the coherence time.
 
    .. list-table::

        * - .. figure:: ../examples/nv_center_decoherence/images/
                          nv_center_decoherence_meas_lr_0.002_G_batchsize_
                          512_num_steps_128_max_resources_128.00_
                          ll_False_cl_True/plot_MeasStep_MSE.png

                Meas=128, beta nuisance

          - .. figure:: ../examples/nv_center_decoherence/images/
                          nv_center_decoherence_time_lr_0.001_G_batchsize_
                          32_num_steps_2048_max_resources_2048.00_
                          ll_False_cl_True/plot_Time_MSE.png

                Time=2048, beta nuisance

        * - .. figure:: ../examples/nv_center_decoherence/images/
                          nv_center_decoherence_meas_lr_0.001_fixbeta_
                          batchsize_
                          512_num_steps_128_max_resources_
                          128.00_ll_False_cl_True/plot_MeasStep_MSE.png

                Meas=128, fixed beta

          - .. figure:: ../examples/nv_center_decoherence/images/
                          nv_center_decoherence_time_lr_0.001_fixbeta_
                          batchsize_
                          32_num_steps_2048_max_resources_2048.00_ll_
                          False_cl_True/plot_Time_MSE.png

                Time=2048, fixed beta

        * - .. figure:: ../examples/nv_center_decoherence/images/
                          nv_center_decoherence_meas_lr_0.001_batchsize_
                          512_num_steps_128_max_resources_
                          128.00_ll_False_cl_True/plot_MeasStep_MSE.png

                Meas=128, both parameters

          - .. figure:: ../examples/nv_center_decoherence/images/
                          nv_center_decoherence_time_lr_0.001_batchsize_
                          32_num_steps_2048_max_resources_2048.00_ll_
                          False_cl_True/plot_Time_MSE.png

                Time=2048, both parameters

    The shaded grey areas in the above plot indicate
    the Bayesian Cramér-Rao bound, which is the
    the ultimate precision bound computed from
    the Fisher information.
    
    There is no advantage in using a NN instead of
    the strategies that optimize the Fisher information.

    Notes
    -----
    Some application of the estimation
    of the decoherence time involve
    the measure of the radical concentration
    in a biological sample and the measurement
    of the local conductivity through the
    Johnson noise.

    All the training of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.

    .. [5] https://arxiv.org/pdf/2210.06103.pdf
    """
    args = parse_args()
    
    decoherence_estimation(
        args, 512, 128, res='meas',
        beta_nuisance=True,
        )

    decoherence_estimation(
        args, 512, 128, res='meas',
        fixed_beta=True,
        )
    
    decoherence_estimation(
        args, 512, 128, res='meas',
        )
    
    decoherence_estimation(
        args, 256, 256, res='meas',
        )
    
    decoherence_estimation(
        args, 32, 2048, res='time',
        gradient_accumulation=4,
        beta_nuisance=True,
        loss_normalization=False,
        )
    
    decoherence_estimation(
        args, 32, 2048, res='time',
        gradient_accumulation=4,
        fixed_beta=True,
        loss_normalization=True,
        )
    
    decoherence_estimation(
        args, 32, 2048, res='time',
        gradient_accumulation=4,
        loss_normalization=True,
       )

    decoherence_estimation(
        args, 16, 4096, res='time',
        gradient_accumulation=4,
        loss_normalization=True,
       )
    
if __name__ == "__main__":
    main()
