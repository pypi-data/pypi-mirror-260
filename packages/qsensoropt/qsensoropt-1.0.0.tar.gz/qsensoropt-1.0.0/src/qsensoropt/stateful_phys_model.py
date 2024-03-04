"""Module containing the stateful version
of :py:obj:`~.PhysicalModel`."""

from typing import Tuple
from tensorflow import Tensor
from tensorflow.random import Generator

from .physical_model import PhysicalModel


class StatefulPhysicalModel(PhysicalModel):
    """Abstract description of a stateful
    quantum probe.
    """

    def initialize_state(
            self, parameters: Tensor,
            num_systems: int,
    ) -> Tensor:
        """Initialization of the probe state.

        **Achtung!** This method must be
        implemented by the user.

        Parameters
        ----------
        parameters: Tensor
            `Tensor` of shape (`bs`, `num_systems`, `d`) and
            of type `prec`, where `bs`, `d`, and `prec` are
            attribute of the :py:obj:`~.Simulation` class.
            These are values for the unknown parameters
            associated to each of the probe states that must be
            initialized in this method, be it the "true values"
            used to simulate the measurement outcomes
            or the particles in the particle filter ensemble.
        num_systems: int
            The number of systems to be initialized
            for each simulation in the batch. This is
            the size of the second dimension of the
            `Tensor` that this method should return.

        Returns
        -------
        state: Tensor
            The initialized state of the
            probe and/or some classical variable state.
            This is a `Tensor` of shape
            (`bs`, `num_systems`, `state_specifics["size"]`)
            of type `state_specifics["type"]`, where
            `state_specifics` is an attribute of the
            :py:obj:`~.PhysicalModel` class.
            It may be desirable
            to initialize the state of the probe depending
            on the values of `parameters`, for example because the
            encoding has happened outside of the
            laboratory and we are given the encoded probe
            state only. However, if the encoding happens in the lab
            between the measurements it make sense to
            reset the probe state at the beginning of the
            estimation with a `parameter` independent state.
        """
        raise NotImplementedError("You should override this method!")

    def wrapper_initialize_state(
            self,  parameters: Tensor,
            num_systems: int,
    ):
        return self.initialize_state(
            parameters, num_systems,
        )

    def perform_measurement(
        self, controls: Tensor, parameters: Tensor,
        true_state: Tensor,
        meas_step: Tensor, rangen: Generator,
    ) -> Tuple[Tensor, Tensor, Tensor]:
        r"""Performs the stochastic extraction of measurement
        outcomes and updates the state of the probe.

        **Achtung!** This method must be implemented
        by the user.

        Samples measurement outcomes to simulate the
        experiment and returns them, together with
        the likelihood of obtaining
        such outcomes and the evolved state of the probe
        after the measurement. Typically, this function
        contains at least one call to the :py:meth:`model`
        method, which produces the probabilities for
        the outcome sampling.

        **Achtung!** When using the
        :py:obj:`~.StatefulPhysicalModel` class
        in combination with
        :py:obj:`~.BoundSimulation` the method
        :py:meth:`~.StatefulPhysicalModel.perform_measurement`
        can be implemented to return an outcome
        extracted from an arbitrary probability
        distribution, which can be different from
        the one predicted by the true model
        of the system. This is used to
        introduce an importance sampling on the
        probe trajectories. The `log_prob`
        outcome should be the log-likelihood
        of the outcome according to the modified
        distribution, while `true_state` remains
        the state of the system conditioned on the
        observation of the outcome.
        It is important that
        :py:obj:`~.StatefulPhysicalModel.model`
        implement the true probability.
        This feature should be used together
        with the activation of the flag
        `importance_sampling` in the
        constructor of the
        :py:obj:`~.BoundSimulation` object,
        and should not be used for
        a Bayesian estimation carried out with
        the :py:obj:`~.Simulation` class.

        Parameters
        ----------
        controls: Tensor
            Contains the controls for the current measurement.
            This is a `Tensor` of shape
            (`bs`, 1, `controls_size`) and type `prec`,
            where `bs` and `controls_size` are attributes
            of the :py:obj:`~.PhysicalModel` class.
        parameters: Tensor
            Contains the true values of the unknown
            parameters in the simulations. The observed
            measurement outcomes must be simulated
            according to them. It is a `Tensor` of shape
            (`bs`, 1, `d`) and type `prec`, where `bs` and `d`
            are attributes of the :py:obj:`~.PhysicalModel` class.
            In the estimation, these values are not observable,
            only their effects through the measurement outcomes are.
        true_states: Tensor
            The true state of the probe in the estimation,
            computed from the evolution determined
            (among other factors) by the encoding of
            the parameter `true_values`.
            Like `true_values`, this information is not observable.
            This is a `Tensor` of shape
            (`bs`, 1, `state_specifics["size"]`),
            where `state_specifics` is an attribute of
            the :py:obj:`~.PhysicalModel` class.
            Its type is `state_specifics["type"]`.
        meas_step: Tensor
            The index of the current measurement on the
            probe system. The counting starts from zero.
            This is a `Tensor` of shape (`bs`, 1, 1) and
            of type `int32`.
        rangen: Generator
            A random number generator from the
            module :py:mod:`tensorflow.random`.

        Returns
        -------
        outcomes: Tensor
            The observed outcomes of the measurement.
            This is a `Tensor` of shape
            (`bs`, 1, `outcomes_size`) and of type `prec`.
            `bs`, `outcomes_size`, and `prec` are attributes of
            the :py:obj:`~.PhysicalModel` class.
        log_prob: Tensor
            The logarithm of the probabilities of
            the observed outcomes. This is a `Tensor` of
            shape (`bs`, 1) and of type `prec`.
            `bs` and `prec` are attributes of
            the :py:obj:`~.PhysicalModel` class.
        true_state: Tensor
            The true state of the probe, encoded with
            the parameters `true_values`, after the
            measurement backreaction corresponding
            to `outcomes` is applied. This is a
            `Tensor` of shape (`bs`, 1, `state_specifics["size"]`),
            where `state_specifics` is an attribute of the
            :py:obj:`~.PhysicalModel` class. Its type
            is `state_specifics["type"]`.
        """
        raise NotImplementedError("You should override this method!")

    def wrapper_perform_measurement(
        self, controls: Tensor, parameters: Tensor, true_state: Tensor,
        meas_step: float, rangen: Generator,
    ) -> Tuple[Tensor, Tensor, Tensor]:
        return self.perform_measurement(
            controls, parameters, true_state, meas_step, rangen,
        )

    def model(
        self, outcomes: Tensor, controls: Tensor, parameters: Tensor,
        state: Tensor, meas_step: Tensor, num_systems: int = 1,
    ) -> Tuple[Tensor, Tensor]:
        r"""Description of the encoding and the measurement
        on the probe. This method returns the probability of
        observing a certain outcome and the corresponding
        evolved state after the measurement backreaction.

        **Achtung!** This method must be implemented by the user.

        **Achtung!** This method does not implement any stochastic
        evolution. All stochastic operations in the
        measurement of the probe and in the evolution of the
        state should be defined in the method
        :py:meth:`perform_measurement`.

        Suppose that the state of the probe after the encoding is
        :math:`\rho_{\vec{\theta}, x}`, where :math:`\vec{\theta}`
        is `parameter` and :math:`x` is `control`. The probe state
        will, in general, depend on the entire history of
        past outcomes and controls, but we neglect the
        corresponding subscripts to avoid making the notation
        too cumbersome. The probe measurement is associated with
        an ensemble of positive operators
        :math:`\lbrace M_y^x \rbrace_{y \in Y}`, where
        :math:`y` is the outcome and :math:`Y` is the set of
        possible outcomes. According to the laws of quantum
        mechanics, the probability of observing the outcome
        :math:`y` is then

        .. math::
            P(y|\vec{\theta}, x) := \text{tr} \left( M_y^x
            \rho_{\vec{\theta}, x} \right) \; ,

        and the backreaction on the probe state after
        having observed :math:`y` is

        .. math::
            \rho_{\vec{\theta}, x}' = \frac{M_{y}^{x} \rho_{\vec{\theta}, x}
            M_{y}^{x \dagger}}{\text{tr} \left[ M_{y}^{x}
            \rho_{\vec{\theta}, x} M_{y}^{x \dagger} \right]} \; .

        Parameters
        ----------
        outcomes: Tensor
            Measurement outcomes. It is a `Tensor` of shape
            (`batchsize`, `num_systems`, `outcomes_size`)
            of type `prec`, where `bs` and `outcomes_size` are
            attributes of the :py:obj:`~.PhysicalModel` class.
        controls: Tensor
            Contains the controls for the measurement.
            This is a `Tensor` of shape
            (`bs`, `num_systems`, `controls_size`) and type `prec`,
            where `bs` and `controls_size` are attributes
            of the :py:obj:`~.PhysicalModel` class.
        parameters: Tensor
            Values of the unknown parameters. It is a `Tensor`
            of shape (`bs`, `num_systems`, `d`) and type
            `prec`, where `bs` and `d`
            are attributes of the :py:obj:`~.PhysicalModel` class.
        state: Tensor
            Current state of the quantum probe, computed from
            the evolution determined
            (among other factors) by the encoding of
            `parameters`. This is a `Tensor` of shape
            (`bs`, `num_systems`, `state_specifics["size"]`),
            where `state_specifics` is an attribute of
            the :py:obj:`~.PhysicalModel` class. Its type
            is `state_specifics["type"]`.
        meas_step: Tensors
            The index of the current measurement on the
            probe system. The Counting starts from zero.
            This is a `Tensor` of shape (`bs`, `num_systems`, 1)
            and of type `int32`.

        Returns
        -------
        prob: Tensor
            Probability of observing the given
            vector of outcomes, having done a measurement
            with the given controls, parameters, and states.
            It is a `Tensor` of
            shape (`bs`, `num_systems`) and type `prec`.
            `bs` and `prec` are attributes of
            the :py:obj:`~.PhysicalModel` class.
        state: Tensor
            State of the probe after the encoding
            of `parameters` and the application
            of the measurement backreaction,
            associated with the observation of the
            given outcomes.
            This is a `Tensor` of shape
            (`bs`, `num_systems`, `state_specifics["size"]`),
            where `state_specifics` is an attribute of the
            :py:obj:`~.PhysicalModel` class.
        """
        raise NotImplementedError("You should override this method!")

    def wrapper_model(
        self, outcomes: Tensor, controls: Tensor, parameters: Tensor,
        state: Tensor, meas_step: float, num_systems: int = 1,
    ) -> Tuple[Tensor, Tensor]:
        return self.model(
            outcomes, controls, parameters, state, meas_step,
            num_systems=num_systems,
        )
