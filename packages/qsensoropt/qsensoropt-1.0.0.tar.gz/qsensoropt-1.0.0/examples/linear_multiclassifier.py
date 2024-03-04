#!/usr/bin/env python3
from typing import Callable, List, Tuple

from tensorflow import cast, ones, \
    gather, concat, expand_dims, \
    where, constant, broadcast_to, \
    zeros, gather_nd, print, \
    reshape, Variable, Tensor
from tensorflow.math import exp, equal, argmax, \
    floormod, round
from tensorflow.linalg import expm, matvec
from tensorflow.random import Generator
from tensorflow.keras.optimizers import Adam
from tensorflow.config.experimental import get_memory_info
from numpy.random import rand as nprand
from numpy import sqrt as npsqrt
from numpy import real as npreal
from numpy import imag as npimag
from numpy import savetxt
from argparse import ArgumentParser
from math import pi
from os.path import join

from qsensoropt import InverseSqrtDecay, \
    ParticleFilter, Parameter, Control, \
        SimulationParameters, StatelessPhysicalModel, \
            StatelessSimulation
from qsensoropt.utils import train, \
    performance_evaluation, store_input_control

from photonic_circuit import PhotonicCircuit

from cmath import exp as cmexp
from cmath import pi as cmpi

def roots_of_unity(n: int):
    """Returns the the n-th roots of the unit.

    Parameters
    ----------
    n: int
        Index of the root.
    
    Returns
    -------
    roots: Tuple
        Tuple of shape (`n`, ) containing
        the unit roots.
    """
    roots = tuple(
        cmexp(2j*k*cmpi/n) for k in range(n)
        )
    return roots


class LinearMulticlassifier(
    StatelessPhysicalModel, PhotonicCircuit,
    ):
    r"""Model for a network of beam splitters (BS) and phase
    shifts that receives as input the signal
    :math:`|\alpha_s\rangle` to be classified, with
    :math:`s \in \lbrace 0, 1, \dots, m-1 \rbrace`
    being the classes. The number :math:`m` is the attribute
    `num_hypothesis` and the length
    of the tuple `list_alphas` passed to the
    constructor.

    .. image:: ../docs/_static/network_beam_splitter.png
        :width: 700
        :alt: network_beam_splitter

    The other inputs of the network are
    in order :math:`|\alpha_0\rangle`,
    :math:`|\alpha_1\rangle`, :math:`|\alpha_2\rangle`,
    ..., :math:`|\alpha_{m-1}\rangle`, that is,
    the reference states corresponding to the
    possible hypothesis (classes), which,
    at difference with the example of the
    :py:mod:`dolinar_three` are fixed for each
    execution of the task. It follows that the
    network has :math:`m+1` wires. The output of
    the network is measured with
    individual photon counters on each wire.

    The signal :math:`|\alpha_s\rangle` will
    be classified according to the photon counters
    outcomes. If more than one signal state
    is available multiple BS networks can be stacked
    on one another and the classification will be based
    on the measurements on all the layers.
    Each layer can have a different network
    BS0, BS1, ...

    Attributes
    ----------
    bs: int
        Batchsize of the simulation.
    list_alphas: Tuple[complex]
        List of reference states. It is a parameter
        passed to the class constructor.
    num_hypothesis: int
        Number of classes or hypothesis. It is the
        length of the tuple `list_alphas`. It is
        also indicated with the symbol :math:`m`.
    num_wires: int
        Number of wires in the network.
        It is `num_hypothesis+1`, i.e. :math:`m+1`.
    controls: List[:py:obj:`~.physical_model.Control`]
        Real parameters identifying the BS network.
    params: List[:py:obj:`~.Parameter`]
        Contains the description of the unknown
        to be estimated,
        i.e. the discrete parameter `Signal` that
        takes values in the set
        :math:`\lbrace 0, 1, \cdots, m-1 \rbrace`.
        The initial value randomization must be
        disabled in this application,
        i.e. the flag `randomize` of the
        :py:obj:`~.Parameter` constructor must be
        set to `False`. In this way initializing
        :math:`m` particle in the :py:obj:`~.ParticleFilter`
        will produce particles with values
        :math:`0, 1, \cdots, m-1` in this order and
        without repetitions.
    controls_size: int
        Number of real parameters of the BS network,
        i.e. :math:`2 (m+1)^2`.
    d: int = 1
        Number of unknown parameters to estimate,
        i.e. one, the signals class.
    outcomes_size: int
        Number of scalar outcomes for each
        layer of networks, i.e. the number of
        wires :math:`m+1`.
    prec: str
        Floating point precision of the controls,
        outcomes, and parameters.
    """
    def __init__(
            self, batchsize: int,
            list_alphas: Tuple[complex],
            prec: str = "float64",
            ):
        r"""Constructor of the
        :py:obj:`~.LinearMulticlassifier` class.

        Parameters
        ----------
        batchsize: int
            Number of simultaneous estimations.
        list_alphas: Tuple[complex]
            Tuple of complex numbers
            :math:`(\alpha_0, \alpha_1, \dots, \alpha_{m-1})`
            that represent the reference states.
        prec: = {"float64", "float32"}
            Floating point precision of the controls,
            outcomes, and parameters.
        """
        self.list_alphas = list_alphas
        self.num_hypothesis = len(self.list_alphas)

        PhotonicCircuit.__init__(
                self, batchsize=batchsize,
                num_wires=self.num_hypothesis+1,
                prec=prec,
            )  
        
        # Real components of the reference states
        self.alpha_real = constant(
            [npreal(alpha) for alpha in self.list_alphas],
            dtype=prec,
            )
        # Imaginary components of the reference states
        self.alpha_imag = constant(
            [npimag(alpha) for alpha in self.list_alphas],
            dtype=prec,
            )
        # Controls of the BS network
        controls = []
        for i in range(self.num_wires):
            for j in range(self.num_wires):
                controls.append(
                    Control(name=f"a{i}{j}")
                )
        for i in range(self.num_wires):
            for j in range(self.num_wires):
                controls.append(
                    Control(name=f"b{i}{j}")
                )
        # Parameter to estimate
        params = [
            Parameter(
            values=tuple(range(self.num_hypothesis)),
            randomize=False, name="Signal", ),
        ]  

        StatelessPhysicalModel.__init__(
            self, batchsize, controls, params,
            outcomes_size=self.num_wires, prec=prec,
            )
        
    def _circuit(
            self, controls: Tensor, parameters: Tensor,
            num_systems: int = 1,
    ) -> Tensor:
        """Applies the BS network."""
        # Build the matrices A and B from controls
        # which has shape (batchsize, 2*num_wires^2)
        parameters = cast(parameters, dtype="int32")
        A = reshape(
            controls[:, :, 0:self.num_wires**2],
            (self.bs, num_systems, \
             self.num_wires, self.num_wires)
        )
        B = reshape(
            controls[:, :, self.num_wires**2:(2*self.num_wires**2)],
            (self.bs, num_systems, \
             self.num_wires, self.num_wires)
        )
        real_disp_signal = expand_dims(gather_nd(
            self.alpha_real, parameters, batch_dims=0,
        ), axis=2)
        real_disp = concat([real_disp_signal, broadcast_to(
            reshape(self.alpha_real, (1, 1, self.num_hypothesis)),
            (self.bs, num_systems, self.num_hypothesis),
            )], 2)
        imag_disp_signal = expand_dims(gather_nd(
            self.alpha_imag, parameters, batch_dims=0,
        ), 2)
        imag_disp = concat([imag_disp_signal, broadcast_to(
            reshape(self.alpha_imag, (1, 1, self.num_hypothesis)),
            (self.bs, num_systems, self.num_hypothesis),
            )], 2)
        disp = concat([real_disp, imag_disp], 2)
        return self.apply_bs_network(
            A, B, disp, self.num_wires,
        )

    def perform_measurement(
            self, controls: Tensor, parameters: Tensor,
            meas_step: Tensor, rangen: Generator,
            ) -> Tuple[Tensor, Tensor]:
        r"""Application of the BS network to the
        input state
        :math:`|\alpha_s\rangle \otimes |\alpha_0\rangle
        \otimes |\alpha_1\rangle \otimes \cdots \otimes
        |\alpha_{m-1}\rangle` and subsequent photon counting
        measurements on all the wires.
        
        Parameters
        ----------
        controls: Tensor
            `Tensor` of shape (`bs`, 1, `2 num_wires^2`)
            and type `prec` that parametrizes
            the BS network.
        parameters: Tensor
            `Tensor` of shape (`bs`, 1, 1) and type
            `prec` that contains the class `s` of the signal
            :math:`|\alpha_s\rangle` for each element of
            the batch.
        meas_step: Tensor
            `Tensor` of shape (`bs`, 1, 1) and type `int32`
            that contains the index of the current
            BS layer. It starts from zero.
        rangen: Generator
            Random number generator from the module
            :py:mod:`tensorflow.random`.

        Returns
        -------
        outcomes: Tensor
            `Tensor` of shape (`bs`, 1, `num_wires`)
            and type `prec` containing the number of
            photons measured on each wire of the system
            after the application of the BS network.
        log_prob: Tensor
            `Tensor` of shape (`bs`, 1) and type
            `prec` containing the logarithm
            of the probability of getting the observed
            number of photons (the likelihood). 
        """
        state = self._circuit(
            controls, parameters,
            )
        # Photon counting measurements
        return self.photon_counting_all(state, rangen)
    
    def model(
            self, outcomes: Tensor, controls: Tensor,
            parameters: Tensor, meas_step: Tensor,
            num_systems: int = 1,
            ) -> Tensor:
        r"""Returns the probability of getting
        a certain number of photons after the
        application of the BS network to the
        input state
        :math:`|\alpha_s\rangle \otimes |\alpha_0\rangle, 
        \otimes |\alpha_1\rangle \otimes \cdots \otimes
        |\alpha_{m-1}\rangle`.

        Parameters
        ----------
        outcomes: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, `num_wires`)
            and type `prec` containing the number of
            photons measured on each wire
            of the system after the application of
            the network.
        controls: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, `2 num_wires^2`)
            and type `prec` that parametrizes
            the BS network.
        parameters: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 1) and type
            `prec` that contains the class `s` of the signal
            :math:`|\alpha_s\rangle` for each particle in
            the particle filter ensemble.
        meas_step: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 1) and type `int32`
            that contains the index of the current
            BS layer. It starts from zero.
        num_systems: int = 1
            Number of BS networks processed per
            batch.

        Returns
        -------
        prob: Tensor
            `Tensor` of shape (`bs`, `num_systems`)
            of type `prec` containing the probabilities
            of getting the number of
            photons `outcomes` after the BS
            network defined by `controls` has been
            applied on the signal defined by
            `parameters`.
        """
        state = self._circuit(
            controls, parameters, num_systems=num_systems,
            )
        return exp(
            self.postselect_photon_counting_all(
                state, outcomes, num_systems,
            ),
        )
        
    def count_resources(
            self, resources: Tensor, controls: Tensor,
            true_values: Tensor, meas_step: Tensor,
            ) -> Tensor:
        """The execution of each BS layer
        is counted as a consumed resource.
        """
        return resources+1.0
    
class ClassifierSimulation(StatelessSimulation):
    """Simulation class associated to the
    :py:obj:`~.LinearMulticlassifier`
    physical model.

    Attributes
    ----------
    bs: int
        Batchsize of the simulation.
    phys_model: :py:obj:`~.LinearMulticlassifier`
        Parameter `phys_model` passed to the
        class constructor.
    control_strategy: Callable
        Parameter `control_strategy` passed to the
        class constructor.
    pf: :py:obj:`~.ParticleFilter`
        Parameter `particle_filter` passed to the
        class constructor.
    input_size: int
        This attribute depends on the flag `random`.
        If `random=False` then `input_size=1` while
        if `random=True` then
        `input_size=2 phys_model.num_wires^2`.
    input_name: List[str]
        If `random=False` then this list contains
        only the string "MeasStepOverMaxStep", while
        if `random=True` then it contains the
        name of all the BS network parameters, i.e.
        :math:`a_{ij}` and :math:`b_{ij}` for
        :math:`i=0, 1, \cdots, m` and 
        :math:`j=0, 1, \cdots, m`
    simpars: :py:obj:`~.SimulationParameters`
        Parameter `simpars` passed to the
        class constructor.
    num_layers: int
        Number of BS layers in the signal estimation.
        It is the :py:attr:`~.SimulationParameters.num_steps`
        attribute of `simpars`. It is indicated
        also with :math:`N` in the formulas.
    random: bool = False
        Flag `random` passed to the class constructor.
    """
    def __init__(
            self, particle_filter: ParticleFilter, 
            phys_model: LinearMulticlassifier,
            control_strategy: Callable,
            simpars: SimulationParameters,
            random: bool = False,
            ):
        """Constructor of the
        :py:obj:`~ClassifierSimulation` class.

        Parameters
        ----------
        particle_filter: :py:obj:`~.ParticleFilter`
            Particle filter responsible for the update
            of the Bayesian posterior on the hypothesis.
        phys_model: :py:obj:`~.LinearMulticlassifier`
            Abstract description of the
            linear multiclassifier.
        control_strategy: Callable
            Callable object (normally a
            function or a lambda function) that
            computes the values of the controls
            for the next measurement from
            the `Tensor` `input_strategy`.
            If `random=False` then `input_strategy`
            contains only the (renormalized)
            index of the current layer
            and the `control_strategy` should return
            the corresponding BS parameters to be
            optimized. If on the other hand `random=True`
            `input_strategy` contains a randomly extracted
            parametrization of a BS network, that
            `control_strategy` can immediately return.
        simpars: :py:obj:`~.SimulationParameters`
            Contains the flags and parameters
            that regulate the stopping
            condition of the measurement loop
            and modify the loss function used in the
            training.
        random: bool = False
            If this flag is `True` the `2 phys_model.num_wires^2`
            randomized controls for the BS network are
            added to the output of the
            :py:meth:`~.generate_input` method.
        """
        self.nw = phys_model.num_wires
        self.ns = simpars.num_steps
        self.random = random
        # Random controls
        if random:
            input_size = 2*self.nw**2
            input_name = []
            for i in range(self.nw):
                for j in range(self.nw):
                    input_name.append(f"a{i}{j}")
            for i in range(self.nw):
                for j in range(self.nw):
                    input_name.append(f"b{i}{j}")
        # Optimized controls
        else:
            input_size = 1
            input_name = ["MeasStepOverMaxStep", ]

        super().__init__(
            particle_filter, phys_model,
            control_strategy,
            input_size, input_name, simpars
            )
        
    def generate_input(
            self, weights: Tensor, particles: Tensor,
            meas_step: Tensor, used_resources: Tensor,
            rangen) -> Tensor:
        """Builds the `input_strategy` tensor.
        
        * If `random=False` this method
          returns :math:`n/N`, where :math:`n`
          is `meas_step`, i.e. the index of the current layer
          and :math:`N` is the total number of layers, i.e.
          the attribute `num_layers`.
          This is a `Tensor` of shape (`bs`, 1) and type `prec`
        * If, on the other hand, `random=True` this method
          returns :math:`2 (m+1)^2` randomly extracted angles
          in :math:`(0, 2 \pi)`, which identify a BS network.
          This is a `Tensor` of shape
          (`bs`, `2 phys_model.num_wires^2`)
          and type `prec`.
        """
        pars = self.simpars
        if self.random:
            return constant(
                2*pi*nprand(self.bs, 2*self.nw**2),
                dtype=pars.prec,
            )
        else:
            return cast(meas_step, dtype=pars.prec)/self.ns
    
    def loss_function(
            self, weights: Tensor, particles: Tensor,
            true_values: Tensor, used_resources: Tensor,
            meas_step: Tensor,
            ) -> Tensor:
        r"""After all the measurements have been performed
        the particle filter contains a discrete
        distribution of posterior probabilities for the
        signal classes, i.e.
        :math:`\mathfrak{p} = \lbrace \hat{p}_i \rbrace_{i=1}^{m-1}`.
        The guess for the signal class is defined by the
        function

        .. math::
            G(\mathfrak{p}) = \text{argmax} (\hat{p}_0, 
            \hat{p}_1, \cdots, \hat{p}_{m-1}) \; ,

        and the loss is

        .. math::
            \ell (\mathfrak{p}, s) = 1 - 
            \delta (G(\mathfrak{p}), s) \; ,

        with

        .. math::
            \delta (x, y) = \begin{cases}
                1 \quad \text{if} \quad x=y \; , \\
                0 \quad \text{if} \quad x \neq y \; ,
            \end{cases}

        Averaged on many batch :math:`\ell (\mathfrak{p}, s)`
        approximates the error probability.
        """
        pars = self.simpars
        zeros_tensor = zeros(
            (self.bs, 1), dtype=pars.prec,)
        ones_tensor = ones(
            (self.bs, 1), dtype=pars.prec,
            )
        choice = expand_dims(
            argmax(weights, axis=1, output_type="int32"),
            axis=1,
            )
        loss_values = where(
            equal(
                choice,
                cast(true_values[:, :, 0],
                     dtype="int32")
            ), zeros_tensor, ones_tensor,
        )
        return loss_values

def parse_args():
    r"""Arguments
    ---------
    scratch_dir: str
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./linear_multiclassifier/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./linear_multiclassifier/data"
        Directory containing the csv files
        produced by the :py:func:`~.utils.performance_evaluation`
        and the :py:func:`~.utils.store_input_control` functions.
    prec: str = "float64"
        Floating point precision of the
        whole simulation.
    batchsize: int = 8192
        Batchsize of the simulation.
    num_layers: int = 12
        Maximum number of layers of BS network.
    iterations: int = 4096
        Number of training steps.
    """
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir", type=str,
                        default="./linear_multiclassifier/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./linear_multiclassifier/data")
    parser.add_argument('--prec', type=str, default="float64")
    parser.add_argument("--batchsize", type=int, default=8192)
    parser.add_argument("--num-layers", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=4096)

    return parser.parse_args()

def bs_network_classify(
    args, batchsize: int,
    list_alphas: Tuple[complex],
    learning_rate: float = 1e-1,
    ):
    r"""Runs the training of the linear multiclassifier
    for the list of reference states `list_alphas`.
    Compares the performances of the trained BS networks
    with that of randomly extracted networks.

    Parameters
    ----------
    args:
        Arguments passed to the Python script.
    batchsize: int
        Number of simultaneous classifications.
    list_alphas: Tuple[complex]
        Tuple of complex numbers
        :math:`(\alpha_0, \alpha_1, \dots, \alpha_{m-1})`
        that represent the reference states.
    learning_rate: float = 1e-1
        Initial learning rate for the training
        of the BS network. The learning rate is reduced
        during the training according
        to :py:obj:`~.InverseSqrtDecay`.

    Notes
    -----

    **Known bugs**: the training on the GPU freezes
    if the number of photons
    in the apparatus is too large.
    This is probably due to a bug
    in the implementation of the function
    `random.poisson`. A preliminary work-around
    has shown that reimplementing the extraction
    from a Poissonian distribution with
    `random.categorical` would solve the problem.

    At difference with other examples
    we haven't used a neural network here, 
    and therefore we don't have adaptivity.

    All the training of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.
    """
    num_hyp = len(list_alphas)
    num_wires = num_hyp+1

    classifier = LinearMulticlassifier(
        batchsize=batchsize,
        list_alphas=list_alphas,
        prec=args.prec,
    )

    particle_filter = ParticleFilter(
        num_particles=num_hyp,
        phys_model=classifier,
        resampling_allowed=False,
        prec=args.prec,
    )

    #-------------------
    # Static strategy
    #-------------------

    #Initial value of the controls
    # in the static optimization
    initial_state = 2*pi*nprand(
        args.num_layers, 2*num_wires**2,
        )
    static_variables = Variable(
        initial_state, dtype=args.prec,
        )
    
    simpars = SimulationParameters(
        sim_name=f"multiclassifier_{num_hyp}",
        num_steps=args.num_layers,
        max_resources=args.num_layers,
        cumulative_loss=True,
        prec=args.prec,
    )

    def static_control(input_tensor):
        static_control = gather(
            params=static_variables,
            indices=cast(
                round(args.num_layers*\
                      input_tensor[:, 0]), dtype="int32",
            ),
        )
        return floormod(static_control, 2*pi)

    sim = ClassifierSimulation(
        particle_filter=particle_filter,
        phys_model=classifier,
        control_strategy=static_control,
        simpars=simpars,
    )

    decaying_learning_rate = InverseSqrtDecay(
        learning_rate, args.prec,
    )

    train(
        sim, Adam(
            learning_rate=decaying_learning_rate,
            ),
        args.iterations, args.scratch_dir,
        custom_controls=static_variables,
        xla_compile=False,
    )

    savetxt(join(args.trained_models_dir, str(sim)),
        static_variables.numpy(),
        )
    
    performance_evaluation(
       sim, args.iterations,
       args.data_dir,
       xla_compile=False,
       delta_resources=1.0,
       y_label='ProbError',
    )

    store_input_control(
       sim, args.data_dir, 5,
       xla_compile=False,
    )

    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)

    #-------------------
    # Random strategy
    #-------------------
    
    simpars = SimulationParameters(
        sim_name=f"multiclassifier_{num_hyp}_random",
        num_steps=args.num_layers,
        max_resources=args.num_layers,
        cumulative_loss=True,
        prec=args.prec,
    )

    sim_rnd = ClassifierSimulation(
        particle_filter=particle_filter,
        phys_model=classifier,
        control_strategy=lambda x: x,
        simpars=simpars,
        random=True,
    )

    performance_evaluation(
       sim_rnd, args.iterations,
       args.data_dir,
       xla_compile=False,
       delta_resources=1.0,
       y_label='ProbError',
    )

    store_input_control(
       sim_rnd, args.data_dir, 5,
       xla_compile=False,
    )

    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)

   
def main():
    r"""The linear multiclassifier has been trained
    and tested for some symmetric configurations
    of the :math:`\alpha_i`. In particular the roots
    of the unit for :math:`m=3, 5, 7, 9` have
    been chosen. For a symmetric configuration of
    states the pretty good measurement (PGM) is optimal,
    but it can't be achieved with linear optics.
    The optimality of the PGM means that a single layer
    BS network can't achieve the performances of the
    PGM, however this raises the interesting question
    of how many layers
    (and copies of the signal :math:`|\alpha_s\rangle`)
    are necessary to match or surpass the
    error probability of the PGM.
    Beside that, the performances of the trained BS
    networks are also compared to that of randomly
    extracted networks.

    The following plots represent the error
    probability in the classification of the
    signal versus the number of layers of the
    linear multiclassifier (a single "resources"
    is the execution of a layer).

    .. list-table::

        * - .. figure:: ../examples/linear_multiclassifier/images/
                        multiclassifier_3_batchsize_8192_num_steps_
                        12_max_resources_12.00_ll_False_cl_True
                        /plot_NumLayers_ProbError.png
                :width: 600

                m=3

          - .. figure:: ../examples/linear_multiclassifier/images/
                        multiclassifier_5_batchsize_8192_num_steps_
                        12_max_resources_12.00_ll_False_
                        cl_True/plot_NumLayers_ProbError.png
                :width: 600

                m=5
        
        * - .. figure:: ../examples/linear_multiclassifier/images/
                        multiclassifier_7_batchsize_8192_num_steps_
                        12_max_resources_12.00_ll_False_cl_True
                        /plot_NumLayers_ProbError.png
                :width: 600

                m=7

          - .. figure:: ../examples/linear_multiclassifier/images/
                        multiclassifier_9_batchsize_2048_num_steps_
                        12_max_resources_12.00_ll_False_
                        cl_True/plot_NumLayers_ProbError.png
                :width: 600

                m=9

    The shaded grey areas in the above plot indicate
    the error probability of the PGM for many
    copies of the signal.

    Three copies of the signal are always sufficient
    in these examples to match the PGM error
    probability. An interesting observation is that
    the advantage over the random strategy that the
    trained network has, decreases as the
    number of hypothesis grows. For :math:`m \rightarrow \infty`
    we expect to have no gain. An adaptive strategy
    may be able to restore the gap with the untrained
    BS networks.
   
    This example has been suggested to us
    by L. Bagnasacco.

    Notes
    -----
    In this example we are estimating two
    quantum incompatible parameters, that are
    the `x` and `p` components of the signal state,
    whose corresponding generators
    don't commute.
    
    All the training of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.
    """
    args = parse_args()

    bs_network_classify(args, 8192, roots_of_unity(3))

    bs_network_classify(args, 8192, roots_of_unity(5))

    bs_network_classify(args, 8192, roots_of_unity(7))
    
    bs_network_classify(args, 2048, roots_of_unity(9))

if __name__ == "__main__":
    main()

