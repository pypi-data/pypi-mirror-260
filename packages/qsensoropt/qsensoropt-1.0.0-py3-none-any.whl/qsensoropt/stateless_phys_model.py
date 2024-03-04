"""Module containing the stateless version
of :py:obj:`~.PhysicalModel`."""

from typing import Tuple, List

from tensorflow import Tensor, zeros
from tensorflow.random import Generator

from .physical_model import PhysicalModel, Control, \
    StateSpecifics
from .parameter import Parameter


class StatelessPhysicalModel(PhysicalModel):
    """Abstract description of a stateless
    quantum probe.
    """

    def __init__(
        self, batchsize: int,
        controls: List[Control],
        params: List[Parameter],
        outcomes_size: int = 1,
        prec: str = "float64",
    ):
        r"""Constructor of the
        :py:obj:`~.StatelessPhysicalModel` class.

        Parameters
        ----------
        batchsize: int
            Batch size of the physical model, i.e.,
            the number of simultaneous estimations
            in the simulation.
        controls: List[:py:obj:`~.Control`]
            A list of controls for the probe
            (the buttons and knobs
            of the experiment).
        params: List[:py:obj:`~.Parameter`]
            A list of :py:obj:`~.Parameter` objects
            that represent the unknowns of the estimation.
        outcomes_size: int = 1
            Number of scalars collected in a measurement on
            the probe.
        prec: str = "float64"
            Floating point precision of the controls,
            outcomes, and parameters. Can be either "float32"
            or "float64".
        """
        state_specifics: StateSpecifics = {
            'size': 0,
            'type': prec,
        }
        super().__init__(
            batchsize, controls, params,
            state_specifics,
            recompute_state=False,
            outcomes_size=outcomes_size,
            prec=prec,
        )

    def wrapper_initialize_state(
            self, parameters: Tensor,
            num_systems: int,
    ):
        return zeros(
            (self.bs, num_systems, 0),
            dtype=self.state_specifics['type'],
        )

    def perform_measurement(
        self, controls: Tensor, parameters: Tensor, meas_step: float,
        rangen: Generator,
    ) -> Tuple[Tensor, Tensor]:
        r"""Performs the stochastic extraction of measurement
        outcomes.

        **Achtung!** This method must be implemented
        by the user.

        Samples measurement outcomes to simulate the
        experiment and returns them, together with
        the likelihood of obtaining
        such outcomes. Typically, this function
        contains at least one call to the :py:meth:`model`
        method, which produces the probabilities for
        the outcome sampling.

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
        """
        raise NotImplementedError("You should override this method!")

    def wrapper_perform_measurement(
        self, controls: Tensor, parameters: Tensor, true_state: Tensor,
        meas_step: float, rangen: Generator,
    ) -> Tuple[Tensor, Tensor, Tensor]:
        outcomes, log_prob = self.perform_measurement(
            controls, parameters, meas_step, rangen,
        )
        return outcomes, log_prob, true_state

    def model(
        self, outcomes: Tensor, controls: Tensor,
        parameters: Tensor, meas_step: Tensor,
        num_systems: int = 1,
    ) -> Tensor:
        r"""Description of the encoding and the measurement
        on the probe. This method returns the probability of
        observing a certain outcome after a measurement.

        **Achtung!** This method must be implemented by the user.

        **Achtung!** This method does not implement any stochastic
        evolution. The stochastic extraction of the outcomes
        should be defined in the method
        :py:meth:`perform_measurement`.

        Suppose that the state of the probe after the encoding is
        :math:`\rho_{\vec{\theta}, x}`, where :math:`\vec{\theta}`
        is `parameter` and :math:`x` is `control`.
        The probe measurement is associated with
        an ensemble of positive operators
        :math:`\lbrace M_y^x \rbrace_{y \in Y}`, where
        :math:`y` is the outcome and :math:`Y` is the set of
        possible outcomes. According to the laws of quantum
        mechanics, the probability of observing the outcome
        :math:`y` is then

        .. math::
            P(y|\vec{\theta}, x) := \text{tr} \left( M_y^x
            \rho_{\vec{\theta}, x} \right) \; .

        Parameters
        ----------
        outcomes: Tensor
            Measurement outcomes. It is a `Tensor` of shape
            (`bs`, `num_systems`, `outcomes_size`)
            of type `prec`, where `bs`, `outcomes_size`, and `prec` are
            attributes of the :py:obj:`~.PhysicalModel` class.
        controls: Tensor
            Contains the controls for the measurement.
            This is a `Tensor` of shape
            (`bs`, `num_systems`, `controls_size`) and type `prec`,
            where `bs`, `controls_size`, and `prec` are attributes
            of the :py:obj:`~.PhysicalModel` class.
        parameters: Tensor
            Values of the unknown parameters. It is a `Tensor`
            of shape (`bs`, `num_systems`, `d`) and
            type `prec`, where `bs`, `d`, and `prec`
            are attributes of the :py:obj:`~.PhysicalModel` class.
        meas_step: Tensors
            The index of the current measurement of the
            probe system. The counting starts from zero.
            This is a `Tensor` of shape (`bs`, `num_systems`, 1)
            and of type `int32`.

        Returns
        -------
        prob: Tensor
            Probability of observing the given
            outcomes vector, having done a measurement
            with the given controls and parameters. It is a `Tensor` of
            shape (`bs`, `num_systems`) and of type `prec`.
            `bs` and `prec` are attributes of
            the :py:obj:`~.PhysicalModel` class.
        """
        raise NotImplementedError("You should override this method!")

    def wrapper_model(
        self, outcomes: Tensor, controls: Tensor, parameters: Tensor,
        state: Tensor, meas_step: float,
        num_systems: int = 1,
    ) -> Tuple[Tensor, Tensor]:
        prob = self.model(
            outcomes, controls, parameters, meas_step,
            num_systems=num_systems,
        )
        return prob, state
