#!/usr/bin/env python3
from typing import Tuple, List
from dataclasses import dataclass

from tensorflow import cast, ones, broadcast_to, ones, \
    concat, expand_dims, eye, reshape, \
        stack, transpose, zeros, sqrt, print, \
            cast, where, gather, Tensor, Variable
from tensorflow.math import cos, sin, abs, exp, \
    multiply, greater, round
from tensorflow.random import stateless_normal, \
    Generator
from tensorflow.linalg import matvec, matmul, \
    diag, trace
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import \
    get_memory_info
from tensorflow.keras.optimizers import Adam
from argparse import ArgumentParser
from numpy.random import rand
from numpy import savetxt, loadtxt
from numpy import sqrt as npsqrt
from numpy import zeros as npzeros
from os.path import join
from math import ceil

from qsensoropt import StatefulPhysicalModel, \
    InverseSqrtDecay, Parameter, Control, \
    SimulationParameters, BoundSimulation
from qsensoropt.utils import train, \
    performance_evaluation, get_seed, \
    store_input_control, standard_model, loggauss, \
    denormalize, denormalize


@dataclass
class CavityParameters:
    """Physical parameters of the optical cavity.
    """
    delta_time: float
    """Time between two consecutive
    homodyne detections."""
    kappa: float
    """Fraction of the signal extracted at each
    homodyne measurement per second.
    """
    chi: float
    """Squeezing parameter of the
    non-linear crystal inside the cavity.
    """
    num_photons: float
    """Thermal noise in the initial state of
    the cavity, i.e. number of photons
    in the thermal state.
    """
    init_displacement: float
    """Magnitude of the initial displacement
    of the cavity state in the phase space
    along the direction (1, 1).
    """
    omega: float
    """Detuning between the cavity
    and the driving laser frequencies.
    It is the parameter to be sensed.
    """

class OpticalCavity(StatefulPhysicalModel):
    """Abstract model for
    an optical cavity with a
    single mode, that can be
    measured via homodyne detection.
    
    .. image:: ../docs/_static/cavity_x.png
        :width: 500
        :alt: cavity_x

    This model is taken from the paper
    of Fallani et al. [9]_.

    .. [9] A. Fallani, M. A. C. Rossi, D. Tamascelli, and M. G. Genoni,
       PRX Quantum 3, 020310 (2022).
    """
    def __init__(
            self, batchsize: int,
            params: List[Parameter],
            cav_parameters: CavityParameters,
            prec: str = "float64",
            ):
        """Constructor
        of the :py:obj:`~.OpticalCavity` class.

        Parameters
        ----------
        batchsize: int
            Number of simultaneous estimations
            of the detuning frequency.
        params: List[:py:obj:`~.Parameter`]
            List of unknown parameters to be
            estimated in the optical cavity experiment.
            It should contain the parameter
            `Omega`, i.e. the detuning frequency, 
            with a single possible admissible
            value, that is the point at which the sensing
            is performed.
        cav_parameters: :py:obj:`~.CavityParameters`
            Contains the values of the
            physical parameters of the cavity.
        prec: {"float64", "float32"}
            Floating point precision of the estimation.
        """
        self.cp = cav_parameters
        
        controls = [
            Control(name="Omega_f"),
        ]
        
        super().__init__(
            batchsize=batchsize,
            controls=controls,
            params=params,
            state_specifics={
                'size': 6, 'type': prec,
            },
            recompute_state=True,
            prec=prec,
            )
        
    def initialize_state(
            self, parameters: Tensor,
            num_systems: int,
            ) -> Tensor:
        r"""Initialization of the cavity state.

        The initial state of the cavity
        is Gaussian and so are all the operations
        performed on it, therefore it remains Gaussian.
        Accordingly the state can be described with
        the covariance matrix :math:`\sigma` and the
        displacement vector :math:`\vec{r}`.
        This method returns the initial state
        of the cavity described by

        .. math::
            \vec{r} = \frac{1}{\sqrt{2}}(r_0, r_0) \quad
            \text{and} \quad
            \sigma = (2 n_{th} + 1) \mathbb{I} \; ,
        
        where :math:`r_0` is
        :py:attr:`~.CavityParameters.init_displacement`
        and :math:`n_{th}` is
        :py:attr:`~.CavityParameters.num_photons`.

        Parameters
        ----------
        parameters: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 1)
            containing the values of `Omega`.
            It is not used for producing the initial
            state.
        num_systems: int
            Size of the second dimension of
            `parameters`. It is the number
            of cavity states instantiated
            for each batch element, i.e. for
            each estimation.
        
        Returns
        --------
        initial_state:
            `Tensor` of shape (`bs`, `num_systems`, 6)
            containing tha flattened and concatenated
            displacement vector :math:`\vec{r}_0` and
            covariance matrix :math:`\sigma`
            of cavity initial Gaussian state.
        """
        r_vector = self.cp.init_displacement*\
            ones((self.bs, num_systems, 2),
                 dtype=self.prec)/npsqrt(2)
        sigma_matrix = reshape((2.0*self.cp.num_photons+1)*\
            eye(2, batch_shape=[self.bs, num_systems],
                dtype=self.prec),
            (self.bs, num_systems, 4))
        return concat([r_vector, sigma_matrix], 2)
    
    def unitary_evolution(
            self, state: Tensor,
            parameters, controls,
            num_systems: int = 1,
            ) -> Tensor:
        r"""Returns the state of the cavity
        after the unitary evolution of time duration
        :py:attr:`~.CavityParameters.delta_time`,
        with external driving.

        The evolution of the Gaussian state
        of the cavity due to the detuning and
        the non-linear crystal is
        described by the following
        differential equations for
        :math:`\vec{r}(t)` and :math:`\sigma(t)`:

        .. math::
            \frac{d \vec{r}(t)}{dt} =
            A \vec{r} (t) \; ,

        .. math::    
            \frac{d \sigma(t)}{dt} =
            A \sigma(t) + \sigma(t) A^T \; ,

        with

        .. math::
            A = \begin{pmatrix} -\chi &
            \omega + \omega_f \\
            -(\omega+\omega_f) & \chi
            \end{pmatrix} \; ,

        where :math:`\chi` is
        :py:attr:`~.CavityParameters.chi`, i.e.
        the squeezing parameter, and
        :math:`\omega` is
        :py:attr:`~.CavityParameters.omega`, i.e. the detuning.
        :math:`\omega_f` is the parameter `controls`
        and is determined by the external driving.

        These differential equations can be solved exactly:

        .. math::
            \vec{r} (t+\Delta t) = e^{A \Delta t} \vec{r} (t) \; ,
        .. math::
            \sigma (t+\Delta t) = e^{A \Delta t}
            \sigma (t) e^{A^T \Delta t} \; ,
        
        where :math:`\Delta t` is
        :py:attr:`~.CavityParameters.delta_time`,
        i.e. the evolution time.   

        Parameters
        ----------
        state: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 6)
            containing the evolved state of the cavity
            before the evolution. It is the
            concatenation of the flattened versions
            of the moments :math:`\vec{r}(t)`
            and the covariance matrix 
            :math:`\sigma (t)`.
        parameters: Tensor
            `Tensor` of shape (`bs`, 1, 1) containing
            the value of the detuning frequency
            :math:`\omega`.
        num_systems: int = 1
            Number of optical cavities
            simulated per batch element, i.e.
            per estimation.

        Returns
        -------
        state: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 6)
            containing the evolved state of the cavity.
            It is the `Tensor` obtained by concatenating
            the flattened versions of
            :math:`\vec{r}(t+\Delta t)`
            and :math:`\sigma(t+\Delta t)`.

        Notes
        -----
        In order to compute the exponential of the
        traceless matrix :math:`A \Delta t` there is an handy
        formula:

        .. math::
            e^{A \Delta t} = \cos (\Delta t \sqrt{|A|})
            \mathbb{I} +
            \frac{\sin (\Delta t \sqrt{|A|})}{\sqrt{|A|}} A \; ,
        
        where :math:`|A|` is the determinant
        of :math:`A`. This formula works for both
        :math:`|A|>0` and :math:`|A|<0`.
        """
        r_vector, sigma_matrix = state[:, :, 0:2], \
            reshape(state[:, :, 2:6], \
                    (self.bs, num_systems, 2, 2))
        omega_f = controls[:, :, 0]
        omega = parameters[:, :, 0]
        one_arr = ones(
            [self.bs, num_systems], dtype=self.prec,
            )
        # Construction of the A matrix without loss
        A = transpose(stack(
            [[-self.cp.chi*one_arr, omega+omega_f],
            [-(omega+omega_f), self.cp.chi*one_arr]],
            ), [2, 3, 0, 1],
        )*self.cp.delta_time
        identity = eye(
            2, batch_shape=[self.bs, num_systems],
            dtype=self.prec,
            )
        sqrt_detA = self.cp.delta_time*sqrt(
            abs((omega+omega_f)**2-self.cp.chi**2),
            )
        coeff1 = where(
            greater((omega+omega_f)**2, self.cp.chi**2*one_arr),
            cos(sqrt_detA), (exp(sqrt_detA)+exp(-sqrt_detA))/2,
        )
        coeff2 = where(
            greater((omega+omega_f)**2, self.cp.chi**2*one_arr),
            sin(sqrt_detA)/sqrt_detA,
            (exp(sqrt_detA)-exp(-sqrt_detA))/(2*sqrt_detA),
        )
        # Exponential of the A matrix
        time_evol = broadcast_to(reshape(coeff1,
                (self.bs, num_systems, 1, 1)),
                (self.bs, num_systems, 2, 2))*identity+\
            broadcast_to(reshape(coeff2,
                                 (self.bs, num_systems, 1, 1)),
                             (self.bs, num_systems, 2, 2))*A
        evolved_r = matvec(time_evol, r_vector)
        evolved_sigma = matmul(
            matmul(time_evol, sigma_matrix),
            time_evol, transpose_b=True,
        )
        return concat(
            [evolved_r,
             reshape(evolved_sigma,
                     (self.bs, num_systems, 4))], 2,
        )

    def _beam_splitter(
            self, state: Tensor,
            num_systems: int = 1,
            ) -> Tensor:
        """Splits the state of the cavity field
        on a beam splitter, and returns
        the state of the two outputs modes."""
        # BS reflectivity
        theta = 1.0-self.cp.delta_time*self.cp.kappa
        # Covariance matrix of the ground state
        # of the oscillator (void)
        sigma_void = eye(
            2, batch_shape=[self.bs, num_systems],
            dtype=self.prec,
            )
        r_vector, sigma_matrix = state[:, :, 0:2], \
            reshape(state[:, :, 2:6],
                    (self.bs, num_systems, 2, 2))
        first_row = concat(
            [theta*sigma_matrix+(1-theta)*sigma_void,
             -npsqrt(theta*(1.0-theta))*\
                (sigma_matrix-sigma_void)], 3,
             )
        second_row = concat(
            [-npsqrt(theta*(1.0-theta))*\
             (sigma_matrix-sigma_void),
             (1.0-theta)*sigma_matrix+theta*sigma_void], 3,
             )
        cov_output_bs = concat([first_row, second_row], 2)
        r_output_bs = concat(
            [npsqrt(theta)*r_vector,
             -npsqrt(1.0-theta)*r_vector], 2)
        return r_output_bs, cov_output_bs
    
    def _apply_homodyne_backrection(
            self, r_output_bs: Tensor,
            cov_output_bs: Tensor, u: Tensor,
            axis: str = 'x', num_systems: int = 1,
            ) -> Tensor:
        """Applies the backreaction on the
        cavity state of the partial
        homodyne measurement on the
        cavity field.
        
        This method can
        be used both in the case
        we are applying a genuine
        backreaction of an extracted
        measurement outcomes, or we are
        conditioning the state
        on a postselected outcome."""
        zero_arr = zeros(
            [self.bs, num_systems, 1], dtype=self.prec,
            )
        u_vec = concat([u, zero_arr], 2) if axis=='x' \
            else concat([zero_arr, u], 2)
        a, b = r_output_bs[:, :, 0:2], \
            r_output_bs[:, :, 2:4]
        A, B, C = cov_output_bs[:, :, 0:2, 0:2], \
            cov_output_bs[:, :, 2:4, 2:4], \
                cov_output_bs[:, :, 0:2, 2:4]
        den = B[:, :, 0:1, 0] if axis=='x' \
            else B[:, :, 1:2, 1]
        # Pi matrix used for the
        # homodyne measurement along x
        Pi_x = diag(concat(
            [ones((self.bs, num_systems, 1),
                  dtype=self.prec),
            zeros((self.bs, num_systems, 1),
                  dtype=self.prec)], 2
        ))
        Pi_y = diag(concat(
            [zeros((self.bs, num_systems, 1),
                   dtype=self.prec),
            ones((self.bs, num_systems, 1),
                 dtype=self.prec)], 2
        ))
        Pi = Pi_x if axis=='x' else Pi_y
        evolved_r = a-multiply(
            (1.0/den), matvec(matmul(C, Pi), b-u_vec),
            )
        evolved_sigma = A-multiply(
            expand_dims((1.0/den), axis=3),
            matmul(C, matmul(Pi, C)),
            )
        return concat(
            [evolved_r,
             reshape(evolved_sigma,
                     (self.bs, num_systems, 4))], 2,
        )
    
    def _extract_homodyne(
            self, r_output_bs: Tensor,
            cov_output_bs: Tensor,
            rangen: Generator, axis: str = 'x',
            num_systems: int = 1,
            ) -> Tuple[Tensor, Tensor]:
        """Extract the result of the partial
        homodyne measurement on the cavity
        field on the selected axis."""
        B, b = cov_output_bs[:, :, 2:4, 2:4], \
            r_output_bs[:, :, 2:4]
        mean = b[:, :, 0] if axis=='x' else b[:, :, 1]
        stddev = sqrt(B[:, :, 0, 0] if \
                      axis=='x' else B[:, :, 1, 1])
        seed = get_seed(rangen)
        u = stddev*stateless_normal(
            [self.bs, num_systems, ], seed,
            dtype=self.prec,
            )+mean
        return expand_dims(u, axis=2), \
            loggauss(u, mean, stddev)
    
    def _postselect_homodyne(
            self, u: Tensor, r_output_bs: Tensor,
            cov_output_bs: Tensor, axis: str = 'x',
            ) -> Tensor:
        """Returns the log-likelihood of
        getting the outcome `u` by measuring
        the cavity field on the indicated axis."""
        B, b = cov_output_bs[:, :, 2:4, 2:4], \
            r_output_bs[:, :, 2:4]
        mean = b[:, :, 0] if axis=='x' else b[:, :, 1]
        stddev = sqrt(B[:, :, 0, 0] \
                      if axis=='x' else B[:, :, 1, 1])
        return loggauss(u[:, :,  0], mean, stddev)
    
    def perform_measurement(
            self, controls: Tensor, parameters: Tensor,
            true_state: Tensor, meas_step: Tensor,
            rangen: Generator,
            ) -> Tuple[Tensor, Tensor, Tensor]:
        r"""Evolves the cavity for a time
        :math:`\Delta t`, then
        performs a homodyne detection
        on the fraction of the cavity field
        that leaks out through the partially
        reflective mirror.

        For each measurement the state of the
        cavity is virtually splitted on a
        beam-splitter
        with transmission coefficient
        :math:`\kappa \Delta t`,
        where :math:`\Delta t` is
        :py:attr:`~.CavityParameters.delta_time`
        and :math:`\kappa` is
        :py:attr:`~.CavityParameters.kappa`.
        The reflected part stays in the cavity,
        while the transmitted part is measured
        through homodyne detection, which
        causes a backreaction on the light
        remaining in the cavity (because of
        the squeezing of the cavity mode).

        Parameters
        ----------
        controls: Tensor
            `Tensor` of shape (`bs`, 1, 1) and
            type `prec` containing
            the feedback frequency
            :math:`\omega_f` of the driving laser.
        parameters: Tensor
            `Tensor` of shape (`bs`, 1, 1) and
            type `prec` containing
            the detuning frequency 
            :math:`\omega` of the cavity,
            at which the point
            estimation must be performed.
        true_state: Tensor
            `Tensor` of shape (`bs`, 1, 6) 
            and type `prec` containing
            the displacement vector and the
            covariance matrix of the Gaussian
            state of the cavity at the moment of the
            call of this method.
        meas_step: Tensor
            `Tensor` of shape
            (`bs`, 1, 1) and type `prec`.
            It is the index of the current
            homodyne measurement and it starts
            from zero.
        rangen: Generator
            Random number generator from the module
            :py:mod:`tensorflow.random`.

        Returns
        -------
        u: Tensor
            `Tensor` of shape (`bs`, 1, 1) and type `prec`
            that contains the outcome of the
            homodyne detection on the
            cavity mode.
        log_prob: Tensor
            Log-likelihood of having
            observed the outcome `u`.
            It is a `Tensor` of shape
            (`bs`, 1) and type `prec`.
        true_state: Tensor
            Evolved state of the cavity after
            the application of the backreaction.
            It is a `Tensor` of shape
            (`bs`, 1, 6) and type `prec`.
        """
        true_state = self.unitary_evolution(
            true_state, parameters, controls,
            )
        # Homodyne on x
        output_bs_r, output_bs_sigma = \
            self._beam_splitter(true_state)
        u_x, log_prob_x = self._extract_homodyne(
            output_bs_r, output_bs_sigma, rangen,
            )
        true_state = self._apply_homodyne_backrection(
            output_bs_r, output_bs_sigma, u_x,
        )
        log_prob = log_prob_x
        u = u_x
        return u, log_prob, true_state
    
    def model(
            self, outcomes: Tensor, controls: Tensor,
            parameters: Tensor, state: Tensor,
            meas_step: Tensor, num_systems: int = 1,
            ) -> Tuple[Tensor, Tensor]:
        r"""Returns the probability
        for the homodyne detection 
        on the cavity field to
        give a certain outcome.

        Parameters
        ----------
        outcomes: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 1) and
            type `prec` containing the
            outcomes of the homodyne measurement
            to postselect on.
        controls: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 1) and
            type `prec` containing
            the feedback frequency :math:`\omega_f` of the
            driving laser.
        parameters: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 1) and
            type `prec` containing
            the detuning frequency 
            :math:`\omega` of the
            cavity at which the point
            estimation is performed.
        state: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 6) 
            and type `prec` containing
            the displacement vector and the
            covariance matrix of the Gaussian
            state of the cavity.
        meas_step: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 1) and type `prec`.
            It is the index of the current
            homodyne measurement and it starts
            from zero.
        num_systems: int = 1
            Number of optical cavities simulated
            per batch, i.e per estimation.

        Returns
        -------
        prob:
            Probability for the homodyne detection
            to return `outcomes` after the
            state has been evolved for a time
            :math:`\Delta t`. It is a `Tensor`
            of shape (`bs`, `num_systems`) and
            type `prec`.
        state:
            State of the cavity conditioned
            on the observation of `outcomes`.
            It is a `Tensor` of shape
            (`bs`, `num_systems`, 6) and of type
            `prec`.
        """
        state = self.unitary_evolution(
            state, parameters, controls,
            num_systems=num_systems,
            )
        # Homodyne on x
        output_bs_r, output_bs_sigma = \
            self._beam_splitter(
            state, num_systems=num_systems,
            )
        log_prob_x = self._postselect_homodyne(
            outcomes[:, :, 0:1], output_bs_r,
            output_bs_sigma,
            )
        state = self._apply_homodyne_backrection(
            output_bs_r, output_bs_sigma,
            outcomes[:, :, 0:1],
            num_systems=num_systems,
        )
        return exp(log_prob_x), state
    
    def count_resources(
            self, resources: Tensor, controls: Tensor,
            true_values: Tensor, meas_step: Tensor,
            ) -> Tensor:
        r"""The consumed resource is the total
        evolution time. We consider the
        measurements instantaneous and spaced
        of :math:`\Delta t`. Therefore
        :math:`n` measurements consume a total
        amount of time :math:`n \Delta t`."""
        return resources+self.cp.delta_time


def parse_args():
    r"""Arguments
    ---------
    scratch_dir: str
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./optical_cavity/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./optical_cavity/data"
        Directory containing the csv files
        produced by the :py:func:`~.utils.performance_evaluation`
        and the :py:func:`~.utils.store_input_control` functions.
    prec: str = "float64"
        Floating point precision of the
        whole simulation.
    n: int = 64
        Number of neurons per layer in the neural network.
    batchsize: int = 16
        Batchsize of the simulation.
    evolution_time: int = 128
        Total evolution time of the cavity.
    learning_rate: float = 1e-2
        Initial learning rate for the neural network.
    iterations: int = 1024
        Number of training steps.
    """
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir", type=str,
                        default="./optical_cavity/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./optical_cavity/data")
    parser.add_argument("--prec", type=str, default="float64")
    parser.add_argument("--n", type=int, default=64)
    parser.add_argument("--batchsize", type=int, default=16)
    parser.add_argument("--evolution-time", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=1e-2)
    parser.add_argument("--iterations", type=int, default=2048)

    return parser.parse_args()

def optimize_optical_cavity(
        args, chi: float, interval: bool = False,
        ):
    r"""Training of the optimal controls for the
    feedback frequency of the driving laser in the
    cavity in order to minimize the
    Cramér-Rao (CR) bound.
    This function evaluates the performances of
    a trained neural network, of a static (open-loop)
    strategy, and of the random controls.

    While the squeezing parameters :math:`\chi`
    is variable and passed to the call of
    the function through the
    parameter `chi`, all the other attributes
    of :py:obj:`~.CavityParameters` are fixed
    to :math:`\Delta t = 1, \,
    \kappa = 10^{-2}, \, n_{th} = 5, \,
    r_0 = 0, \, \omega = 10^{-3}`.

    With approximately 1% of the cavity field
    measured by the homodyne detection at every
    step we are in the regime of continuous
    measurements.

    Parameters
    ----------
    args:
        Arguments passed to the Python script.
    chi: float
        Squeezing parameter of the non-linear
        crystal in the cavity.
    interval: bool = False
        If this flag is `True`, the minimization
        of the CR bound is done in the range
        of detuning frequency
        :math:`(\omega, 10 \omega)`.
    """

    network = standard_model(
        input_size=10,
        controls_size=1,
        neurons_per_layer=args.n,
        prec=args.prec,
    )
    network.compile()

    cav_parameters = CavityParameters(
        delta_time=1, kappa=1e-2,
        chi=chi, num_photons=5.0,
        init_displacement=0.0,
        omega=1e-3,
        )
    
    num_steps = ceil(
        args.evolution_time/cav_parameters.delta_time,
        )

    cavity = OpticalCavity(
        batchsize=args.batchsize,
        params=[
            Parameter(bounds=(
            cav_parameters.omega, 10*cav_parameters.omega,
            ), name="Omega"),
        ] if interval else [Parameter(values=(
            cav_parameters.omega, ), name="Omega")],
        cav_parameters=cav_parameters,
        prec=args.prec,
    )

    name = "cavity"
    name += "_int" if interval else ""

    # Neural network training
    # ------------------------------

    # simpars = SimulationParameters(
    #     sim_name=f"{name}_chi_{cav_parameters.chi}",
    #     num_steps=num_steps,
    #     max_resources=args.evolution_time,
    #     prec=args.prec,
    #     loss_logl_outcomes=False,
    #     log_loss=True,
    # )

    # sim_nn = BoundSimulation(
    #     simpars=simpars,
    #     phys_model=cavity,
    #     control_strategy= lambda x: \
    #      cav_parameters.omega*(-1.0+network(x)),
    # )

    # decaying_learning_rate = InverseSqrtDecay(
    #     args.learning_rate, prec=args.prec,
    # )

    # train(
    #     sim_nn,
    #     Adam(learning_rate=decaying_learning_rate),
    #     args.iterations,
    #     args.scratch_dir, network=network,
    #     xla_compile=False,
    # )

    # network.save(
    #     join(args.trained_models_dir, str(sim_nn)),
    #     )
    # network = load_model(
    #     join(args.trained_models_dir, str(sim_nn)),
    #     )

    # performance_evaluation(
    #     sim_nn, args.iterations, args.data_dir,
    #     xla_compile=False,
    #     delta_resources=cav_parameters.delta_time,
    #     y_label='CRBound',
    # )

    # store_input_control(
    #     sim_nn, args.data_dir, 5,
    #     xla_compile=False,
    # )

    # print("Memory:")
    # print(get_memory_info('GPU:0')['peak']/1024**3)

    # Random strategy
    #-------------------------------------------

    # simpars_rnd = SimulationParameters(
    #     sim_name=f"{name}_random_chi_{cav_parameters.chi}",
    #     num_steps=num_steps,
    #     max_resources=args.evolution_time,
    #     prec=args.prec,
    #     loss_logl_outcomes=False,
    #     log_loss=True,
    # )

    # sim_rnd = BoundSimulation(
    #     simpars=simpars_rnd,
    #     phys_model=cavity,
    #     control_strategy=lambda x: \
    #         cav_parameters.omega*(-1.0+x[:, -1:]),
    #     random=True,
    # )

    # performance_evaluation(
    #     sim_rnd, args.iterations, args.data_dir,
    #     xla_compile=False,
    #     delta_resources=cav_parameters.delta_time,
    #     y_label='CRBound',
    # )

    # store_input_control(
    #     sim_rnd, args.data_dir, 5,
    #     xla_compile=False,
    # )

    # Static strategy
    # -------------------------------

    simpars_static = SimulationParameters(
        sim_name=f"{name}_static_chi_{cav_parameters.chi}",
        num_steps=num_steps,
        max_resources=args.evolution_time,
        prec=args.prec,
        loss_logl_outcomes=False,
        log_loss=True,
    )

    #Initial value of the controls
    # in the static optimization
    initial_state = npzeros((int(num_steps), 1))
    for i in range(int(num_steps)):
        initial_state[i, :] = -1.0+rand()

    static_variables = Variable(
        initial_state, dtype=args.prec,
        )
    
    sim_static = BoundSimulation(
        simpars=simpars_static,
        phys_model=cavity,
        control_strategy=lambda input_tensor:
            gather(
                params=cav_parameters.omega*static_variables,
                indices=cast(
        round(denormalize(input_tensor[:, -2],
                          (0, num_steps))),
        dtype="int32"),
            ),
    )

    decaying_learning_rate = InverseSqrtDecay(
        1e-1, prec=args.prec,
    )

    train(
        sim_static,
        Adam(learning_rate=decaying_learning_rate),
        args.iterations,
        args.scratch_dir,
        custom_controls=static_variables,
        xla_compile=False,
    )

    savetxt(
        join(args.trained_models_dir, str(sim_static)),
            static_variables.numpy(),
            )
    # static_variables = Variable(loadtxt(
    #     join(args.trained_models_dir, str(sim_static)),
    #     )[:, None], dtype=args.prec,
    # )

    performance_evaluation(
        sim_static, args.iterations,
        args.data_dir,
        xla_compile=False,
        delta_resources=cav_parameters.delta_time,
        y_label='CRBound',
    )

    store_input_control(
        sim_static, args.data_dir, 5,
        xla_compile=False,
    )

def main():
    r"""We trained both the adaptive
    and the static strategies for controlling
    the feedback frequency and we found no advantage
    in using a neural network for all the
    values of :math:`\chi` that we have explored.
    In the following we report on the left
    the Fisher information
    per unit of time, i.e.
    :math:`F_t = F/T` as a function of the
    evolution time :math:`T`
    for the optimal adaptive strategies,
    and on the right a plot
    of the squeezing parameter

    .. math::
        \xi_{dB}  = -20 \log \frac{\sigma_x}{\sigma_p} \; ,

    computed as function of time.

    .. list-table::

        * - .. figure:: ../examples/optical_cavity/images/
                          plot_EvolutionTime_F_t.png
                :width: 600

                Fisher/Time

          - .. figure:: ../examples/optical_cavity/images/
                          plot_EvolutionTime_Xi_dB.png
                
                Squeezing parameter

    The point
    of the optimal strategies is to create squeezing
    on the `x`-axis (the one measured by the
    homodyne detection) and position the state
    on the `p` axis as far as possible from
    the origin, so that the
    rotation sensitivity is maximized.

    In the following plots
    we report the mean value of the displacement
    in the phase space for the cavity state,
    always as a function of time.

    At the very beginning the states spread
    on the x-axis due to the relative high initial
    thermal noise and the homodyne measurement
    backreaction, but at the end
    the controls have managed to
    give the states a p-components and to
    reduce the displacement along the
    x-axis.

    .. list-table::
    
        * - .. figure:: ../examples/optical_cavity/images/
                        plot_EvolutionTime_|r_p|.png
                :width: 600

                Mean of :math:`|r_p|`.

          - .. figure:: ../examples/optical_cavity/images/
                          plot_EvolutionTime_|r_x|.png
                
                Mean of :math:`|r_x|`.

    Notes
    -----
    If instead of fixing :math:`\omega`
    we had a interval of possible values for the parameter,
    i.e. by setting the flag `interval` of the
    function :py:func:`~.optical_cavity.optimize_optical_cavity`,
    the neural
    network would be useful to modulate the optimal
    strategy as a function of :math:`\omega`.

    All the training of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.
    """
    args = parse_args()

    optimize_optical_cavity(args, chi=1e-3)
    optimize_optical_cavity(args, chi=2e-3)
    optimize_optical_cavity(args, chi=3e-3)
    optimize_optical_cavity(args, chi=4e-3)
    optimize_optical_cavity(args, chi=4.9e-3)
    optimize_optical_cavity(args, chi=5e-3)

if __name__ == "__main__":
    main()
