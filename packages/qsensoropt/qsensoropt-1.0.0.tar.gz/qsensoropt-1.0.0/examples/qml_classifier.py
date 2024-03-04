#!/usr/bin/env python3
from typing import Callable, List, Tuple

from tensorflow import cast, ones, \
    gather, concat, expand_dims, \
    where, constant, broadcast_to, \
    zeros, gather_nd, Variable, Tensor
from tensorflow.math import exp, log, cos, sin, \
    reciprocal_no_nan, equal, argmax, \
    reduce_sum, floormod, sqrt, greater_equal, \
        real, imag, minimum, maximum
from tensorflow.math import round as tfround
from tensorflow.math import pow as tfpow
from tensorflow.linalg import diag_part, \
    matrix_transpose, expm, matvec
from tensorflow.random import stateless_poisson, \
    stateless_categorical, Generator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from numpy import array as nparray
from numpy import concatenate as npconcat
from numpy import savetxt, loadtxt
from numpy.random import rand as nprand
from numpy import sqrt as npsqrt
from numpy import repeat as nprepeat
from numpy import concatenate as npconcat
from argparse import ArgumentParser
from math import pi
from os.path import join

from qsensoropt import PhysicalModel, \
    InverseSqrtDecay, ParticleFilter, \
        Parameter, Control, SimulationParameters, \
            StatefulPhysicalModel, StatefulSimulation

from qsensoropt.utils import train, \
    performance_evaluation, get_seed, \
        store_input_control, logpoisson, \
            normalize, standard_model

class CoherentStates:
    """This class contains the methods to
    operated on one ore more bosonic wires
    carrying coherent states. It can't deal
    with squeezing or with noise, only
    with displacements, phase shifts and
    photon counting measurements.

    Notes
    -----
    The covariance matrix of the system is always
    proportional to the identity and corresponds
    to zero temperature.
    """
    def __init__(
            self, batchsize: int,
            prec: str = "float64",
            ):
        """Constructor of the
        :py:obj:`CoherentStates` class.

        Parameters
        ----------
        batchsize: int
            Number of experiments that are
            simultaneously treated by the object.

            **Achtung!** This is not the
            number of bosonic lines that an object of
            this class can deal with. This is in fact
            not an attribute of the class, and is
            not fixed during the initialization.
        """
        self.bs = batchsize
        self.prec = prec

    def phase_shift(
            self, input_state: Tensor, phase: Tensor,
            ) -> Tensor:
        """Applies a phase shift on the coherent
        states encoded in `input_state`.

        Parameters
        ----------
        input_state: Tensor
            `Tensor` of shape (`bs`, ?, 2)
            and of type `prec` containing the
            `x` and `y` components of the coherent state
            to be rotated.
        phase: Tensor
            `Tensor` of shape (`bs`, ?) containing
            the phase for the rotation of each state
            in the batch.

        Returns
        -------
        Tensor:
            `Tensor` of shape (`bs`, ?, 2)
            and of type `prec` containing the rotated
            coherent state.
        """ 
        rot_x = expand_dims(
            cos(phase)*input_state[:, :, 0]+\
                sin(phase)*input_state[:, :, 1],
            axis=2,
        )
        rot_y = expand_dims(
            -sin(phase)*input_state[:, :, 0]+\
                cos(phase)*input_state[:, :, 1],
            axis=2,
        )
        return concat([rot_x, rot_y], 2)
        
    def beamsplitter(
            self, input1: Tensor, input2: Tensor,
            theta: Tensor, phi: Tensor,
            ) -> Tuple[Tensor, Tensor]:
        r"""Beam splitter (BS) operating on two
        bosonic modes carrying coherent states.
        It returns the two states outputted by the BS.

        Parameters
        ----------
        input1: Tensor
            `Tensor` of shape (`bs`, ?, `2`)
            and of type `prec` containing the `x` and
            `y` components of the first incident state
            on the BS.
        input2: Tensor
            `Tensor` of shape (`bs`, ?, `2`)
            and of type `prec` containing the `x` and
            `y` components of the second incident state
            on the BS.
        theta: Tensor
            `Tensor` of shape (`bs`, ?)
            and of type `prec`. It contains the
            transmission coefficient of the BS.
            It is indicated with :math:`\theta`
            in the formulas.
        phi: 
            `Tensor` of shape (`bs`, ?)
            and of type `prec`. It contains the phase
            applied by the BS. It is indicated with
            :math:`\phi` in the formulas.

        Returns
        -------
        Tensor:
            `Tensor` of shape (`bs`, ?, `2`) and type `prec`.
            Contains the first output state of the BS.
        Tensor:
            `Tensor` of shape (`bs`, ?, `2`) and type `prec`.
            Contains the second output state of the BS.
        """
         # Alpha_x - First outcome
        outcome1_x = cos(theta)*input1[:, :, 0]+\
            sin(theta)*(cos(phi)*input2[:, :, 0]+\
                        sin(phi)*input2[:, :, 1])
        # Alpha_y - First outcome
        outcome1_y = cos(theta)*input1[:, :, 1]+\
            sin(theta)*(-sin(phi)*input2[:, :, 0]+\
                        cos(phi)*input2[:, :, 1])
        # Alpha_x - Second outcome
        outcome2_x = -sin(theta)*(cos(phi)*input1[:, :, 0]-\
                                  sin(phi)*input1[:, :, 1])+\
                                    cos(theta)*input2[:, :, 0]
        # Alpha_y - Second outcome
        outcome2_y = -sin(theta)*(sin(phi)*input1[:, :, 0]+\
                                  cos(phi)*input1[:, :, 1])+\
                                    cos(theta)*input2[:, :, 1]
        outcome1_x = expand_dims(outcome1_x, axis=2)
        outcome1_y = expand_dims(outcome1_y, axis=2)
        outcome2_x = expand_dims(outcome2_x, axis=2)
        outcome2_y = expand_dims(outcome2_y, axis=2)
        return concat([outcome1_x, outcome1_y], 2), \
            concat([outcome2_x, outcome2_y], 2)
    
    def mean_phot(
        self, input_state: Tensor,
    ) -> Tensor:
        """Returns the mean photon
        number on a coherent state.

        Parameters
        ----------
        input_state: Tensor
            `Tensor` of shape (`bs`, ?, `2`)
            and of type `prec` containing the
            `x` and `y` components of the
            coherent state.

        Returns
        -------
        Tensor
            `Tensor` of shape (`bs`, ?) and
            type `prec` containing the average
            number of photons of the coherent states
            described in `input_state`.
        """
        return input_state[:, :, 0]**2+input_state[:, :, 1]**2
    
    def photon_counter(
            self, input_state: Tensor, rangen: Generator,
            num_systems: int = 1,
            ) -> Tuple[Tensor, Tensor]:
        """Photon counting measurement
        on a bosonic line carrying a coherent state.

        Parameters
        ----------
        input_state: Tensor
            `Tensor` of shape (`bs`, ?, `2`)
            and of type `prec` containing the
            `x` and `y` components of the coherent state
            on which the photon counting measurement will
            be performed.
        rangen: Generator
            Random number generator from the module
            :py:mod:`tensorflow.random`.
        num_systems: int = 1
            Number of independent coherent states
            processed per batch. It is the size
            of the second dimension of `input_state`.

        Returns
        -------
        outcomes: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 1)
            and type `prec` containing the outcomes
            of the photon counting measurement (the 
            number of photons).
        log_prob: Tensor
            `Tensor` of shape (`bs`, `num_systems`)
            and type `prec` containing the logarithm of
            the probability of the observed number
            of photons.
        """
        alpha_square = self.mean_phot(input_state)
        seed = get_seed(rangen)
        outcomes = cast(stateless_poisson(
            (self.bs, num_systems), seed, alpha_square),
            dtype=self.prec,
            )
        log_prob = logpoisson(alpha_square, outcomes)
        return expand_dims(outcomes, axis=2), log_prob
    
    def postselect_photon_counter(
            self, input_state: Tensor,
            outcomes: Tensor,
            ) -> Tensor:
        """Returns the logarithm of the probability
        of observing `outcomes` after a photon counting
        measurement on `input_state`.

        Parameters
        ----------
        input_state: Tensor
            `Tensor` of shape (`bs`, ?, `2`)
            and of type `prec` containing the
            `x` and `y` components of the coherent state
            on which the photon counting measurement
            is performed.
        outcomes: Tensor
            `Tensor` of shape (`bs`, ?, 1)
            and type `prec` containing the outcomes
            of the photon counting measurement (the 
            number of photons).

        Returns
        -------
        log_prob: Tensor
            `Tensor` of shape (`bs`, ?)
            and type `prec` containing the logarithm of
            the probability of observing `outcomes`
            on `input_state`.
        """
        alpha_square = input_state[:, :, 0]**2+\
            input_state[:, :, 1]**2
        log_prob = logpoisson(
            alpha_square, outcomes[:, :, 0],
            )
        return log_prob

    def apply_bs_network(
        self, variables_real: Tensor,
        variables_imag: Tensor,
        input_channels: Tensor,
        num_wires: int,
    ):
        """Applies the beam splitter network identified by
        `variables_real` and `variables_imag` to the
        state carried by the bosonic lines.
        
        Parameters
        ----------
        variables_real: Tensor
            `Tensor` of shape
            (`batchsize`, ?, `num_wires`, `num_wires`)
            and type `prec`.
        variables_imag: Tensor
            `Tensor` of shape
            (`batchsize`, ?, `num_wires`, `num_wires`)
            and type `prec`.
        input_channels: Tensor
            Displacement vector of the bosonic wires.
            It is a `Tensor` of type `prec` and
            shape (`batchsize`, ?, `2 num_wires`).
            The components of the `i`-th wire
            are at position `i` and `i+num_wires`.
        num_wires: int
            Number of wires in the system.

        Returns
        -------
        Tensor
            `Tensor` of shape
            (`batchsize`, ?, `2 num_wires`)
            and type `prec`, 
            containing the evolved displacements
            of the bosonic wires state.
        """
        type_complex = "complex128" if self.prec=="float64" else \
            "complex64"
        H = cast(
            variables_real+matrix_transpose(variables_real),
            dtype=type_complex)+\
                1.0j*cast(
            variables_imag-matrix_transpose(variables_imag),
            dtype=type_complex)
        U = expm(1.0j*H)
        X, Y = real(U), imag(U)
        S = concat(
            [concat([X, Y], 2), concat([-Y, X], 2)], 3,
        )
        return matvec(
            S, input_channels,
        )

    def apply_bs_network_from_unitary(
        self, unitary: Tensor,
        input_channels: Tensor,
    ):
        """Applies the beam splitter identified by
        `variables_real` and `variables_imag`.
        
        Parameters
        ----------
        unitary: Tensor
            `Tensor` of shape
            (`batchsize`, ?, `num_wires`, `num_wires`)
            and type `complex64` if `prec` is `float32`
            or `complex128` if `prec` if `float64`.
        input_channels: Tensor
            Displacement vector of the bosonic wires.
            It is a `Tensor` of type `prec` and
            shape (`batchsize`, ?, `2 num_wires`).
            The components of the `i`-th wire
            are at position `i` and `i+num_wires`.

        Returns
        -------
        Tensor
            `Tensor` of shape
            (`batchsize`, ?, `2 num_wires`)
            and type `prec`, 
            containing the evolved displacements
            of the bosonic wires wires.

        Notes
        -----
        The covariance matrix of the system is always
        proportional to the identity and corresponds
        to zero temperature.
        """
        X, Y = real(unitary), imag(unitary)
        S = concat(
            [concat([X, Y], 2), concat([-Y, X], 2)], 3,
        )
        return matvec(
            S, input_channels, 
        )

class QMLDiscriminator(
    StatefulPhysicalModel, CoherentStates,
    ):
    r"""Blueprint class for the quantum Machine Learning
    (QML) based classifier able to distinguish between
    three coherent states :math:`|\alpha_0\rangle`,
    :math:`|\alpha_1\rangle`, :math:`|\alpha_2\rangle`,
    given :math:`n` copies of each of them, which
    constitute the quantum training set.
    The signal state is a single copy of a
    coherent state, promised to be one of the 
    three training states, i.e. :math:`|\alpha_s\rangle`
    with `s=0, 1, 2`. 

    Notes
    -----
    The priors on the real components
    of the training states :math:`|\alpha_0\rangle`,
    :math:`|\alpha_1\rangle`, :math:`|\alpha_2\rangle`
    are uniform, as the prior on the signal classes
    `s=0, 1, 2`.

    Attributes
    ----------
    bs: int
        The batchsize of the physical model,
        i.e., the number of simultaneous signal
        testings simulated.
    controls: List[:py:obj:`~.physical_model.Control`]
        The controls of the QML classifier are the transmission
        coefficient and the
        extra phase of the beam splitter that
        precedes the photon counting. These can be chosen
        adaptively according to the previous measurements
        outcomes.
    params: List[:py:obj:`~.Parameter`]
        List of parameters to be estimated, passed
        to the class constructor. These are the
        real components of the unknown training states
        (continuous parameter), and the class of the
        signal.
    controls_size: int = 2
        Number of scalar controls in the QML classifier,
        i.e. 2, the two angles :math:`\theta`
        and :math:`\phi` characterizing the beam splitter
        transformation performed by 
        :py:meth:`~.CoherentStates.beamsplitter`.
    d: int = 7
        The number of unknown parameters to estimate,
        i.e. 7.
    state_specifics: :py:obj:`~.physical_model.StateSpecifics`
        Size of the state of the apparatus, which
        can be 2 for the `serial` architecture or
        6 for the `parallel`, plus the type of the
        state, i.e. `prec`. If `decision_tree=True`
        the size of the state is increased by one.
    recompute_state: bool = True
        Flag to the constructor of
        the :py:obj:`~.PhysicalModel` class.
    outcomes_size: int = 1
        Number of scalar outcomes for each measurement
        in the apparatus, i.e. one, the number of
        photons in the photon counter.
    prec: str
        The floating point precision of the controls,
        outcomes, and parameters.
    num_ref: int
        Number of copies of each training state,
        passed to the class constructor.
    num_steps: int
        Total number of photon counting measurements
        in the apparatus. It depends on `num_ref` and on
        the architecture, in particular it is
        `3 num_ref+1` for the serial apparatus and
        `3 num_ref+3` for the parallel one.
    resources: {"alpha", "step"}
        Resource type passes to the class constructor.
        It can be the average number of photons in the
        device ("alpha") or the number of measurements
        ("step").
    dt: bool
        Flag `decision_tree` passed to the class
        constructor. It should be activated if a decision
        tree is used for controlling the beam splitters.
    arch: {"serial", "parallel"}
        Architecture of the QML classifier
        passed to the class constructor.
        An object of the child class
        :py:obj:`~.QMLDiscriminatorSerial` will have
        `arch="serial"`, while an instance of
        :py:obj:`~.QMLDiscriminatorParallel` will have
        `arch="parallel"`.
    """
    def __init__(
        self, batchsize: int,
        params: List[Parameter],
        num_ref: int,
        resources: str = "alpha",
        arch: str = "serial",
        decision_tree: bool = False,
        prec: str = "float64",
    ):
        r"""Constructor of the :py:obj:`~.QMLDiscriminator`
        class.

        Parameters
        ----------
        batchsize: int
            Batchsize of the physical model, i.e.,
            the number of simultaneous estimations.
        params: List[:py:obj:`~.Parameter`]
            A list of unknown parameters to be estimated,
            alongside the corresponding
            sets of admissible values. For the three states
            Dolinar these are the `x` and `y` components
            of :math:`|\alpha_0\rangle`,
            :math:`|\alpha_1\rangle`, :math:`|\alpha_2\rangle`
            (six continuous parameters in total) plus the
            class of the signal, which is a discrete parameter
            that takes values in the set {`0`, `1`, `2`}.
        num_ref: int
            Number of copies of each training state.
        resources: {"alpha", "step"}
            Two types of resource counting are possible in
            the apparatus. The first is the
            the total number of photon counting measurements,
            corresponding to the value "step" for the
            `resources` parameter. The second is the
            mean number of photons in the apparatus,
            corresponding to
            the value "alpha" for this parameter.
            The average photon number is

            .. math::
                n \left( |\alpha_0|^2+|\alpha_1|^2+
                |\alpha_2|^2 \right) + |\alpha_s|^2 \; ,
            
            where :math:`n` is the number of training copies,
            i.e. `num_ref`.
        arch: {"serial", "parallel"}
            Architecture of the QML classifier.
        decision_tree: bool = False
            If this flag is `True`, then the physical
            model of the device is set up to be
            used with a decision tree controlling the
            beam splitters. This affect the state size,
            which now contains an integer that univocally
            identifies the string of outcomes
            that have already appeared in the photon counting
            measurements.
        prec: str = "float64"
            Floating point precision of the controls,
            outcomes, and parameters.
        """
        self.num_ref = num_ref
        self.resources = resources
        self.arch = arch
        self.dt = decision_tree

        if self.arch not in ("serial", "parallel"):
            raise ValueError("The parameter arch can\
                             only be serial or parallel.")

        if self.resources not in ("alpha", "step"):
            raise ValueError("The parameter resources can\
                             only be alpha or step.")
        
        controls = [
            Control(name="Theta"),
            Control(name="Phi"),
        ]

        CoherentStates.__init__(
            self, batchsize=batchsize,
            prec=prec,
        )

        state_size = 2 if self.arch=="serial" else 6
        # Total codified photon number added to the state
        if self.dt:
            state_size += 1
        StatefulPhysicalModel.__init__(
            self, batchsize, controls, params,
            state_specifics={'size': state_size, 'type': prec},
            outcomes_size=1,
            prec=prec,
        )

        if self.arch=="serial":
            self.num_steps = 3*self.num_ref+1
        else:
            self.num_steps = 3*self.num_ref+3

    def _slice_alphas(
            self, parameters: Tensor,
            signal_index: Tensor,
            ) -> Tensor:
        r"""Given a `Tensor` of parameters, of shape
        (`bs`, `np`, 7), this method returns a
        `Tensor` of shape (`bs`, `np`, 2), with the
        real components :math:`\alpha_x` and :math:`\alpha_y`
        of the true signal, which is determined
        by `signal_index`,
        which can take values `0, 1, 2`.
        """
        alpha_x = expand_dims(gather_nd(
            parameters[:, :, 0:6],
            2*cast(signal_index, dtype="int32"),
            batch_dims=2,
            ), axis=2)
        alpha_y = expand_dims(gather_nd(
            parameters[:, :, 0:6],
            2*cast(signal_index, dtype="int32")+1,
            batch_dims=2,
            ), axis=2)
        return concat([alpha_x, alpha_y], 2)

    def _codify_photon_string(
            self, previous_string: Tensor,
            outcomes: Tensor,
            meas_step: Tensor,
            num_systems: int = 1,
    ):
        ones_tensor = ones(
            (self.bs, num_systems, 1), dtype="int32",
            )
        mean_photon = 0.0
        for param in self.params[:-1]:
            mean_photon += param.bounds[0]**2+param.bounds[1]**2
        mean_photon /= 2*(len(self.params)-1)
        mean_photon = round(mean_photon)
        out_int = cast(outcomes, dtype="int32")
        trim_outcomes = minimum(
            max((mean_photon+1), 2)*ones_tensor,
            out_int,
        )
        trim_outcomes = maximum(
            (mean_photon-1)*ones_tensor,
            trim_outcomes,
        )
        encoded_out = trim_outcomes-(mean_photon-1)*ones_tensor
        new_string = previous_string + cast(tfpow(
            3*ones_tensor,
            cast(meas_step, dtype="int32"),
        )*(encoded_out+ones_tensor), dtype=self.prec)
        return new_string

    def count_resources(
        self, resources: Tensor, controls: Tensor,
        true_values: Tensor, meas_step: Tensor,
    ) -> Tensor:
        """The resources can be either the
        number of measurement steps or the mean
        number of photons in the system.
        In the second case the resource is considered
        consumed after the last photon counting
        measurement closing the device.
        """
        if self.resources=="alpha":
            num_copies = (self.num_steps-1)/3 \
                if self.arch=="serial" \
                else (self.num_steps-3)/3
            mean_photon = num_copies*(
                self.mean_phot(true_values[:, :, 0:2]) + \
                    self.mean_phot(true_values[:, :, 2:4]) + \
                        self.mean_phot(true_values[:, :, 4:6]))
            mean_photon += self.mean_phot(
                self._slice_alphas(
                    true_values, true_values[:, :, 6:7],
                ),)
            if equal(meas_step[0, 0], \
                    constant(self.num_steps-1, dtype="int32")):
                resources = mean_photon
        elif self.resources=="step":
            resources += 1.0
        return resources

class QMLDiscriminatorSerial(QMLDiscriminator):
    r"""Serial strategy for classifying
    a coherent state, given three hypothesis.

    .. image:: ../docs/_static/dolinar_three_serial.png
        :width: 600
        :alt: dolinar_three_serial

    The signal :math:`|\alpha_s\rangle` is alternatively
    mixed with the training states and measured.

    The order of the measurements is shown in the figure
    near the symbols for the for the photon counters.
    All the outcomes of the previous photon counters
    contribute to the determination of the next
    controls through the
    particle filter and the neural network
    (or the decision tree)
    """
    def __init__(
            self, batchsize: int,
            params: List[Parameter],
            num_ref: int,
            resources: str = "alpha",
            prec: str = "float64",
            decision_tree: bool = False,
            ):
        """Constructor of
        the :py:obj:`~.QMLDiscriminatorSerial` class.

        Parameters
        ----------
        batchsize: int
            Number of simultaneous estimations.
        params:
            Real components of the unknown
            training states and signal to be
            classified.
        num_ref: int
            Number of training states for each class.
        resources: {"alpha", "step"}
            Type of resources counted.
        prec:
            Floating point precision of the
            estimation.
        """
        super().__init__(
            batchsize, params, num_ref,
            resources=resources,
            arch="serial", prec=prec,
            decision_tree=decision_tree,
            )

    def initialize_state(
            self, parameters: Tensor,
            num_systems: int,
            ) -> Tensor:
        r"""Initializes the true state of the signal
        :math:`|\alpha_s\rangle`
        for the serial architecture.

        Parameters
        ----------
        parameters: Tensor[bs, num_systems, 7]
            `Tensor` of shape (`bs`, `num_system`, 7)
            and type `prec` containing the real components
            of the three training states and the index
            classifying the true signal
            (the seventh parameter).
        num_systems: int
            Size of the second dimension of the
            `parameters` tensor. It is the number of
            systems treated per batch element.

        Returns
        -------
        Tensor:
            `Tensor` of shape (`bs`, `num_system`, 2)
            containing the initial state of the signal
            :math:`|\alpha_s\rangle`, computed according
            to `parameters`. If `decision_tree=True` the size of the
            last dimension of the returned `Tensor` is 3.
        """

        zeros_tensor = zeros(
            (self.bs, num_systems, 1), dtype=self.prec,
            )
        light_state = self._slice_alphas(
            parameters, parameters[:, :, 6:7],
            )
        if self.dt:
            return concat([light_state, zeros_tensor], 2)
        return light_state
    
    def perform_measurement(
        self, controls: Tensor,
        parameters: Tensor, true_state: Tensor,
        meas_step: Tensor, rangen: Tensor,
    ) -> Tuple[Tensor, Tensor, Tensor]:
        r"""Mixing of the signal with the
        training state and photon counting
        on one end of the beam splitter.

        Parameters
        ----------
        controls: Tensor
            `Tensor` of shape (`bs`, 1, 2) and
            of type `prec` containing the two
            angles :math:`\theta` and :math:`\phi`
            characterizing the BS placed
            before a photon counter.
        parameters: Tensor
            `Tensor` of shape (`bs`, 1, 7) and type
            `prec` containing the six
            real components of the three
            training states plus the signal class.
        true_state: Tensor
            `Tensor` of shape (`bs`, 1, 2) containing
            the real components in the phase space
            of the signal traveling through the
            apparatus. If `decision_tree=True` the
            shape of this `Tensor` is
            (`bs`, 1, 3) and
            it contains also the whole history of
            outcomes codified in the last entry.
        meas_step: Tensor
            `Tensor` of shape (`bs`, 1, 1) and type `prec`.
            It is the index of the current measurement
            and starts from zero.
        rangen: Generator
            Random number generator from the module
            :py:mod:`tensorflow.random`.

        Return
        ------
        outcomes: Tensor
            `Tensor` of shape (`bs`, 1, 1) and type
            `prec` containing the number of photons
            observed in the photon counting measurement.
        log_prob: Tensor
            `Tensor` of shape (`bs`, 1) and type
            `prec` containing the logarithm of the
            probability of getting the observed
            number of photons.
        state: Tensor
            `Tensor` of shape (`bs`, 1, 2) and type `prec`
            containing the state of the signal evolved after
            the photon counting measurement.
            If `decision_tree=True` the
            shape of this `Tensor` is
            (`bs`, 1, 3) and
            it contains also the whole history of
            outcomes codified in the last entry.
        """
        # Reference state
        training_state = self._slice_alphas(
            parameters,
            floormod(
                meas_step,
                3*ones((self.bs, 1, 1), dtype="int32"),
            )
        )
        # Controls
        theta, phi = controls[:, :, 0], controls[:, :, 1]
        # The last measurement is a direct
        # photon counting on the signal
        if equal(meas_step[0, 0, 0], \
                 constant(self.num_steps-1, dtype="int32")):
            outcomes, log_prob = self.photon_counter(
                true_state[:, :, 0:2], rangen,
            )
            # It's not important to update the state after
            # the last measurement.
            signal = true_state[:, :, 0:2]
        else:
            signal, to_photodetector = self.beamsplitter(
                true_state[:, :, 0:2],
                training_state, theta, phi,
                )
            outcomes, log_prob = self.photon_counter(
                to_photodetector, rangen,
                )
        new_string = self._codify_photon_string(
            true_state[:, :, 2:], outcomes, meas_step,
        )
        return outcomes, log_prob, concat([signal, new_string], 2)

    def model(
            self, outcomes: Tensor, controls: Tensor,
            parameters: Tensor, state: Tensor,
            meas_step: Tensor,
            num_systems: int = 1,
            ) -> Tuple[Tensor, Tensor]:
        r"""Probability of observing a certain
        number of photons in a photon counting measurement
        in the serial device.

        Parameters
        ----------
        outcomes:
            `Tensor` of shape (`bs`, `num_systems`, 1) and
            type `prec` containing the observed
            number of photons in a measurement.
        controls: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 2) and
            of type `prec` containing the two
            angles :math:`\theta` and :math:`\phi`
            characterizing the BS placed before
            a photon counter.
        parameters: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 7)
            and type `prec` containing the six
            real components of the three
            training states plus the signal class.
        state: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 2) containing
            the real components in the phase space
            of the signal traveling through the
            apparatus. If `decision_tree=True` the
            shape of this `Tensor` is
            (`bs`, `num_systems`, 3) and
            it contains also the whole history of
            outcomes codified in the last entry.
        meas_step: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 1)
            and type `prec`. It is the
            index of the current measurement
            and starts from zero.
        num_systems: int = 1
            Number of system treated for each
            element of the batch.

        Return
        ------
        log_prob: Tensor
            `Tensor` of shape (`bs`, `num_systems`)
            and type
            `prec` containing the logarithm of the
            probability of getting the observed
            number of photons.
        state: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 2)
            and type `prec`
            with the state of the signal evolved after
            the photon counting measurement.
            If `decision_tree=True` the
            shape of this `Tensor` is
            (`bs`, `num_systems`, 3) and
            it contains also the whole history of
            outcomes codified in the last entry.
        """
        # Reference state
        training_state = self._slice_alphas(
            parameters,
            floormod(
                meas_step,
                3*ones((self.bs, num_systems, 1),
                       dtype="int32"))
        )
        # Controls
        theta, phi = controls[:, :, 0], \
            controls[:, :, 1]
        # The last measurement is a direct photon counting on
        # the signal
        if equal(meas_step[0, 0, 0], \
                 constant(self.num_steps-1, dtype="int32")):
            log_prob = self.postselect_photon_counter(
                state[:, :, 0:2], outcomes,
            )
            # It's not important to update the state after the
            # last measurement
            signal = state[:, :, 0:2]
        else:
            signal, to_photodetector = self.beamsplitter(
                state[:, :, 0:2], training_state,
                theta, phi,
                )
            log_prob = self.postselect_photon_counter(
                to_photodetector, outcomes,
                )
        new_string = self._codify_photon_string(
            state[:, :, 2:], outcomes, meas_step,
            num_systems=num_systems,
        )
        return exp(log_prob), \
            concat([signal, new_string], 2)
    
class QMLDiscriminatorParallel(QMLDiscriminator):
    r"""Parallel strategy for classifying
    a coherent state, given three hypothesis.

    .. image:: ../docs/_static/dolinar_three_parallel.png
        :width: 500
        :alt: dolinar_three_parallel

    The original signal is first equally splitted on three
    wires, i.e. :math:`|\alpha_s\rangle \rightarrow 
    |\frac{\alpha_s}{\sqrt{3}}\rangle^{\otimes 3}`. On each
    line the signal is mixed with the copies of the same
    training state.

    The order of the measurements is show in the figure
    near the symbol for the photon counter. The
    measurements are not really done in parallel as it
    can be seen. All
    the outcomes of the previous photon counters
    contributes to the determination of the next
    controls through the
    particle filter and the neural network
    (or the decision tree). In order to realize the
    measurements in this order the optical path along the
    the wires should be prolonged differently.
    """
    def __init__(
            self, batchsize: int,
            params: List[Parameter],
            num_ref: int,
            resources: str = "alpha",
            decision_tree: bool = False,
            prec: str = "float64",
            ):
        r"""Constructor of
        the :py:obj:`~.QMLDiscriminatorParallel` class.

        Parameters
        ----------
        batchsize: int
            Number of simultaneous estimations.
        params: List[:py:obj:`~.Parameter`]
            Contains the real components of the unknown
            training states and the signal to be
            classified.
        num_ref: int
            Number of training states for each class.
        resources: {"alpha", "step"}
            Type of resources counted.
        decision_tree: bool = False
            Indicates that a decision tree is used for
            controlling the beam splitters.
        prec:
            Floating point precision of the
            estimation.
        """
        super().__init__(
            batchsize, params, num_ref,
            resources=resources,
            arch="parallel", prec=prec,
            decision_tree=decision_tree,
            )

    def initialize_state(
            self, parameters: Tensor,
            num_systems: int,
            ) -> Tensor:
        r"""Initializes the true state of the signal
        :math:`|\frac{\alpha_s}{\sqrt{3}}\rangle^{\otimes 3}`
        for the parallel device.

        Parameters
        ----------
        parameters: Tensor
            `Tensor` of shape (`bs`, `num_system`, 7)
            and type `prec` containing the real components
            of the three training states and the index
            classifying the true signal
            (the seventh parameter).
        num_systems: int
            Size of the second dimension of the
            `parameters` `Tensor`. It is the number of
            systems treated per batch element.

        Returns
        -------
        Tensor:
            `Tensor` of shape (`bs`, `num_system`, 6)
            containing the state of the true signal,
            equally distributed on the three lines of the
            discrimination device with parallel architecture.
            If `decision_tree=True` the size of the
            last dimension of the returned `Tensor` is 7.
        """
        zeros_tensor = zeros(
            (self.bs, num_systems, 1), dtype=self.prec,
            )
        signal = self._slice_alphas(
            parameters, parameters[:, :, 6:7],
            )
        light_state = concat(
            [signal/npsqrt(3),
             signal/npsqrt(3),
             signal/npsqrt(3)], 2,
            )
        if self.dt:
            return concat([light_state, zeros_tensor], 2)
        return light_state
        
    
    def perform_measurement(
        self, controls: Tensor,
        parameters: Tensor, true_state: Tensor,
        meas_step: Tensor, rangen: Tensor,
    ):
        r"""Mixing of the signal on one wire with the
        corresponding training state and photon counting
        on one end of the beam splitter.

        Parameters
        ----------
        controls: Tensor
            `Tensor` of shape (`bs`, 1, 2) and
            of type `prec` containing the two
            angles :math:`\theta` and :math:`\phi`
            characterizing the BS placed
            before a photon counter.
        parameters: Tensor
            `Tensor` of shape (`bs`, 1, 7) and type
            `prec` containing the six
            real components of the three
            training states plus the signal class.
        true_state: Tensor
            `Tensor` of shape (`bs`, 1, 6) containing
            the real components in the phase space
            of the signal traveling through the three
            wires of the apparatus.
            If `decision_tree=True` the
            shape of this `Tensor` is
            (`bs`, 1, 7) and
            it contains also the whole history of
            outcomes codified in the last entry.
        meas_step: Tensor
            `Tensor` of shape (`bs`, 1, 1) and type `prec`.
            It is the index of the current measurement
            and starts from zero.

        Return
        ------
        outcomes: Tensor
            `Tensor` of shape (`bs`, 1, 1) and type
            `prec` containing the number of photons
            observed in the photon counting measurement.
        log_prob: Tensor
            `Tensor` of shape (`bs`, 1) and type
            `prec` containing the logarithm of the
            probability of getting the observed
            number of photons.
        state: Tensor
            `Tensor` of shape (`bs`, 1, 6) and type `prec`
            with the state of the signal evolved after
            the photon counting measurement.
            If `decision_tree=True` the
            shape of this `Tensor` is
            (`bs`, 1, 7) and
            it contains also the whole history of
            outcomes codified in the last entry.
        """
        # Reference state
        training_state = self._slice_alphas(
            parameters,
            floormod(
                meas_step,
                3*ones((self.bs, 1, 1), dtype="int32"),
            )
        )
        if equal(floormod(meas_step[0, 0, 0],
                          constant(3, dtype="int32"),),
                 constant(0, dtype="int32"),
            ):
            local_state = true_state[:, :, 0:2]
            outcomes, log_prob, local_state = \
                self._meas(
                meas_step, controls, training_state,
                local_state, rangen,
            )
            signal = concat(
                [local_state, true_state[:, :, 2:6]], 2,
                )
        elif equal(floormod(meas_step[0, 0, 0],
                            constant(3, dtype="int32"),),
                 constant(1, dtype="int32"),
            ):
            local_state = true_state[:, :, 2:4]
            outcomes, log_prob, local_state = \
                self._meas(
                meas_step, controls,
                training_state, local_state, rangen,
            )
            signal = concat(
                [true_state[:, :, 0:2],
                 local_state, true_state[:, :, 4:6]], 2,
                )
        else:
            local_state = true_state[:, :, 4:6]
            outcomes, log_prob, local_state = \
                self._meas(
                meas_step, controls,
                training_state, local_state, rangen,
            )
            signal = concat(
                [true_state[:, :, 0:4], local_state,], 2,
                )
        new_string = self._codify_photon_string(
            true_state[:, :, 6:], outcomes, meas_step,
        )
        return outcomes, log_prob, \
            concat([signal, new_string], 2)
      
    def _meas(
            self, meas_step: Tensor,
            controls: Tensor,
            training_state: Tensor,
            local_state: Tensor, rangen,
        ):
        theta, phi = controls[:, :, 0], controls[:, :, 1]
        if greater_equal(meas_step[0, 0, 0], \
            constant(self.num_steps-3, dtype="int32")):
            outcomes, log_prob = self.photon_counter(
                    local_state, rangen,
                )
            evolved_local_state = local_state
        else:
            evolved_local_state, to_photodetector = \
                self.beamsplitter(
                local_state, training_state,
                theta, phi,
            )
            outcomes, log_prob = self.photon_counter(
                to_photodetector, rangen,
            )
        return outcomes, log_prob, evolved_local_state

    def model(
            self, outcomes: Tensor, controls: Tensor,
            parameters: Tensor, state: Tensor,
            meas_step: Tensor,
            num_systems: int = 1,
            ):
        r"""Probability of observing a certain
        number of photons in a photon counting
        measurement in the parallel device.

        Parameters
        ----------
        outcomes:
            `Tensor` of shape (`bs`, `num_systems`, 1) and
            type `prec` containing the observed
            number of photons in a measurement.
        controls: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 2) and
            of type `prec` containing the two angles
            :math:`\theta` and :math:`\phi`
            characterizing the BS placed
            before a photon counter.
        parameters: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 7)
            and type `prec` containing the six
            real components of the three
            training states plus the signal class.
        state: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 6) containing
            the real components in the phase space
            of the signal traveling through the
            three wires of the
            apparatus. If `decision_tree=True` the
            shape of this `Tensor` is
            (`bs`, `num_systems`, 7) and
            it contains also the whole history of
            outcomes codified in the last entry.
        meas_step: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 1)
            and type `prec`. It is the
            index of the current measurement
            and starts from zero.
        num_systems: int = 1
            Number of system treated for each
            element of the batch.

        Return
        ------
        log_prob: Tensor
            `Tensor` of shape (`bs`, `num_systems`)
            and type
            `prec` containing the logarithm of the
            probability of getting the observed
            number of photons.
        state: Tensor
            `Tensor` of shape (`bs`, `num_systems`, 6)
            and type `prec`
            with the state of the signal evolved after
            the photon counting measurement.
            If `decision_tree=True` the
            shape of this `Tensor` is
            (`bs`, `num_systems`, 7) and
            it contains also the whole history of
            outcomes codified in the last entry.
        """
        # Reference state
        training_state = self._slice_alphas(
            parameters,
            floormod(
                meas_step,
                3*ones((self.bs, num_systems, 1), dtype="int32")
            ),
        )
        # Controls
        if equal(floormod(meas_step[0, 0, 0],
                          constant(3, dtype="int32"),),
                constant(0, dtype="int32"),
            ):
            local_state = state[:, :, 0:2]
            log_prob, local_state = \
                self._post(
                meas_step, controls, outcomes,
                training_state, local_state,
            )
            signal = concat([local_state, state[:, :, 2:6]], 2)
        if equal(floormod(meas_step[0, 0, 0],
                          constant(3, dtype="int32"),),
                constant(1, dtype="int32"),
            ):
            local_state = state[:, :, 2:4]
            log_prob, local_state = self._post(
                meas_step, controls, outcomes,
                training_state, local_state,
            )
            signal = concat(
                [state[:, :, 0:2], local_state,
                 state[:, :, 4:6]], 2,
                )
        else:
            local_state = state[:, :, 4:6]
            log_prob, local_state = \
                self._post(
                meas_step, controls, outcomes,
                training_state, local_state,
            )
            signal = concat(
                [state[:, :, 0:4], local_state,], 2,
                )
        new_string = self._codify_photon_string(
            state[:, :, 6:], outcomes, meas_step,
        )
        return exp(log_prob), concat([signal, new_string], 2)
    
    def _post(
            self, meas_step: Tensor,
            controls: Tensor,
            outcomes: Tensor,
            training_state: Tensor,
            local_state: Tensor,
            ):
        theta, phi = controls[:, :, 0], controls[:, :, 1]
        if greater_equal(meas_step[0, 0, 0], \
            constant(self.num_steps-3, dtype="int32")):
            log_prob = self.postselect_photon_counter(
                local_state, outcomes,
            )
            evolved_local_state = local_state
        else:
            evolved_local_state, to_photodetector = \
                self.beamsplitter(
                local_state, training_state, theta, phi,
            )
            log_prob = self.postselect_photon_counter(
                to_photodetector, outcomes,
            )
        return log_prob, evolved_local_state
    
class QMLSimulation(StatefulSimulation):
    """Simulation class for the QML classifier
    with three states.
    """
    def __init__(
            self, particle_filter: ParticleFilter,
            phys_model: QMLDiscriminator,
            control_strategy: Callable,
            simpars: SimulationParameters,
            loss: int = 0,
    ):
        """Constructor of the
        :py:obj:`~.QMLSimulation` class.

        Parameters
        ----------
        particle_filter: :py:obj:`~.ParticleFilter`
            Particle filter responsible for the update
            of the Bayesian posterior on the parameters
            and on the state of the probe.
        phys_model: :py:obj:`~.DolinarThree`
            Abstract description of
            the QML classifier.
        control_strategy: Callable
            Callable object (normally a
            function or a lambda function) that
            computes the values of the controls
            for the next measurement from
            the `Tensor` `input_strategy`, which is
            produced by the method
            :py:meth:`~.QMLSimulation.generate_input`.
        simpars: :py:obj:`~.SimulationParameters`
            Contains the flags and parameters
            that regulate the stopping
            condition of the measurement loop
            and modify the loss function used in the
            training.
        loss: {0, 1}
            In principle the loss of the QML classifier
            is always the error probability
            of classifying the state wrongly. However there
            can be different classification strategies and
            accordingly different estimators for
            the error probability.
            In this class two possible loss functions are
            implemented. The details are reported in the
            documentation of the 
            :py:meth:`~.QMLSimulation.loss_function`
            method.
        """
        if phys_model.dt:
            # Set the input size
            input_size = 1
            # Set the name of each column of the input
            input_name = ["OutcomesString", ]
        else:
            # Set the input size
            input_size = 19 if phys_model.arch=="serial" else 23
            # Set the name of each column of the input
            input_name = [
                'MeanState_x', 'MeanState_y',
                'MeanAlpha_x_0', 'MeanAlpha_y_0',
                'MeanAlpha_x_1', 'MeanAlpha_y_1',
                'MeanAlpha_x_2', 'MeanAlpha_y_2',
                'LogSigma_x_0', 'LogSigma_y_0',
                'LogSigma_x_1', 'LogSigma_y_1',
                'LogSigma_x_2', 'LogSigma_y_2',
                'Prob0', 'Prob1', 'Prob2',
                'MeasStepOverNumStep', 'MeasStepMod3',] \
                if phys_model.arch=="serial" else \
                ['MeanState_x_0', 'MeanState_y_0',
                'MeanState_x_1', 'MeanState_y_1',
                'MeanState_x_2', 'MeanState_y_2',
                'MeanAlpha_x_0', 'MeanAlpha_y_0',
                'MeanAlpha_x_1', 'MeanAlpha_y_1',
                'MeanAlpha_x_2', 'MeanAlpha_y_2',
                'LogSigma_x_0', 'LogSigma_y_0',
                'LogSigma_x_1', 'LogSigma_y_1',
                'LogSigma_x_2', 'LogSigma_y_2',
                'Prob0', 'Prob1', 'Prob2',
                'MeasStepOverNumStep', 'MeasStepMod3', ]

        super().__init__(
            particle_filter,
            phys_model,
            control_strategy,
            input_size, input_name,
            simpars,
            )
        
        self.loss = loss
        if self.loss not in (0, 1):
            raise ValueError("The parameter loss can\
                             only be 0 or 1.")
        
    def _select_hypothesis(
            self, particles: Tensor,
            weights: Tensor,
            hypothesis: int,
    ) -> Tuple[Tensor, Tensor]:
        """Returns the posterior
        probability distribution conditioned
        on a certain classification for the unknown
        signal.
        """
        pars = self.simpars
        zeros_tensor = zeros(
            (self.bs, self.pf.np), dtype=pars.prec,
            )
        ones_tensor = ones(
            (self.bs, self.pf.np), dtype=pars.prec,
            )
        selected_weights = where(
            equal(particles[:, :, 6],
                  hypothesis*ones_tensor),
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
            state: Tensor,
    ) -> Tuple[Tensor, Tensor, Tensor]:
        """Computes the average estimated
        training state, its standard deviation,
        and the average signal state for the
        provided posterior distribution.
        """
        mean_state = normalize(self.pf.compute_state_mean(
            weights, state,
            ), [0, 1], )
        mean_alpha = normalize(self.pf.compute_mean(
            weights, particles[:, :, 0:6], dims=6,
        ), [0, 1], )
        sigma_alpha = self.pf.compute_covariance(
            weights, particles[:, :, 0:6], dims=6,
        )
        logdev_alpha = normalize(
            log(sqrt(diag_part(sigma_alpha))+1e-33),
            [-10.0, 0.0],
            )
        return mean_state, mean_alpha, logdev_alpha
        
    def generate_input(
        self, weights: Tensor, particles: Tensor,
        state_ensemble: Tensor, meas_step: Tensor,
        used_resources: Tensor,
        rangen: Generator,
    ) -> Tensor:
        r"""Generates the input to the control strategy
        (the neural network or
        the decision tree) starting from
        the particle filter ensemble.

        The values chosen to be inputs of the
        neural network are similar to those provided
        in the example of the :py:mod:`dolinar` module.
        These are

        * the average state of the signal after the photon
          counting measurements, computed from
          the posterior distribution.
          These can be 2 ore 6 scalar values according
          to the architecture of the apparatus,

        * :math:`(\hat{\alpha}_{0x}, \hat{\alpha}_{0y}, \
          \hat{\alpha}_{1x}, \hat{\alpha}_{1y}, \
          \hat{\alpha}_{2x}, \hat{\alpha}_{2y})`, i.e. the
          average values of the real components of
          the training states computed
          from the posterior distribution,

        * :math:`(\hat{\sigma}_{0x}, \hat{\sigma}_{0y}, \
          \hat{\sigma}_{1x}, \hat{\sigma}_{1y}, \
          \hat{\sigma}_{2y}, \hat{\sigma}_{2y})`, i.e. the
          standard deviation
          from the mean of the real components of the
          training states computed from the
          posterior distribution.

          Given :math:`\hat{\sigma}` one of these deviations,
          the value passed to the control strategy is actually
          :math:`-\frac{1}{10} \log \hat{\sigma}`.

        * :math:`2 \hat{p}_{0}-1`, i.e. the posterior
          probability for the initial state to be `s=0`,
          normalized in [-1, +1],

        * :math:`2 \hat{p}_{1}-1`, i.e. the posterior
          probability for the initial state to be `s=1`,
          normalized in [-1, +1],

        * :math:`2 \hat{p}_{2}-1`, i.e. the posterior
          probability for the initial state to be `s=2`,
          normalized in [-1, +1],
        
        * :math:`2 m/M -1`, i.e. the number of
          measurements normalized in [-1, +1].
          :math:`M` is the total number
          measurement and corresponds to the attribute
          `num_steps` of :py:obj:`~.DolinarThree`,
          while `m` is the index
          of the current photon counting measurement, i.e.
          `meas_step`,
        
        * :math:`m \bmod 3 - 1`, this tells
          whether the current measure is performed
          by mixing the signal with :math:`| \alpha_0 \rangle`,
          :math:`| \alpha_1 \rangle`,
          or :math:`| \alpha_2 \rangle`.

        For a serial architecture the number of
        scalar input is 19, while for a parallel
        one this number is 23.

        **Achtung!** If `decision_tree=True` then
        `input_tensor` is composed of a single
        scalar value which encodes the string
        of outcomes already observed in the
        measurements.
        """
        pars = self.simpars
        # Extraction of the weights for each hypothesis
        _, prob_0 = self._select_hypothesis(
            particles, weights, 0,
            )
        _, prob_1 = self._select_hypothesis(
            particles, weights, 1,
            )
        _, prob_2 = self._select_hypothesis(
            particles, weights, 2,
            )
        mean_state, mean_alpha, logdev_alpha = \
            self._compute_partial_input(
            weights, particles, state_ensemble,
            )
        norm_meas_step = \
            cast(meas_step, dtype=pars.prec)/\
                (pars.num_steps)
        meas_step_mod = cast(
            floormod(cast(tfround(meas_step), dtype="int32"),
                     3*ones((self.bs, 1), dtype="int32")),
            dtype=pars.prec,
        )
        if self.phys_model.dt:
            return state_ensemble[:, 0, -1:]
        return concat(
            [mean_state, mean_alpha, logdev_alpha,
             2*prob_0-1, 2*prob_1-1, 2*prob_2-1,
             2*norm_meas_step-1, meas_step_mod-1, ], 1)
        

    def loss_function(
        self, weights: Tensor, particles: Tensor,
        true_state: Tensor, state_ensemble: Tensor,
        true_values: Tensor, used_resources: Tensor,
        meas_step: Tensor,
    ):
        r"""Returns the estimated error
        probability for each simulation in the batch.
        Two possible losses are implemented, and we can
        select which one to use in the simulation
        via the parameter `loss` of the
        :py:obj:`~.QMLSimulation` class constructor.
        Before defining these losses we need to
        introduce some notation.

        As in :py:meth:`~.generate_input` the posterior
        Bayesian
        probabilities of the signal being respectively
        `s=0, 1, 2` are denominated :math:`\hat{p}_0`,
        :math:`\hat{p}_1`, and :math:`\hat{p}_2`.
        We introduce the :math:`\delta`-function, i.e.

        .. math::
            \delta (x, y) = \begin{cases}
                1 \quad \text{if} \quad x=y \; , \\
                0 \quad \text{if} \quad x \neq y \; ,
            \end{cases}
        
        and the guess function :math:`G`:

        .. math::
            G (\vec{\hat{p}}) =
            \text{argmax} (\hat{p}_0, \hat{p}_1, \hat{p}_2) \; .

        * The first possible loss, corresponding to `loss=0`, is

          .. math::
              \ell (\vec{\hat{p}}, s) = 1 - \hat{p}_{s} \; ,
          
          for which the idea is to try to push down the
          probabilities corresponding to the wrong hypothesis.
          This loss doesn't operate on the guess
          :math:`G (\vec{\hat{p}})` but directly on the
          posterior probabilities :math:`\vec{\hat{p}}`.
        
        * The second loss, corresponding to `loss=1`, is

          .. math::
              \ell (\vec{\hat{p}}, s) = 1 -
              \delta (G(\vec{\hat{p}}), s) \; .

          This loss is one if an error is
          made and zero if the guess is right.
          Averaged on many batches this loss
          converges to the error probability.
  
        Both losses corresponds to an estimation
        strategy where the
        hypothesis with the highest posterior probability
        is always guessed.
        """
        pars = self.simpars
        zeros_tensor = zeros(
            (self.bs, 1), dtype=pars.prec,)
        ones_tensor = ones(
            (self.bs, 1), dtype=pars.prec,
            )
        _, prob_0 = self._select_hypothesis(
            particles, weights, 0,
            )
        _, prob_1 = self._select_hypothesis(
            particles, weights, 1,
            )
        _, prob_2 = self._select_hypothesis(
            particles, weights, 2,
            )
        prob = concat([prob_0, prob_1, prob_2], 1)
        if self.loss==0:
            prob_true_values = expand_dims(gather_nd(
                params=prob,
                indices=cast(true_values[:, :, 6], dtype="int32"),
                batch_dims=1,
                name = "prob_true"
            ), axis=1)
            # The loss tries to push down the probability
            # of all the wrong hypothesis
            return 1.0-prob_true_values
        else:
            guess = expand_dims(
                argmax(prob, axis=1, output_type="int32"),
                axis=1,
            )
            loss_values = where(
                equal(
                    guess,
                    cast(true_values[:, :, 6], dtype="int32")
                ), zeros_tensor, ones_tensor,
            )
            return loss_values
    
    def __str__(self):
        return super().__str__() + f"_loss_{self.loss}"
    
def parse_args():
    r"""Arguments
    ---------
    scratch_dir: str
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./qml_classifier/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./qml_classifier/data"
        Directory containing the csv files
        produced by the :py:func:`~.utils.performance_evaluation`
        and the :py:func:`~.utils.store_input_control` functions.
    prec: str = "float64"
        Floating point precision of the
        whole simulation.
    batchsize: int = 1024
        Batchsize of the simulation.
    n: int = 64
        Number of neurons per layer in the neural network.
    num_particles: int = 512
        Number of particles in the ensemble representing
        the posterior.
    num_ref: int = 4
        Number of copies of each training state
        :math:`|\alpha_0\rangle`,
        :math:`|\alpha_1\rangle`,
        :math:`|\alpha_2\rangle`.
    iterations: int = 32768
        Number of training steps.
    """
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir", type=str,
                        default="./qml_classifier/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./qml_classifier/data")
    parser.add_argument('--prec', type=str, default="float64")
    parser.add_argument("--batchsize", type=int, default=1024)
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument("--num-particles", type=int, default=512)
    parser.add_argument("--num-ref", type=int, default=4)
    parser.add_argument("--iterations", type=int, default=32768)

    return parser.parse_args()

def simulation_qmlclassifier(
        args,
        alpha_bound: float = 1.0,
        learning_rate: float = 1e-2,
        loss: int = 0,
        arch: str = "serial",
):
    r"""Simulation of the QML classifier.

    Parameters
    ----------
    args:
        Arguments passed to the Python script.
    alpha_bound: float = 1.0
        Size of the hypercube of the admissible
        values for the real components of the
        three training states. 
    learning_rate: float = 1e-2
        Initial learning rate for the neural network.
        The static strategy has a fixed initial
        learning rate of `1e-1`. Both are reduced
        during the training according
        to :py:obj:`~.InverseSqrtDecay`.
    loss: {0, 1}
        Type of loss for the training.
        The two possibilities
        (`loss=0, 1`) are discussed in the
        documentation of the
        :py:meth:`~.QMLSimulation.loss_function`
        method.
    arch: {"serial", "parallel"}
        Architecture of device. If
        it is "serial" then an object
        :py:obj:`~.QMLDiscriminatorSerial` is instantiated
        for the simulation, if it is "parallel" instead,
        an object :py:obj:`~.QMLDiscriminatorParallel` is
        instantiated.
    """
    if arch not in ("serial", "parallel"):
        raise ValueError("The parameter arch can\
                         only be serial or parallel.")

    # Input s
    input_size = 19 if arch=="serial" else 23
    # Size of the controls
    control_size = 2

    network = standard_model(
        input_size=input_size,
        controls_size=control_size,
        neurons_per_layer=args.n,
        prec=args.prec,
    )
    network.compile()
    
    max_steps = 3*args.num_ref+1 if arch=="serial" \
        else 3*args.num_ref+3

    params=[Parameter(bounds=(-alpha_bound, alpha_bound),
                      name="alpha_x_0"),
            Parameter(bounds=(-alpha_bound, alpha_bound),
                      name="alpha_y_0"),
            Parameter(bounds=(-alpha_bound, alpha_bound),
                      name="alpha_x_1"),
            Parameter(bounds=(-alpha_bound, alpha_bound),
                      name="alpha_y_1"),
            Parameter(bounds=(-alpha_bound, alpha_bound),
                      name="alpha_x_2"),
            Parameter(bounds=(-alpha_bound, alpha_bound),
                      name="alpha_y_2"),
            Parameter(values=(0, 1, 2), name="signal"),
        ]
    
    qml_classifier = QMLDiscriminatorSerial(
        batchsize=args.batchsize,
        params=params,
        num_ref=args.num_ref,
        prec=args.prec,
    ) if arch=="serial" else \
    QMLDiscriminatorParallel(
        batchsize=args.batchsize,
        params=params,
        num_ref=args.num_ref,
        prec=args.prec,
    )
        
    particle_filter = ParticleFilter(
        num_particles=args.num_particles,
        phys_model=qml_classifier,
        resample_fraction=0.98,
        prec=args.prec,
    )

    # NN strategy
    # ----------------------------------------------

    max_res = (3*args.num_ref+1)*2*alpha_bound**2
    
    simpars = SimulationParameters(
        sim_name="dolinar3serial" \
            if arch=="serial" else \
            "dolinar3parallel",
        num_steps=max_steps,
        max_resources=max_res,
        prec=args.prec,
    )

    sim_nn = QMLSimulation(
        particle_filter=particle_filter,
        simpars=simpars,
        phys_model=qml_classifier,
        control_strategy=\
            lambda x: floormod(network(x), 2*pi),
        loss=loss,
    )

    decaying_learning_rate = InverseSqrtDecay(
        learning_rate, args.prec,
    )

    train(
       sim_nn,
       Adam(learning_rate=decaying_learning_rate),
       args.iterations, args.scratch_dir,
       network=network,
       xla_compile=False,
    )

    network.save(
            join(args.trained_models_dir, str(sim_nn)),
            )
    # network=load_model(
    #         join(args.trained_models_dir, str(sim_nn)),
    #         )

    performance_evaluation(
       sim_nn, args.iterations,
       args.data_dir,
       xla_compile=False,
       delta_resources=1.0,
       y_label='ProbError',
    )

    qml_classifier.resources = "step"

    store_input_control(
       sim_nn, args.data_dir, 5,
       xla_compile=False,
    )

    qml_classifier.resources = "alpha"

    # Static strategy
    # ---------------------------------------------

    # Initial value of the controls in the static
    # optimization
    initial_state = nprand(int(3*args.num_ref), 2)
    static_variables = Variable(
        initial_state, dtype=args.prec,
        )

    simpars = SimulationParameters(
        sim_name="dolinar3serial_static" \
            if arch=="serial" else \
            "dolinar3parallel_static",
        num_steps=max_steps,
        max_resources=max_res,
        prec=args.prec,
    )

    def qmlc_control_strategy_static(input_tensor):
        static_control = gather(
            params=2*pi*static_variables,
            indices=cast(
                tfround(max_steps*((\
            input_tensor[:, -2]+1)/2)), dtype="int32",
            ),
        )
        return floormod(static_control, 2*pi)

    sim_static = QMLSimulation(
        particle_filter=particle_filter,
        simpars=simpars,
        phys_model=qml_classifier,
        control_strategy=\
            qmlc_control_strategy_static,
        loss=loss,
    )

    decaying_learning_rate = InverseSqrtDecay(
        1e-1, args.prec,
    )

    train(
        sim_static, Adam(
            learning_rate=decaying_learning_rate,
            ),
        args.iterations, args.scratch_dir,
        custom_controls=static_variables,
        xla_compile=False,
    )

    savetxt(
        join(args.trained_models_dir, str(sim_static)),
            static_variables.numpy(),
            )
    # static_variables = Variable(loadtxt(
    #     join(args.trained_models_dir, str(sim_static)),
    #     ), dtype=args.prec,
    # )

    performance_evaluation(
        sim_static,
        args.iterations, args.data_dir,
        xla_compile=False,
        delta_resources=1.0,
        y_label='ProbError',
    )
    
    qml_classifier.resources = "step"

    store_input_control(
        sim_static, args.data_dir, 5,
        xla_compile=False,
    )

    qml_classifier.resources = "alpha"

    # Decision tree
    # ---------------------------------------------

    # Size of the controls
    control_size = 2

    qml_classifier = QMLDiscriminatorSerial(
        batchsize=args.batchsize,
        params=params,
        num_ref=args.num_ref,
        prec=args.prec,
        decision_tree=True,
    ) if arch=="serial" else \
    QMLDiscriminatorParallel(
        batchsize=args.batchsize,
        params=params,
        num_ref=args.num_ref,
        prec=args.prec,
        decision_tree=True,
    )

    particle_filter = ParticleFilter(
        num_particles=args.num_particles,
        phys_model=qml_classifier,
        resample_fraction=0.98,
        prec=args.prec,
    )

    #Initial value of the controls in the decision tree
    static_variables = loadtxt(
        join(args.trained_models_dir, str(sim_static)),
        )
    list_tree = []
    for i in range(static_variables.shape[0]):
        list_tree.append(
            nprepeat(static_variables[i:(i+1), :],
                     3**i, axis=0),
            )
    initial_state = npconcat(list_tree)
    
    decision_tree_var = Variable(
        initial_state, dtype=args.prec,
        )

    simpars = SimulationParameters(
        sim_name="dolinar3serial_dtree" \
            if arch=="serial" else \
            "dolinar3parallel_dtree",
        num_steps=max_steps,
        max_resources=max_res,
        prec=args.prec,
    )

    def qmlc_control_strategy_dtree(input_tensor):
        static_control = gather(
            params=2*pi*decision_tree_var,
            indices=cast(input_tensor[:, 0],
                         dtype="int32"),
            )
        return floormod(static_control, 2*pi)

    sim_dtree = QMLSimulation(
        particle_filter=particle_filter,
        simpars=simpars,
        phys_model=qml_classifier,
        control_strategy=\
            qmlc_control_strategy_dtree,
        loss=loss,
    )

    decaying_learning_rate = InverseSqrtDecay(
        1e-2, args.prec,
    )

    train(
        sim_dtree, Adam(
            learning_rate=decaying_learning_rate,
            ),
        args.iterations, args.scratch_dir,
        custom_controls=decision_tree_var,
        xla_compile=False,
    )

    savetxt(
        join(args.trained_models_dir, str(sim_dtree)),
            decision_tree_var.numpy(),
            )
    # decision_tree_var = Variable(loadtxt(
    #     join(args.trained_models_dir, str(sim_dtree)),
    #     ), dtype=args.prec,
    # )

    performance_evaluation(
        sim_dtree,
        args.iterations, args.data_dir,
        xla_compile=False,
        delta_resources=1.0,
        y_label='ProbError',
    )
    
    qml_classifier.resources = "step"

    store_input_control(
        sim_dtree, args.data_dir, 5,
        xla_compile=False,
    )

    qml_classifier.resources = "alpha"

    # Non-optimized strategy
    # ---------------------------------------------

    # Fixed value for the beamsplitter reflectivity
    # in the non optimized strategy

    if arch=="serial":
        array_theta = nparray(
            [[1/n] for n in \
            range(3*args.num_ref+1, 1, -1)],
        )
        array_phi = nparray(
            [[0], ]*(3*args.num_ref),
        )
        initial_state = npconcat(
            [array_theta, array_phi],
            axis=1,
        )
    else:
        tmp_array_theta = nparray(
            [[1/n, 1/n, 1/n] for n in \
            range(args.num_ref+1, 1, -1)],
        )
        array_theta = nparray(
            [[item] for sublist in \
                tmp_array_theta for item in sublist]
        )
        array_phi = nparray(
            [[0], ]*3*args.num_ref,
        )
        initial_state = npconcat(
            [array_theta, array_phi],
            axis=1,
        )
    
    nonoptimal_variables = Variable(
        initial_state, dtype=args.prec,
        )

    simpars = SimulationParameters(
        sim_name="dolinar3serial_nonoptimal" \
            if arch=="serial" else \
            "dolinar3parallel_nonoptimal",
        num_steps=max_steps,
        max_resources=max_res,
        prec=args.prec,
    )

    def qmlc_control_strategy_nonoptimal(input_tensor):
        nonoptimal_control = gather(
            params=2*pi*nonoptimal_variables,
            indices=cast(
                tfround(max_steps*((\
            input_tensor[:, -2]+1)/2)), dtype="int32",
            ),
        )
        return floormod(nonoptimal_control, 2*pi)

    sim_nonoptimal = QMLSimulation(
        particle_filter=particle_filter,
        simpars=simpars,
        phys_model=qml_classifier,
        control_strategy=\
            qmlc_control_strategy_nonoptimal,
        loss=loss,
    )

    performance_evaluation(
        sim_nonoptimal,
        args.iterations, args.data_dir,
        xla_compile=False,
        delta_resources=1.0,
        y_label='ProbError',
    )
    
    qml_classifier.resources = "step"

    store_input_control(
        sim_nonoptimal, args.data_dir, 5,
        xla_compile=False,
    )

    qml_classifier.resources = "alpha"


def main():
    r"""We have trained the quantum Machine Learning
    classifier for both the parallel and the static
    architecture, for both losses, and two values
    of `alpha_bound`, i.e. :math:`\alpha=0.75` and
    :math:`\alpha=1.00`. We have
    observed the superiority of the serial architecture
    and of `loss=1` in all the experiments carried out,
    and accordingly we report in the following
    only the performances of
    those simulations. All the estimations
    have been performed for `num_ref=4`.
    The resources are the mean number of photons
    in the apparatus, as described in the documentation
    of the :py:meth:`~.DolinarThree.count_resources`
    method.

    We studied the performances of the discrimination
    device in the quantum regime, i.e. with a small
    number of photons, since for :math:`\alpha \gg 1`
    the coherent states are perfectly distinguishable.
    With :math:`\alpha=0.75` the signal
    contains on average 0.5 photons, we should therefore
    expect relatively high discrimination errors
    even with optimal strategies.
    Nevertheless the point of the optimization is
    to extract every last bit of information from
    the device, even in a regime where the errors
    are relatively frequent.

    This example is to be taken as less applicative
    then the others, instead, as a proof of principle
    of the potentials of the `qsensoropt` library.

    The performances of the neural network and the
    decision tree are
    compared to that of the static strategy and to the
    pretty good measurement (PGM). This last
    cannot be realized with linear optics and
    photon counting and assumes a perfect a
    priori knowledge of the training states
    :math:`|\alpha_0\rangle`, 
    :math:`|\alpha_1\rangle`, and
    :math:`|\alpha_2\rangle`. To make a more
    fair comparison we assumed the PGM
    consumes `2 num_ref` training states
    where the agnostic Dolinar consumes only `num_ref`.
    The extra copies are intended to be used
    to estimate the training states in order
    to later perform
    the corresponding PGM. Still the PGM
    error probability is not expected
    to be achievable.

    The decision tree computes the next
    control based on the whole string of outcomes
    of the previous measurements.
    Given :math:`\bar{n} = \lfloor \alpha^2 \rceil`,
    the outcome :math:`n` of each measurement
    is classified into one of the three branches
    of the tree according to the conditions
    :math:`n \le \bar{n}-1`, :math:`n = \bar{n}`,
    and :math:`n \ge \bar{n}+1`. The infinite
    possibilities for the outcomes (the number
    of observed photons) gets reduced to only three
    classes without too much loss of information.

    .. list-table::

        * - .. figure:: ../examples/qml_classifier/images/
                          dolinar3serial_batchsize_1024_
                          num_steps_13_max_resources_14.62_ll_
                          False_cl_False_loss_1/
                          plot_AvgPhotonNum_ProbError.png

                alpha_bound=0.75, loss=1

          - .. figure:: ../examples/qml_classifier/images/
                          dolinar3serial_batchsize_1024_
                          num_steps_13_max_resources_26.00_ll_
                          False_cl_False_loss_1/
                          plot_AvgPhotonNum_ProbError.png

                alpha_bound=1.00, loss=1

    The non-optimized strategy refers to a device where
    the phase imprinted by the beam-splitters are all
    zero and the reflectivity is chosen, so that
    the same fraction of the signal reaches each one
    of the photon counter.

    There is an "adaptivity-gap" between the
    performances of the static controls and the
    two adaptive strategies (NN and decision tree).
    This gap starts from zero
    and grows with the average number of photons.
    This make sense, since with very few photons
    we don't expect the adaptive measurements to
    be better than the static one, since almost
    always the measurement outcomes of the
    photon counters will be zero, which doesn't
    give any information about the training states.
    On the other hand with many photons there is
    more space for learning. This can be also
    understood considering the number of
    possible trajectories
    of the particle filter ensemble during
    the estimation, which is one for :math:`\alpha_i = 0`,
    and grows with the number of photons.
    More possible trajectories means
    having different controls on each
    one of them in order to improve the precision,
    which is by definition adaptivity.

    In our experiments we observed that the
    convergence of the NN to the optimal strategy
    is slow and doesn't always happen (see
    the case `alpha_bound=0.75` in the figures),
    while the decision tree is shown to be a
    superior control for this device. In general,
    in a problem with many parameters and a relatively
    small space of possible outcome trajectories, the
    decision three is superior to the
    neural network. On the other hand with few
    parameters and a large space of outcome trajectories
    (like in the examples on NV centers) the
    decision three is unapplicable in the
    form we presented here and the NN is superior.

    In the figure on the left the first
    nodes of the decision tree for `alpha_bound=0.75`
    are shown. The controls from the decision tree
    have the advantage of being faster to compute with
    respect to those of the NN, but storing
    the tree requires more memory. A future work could
    be to trim the tree by keeping only the paths
    that correspond to the most probable trajectories
    (see the figure on the right).

    .. list-table::

        * - .. image:: ../docs/_static/tree.png
            
            alpha_bound=0.75, decision tree

          - .. image:: ../docs/_static/tree2.png
            
            trimmed decision tree

    In the following figure five trajectories
    for the neural network
    controls :math:`\theta` and :math:`\phi`
    are showed.
    There is a tendency for the control trajectories
    to diverge in time (this can be seen well in
    the plot for :math:`\theta`),
    since having already done some
    measurements means that the controls can be tailored
    to the particular instance of the task.
    This behaviour is trained in the
    neural network but is hard coded
    in the decision tree strategy.

    .. list-table::

        * - .. figure:: ../examples/qml_classifier/images/
                          dolinar3serial_batchsize_1024_num_steps_
                          13_max_resources_26.00_ll_False_
                          cl_False_loss_1/plot_MeasStep_Theta.png

                alpha_bound=1.00, loss=1

          - .. figure:: ../examples/qml_classifier/images/
                          dolinar3serial_batchsize_1024_num_steps_
                          13_max_resources_26.00_ll_False_
                          cl_False_loss_1/plot_MeasStep_Phi.png

                alpha_bound=1.00, loss=1
         
    The shaded grey areas in the above plot indicate
    the performances of the pretty good measurement,
    computed for multiple copies of the encoded states.
    This is not the ultimate precision bound regarding
    this discrimination problems, but it is a reasonable
    reference value not achievable with linear optics.
    
    The fact the the training is
    able to find and exploit such small
    gain from the adaptivity
    speeks for the efficiency and power
    of the method.
    
    Notes
    -----
    For a large number of resources the error
    probability curves tend to saturate. This is
    because even with infinite `num_ref` and therefore
    perfect knowledge of the training states a single
    copy of the signal can't be classified unambiguously.

    For the estimation of seven parameter
    512 particles in the ensamble are too few. Using
    1024 particles improves the performances
    a bit, but not that much.

    We mentioned that `loss=1` always
    outperforms `loss=0`. This is because
    with `loss=0` we assume that the error
    probability of the apparatus is the one estimated
    by the particle filter. In this way, however, the
    error probability is overeatimated.

    In this example we are estimating multiple
    quantum incompatible parameters, that are the
    `x` and `p` components of the training states
    and the signal, whose corresponding generators
    don't commute.

    **Known bugs**: the training on the GPU freezes
    if the parameter `alpha_bound` is set to be
    too large. This is probably due to a bug
    in the implementation of the function
    `random.poisson`. A preliminary work-around
    has shown that reimplementing the extraction
    from a Poissonian distribution with
    `random.categorical` would solve the problem.

    All the trainings of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB
    or on a GPU NVIDIA GeForce RTX-4090-24GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.
    """
    args = parse_args()
    
    simulation_qmlclassifier(
        args, arch="serial", alpha_bound=0.75, loss=1,
        )
    
    simulation_qmlclassifier(
        args, arch="parallel", alpha_bound=0.75, loss=1,
        )

    simulation_qmlclassifier(
        args, arch="serial", alpha_bound=1.00, loss=1,
        )
    
    simulation_qmlclassifier(
       args, arch="parallel", alpha_bound=1.00, loss=1,
      )
    
    # simulation_qmlclassifier(
    #    args, arch="serial", alpha_bound=1.73, loss=1,
    #    )
    
    # simulation_qmlclassifier(
    #    args, arch="parallel", alpha_bound=1.73, loss=1,
    #   )
    
    # simulation_qmlclassifier(
    #     args, arch="serial", alpha_bound=1.00, loss=0,
    #     )
    
    # simulation_qmlclassifier(
    #    args, arch="serial", alpha_bound=1.73, loss=0,
    #   )

    # simulation_qmlclassifier(
    #    args, arch="parallel", alpha_bound=1.00, loss=0,
    #   )
    
    # simulation_qmlclassifier(
    #    args, arch="parallel", alpha_bound=1.73, loss=0,
    #   )
    
if __name__ == "__main__":
    main()
