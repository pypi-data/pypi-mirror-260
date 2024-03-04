#!/usr/bin/env python3
from typing import Callable, List, Tuple, Optional
from qsensoropt.parameter import Parameter
from qsensoropt.physical_model import Control

from tensorflow import cast, ones, \
    gather, concat, reshape, expand_dims, \
        broadcast_to, where, zeros, ones, \
            constant, Variable, Tensor
from tensorflow.math import exp, equal, \
    floormod, round, reduce_max
from tensorflow.linalg import expm, matvec
from tensorflow.random import Generator, \
    stateless_uniform
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import \
    get_memory_info
from numpy import zeros as npzeros
from numpy import savetxt
from numpy.random import rand
from argparse import ArgumentParser
from math import pi
from os.path import join

from qsensoropt import InverseSqrtDecay, \
    ParticleFilter, Parameter, Control, \
        SimulationParameters, StatelessPhysicalModel, \
        StatelessMetrology

from qsensoropt.utils import train, \
    performance_evaluation, store_input_control, \
    standard_model, get_seed, denormalize

from qml_classifier import CoherentStates

from cmath import exp as cmexp
from cmath import pi as cmpi

class PhotonicCircuit(CoherentStates):
    """Programmable multimode
    photonic circuit. Non-linear elements (other
    than photon counting) can't be implemented.
    No homodyne measurement is available.
    """
    def __init__(
        self, batchsize: int,
        num_wires: int,
        prec: str = "float64",
    ):
        """Constructor
        of the :py:obj:`~.PhotonicCircuit` class.

        Parameters
        ----------
        batchsize: int
            Number of simultaneous simulations of
            the circuit.
        num_wires: int
            Number of bosonic lines in the circuit.
        prec: {"float64", "float32"}
            Floating point precision of the simulation.
        """
        self.num_wires = num_wires
        self.prec = prec
        self.type_complex = "complex128" if \
            self.prec=="float64" else "complex64"
        
        CoherentStates.__init__(
            self, batchsize=batchsize,
            prec=prec,
        )

    def phase_shift_line(
            self, state: Tensor,
            phase: Tensor, i: int,
        ) -> Tensor:
        """Controllable phase shift on the `i`-th
        bosonic mode.

        The symbol ? in the shape of a `Tensor`
        means that this dimension can have arbitrary
        size unknown to this method.

        Parameters
        ----------
        state: Tensor
            `Tensor` of shape (`bs`, ?, `2 num_wires`)
            of type `prec` containing the real
            components of the state of the `num_wires`
            bosonic modes. The `x`-components are
            the entries from 0 to `num_wires-1`,
            and the `p`-components the entries from
            `num_wires` to `2 num_wires-1`.
        phase: Tensor
            `Tensor` of shape (`bs`, ?) and type `prec`
            containing the phase shift to be applied to
            the `i`-th bosonic mode.
        i: int
            Index of the bosonic mode to be phase
            shifted. The counting starts from zero.

        Returns
        -------
        state: Tensor
            `Tensor` of shape (`bs`, ?, `2 num_wires`)
            of type `prec` containing the evolved state
            of the photonic circuit.
        """
        part_0 = state[:, :, :i]
        comp_x = state[:, :, i:(i+1)]
        part_1 = state[:, :, (i+1):(i+self.num_wires)]
        comp_y = state[:, :, (self.num_wires+i):\
                       (self.num_wires+i+1)]
        part_2 = state[:, :, (self.num_wires+i+1):]
        evolved_line = self.phase_shift(
            concat([comp_x, comp_y], 2), phase,
        )
        return concat(
            [part_0, evolved_line[:, :, 0:1], part_1,
             evolved_line[:, :, 1:2], part_2], 2,
        )
    
    def beamsplitter_line(
            self, state: Tensor,
            theta: Tensor, phi: Tensor, i: int,
        ) -> Tensor:
        r"""Controllable beamsplitter between two
        consecutive lines.

        The symbol ? in the shape of a `Tensor`
        means that this dimension can have arbitrary
        size unknown to this method.

        Parameters
        ----------
        state: Tensor
            `Tensor` of shape (`bs`, ?, `2 num_wires`)
            of type `prec` containing the real
            components of the state of the `num_wires`
            bosonic modes. The `x`-components are
            the entries from 0 to `num_wires-1`,
            and the `p`-components the entries from
            `num_wires` to `2 num_wires-1`.
        theta: Tensor
            `Tensor` of shape (`bs`, ?)
            and of type `prec`. It contains the
            transmission coefficient of the BS.
            It is indicated with :math:`\theta`.
        phi: 
            `Tensor` of shape (`bs`, ?)
            and of type `prec`. It contains the phase
            applied by the BS. It is indicated with
            :math:`\phi`.
        i: int
            The BS is applied between the `i`-th
            and the `i+1`-th line. The counting starts
            from zero.

        Returns
        -------
        state: Tensor
            `Tensor` of shape (`bs`, ?, `2 num_wires`)
            of type `prec` containing the evolved state
            of the photonic circuit after the application
            of the beamsplitter.
        """
        part_0 = state[:, :, :i]
        comp_x_1 = state[:, :, i:(i+1)]
        comp_x_2 = state[:, :, (i+1):(i+2)]
        part_1 = state[:, :, (i+2):(i+self.num_wires)]
        comp_y_1 = state[:, :, (self.num_wires+i):\
                         (self.num_wires+i+1)]
        comp_y_2 = state[:, :, (self.num_wires+i):\
                         (self.num_wires+i+2)]
        part_2 = state[:, :, (self.num_wires+i+2):]
        first_input = concat([comp_x_1, comp_y_1], 2)
        second_input = concat([comp_x_2, comp_y_2], 2)
        output1, output2 = self.beamsplitter(
            first_input, second_input, theta, phi,
        )
        return concat([part_0, output1[:, :, 0:1],
                       output2[:, :, 0:1],
                       part_1, output1[:, :, 1:2],
                       output2[:, :, 1:2],
                       part_2], 2)

    def balanced_beamsplitter_line(
        self, state: Tensor, i: int,
        num_systems: int,
        ) -> Tensor:
        r"""Applies a balanced beamsplitter without
        phase shift between two consecutive
        bosonic lines.

        Parameters
        ----------
        state: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, `2 num_wires`)
            of type `prec` containing the real
            components of the state of the `num_wires`
            bosonic modes. The `x`-components are
            the entries from 0 to `num_wires-1`,
            and the `p`-components the entries from
            `num_wires` to `2 num_wires-1`.
        i: int
            The balanced BS is applied between the `i`-th
            and the `i+1`-th line. The counting starts
            from zero.
        num_systems: int
            Size of the second dimension of
            `state`. It is the number of circuits
            simulated for each element of the
            batch, i.e. for each estimation.

        Returns
        -------
        state: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, `2 num_wires`)
            of type `prec` containing the evolved state
            of the photonic circuit after the application
            of the beamsplitter.
        """
        theta = pi/4*ones(
            (self.bs, num_systems), dtype=self.prec,
            )
        phi = zeros(
            (self.bs, num_systems), dtype=self.prec,
            )
        return self.beamsplitter_line(
            state, theta, phi, i,
            )
    
    def total_mean_phot(
            self, state: Tensor, num_systems: int,
            ) -> Tensor:
        r"""Computes the total mean photon number in
        the photonic circuit.

        Given a list of states
        :math:`\lbrace \alpha_i \rbrace_{i=0}^{n-1}`
        for the :math:`n` bosonic line,
        this method returns

        .. math::
            N = \sum_{i=0}^{n-1} |\alpha_i|^2 \; .

        Parameters
        ----------
        state: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, `2 num_wires`)
            of type `prec` containing the real
            components of the state of the `num_wires`
            bosonic modes. The `x`-components are
            the entries from 0 to `num_wires-1`,
            and the `p`-components the entries from
            `num_wires` to `2 num_wires-1`.
        num_systems: int
            Size of the second dimension of
            `state`. It is the number of circuits
            simulated for each element of the
            batch, i.e. for each estimation.
        
        Returns
        -------
        Tensor:
            Mean number of photons present
            in the entire circuit. It is
            a `Tensor` of shape (`bs`, `num_systems`)
            and type `prec`.
        """
        partial = zeros(
            (self.bs, num_systems), dtype=self.prec,
            )
        for i in range(self.num_wires):
            partial += state[:, :, i]**2+\
                state[:, :, i+self.num_wires]**2
        return partial
    
    def photon_counting_all(
            self, state: Tensor,
            rangen: Generator,
        ) -> Tuple[Tensor, Tensor]:
        """Performs the photon counting
        on each line of the circuit individually.
        
        Parameters
        ----------
        state: Tensor
            `Tensor` of shape
            (`bs`, 1, `2 num_wires`)
            of type `prec` containing the real
            components of the state of the `num_wires`
            bosonic modes. The `x`-components are
            the entries from 0 to `num_wires-1`,
            and the `p`-components the entries from
            `num_wires` to `2 num_wires-1`.
        rangen: Generator
            Random number generator from the module
            :py:mod:`tensorflow.random`.

        Returns
        -------
        outcomes: Tensor
            Number of photons observed on
            each line. It is a `Tensor` of
            shape (`bs`, 1, `num_wires`)
            and type `prec`. 
        log_prob: Tensor
            Log-likelihood of getting the
            observed outcomes upon the measurement.
            It is a `Tensor` of shape
            (`bs`, 1) and type `prec`.
        """
        out_list = zeros(
            (self.bs, 1, 0), dtype=self.prec,
            )
        log_prob_tot = zeros(
            (self.bs, 1), dtype=self.prec,
            )
        for i in range(self.num_wires):
            channel = concat([state[:, :, i:(i+1)],
                    state[:, :, (i+self.num_wires):\
                                 (i+self.num_wires+1)]],
                    2, )
            partial_outcomes, partial_log_prob = \
                self.photon_counter(channel, rangen,
            )
            out_list = concat(
                [out_list, partial_outcomes], 2,
                )
            log_prob_tot += partial_log_prob
        return out_list, log_prob_tot
    
    def postselect_photon_counting_all(
            self, state: Tensor, outcomes: Tensor,
            num_systems: int = 1,
        ) -> Tensor:
        """Postselection of the photon counting
        result on each line of the photonic circuit.
        
        Parameters
        ----------
        state: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, `2 num_wires`)
            of type `prec` containing the real
            components of the state of the `num_wires`
            bosonic modes. The `x`-components are
            the entries from 0 to `num_wires-1`,
            and the `p`-components the entries from
            `num_wires` to `2 num_wires-1`.
        outcomes: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, `num_wires`)
            and type `prec` containing the
            number of photons in each line
            to condition on.
        num_systems: int
            Size of the second dimension of
            `state`. It is the number of circuits
            simulated for each element of the
            batch, i.e. for each estimation.

        Returns
        -------
        log_prob: Tensor
            Log-likelihood of getting
            `outcomes` as result upon the
            photon counting measurements.
            It is a `Tensor` of shape
            (`bs`, `num_systems`) and type `prec`.
        """
        log_prob_tot = zeros(
            (self.bs, num_systems), dtype=self.prec,
            )
        for i in range(self.num_wires):
            channel = concat([state[:, :, i:(i+1)], \
                    state[:, :, (i+self.num_wires):\
                                 (i+self.num_wires+1)]], 2,)
            partial_log_prob = \
                self.postselect_photon_counter(
                channel, outcomes[:, :, i:(i+1)],
            )
            log_prob_tot += partial_log_prob
        return log_prob_tot


class FourModesCircuit(
    StatelessPhysicalModel, PhotonicCircuit,
    ):
    r"""Four modes interferometer
    for the simultaneous estimation of
    three phases [8]_.

    The interferometer has two balanced
    quarter as opening and closing elements,
    which are the generalization of the
    balanced beam splitter for four modes
    in input and four modes in output. The three
    unknown phases are called
    :math:`\varphi_0, \varphi_1, \varphi_2`, while the
    control phases are :math:`c_0, c_1, c_2`.
    See also the picture in the documentation
    of the :py:obj:`~.PhotonicCircuitSimulation`
    class.

    .. [8] https://arxiv.org/abs/2209.00671.
    """
    def __init__(
            self, batchsize: int,
            params: List[Parameter],
            prec: str = "float64",
            single_control: bool = False,
            num_photons: int = 1,
            ):
        r"""Constructor of the
        :py:obj:`FourModesCircuit` class.

        Parameters
        ----------
        batchsize: int
            Number of simultaneous estimations
            of the phases.
        params: List[:py:obj:`~.Parameter`]
            List of parameters to be estimated, passed
            to the class constructor. These must be
            the three unknown phases in the interferometer,
            with their respective priors.
        prec: str = {"float64", "float32"}
            Floating point precision of the
            simulation.
        single_control: bool = False
            If this flag is active, then the three
            control phases in the interferometer,
            i.e. :math:`c_0, c_1, c_2`, are all equal
            to a single control phase :math:`c` to
            be optimized, i.e.
            :math:`c_0=c_1=c_2=c`.
        num_photons: {1, 2, 3, 4}
            Mean number of photons in the
            input state to the interferometer,
            which is always a collection of
            coherent states
            :math:`|\alpha_0 \alpha_1 \alpha_2 \alpha_3\rangle`.
            This parameter can take integer values
            from 1 to 4 (extrema included), and the
            corresponding input states are
            
            * `num_photons=1`: :math:`\alpha_0=1`,
              :math:`\alpha_1=\alpha_2=\alpha_3=0`,
            * `num_photons=2`:
              :math:`\alpha_0=\alpha_1=1`,
              :math:`\alpha_2=\alpha_3=0`,
            * `num_photons=3`:
              :math:`\alpha_0=\alpha_1=\alpha_2=1`,
              :math:`\alpha_3=0`,
            * `num_photons=4`:
              :math:`\alpha_0=\alpha_1=\alpha_2=\alpha_3=1`.

            An average of one photon at most enters
            each line of the circuit.
            
            **Achtung!**: The input states are not
            Fock states.
        """
        self.single_control = single_control
        self.num_photons = num_photons
        
        PhotonicCircuit.__init__(
                self, batchsize=batchsize,
                num_wires=4,
                prec=prec,
            )

        if self.single_control:
            controls = [
                Control(name="c0"),
            ]
        else:
            controls = [
                Control(name="c0"),
                Control(name="c1"),
                Control(name="c2"),
            ]
            
        StatelessPhysicalModel.__init__(
            self, batchsize, controls, params,
            outcomes_size=self.num_wires, prec=prec,
            )

        self.unitary = 0.5*broadcast_to(reshape(constant(
            [[1.0+0.0j, 0.0+1.0j, 0.0+1.0j, -1.0+0.0j],
             [0.0+1.0j, -1.0+0.0j, 1.0+0.0j, 0.0+1.0j],
             [0.0+1.0j, 1.0+0.0j, -1.0+0.0j, 0.0+1.0j],
             [-1.0+0.0j, 0.0+1.0j, 0.0+1.0j, 1.0+0.0j]],
             dtype=self.type_complex,
        ), (1, 1, 4, 4)), (self.bs, 1, 4, 4))

    def _interferometer(
        self, controls: Tensor, parameters: Tensor,
        num_systems: int = 1,
        ):
        initial_x = [1.0 for _ in range(self.num_photons)]+\
            [0.0 for _ in \
             range(self.num_wires-self.num_photons)]
        # One photon average enters each line
        # of the photonic circuit
        state_x = broadcast_to(reshape(
            constant(initial_x,
                     dtype=self.prec),
            (1, 1, self.num_wires)),
            (self.bs, num_systems, self.num_wires),
            )
        state_y = zeros(
            (self.bs, num_systems, self.num_wires),
            dtype=self.prec,
            )
        state = concat([state_x, state_y], 2)
        # First quarter
        state = self.apply_bs_network_from_unitary(
            broadcast_to(self.unitary,
                         (self.bs, num_systems, 4, 4)),
            state,
        )
        if self.single_control:
            c0, c1, c2 = controls[:, :, 0], \
                controls[:, :, 0], controls[:, :, 0]
        else:
            c0, c1, c2 = controls[:, :, 0], \
                controls[:, :, 1], controls[:, :, 2]
        state = self.phase_shift_line(
            state, parameters[:, :, 0]+c0, 0,
        )
        state = self.phase_shift_line(
            state, parameters[:, :, 1]+c1, 1,
        )
        state = self.phase_shift_line(
            state, parameters[:, :, 2]+c2, 2,
        )
        # Second quarter
        return self.apply_bs_network_from_unitary(
            broadcast_to(self.unitary,
                         (self.bs, num_systems, 4, 4)),
            state,
        )
    
    def perform_measurement(
            self, controls: Tensor, parameters: Tensor,
            meas_step: Tensor, rangen: Generator,
            ) -> Tuple[Tensor, Tensor]:
        r"""The input state of the four
        bosonic modes is fed to the
        circuit and a photon counting measurement
        is performed on each output lines after the
        closing quarter.

        Parameters
        ----------
        controls: Tensor
            If `single_control=False` this
            is a `Tensor` of shape (`bs`, 1, 3) and
            of type `prec` containing the three
            control phases, while if
            `single_control=True` this `Tensor`
            has shape (`bs`, 1, 1) and contains the
            single control phase.
        parameters: Tensor
            `Tensor` of shape (`bs`, 1, 3) and type
            `prec` containing the true values of the three
            phases to be estimated
            :math:`\varphi_0, \varphi_1, \varphi_2`.
        meas_step: Tensor
            `Tensor` of shape (`bs`, 1, 1) and type `prec`.
            It is the index of the current execution of the
            interferometer and starts from zero.
            We call a single circuit execution, i.e.
            sending the input and measuring the outcome, 
            a step.
        rangen: Generator
            Random number generator from the module
            :py:mod:`tensorflow.random`.

        Returns
        -------
        outcomes: Tensor
            `Tensor` of shape (`bs`, 1, 4)
            and type
            `prec` containing the number of photons
            observed in the photon counting measurement
            on each of the four lines.
        log_prob: Tensor
            `Tensor` of shape (`bs`, 1) and type
            `prec` containing the logarithm of the
            probability of getting the observed
            number of photons.
        """
        state = self._interferometer(
            controls, parameters, 1,
        )
        # Photon counting measurements
        return self.photon_counting_all(
            state, rangen,
            )
    
    def model(
            self, outcomes: Tensor, controls: Tensor,
            parameters: Tensor, meas_step: Tensor,
            num_systems: int = 1,
            ) -> Tensor:
        r"""Returns the log-likelihood of getting
        a particular outcome for the photon
        counting measurements on each mode of the
        interferometer after the closing quarter.

        Parameters
        ----------
        outcomes: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 4)
            and type `prec` containing
            the number of photons to condition on
            for each of the four lines.
        controls: Tensor
            If `single_control=False` this
            is a `Tensor` of shape
            (`bs`, `num_systems`, 3) and
            of type `prec` containing the three
            control phases, while if
            `single_control=True` this `Tensor`
            has shape (`bs`, `num_systems`, 1)
            and contains the single control phase.
        parameters: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 3) and type
            `prec` containing the ensemble particles
            for the three unknown phases.
        meas_step: Tensor
            `Tensor` of shape
            (`bs`, `num_systems`, 1) and type `prec`.
            It is the index of the current execution of the
            interferometer and starts from zero.
            We call a single circuit execution, i.e.
            sending the input and measuring the outcome, 
            a step.
        num_systems: int = 1
            Number of circuits simulated for
            each batch element.
            
        Returns
        -------
        prob: Tensor
            `Tensor` of shape (`bs`, `num_systems`)
            and type `prec` containing the
            probability of getting `outcomes` as a results
            upon the execution of the
            photon counting measurement.
        """
        state = self._interferometer(
            controls, parameters, num_systems,
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
        """Each execution of the photonic circuit
        is counted as a consumed resource, and it
        is called a step.
        """
        return resources+1.0
    
class PhotonicCircuitSimulation(StatelessMetrology):
    r"""Simulation for the
    :py:obj:`~.FourModesCircuit` class.

    **Achtung!** This :py:obj:`~.Simulation`
    class is implemented for unknown
    phases that are defined as
    discrete parameters,
    that is, that can take values only
    in a finite set. For this reason
    the task solved here is hypothesis testing.

    .. image:: ../docs/_static/photonic_circuit.png
        :width: 700
        :alt: photonic_circuit

    Given the number of possible values
    :math:`l_0, l_1, l_2` that each phase
    can assume, i.e. the length of the
    `values` attributes of their respective
    :py:obj:`~.Parameter` objects,
    the total number of hypothesis to
    discriminate is
    :math:`n_h = l_0 l_1 l_2`. The particle
    filter contains one and only one particle for
    each hypothesis along with their
    corresponding weights
    :math:`\lbrace w_{j} \rbrace_{j=0}^{n_h-1}`,
    that are updated with the Bayes rule
    after each step.

    The posterior distribution
    on the hypothesis is the input to the
    control strategy. The loss function
    :py:meth:`~.PhotonicCircuitSimulation.loss_function`
    simply returns the probability
    of guessing the wrong hypothesis after
    all the measurements.
    """
    def __init__(
            self, particle_filter: ParticleFilter,
            phys_model: FourModesCircuit,
            control_strategy: Callable,
            simpars: SimulationParameters,
            random: bool = False,
            ):
        r"""Constructor
        of the :py:obj:`~.PhotonicCircuitSimulation`
        class.

        Parameters
        ----------
        particle_filter: :py:obj:`~.ParticleFilter`
            Particle filter responsible for the update
            of the Bayesian posterior on the
            hypothesis.
        phys_model: :py:obj:`~.FourModesCircuit`
            Abstract description of the balanced
            four mode interferometer.
        control_strategy: Callable
            Callable object (normally a
            function or a lambda function) that
            computes the values of the
            controls :math:`c_0, c_1, c_2`
            for the next step.
        simpars: :py:obj:`~.SimulationParameters`
            Contains the flags and parameters
            that regulate the stopping
            condition of the measurement loop
            and modify the loss function used in the
            training.
        random: bool = False
            If this flag is `True` a column
            of random numbers extracted uniformly in
            :math:`[0, 2 \pi]` is appended to the
            `input_tensor` generated by 
            :py:meth:`~.PhotonicCircuitSimulation.generate_input`
            for each control in the circuit.
            The number of controls can be either
            three or one according to the flag
            `single_control` of `phys_model`.
        """
        super().__init__(
            particle_filter, phys_model,
            control_strategy,
            simpars,
            )
        
        self.random = random

        self.hyp_num = 1
        for param in self.phys_model.params:
            self.hyp_num *= len(param.values)

        self.input_size = self.hyp_num+2

        self.input_name = []
        for i in range(self.hyp_num):
            self.input_name.append(f"w{i}")
        self.input_name += ["Step", "Res",]

        if self.random:
            if self.phys_model.single_control:
                self.input_size += 1
                self.input_name += ["c0r", ]
            else:
                self.input_size += 3
                self.input_name += ["c0r", "c1r", "c2r"]

    def generate_input(
            self, weights: Tensor, particles: Tensor,
            meas_step: Tensor, used_resources: Tensor,
            rangen: Generator,
            ) -> Tensor:
        r"""Generates the `input_tensor`
        passed to `control_strategy`, on the basis
        which the next controls are predicted.
        
        The `input_tensor` is composed on the
        following columns:

        * `weights`, i.e. the posterior distribution
          on the possible values of the phases. These
          are :math:`n_h` columns,
        * `meas_step` normalized in `[-1, +1`],
        * `used_resources` normalized in `[-1, +1]`.
        * one or three columns of random
          numbers uniformly extracted in
          :math:`[0, 2 \pi)`. This is present only
          if `random=True`.

        The shape of the returned input is
        (`bs`, `input_size`), with `input_size`
        being :math:`n_h+2` if `random=False` or
        :math:`n_h+5` if `random=True` and
        `single_control=False`.
        """
        pars = self.simpars
        old_input = concat(
            [weights, 2*meas_step/pars.num_steps-1,
             2*used_resources/pars.max_resources-1], 1,
            )
        if self.random:
            if self.phys_model.single_control:
                random_controls = 2*pi*stateless_uniform(
                    (self.bs, 1), get_seed(rangen),
                    maxval=1, dtype=pars.prec,
                )
            else:
                random_controls = 2*pi*stateless_uniform(
                    (self.bs, 3), get_seed(rangen),
                    maxval=1, dtype=pars.prec,
                )
            return concat(
                [old_input, random_controls], 1,
                )
        else:
            return old_input

    def loss_function(
            self, weights: Tensor, particles: Tensor,
            true_values: Tensor, used_resources: Tensor,
            meas_step: Tensor
            ) -> Tensor:
        r"""Loss function for the hypothesis testing
        in the four arms interferometer.
        
        On each estimation in the batch
        the loss is zero if the correct phases are
        guessed correctly and one if they are guessed
        wrongly. In symbols, given the delta function

        .. math::
            \delta (x, y) = \begin{cases}
                1 \quad \text{if} \quad x=y \; , \\
                0 \quad \text{if} \quad x \neq y \; ,
            \end{cases}

        the guess based on the Bayesian posterior is

        .. math::
            G \left( \lbrace w_j \rbrace_{j=0}^{n_h}
            \right) = \text{argmax}
            (w_0, w_1, \dots w_{n_h-1}) \; ,

        and calling :math:`s` the index of the
        correct hypothesis for the phases values
        the loss can be expressed as

        .. math::
            \ell \left( \lbrace w_j \rbrace_{j=0}^{n_h}
            , s \right) = 1 - \delta (G, s) \; ,
        
        which, averaged on the batch is the error probability.
        """
        pars = self.simpars
        estimator = expand_dims(self.pf.compute_max_weights(
            weights, particles,
            ), 1, )
        zeros_tensor = zeros(
            (self.bs, 1, 3), dtype=pars.prec,)
        ones_tensor = ones(
            (self.bs, 1, 3), dtype=pars.prec,
            )
        right_guess = where(
            equal(true_values, estimator),
            zeros_tensor, ones_tensor,
        )
        return reduce_max(right_guess, axis=2)
        
def parse_args():
    r"""Arguments
    ---------
    scratch_dir: str
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./photonic_circuit/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./photonic_circuit/data"
        Directory containing the csv files
        produced by the :py:func:`~.utils.performance_evaluation`
        and the :py:func:`~.utils.store_input_control` functions.
    prec: str = "float64"
        Floating point precision of the
        whole simulation.
    batchsize: int = 4096
        Batchsize of the simulation.
    n: int = 64
        Number of neurons per layer in the neural network.
    num_steps: int = 32
        Number of uses of the interferometer, i.e.
        number of measurements in the hypothesis testing.
    iterations: int = 32768
        Number of training steps.
    """
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir", type=str,
                        default="./photonic_circuit/trained_models")
    parser.add_argument("--data-dir", type=str,
                        default="./photonic_circuit/data")
    parser.add_argument("--prec", type=str, default="float64")
    parser.add_argument('--batchsize', type=int, default=4096)
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument("--num-steps", type=int, default=32)
    parser.add_argument("--iterations", type=int, default=32768)

    return parser.parse_args()

def photonic_circuit_estimation(
    args,
    learning_rate: float = 1e-2,
    gradient_accumulation: int = 1,
    cumulative_loss: bool = True,
    phase_values: Tuple = (0, 1),
    single_control: bool = False,
    num_photons: int = 1,
):
    r"""Simultaneous estimation of three phases in
    the four arms interferometer as
    describe by the
    :py:obj:`~.FourModesCircuit` class.

    Each call to this function will perform
    the hypothesis testing on the values of the
    three phases for three strategies, i.e.
    the adaptive one implemented with a NN,
    the static, and the random strategies.

    Parameters
    ----------
    args:
        Arguments passed to the Python script.
    learning_rate: float = 1e-2
        Initial learning rate for the neural network.
        The static strategy has a fixed initial
        learning rate of `1e-1`. Both are reduced
        during the training according
        to :py:obj:`~.InverseSqrtDecay`.
    gradient_accumulation: int = 1
        Flag of the :py:func:`~.utils.train` function.
    cumulative_loss: bool = True
        Flag :py:obj:`~.SimulationParameters.cumulative_loss`.
        Set for all the simulations.
    phase_values: Tuple = (0, 1)
        Contains the possible discrete values
        that each phase :math:`\varphi_i` can assume
        independently.
    single_controls: bool = False
        If the function is called with `single_control=True`,
        then it will evaluate the performances of the
        adaptive, random, and static strategies
        in the scenario
        where the three controllable phases are all
        equal, i.e. :math:`c_0=c_1=c_2=c`,
        and there is therefore only a single
        scalar control :math:`c`. This flag is
        used in the initialization of the
        :py:obj:`~.FourModesCircuit` object.
    num_photons: int = 1
        Mean number of photons in the input
        state of the interferometer for each
        measurement step. This values is
        used in the initialization of the
        :py:obj:`~.FourModesCircuit` object.
    """
    control_size = 1 if single_control else 3
    
    num_hyp = len(phase_values)
    input_size = num_hyp**3+2

    single_name = "_s" if single_control else ""

    network = standard_model(
        input_size=input_size,
        controls_size=control_size,
        neurons_per_layer=args.n,
        prec=args.prec,
    )
    network.compile()
    
    four_interferometer = FourModesCircuit(
        batchsize=args.batchsize,
        params=[
            Parameter(values=phase_values,
                      name="phi0", randomize=False),
            Parameter(values=phase_values,
                      name="phi1", randomize=False),
            Parameter(values=phase_values,
                      name="phi2", randomize=False),
        ],
        single_control=single_control,
        num_photons=num_photons,
        prec=args.prec,
    )
 
    particle_filter = ParticleFilter(
        num_particles=num_hyp**3,
        phys_model=four_interferometer,
        resampling_allowed=False,
        prec=args.prec,
    )

    # NN strategy - training
    # ----------------------------------------------

    simpars_nn = SimulationParameters(
        sim_name="photonic_circuit"+\
            single_name+f"_{num_photons}",
        num_steps=args.num_steps,
        max_resources=args.num_steps,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
    )

    sim_nn = PhotonicCircuitSimulation(
        particle_filter=particle_filter,
        simpars=simpars_nn,
        phys_model=four_interferometer,
        control_strategy=lambda x: 2*pi*network(x),
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

    simpars_random = SimulationParameters(
        sim_name="photonic_circuit_random"+\
            single_name+f"_{num_photons}",
        num_steps=args.num_steps,
        max_resources=args.num_steps,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
    )

    sim_random = PhotonicCircuitSimulation(
        particle_filter=particle_filter,
        simpars=simpars_random,
        phys_model=four_interferometer,
        control_strategy=lambda x: x[:, -control_size:],
        random=True,
    )
    
    performance_evaluation(
       sim_nn, args.iterations, args.data_dir,
       delta_resources=1.0,
       y_label='ProbErr',
       xla_compile=False
    )

    store_input_control(
       sim_nn, args.data_dir, 5,
       xla_compile=False
    )

    performance_evaluation(
       sim_random, args.iterations, args.data_dir,
       delta_resources=1.0,
       y_label='ProbErr',
       xla_compile=False
    )

    store_input_control(
       sim_random, args.data_dir, 5,
       xla_compile=False
    )

    print("Memory:")
    print(get_memory_info('GPU:0')['peak']/1024**3)

    # Static simulation
    #-------------------------------------------------

    # Initial value of the controls
    # in the static optimization
    initial_state = npzeros(
        (int(args.num_steps), control_size),
        )
    for i in range(int(args.num_steps)):
        initial_state[i, :] = rand()
        
    static_variables = Variable(
        initial_state, dtype=args.prec,
        )

    def static_control(input_tensor: Tensor):
        return gather(
                params=2*pi*static_variables,
                indices=cast(
            round(denormalize(
            input_tensor[:, -2], (0, args.num_steps))),
            dtype="int32"),
            )
    
    simpars_static = SimulationParameters(
        sim_name="photonic_circuit_static"+\
            single_name+f"_{num_photons}",
        num_steps=args.num_steps,
        max_resources=args.num_steps,
        prec=args.prec,
        cumulative_loss=cumulative_loss,
    )
    
    sim_static = PhotonicCircuitSimulation(
        particle_filter=particle_filter,
        simpars=simpars_static,
        phys_model=four_interferometer,
        control_strategy=static_control,
    )

    decaying_learning_rate = InverseSqrtDecay(
        1e-1, args.prec
    )

    train(
        sim_static,
        Adam(learning_rate=decaying_learning_rate),
        args.iterations, args.scratch_dir,
        custom_controls=static_variables,
        xla_compile=False,
        gradient_accumulation=gradient_accumulation,
    )
    
    savetxt(
        join(args.trained_models_dir, str(sim_static)),
            static_variables.numpy()
            )

    performance_evaluation(
       sim_static, args.iterations, args.data_dir,
       delta_resources=1.0,
       y_label='ProbErr',
       xla_compile=False
    )

    store_input_control(
       sim_static, args.data_dir, 5,
       xla_compile=False
    )

def main():
    r"""In the following we report the evaluated
    error probability in the correct identification
    of three phases in a four arms interferometer
    with various input states.
    Each phase can assume the two values
    :math:`\varphi_i \in \lbrace 0, 1 \rbrace`.
    The three phases
    :math:`c_0, c_1, c_2` can be controlled,
    see the picture in the documentation
    of the :py:obj:`~.PhotonicCircuitSimulation` class,
    and the performances of three control
    strategies have been compared for the
    same input states.

    With this circuit we are testing in parallel
    for each slot whether a phase shift is there
    or not. This phase shift could be due to the
    presence of a certain object, a chemical species,
    or it could be a piece of codified information.

    The following plots represent the
    probability of guessing the
    unknown phases wrong as a function
    of the mean number of photons
    consumed in the estimation and of the number
    of measurements, for the adaptive,
    the static, and the random strategies.

    .. list-table::

        * - .. figure:: ../examples/photonic_circuit/images/
                          photonic_circuit_1_batchsize_4096_num_
                          steps_32_max_resources_32.00_ll_False_
                          cl_True/plot_NumPhotons_ProbErr.png
                :width: 600

                num_photons=1

          - .. figure:: ../examples/photonic_circuit/images/
                          photonic_circuit_2_batchsize_4096_num_
                          steps_32_max_resources_32.00_ll_False_
                          cl_True/plot_NumPhotons_ProbErr.png

                num_photons=2

        * - .. figure:: ../examples/photonic_circuit/images/
                          photonic_circuit_3_batchsize_4096_num_
                          steps_32_max_resources_32.00_ll_False_
                          cl_True/plot_NumPhotons_ProbErr.png

               num_photons=3

          - .. figure:: ../examples/photonic_circuit/images/
                          photonic_circuit_4_batchsize_4096_num_
                          steps_32_max_resources_32.00_ll_False_
                          cl_True/plot_NumPhotons_ProbErr.png

                num_photons=4
        
    The shaded grey areas in the above plot indicate
    the performances of the pretty good measurement,
    computed for multiple copies of the encoded states.
    This is not the ultimate precision bound regarding
    this discrimination problems, but it is a reasonable
    reference value not achievable with linear optics.

    Only for `num_photons=1, 2` the adaptive
    strategy has been proven to give some
    advantage with respect to the static one.
    The state with three photons doesn't perform
    well in comparison to all the other inputs.
    The best input in terms of the consumed
    number of photons to reach a certain
    probability error is the state
    with a single photon on average.
    It is possible that in terms of the
    damage caused to the sample or
    the energy used (which are both
    proportional to the total number of
    photons) performing many measures each
    with a vanishingly small photon number
    is optimal. This hypothesis should be verified
    with more simulations in the range `num_photons<1`.
    If it that is the case, then minimizing the
    energy or the damage would mean stretching
    the total measurement time, which could also
    be unfeasible beyond a certain amount.
    For a fixed number of measurements,
    therefore for a fixed estimation time,
    the states with many photons seem to perform
    better then those with less photons
    (`num_photons=3` being an exception).
    The fact that for different resources
    either the states
    with many of with few photons are optimal
    underlines the importance of clearly identifying
    the resource when discussing metrology.
    Other simulations should be performed
    for the input states
    :math:`|2000\rangle`, :math:`|3000\rangle`
    and :math:`|4000\rangle` to asses their
    usefulness.

    Notes
    -----

    **Known bugs**: the training on the GPU freezes
    if the number of input photons is
    too large. This is probably due to a bug
    in the implementation of the function
    `random.poisson`. A preliminary work-around
    has shown that reimplementing the extraction
    from a Poissonian distribution with
    `random.categorical` would solve the problem.

    All the training of this module
    have been done on a
    GPU NVIDIA Tesla V100-SXM2-32GB,
    each requiring :math:`\mathcal{O}(1)`
    hours.
    """
    # This four arms interferometer has been
    # studied in [8]_, where the there unknown
    # phases could take values in :math:`[0, \pi)`.
    # In this paper the mean square error
    # as well as the median square error
    # for the three phases
    # have been computed and optimized with
    # Reinforcement Learning. We repeated their
    # simulations
    # using the Fock state
    # :math:`|1100\rangle` as input, as they do.
    # The median square error as been computed
    # on a batch of 32 elements. We noticed,
    # that we could come very close to the
    # results of Cimini et. al. by using
    # a random strategy that selects the
    # controls uniformly in :math:`[0, 2 \pi)`.
    # The training of the adaptive strategy
    # implemented with a NN has
    # showed no considerable advantage with respect
    # to the random one.
    # In order to obtain this good
    # performances, it was fundamental to
    # use many particles in the particle
    # filter ensemble.
    # In the following we report the precision
    # of the random strategy, referring to both the mean
    # and the median errors, compared to the
    # Cramér-Rao bound, i.e.
    # :math:`2.5/N`, where `N` is the
    # number of measurements.

    # .. list-table::

    #     * - .. figure:: ../examples/four_interferometer/images/
    #                       four_interferometer_num_part_8192_
    #                       batchsize_32_num_steps_100_max_resources_
    #                       100.00_ll_False_cl_True/plot_NumShot_Error.png
    #             :width: 600

    #             num_particles=8192

    #       - .. figure:: ../examples/four_interferometer/images/
    #                       four_interferometer_num_part_16384_
    #                       batchsize_32_num_steps_100_max_resources_
    #                       100.00_ll_False_cl_True/plot_NumShot_Error.png

    #             num_particles=16384

    args = parse_args()

    photonic_circuit_estimation(
        args, num_photons=1,
    )

    # photonic_circuit_estimation(
    #     args, num_photons=1, single_control=True,
    # )

    photonic_circuit_estimation(
        args, num_photons=2,
    )

    # photonic_circuit_estimation(
    #     args, num_photons=2, single_control=True,
    # )

    photonic_circuit_estimation(
        args, num_photons=3,
    )

    # photonic_circuit_estimation(
    #     args, num_photons=3, single_control=True,
    # )

    photonic_circuit_estimation(
        args, num_photons=4,
    )

    # photonic_circuit_estimation(
    #     args, num_photons=4, single_control=True,
    # )

if __name__ == "__main__":
    main()
        