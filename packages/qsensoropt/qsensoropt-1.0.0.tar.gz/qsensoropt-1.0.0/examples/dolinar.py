#!/usr/bin/env python3
from typing import Callable, List

from tensorflow import cast, ones, \
    concat, expand_dims, where, gather, \
        constant, broadcast_to, linspace, \
            zeros_like, zeros, \
                gather_nd, Variable, Tensor
from tensorflow.math import exp, cos, sin, abs, \
    reciprocal_no_nan, equal, logical_not, \
    reduce_sum, greater, floormod, sqrt, round
from tensorflow.random import stateless_poisson, Generator
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from numpy import zeros as npzeros
from argparse import ArgumentParser
from math import pi
from os.path import join

from qsensoropt import InverseSqrtDecay, \
    ParticleFilter, Parameter, Control, \
        SimulationParameters, StatefulPhysicalModel, \
            StatefulSimulation

from qsensoropt.utils import train, \
    performance_evaluation, get_seed, \
    store_input_control, logpoisson, standard_model

def helstrom_bound(
        batchsize: int,
        n: int,
        alpha: Tensor,
        iterations: int = 200,
        prec: str = "float64",
        ):
    r"""Calculates the Helstrom bound for the
    agnostic Dolinar receiver with `n` copies
    of :math:`|\alpha\rangle`. It is the lower bound
    on the error probability for the
    discrimination task and it is given by the
    formula

    .. math::
        p_H(\alpha) := \frac{1}{2} \left( 
            1- \frac{1}{2} \sum_{k=0}^\infty \mathfrak{p} 
            (k; \sqrt{n+1}\alpha) \sqrt{1-\left( 
            \frac{n-1}{n+1} \right)^{2 k}} \right) \; ,
        :label: p_helstr

    where :math:`\mathfrak{p} (k; \mu)` is the probability
    distribution of a Poissonian variable, i.e.

    .. math::
        \mathfrak{p} (k; \mu) := 
        \frac{\mu^k e^{-\mu}}{k!} \; .
        
    Parameters
    ----------
    batchsize: int
        Number of bounds to be computed
        simultaneously, it is the first dimension
        of the `alpha` Tensor.
    n: int
        Number of copies of :math:`|\alpha\rangle`
        at disposal.
    alpha: Tensor
        `Tensor` of shape (`batchsize`, 1), with
        the amplitudes of the coherent states
        for each discrimination task.
    iterations: int = 200
        There is no closed formula for the
        error probability, this parameter
        is the number of summand to be
        computed in :eq:`p_helstr`.
    prec: str = "float64"
        Floating point precision of the
        `alpha` parameter.
    
    Returns
    -------
    Tensor:
        `Tensor` of shape (`batchsize`, 1) and
        type `prec` containing the evaluated
        values of the Helstrom error
        probability for the discrimination
        taks.
    """
    n_tens = n*ones((batchsize, 1), dtype=prec)
    mu_tens = broadcast_to(
        (n+1)*abs(alpha)**2,
        (batchsize, iterations),
        )
    k_tens = cast(
        broadcast_to(expand_dims(linspace(
        0, iterations-1, iterations), axis=0),
        (batchsize, iterations)),
        dtype=prec,
        )
    prob = exp(logpoisson(mu_tens, k_tens))
    n_tens = broadcast_to(n_tens, (batchsize, iterations))
    return 0.5*(1.0-reduce_sum(
        prob*sqrt(1.0-((n_tens-1)/(n_tens+1))**(2.0*k_tens)), 
        axis=1, keepdims=True, )
        )

class AgnosticDolinar(StatefulPhysicalModel):
    r"""Schematization of the agnostic
    Dolinar receiver [6]_.

    The task is to discriminate between
    :math:`|+\alpha\rangle`
    and :math:`|-\alpha\rangle`, given a single copy
    of :math:`| \pm \alpha\rangle` and :math:`n` copies
    of :math:`|\alpha\rangle`, that have been
    prepared in another lab. At difference with the
    usual Dolinar receiver the intensity
    of the signal :math:`\alpha` is not known, but can
    be estimated from :math:`|\alpha\rangle^{\otimes n}`
    to adapt the strategy. The physical motivations
    behind this model is that of a series of wires, 
    with only one carrying the signal, subject
    to a loss noise of fluctuating intensity.

    .. [6] F. Zoratti, N. Dalla Pozza, M. Fanizza,
        and V. Giovannetti, Phys. Rev. A 104, 042606 (2021).
    """
    def __init__(
        self, batchsize: int,
        params: List[Parameter],
        n: int, 
        resources: str = "alpha",
        prec: str = "float64",
    ):
        r"""Constructor of the
        :py:obj:`AgnosticDolinar` class.

        Parameters
        ----------
        batchsize: int
            Number of agnostic Dolinar receivers simulated
            at the same time in a mini-batch.
        params: List[:py:obj:`~.Parameter`]
            List of parameters. It must contain the
            continuous parameter `alpha` with its admissible
            range of values, and the discrete sign parameter, 
            that can take the values (`-1`, `+1`). 
        n: int
            Number of states :math:`|\alpha \rangle` that the
            agnostic Dolinar receiver consumes to make a
            decision on the sign of the sign of the signal.

            **Achtung!** Note that in the simulation `n+1`
            measurement are actually performed, because both
            outputs of the last beam splitter are measured.
        resources: {"alpha", "step"}
            Resources of the model, can be the amplitude
            :math:`\alpha` of the signal or the number
            of state :math:`|\alpha\rangle` consumed
            in the procedure.
        prec: str = "float64"
            Floating point precision of the model.
        """
        controls = [
            Control(name="Theta"),
        ]
        # ψ+ and ψ- are the state variables,
        # plus the total number of
        # photons measured up to that point.
        super().__init__(
            batchsize, controls, params,
            state_specifics={'size': 3, 'type': prec},
            prec=prec,
        )
        self.num_steps = n
        # Resource type
        self.resources = resources
        
        if not self.resources in ("alpha", "step"):
            raise ValueError("The parameter resources can\
                             only be alpha or step.")

    def initialize_state(
            self, parameters: Tensor, num_systems: int,
            ) -> Tensor:
        """State initialization for the agnostic
        Dolinar receiver. The state contains the amplitude
        of the remaining signal after the measurements
        (for both hypothesis) and the total number
        of measured photons.
        """
        psi_plus = ones(
            (self.bs, num_systems, 1), dtype=self.prec,
            )  # ψ+
        psi_minus = -1.0*ones(
            (self.bs, num_systems, 1), dtype=self.prec,
            )  # ψ-
        photon_num = zeros(
            (self.bs, num_systems, 1), dtype=self.prec,
            )
        return concat([psi_plus, psi_minus, photon_num], 2)

    def perform_measurement(
        self, controls: Tensor, parameters: Tensor,
        true_state: Tensor, meas_step: Tensor,
        rangen: Generator,
    ):
        r"""The signal :math:`| \pm \alpha\rangle` and
        the reference states :math:`\alpha` are
        sequentially mixed on a beam splitter
        with tunable transmission :math:`\theta`, and
        one output of the beam splitter is measured
        through photon counting, while the other gets
        mixed again. The left over signal after
        `n` uses of the beam splitter is then
        measured on a photon counter.
        """
        # The second parameter is the sign
        psi = where(
            greater(parameters[:, :, 1],
                    zeros((self.bs, 1), dtype=self.prec)),
                    true_state[:, :, 0], true_state[:, :, 1])
        alpha = parameters[:, :, 0]  # The first parameter is alpha

        # Beam splitter angle
        theta_bs = controls[:, :, 0]
        # All the estimations in the batch run at the same speed
        if (equal(meas_step[0, 0, 0],
                  constant(self.num_steps-1, dtype="int32"))):
            mean = (abs(alpha)**2)*(psi**2)
        else:
            mean = abs(alpha)**2*\
                (psi*sin(theta_bs)-cos(theta_bs))**2
        seed = get_seed(rangen)
        outcomes = cast(stateless_poisson(
            (self.bs, 1), seed, mean), dtype=self.prec)
        outcomes = expand_dims(outcomes, axis=1)
        evolved_state = concat([
            expand_dims(cos(theta_bs) *
                        true_state[:, :, 0] + \
                            sin(theta_bs), axis=2),  # ψ+
            expand_dims(cos(theta_bs) * \
                        true_state[:, :, 1] + \
                            sin(theta_bs), axis=2),  # ψ-
            true_state[:, :, 2:3]+outcomes,
        ], 2)

        return outcomes, logpoisson(mean, outcomes[:, 0, :]), \
            evolved_state

    def model(
            self, outcomes: Tensor, controls: Tensor,
            parameters: Tensor, state: Tensor,
            meas_step: Tensor,
            num_systems: int = 1,
            ):
        """Probability of observing the number of
        photons `outcomes` in a photon counter
        measurement in the agnostic Dolinar receiver.
        """
        # The sign is the second parameter
        sign = parameters[:, :, 1]
        # Signal wavefunction psi
        psi = where(
            greater(sign, zeros_like(sign, dtype=self.prec)),
            state[:, :, 0], state[:, :, 1],
        )
        # Alpha is the first parameter
        alpha = parameters[:, :, 0]
        # Beam splitter angle
        theta_bs = controls[:, :, 0]
        if (equal(meas_step[0, 0, 0],
                  constant(self.num_steps-1, dtype="int32"))):
            mean = (abs(alpha)**2)*(psi**2)
        else:
            mean = abs(alpha)**2*(psi*sin(theta_bs)-\
                                  cos(theta_bs))**2

        observed_photons = outcomes[:, :, 0]

        evolved_state = concat([
            expand_dims(cos(theta_bs) *
                        state[:, :, 0] + sin(theta_bs),
                        axis=2),  # ψ+
            expand_dims(cos(theta_bs) * \
                        state[:, :, 1] + sin(theta_bs),
                        axis=2),  # ψ-
            expand_dims(state[:, :, 2]+observed_photons, axis=2),
        ], 2)

        return exp(logpoisson(mean, observed_photons)), \
            evolved_state

    def count_resources(
        self, resources: Tensor, controls: Tensor,
        true_values: Tensor, meas_step: Tensor,
    ) -> Tensor:
        r"""The resources can be either the number of
        states :math:`|\alpha\rangle` consumed,
        which is update after every beam splitter,
        or the amplitude :math:`\alpha`, that is
        related to the mean number of photons in
        the signal.
        """
        # Only at the last measurement step
        if (self.resources == "alpha"):
            if (equal(meas_step[0, 0],
                      constant(self.num_steps-1, dtype="int32"))):
                resources += abs(true_values[:, :, 0])
        else:
            resources += 1.0
        return resources


class DolinarSimulation(StatefulSimulation):
    """Simulation class for the agnostic Dolinar
    receiver. It works with a :py:obj:`~.ParticleFilter`
    and a :py:obj:`~.AgnosticDolinar` objects.

    The measurement loop is showed in the following
    picture.

    .. image:: ../docs/_static/dolinar.png
        :width: 700
        :alt: dolinar
    """

    def __init__(
            self, particle_filter: ParticleFilter,
            phys_model: AgnosticDolinar,
            control_strategy: Callable,
            simpars: SimulationParameters,
            loss: int = 3,
    ):
        r"""Constructor
        of the :py:obj:`DolinarSimulation` class.

        Parameters
        ----------
        particle_filter: :py:obj:`~.ParticleFilter`
            Particle filter responsible for the update
            of the Bayesian posterior on :math:`\alpha`
            and on the sign of the signal. It
            contains the methods for applying the Bayes
            rule and computing Bayesian estimators
            from the posterior.
        phys_model: :py:obj:`~.AgnosticDolinar`
            Model of the agnostic Dolinar receiver.
        simpars: :py:obj:`~.SimulationParameters`
            Parameter `simpars` passed to the
            class constructor.
        loss: int = 3
            Type of loss to be used in the simulation.
            It regulates the behavior of the 
            :py:meth:`~.DolinarSimulation.loss_function`
            method. There are nine
            possible losses to choose from.
            These are explained in the documentation of
            :py:meth:`~.DolinarSimulation.loss_function`.
        """
        # Set the input size
        input_size = 9
        # Set the name of each column of the input
        input_name = \
            ['PsiPlus', 'Mean_AlphaPlus', 'Sigma_AlphaPlus',
            'PsiMinus', 'Mean_AlphaMinus', 'Sigma_AlphaMinus',
            'ProbPlus', 'MeasStepOverNumStep', 'NumPhotons',
            ]
        
        super().__init__(
            particle_filter, phys_model,
            control_strategy,
            input_size, input_name,
            simpars,
            )
        # Loss variable
        self.loss = loss

    def generate_input(
        self, weights: Tensor, particles: Tensor,
        state_ensemble: Tensor, meas_step: Tensor,
        used_resources: Tensor, rangen: Generator,
    ):
        r"""This method collects the information
        on :math:`\alpha` and on the sign of the signal
        produced by the particle filter and builds from
        them the `input_strategy` object to be fed
        to the neural network. This `Tensor` has nine
        scalar components, that are:

        * :math:`\psi_{+}`, the normalized
          intensity of the signal after the
          measurements, assuming that it was
          :math:`|+\alpha\rangle`
          at the beginning.
        * :math:`\hat{\alpha}_+`, the mean posterior
          estimator for signal intensity assuming
          :math:`|+\alpha\rangle`.
        * :math:`\hat{\sigma}_+`, the variance of the
          posterior distribution for the signal intensity,
          assuming :math:`|+\alpha\rangle`.
        * :math:`\psi_{-}`, the normalized
          intensity of the signal after the
          measurements, assuming that it was
          :math:`|-\alpha\rangle`
          at the beginning.
        * :math:`\hat{\alpha}_{-}`, the mean posterior
          estimator for signal intensity assuming
          :math:`|-\alpha\rangle`.
        * :math:`\hat{\sigma}_-`, the variance of the
          posterior distribution for the signal intensity,
          assuming :math:`|-\alpha\rangle`.
        * :math:`\hat{p}_{+}` the posterior probability
          for the original signal to be :math:`|+\alpha\rangle`,
        * the index of the current measurement `meas_step`
          normalized against the total number of measurements,
        * the total number of photons measured, up to the point this
          method is called.
        """
        pars = self.simpars
        # For all the particles the amplitudes
        # of the signals are the same
        # in this model.
        mean_state = self.pf.compute_state_mean(
            weights, state_ensemble
        )
        # We need to divide the ensemble particles
        # according to their sign.
        is_plus = greater(
            particles[:, :, 1],
            zeros((self.bs, self.pf.np), dtype=pars.prec),
        )
        # Not normalized
        weights_plus = where(
            is_plus, weights,
            zeros((self.bs, self.pf.np), dtype=pars.prec),
        )
        # Not normalized
        weights_minus = where(
            logical_not(is_plus),
            weights,
            zeros((self.bs, self.pf.np), dtype=pars.prec),
        )
        prob_plus = reduce_sum(
            weights_plus, axis=1, keepdims=True,
            )
        prob_minus = reduce_sum(
            weights_minus, axis=1, keepdims=True,
            )
        weights_plus = weights_plus*reciprocal_no_nan(
            broadcast_to(prob_plus, (self.bs, self.pf.np)),
        )
        weights_minus = weights_minus*reciprocal_no_nan(
            broadcast_to(prob_minus, (self.bs, self.pf.np)),
        )
        mean_alpha_plus = self.pf.compute_mean(
            weights_plus, particles,
            )[:, 0:1]
        mean_alpha_minus = self.pf.compute_mean(
            weights_minus, particles,
            )[:, 0:1]
        sigma_alpha_plus = (self.pf.compute_covariance(
            weights_plus, particles)[:, 0, 0:1])**0.5
        sigma_alpha_minus = (self.pf.compute_covariance(
            weights_minus, particles)[:, 0, 0:1])**0.5
        return concat(
            [mean_state[:, 0:1], mean_alpha_plus, sigma_alpha_plus,
            mean_state[:,1:2], mean_alpha_minus, sigma_alpha_minus,
            prob_plus,
            cast(meas_step, dtype=pars.prec)/(pars.num_steps-1),
            mean_state[:, 2:3]], 1, name="input_strategy", )

    def loss_function(
        self, weights: Tensor, particles: Tensor,
        true_state: Tensor, state_ensemble: Tensor,
        true_values: Tensor, used_resources: Tensor,
        meas_step: Tensor,
    ):
        r"""The loss of the agnostic Dolinar receiver measures
        the error in guessing the sign of the signal
        :math:`|\pm \alpha \rangle`, after the signal
        has been completely measured.

        There are nine possible choices for the loss,
        which can be tuned through the parameter
        `loss` passed to the constructor of the
        :py:obj:`~.DolinarSimulation` class. Before
        analyzing one by one these losses we establish
        some notation. :math:`\hat{p}_{+}` is the posterior
        probability that the original signal is
        :math:`| + \alpha \rangle`,
        :math:`\hat{p}_{-} = 1 -\hat{p}_{+}`, :math:`s`
        is the sign of the signal in :math:`| s \alpha \rangle`,
        and :math:`n_{\text{Phot}}` is the total number of observed
        photons. The error probability given by the resource
        limited Helstrom bound is
        indicated with :math:`p_H(\alpha)`. This is computed
        by the function :py:func:`helstrom_bound`.
        We also define the Kronecker delta function

        .. math::
            \delta (x, y) = \begin{cases}
                1 \quad \text{if} \quad x=y \; , \\
                0 \quad \text{if} \quad x \neq y \; .
            \end{cases}
        
        There are two possible policies for guessing the
        signal sign, that we indicate respectively with
        :math:`G_{\text{Bayes}}` and :math:`G_{\text{Parity}}`.
        They are respectively

        .. math::
            G_{\text{Bayes}} (\hat{p}_{+}) = \begin{cases}
                +1 \quad \text{if} \quad
                \hat{p}_{+}  > 0.5 \; ,\\
                -1 \quad \text{if} \quad
                \hat{p}_{+}  \le 0.5 \; ,\\
            \end{cases}

        and

        .. math::
            G_{\text{Parity}} (n_{\text{Phot}})= \begin{cases}
                +1 \quad \text{if} \quad
                n_{\text{Phot}} \bmod 2 = 0 \; ,\\
                -1 \quad \text{if} \quad
                n_{\text{Phot}} \bmod 2 = 1 \; .\\
            \end{cases}

        The possible choices for the loss are

        * `loss=0`: :math:`\ell (\hat{p}_{+}, s) =
          1-\delta(G_{\text{Bayes}}, s)`,
        * `loss=1`: :math:`\ell (\hat{p}_{+}, s) =
          1-\hat{p}_{s}`,
        * `loss=2`: :math:`\ell (n_{\text{Phot}}, s) =
          1-\delta(G_{\text{Parity}}, s)`,
        * `loss=3`: :math:`\ell (\hat{p}_{+}, s, \alpha) =
          1-\delta(G_{\text{Bayes}}, s) - p_H(\alpha)`,
        * `loss=4`: :math:`\ell (\hat{p}_{+}, s, \alpha) =
          1-\hat{p}_{s} - p_H(\alpha)`,
        * `loss=5`: :math:`\ell (n_{\text{Phot}}, s, \alpha) =
          1-\delta(G_{\text{Parity}}, s) - p_H(\alpha)`,
        * `loss=6`: :math:`\ell (\hat{p}_{+}, s, \alpha) =
          \frac{1-\delta(G_{\text{Bayes}}, s)}{p_H(\alpha)}`,
        * `loss=7`: :math:`\ell (\hat{p}_{+}, s, \alpha) =
          \frac{1-\hat{p}_{s}}{p_H(\alpha)}`,
        * `loss=8`: :math:`\ell (n_{\text{Phot}}, s, \alpha) =
          \frac{1-\delta(G_{\text{Parity}}, s)}{p_H(\alpha)}`,
        
        Notes
        -----
        The optimization with `loss=3` works better
        for small :math:`\alpha` then for large :math:`\alpha`.
        This is because the scalar loss is the mean
        of the error probability on the batch and it
        is not so relevant to optimize the estimations
        those regions
        of the parameter :math:`\alpha` that have low
        error probability anyway. To summarize, `loss=3`
        makes the optimization concentrate on the region of small
        :math:`\alpha`, since this region dominates the error.

        **Achtung!**: A constant added to the loss is
        not irrelevant for the training, since the loss
        itself and not only the gradient is appears in the
        gradient descent update.
        """
        pars = self.simpars
        p_err = helstrom_bound(
            self.bs, pars.num_steps-1,
            true_values[:, :, 0], prec=pars.prec,
        )
        # We need to divide the PF
        # particles according to their sign.
        is_plus = greater(particles[:, :, 1], zeros(
            (self.bs, self.pf.np), dtype=pars.prec))
        # Not normalized
        weights_plus = where(
            is_plus, weights,
            zeros((self.bs, self.pf.np), dtype=pars.prec),
        )
        prob_plus = reduce_sum(
            weights_plus, axis=1, keepdims=True,
            )
        zeros_tensor = zeros((self.bs, 1), dtype=pars.prec)
        ones_tensor = ones((self.bs, 1), dtype=pars.prec)

        if self.loss in (0, 3, 6):
            guess = where(
                greater(prob_plus, 0.5*ones_tensor),
                ones_tensor, -1.0*ones_tensor,
                )
            guessed_right = greater(
                true_values[:, :, 1]*guess, zeros_tensor,
                )
            loss_value = where(
                guessed_right, zeros_tensor, ones_tensor,
                )
        if self.loss in (1, 4, 7):
            prob_true_values = expand_dims(gather_nd(
                params=concat([prob_plus, 1.0-prob_plus], axis=1),
                indices=cast(true_values[:, :, 1], dtype="int32"),
                batch_dims=1,
                name = "prob_true"
            ), axis=1)
            # The loss tries to push down the probability
            # of all the wrong hypothesis
            return 1.0-prob_true_values
        if self.loss in (2, 5, 8):
            tensor_two = 2.0*ones((self.bs, 1), dtype=pars.prec)
            parity = floormod(
                state_ensemble[:, 0:1, 2], tensor_two,
                )
            guess = where(
                equal(parity, zeros_tensor),
                ones_tensor, -1.0*ones_tensor,
                )
            guessed_right = greater(
                true_values[:, :, 1]*guess, zeros_tensor,
                )
            loss_value = where(
                guessed_right, zeros_tensor, ones_tensor,
                )
        if self.loss in range(3, 6):
            loss_value -= p_err
        if self.loss in range(6, 9):
            loss_value *= reciprocal_no_nan(p_err)

        return loss_value
    
    def __str__(self):
        return super().__str__() + f"_loss_{self.loss}"


def parse_args():
    r"""Arguments
    ---------
    scratch_dir: str
        Directory in which the intermediate models should
        be saved alongside the loss history.
    trained_models_dir: str = "./dolinar/trained_models"
        Directory in which the finalized trained model
        should be saved.
    data_dir: str = "./dolinar/data"
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
    num_particles: int = 512
        Number of particles in the ensemble representing
        the posterior.
    num_steps: int = 8
        Number of reference states :math:`|\alpha\rangle`,
        i.e. number of beam splitters.
    training_loss: int = 3
        Loss used in the training. It is an integer in
        th range [`0`, `8`]. The various possible
        losses are reported in the description of
        the
        :py:meth:`~.DolinarSimulation.loss_function`
        method. 
    iterations: int = 32768
        Number of training steps.
    """
    parser = ArgumentParser()
    parser.add_argument("--scratch-dir", type=str, required=True)
    parser.add_argument("--trained-models-dir",
                        type=str, default="./dolinar/trained_models")
    parser.add_argument("--data-dir", type=str, default="./dolinar/data")
    parser.add_argument("--prec", type=str, default="float64")
    parser.add_argument("--batchsize", type=int, default=4096)
    parser.add_argument('--n', type=int, default=128)
    parser.add_argument("--num-particles", type=int, default=512)
    parser.add_argument("--iterations", type=int, default=32768)

    return parser.parse_args()

def dolinar_receiver(
        args, num_steps: int,
        loss: int = 3,
        learning_rate: float = 1e-2,
):
    r"""Training and performance evaluation
    of the neural network and the static
    strategies that control the
    beam splitter reflectivity in the agnostic Dolinar
    receiver.

    Parameters
    ----------
    args:
        Arguments passed to the Python script.
    num_steps: int
        Number of reference states
        :math:`\alpha` in the Dolinar receiver.
    loss: int = 3
        Type of loss used for the training, among
        the ones described in the documentation
        of :py:meth:`~.DolinarSimulation.loss_function`.
        The loss used for the performances
        evaluation is always `loss=0`.
    learning_rate: float = 1e-2
        Initial learning rate for the neural
        network. The initial learning rate of the
        static strategy is fixed to `1e-2`.
        They both decay with
        :py:obj:`~.InverseSqrtDecay`.
    """
    trained_models_dir = join(
        args.trained_models_dir, f"training_loss_{loss}",
        )
    data_dir = join(
        args.data_dir, f"training_loss_{loss}",
        )
    
    network = standard_model(
        input_size=8,
        controls_size=1,
        neurons_per_layer=args.n,
        prec=args.prec,
        normalize_activation=True,
        )
    network.compile()

    dolinar = AgnosticDolinar(
        batchsize=args.batchsize,
        params=[
            Parameter(bounds=(0.05, 1.55), name="alpha"),
            Parameter(values=(-1, 1), name="sign"),
        ],
        n=num_steps+1,
        prec=args.prec,
    )
        
    particle_filter = ParticleFilter(
        num_particles=args.num_particles,
        phys_model=dolinar,
        resample_fraction=0.98,
        prec=args.prec,
    )

    # NN strategy
    # ----------------------------------------------

    simpars = SimulationParameters(
        sim_name="dolinar",
        num_steps=num_steps+1,
        max_resources=1.55,
        prec=args.prec,
    )

    def dolinar_control_strategy(input_tensor):
        tot_photons = input_tensor[:, -1:]
        tensor_two = 2.0*ones(
            (args.batchsize, 1), dtype=args.prec,
            )

        return floormod(
            network(input_tensor[:, :-1])-pi*\
                floormod(tot_photons, tensor_two), 2*pi,
        )

    sim_nn = DolinarSimulation(
        particle_filter=particle_filter,
        simpars=simpars,
        phys_model=dolinar,
        control_strategy=dolinar_control_strategy,
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
        join(trained_models_dir, str(sim_nn)),
        )
    # network = load_model(
    #     join(trained_models_dir, str(sim_nn)),
    #     )
    
    sim_nn.loss = 0

    performance_evaluation(
        sim_nn, args.iterations, data_dir,
        xla_compile=False,
        delta_resources=0.05,
    # precision_fit=precision_fit,
        y_label='ProbError',
    )

    dolinar.resources = "step"
    simpars.max_resources = num_steps+1

    store_input_control(
        sim_nn, data_dir, 5,
        xla_compile=False,
    )

    # Static strategy
    # ---------------------------------------------

    dolinar = AgnosticDolinar(
        batchsize=args.batchsize,
        params=[
            Parameter(bounds=(0.05, 1.55), name="alpha"),
            Parameter(values=(-1, 1), name="sign"),
        ],
        n=num_steps+1,
        prec=args.prec,
    )

    #Initial value of the controls
    # in the static optimization
    initial_state = npzeros(
        (int(num_steps+1), 1),
        )
    for i in range(int(num_steps+1)):
        x = (i+1)/(int(num_steps+1))
        initial_state[i, :] = 0.3/((x)**(0.3))

    static_variables = Variable(
        initial_state, dtype=args.prec,
        )

    simpars = SimulationParameters(
        sim_name="dolinar_static",
        num_steps=num_steps+1,
        max_resources=1.55,
        prec=args.prec,
    )

    def dolinar_control_strategy_static(
            input_tensor,
            ):
        tot_photons = input_tensor[:, -1:]
        tensor_two = 2.0*ones(
            (args.batchsize, 1), dtype=args.prec,
            )
        static_control = gather(
            params=static_variables,
            indices=cast(
            round(num_steps*input_tensor[:, -2]),
            dtype="int32"),
        )
        return static_control-\
            pi*floormod(tot_photons, tensor_two)

    sim_static = DolinarSimulation(
        particle_filter=particle_filter,
        simpars=simpars,
        phys_model=dolinar,
        control_strategy=\
            dolinar_control_strategy_static,
    )

    decaying_learning_rate = InverseSqrtDecay(
        learning_rate, args.prec,
    )

    train(
        sim_static,
        Adam(
            learning_rate=decaying_learning_rate,
        ),
        args.iterations, args.scratch_dir,
        custom_controls=static_variables,
        xla_compile=False,
    )

    sim_static.loss = 0

    performance_evaluation(
        sim_static, args.iterations, data_dir,
        xla_compile=False,
        delta_resources=0.05,
    # precision_fit=precision_fit,
        y_label='ProbError',
    )

    dolinar.resources = "step"
    simpars.max_resources = num_steps+1

    store_input_control(
        sim_static, data_dir, 5,
        xla_compile=False,
    )

def main():
    r"""We have trained
    the optimal adaptive and static
    strategies for the agnostic Dolinar
    receiver.

    The error probabilities as a function
    of :math:`\alpha` are reported in the following
    figure for :math:`n=4` and :math:`n=8`
    reference states
    :math:`|\alpha\rangle`, for two different
    training losses (`loss=3` and `loss=6`).

    The `Heterodyne` and `Photon counting` are two
    2-stage adaptive strategies based on first measuring
    all the reference state :math:`|\alpha\rangle^{\otimes n}`
    and then trying to discriminate the signal based
    on the acquired information [5]_.

    .. list-table::

        * - .. figure:: ../examples/dolinar/images/training_loss_3/
                          dolinar_batchsize_4096_num_steps_5_max_
                          resources_1.55_ll_False_cl_False_
                          loss_0/plot_Alpha_ProbError.png
                :width: 600

                n=4, loss=3

          - .. figure:: ../examples/dolinar/images/training_loss_3/
                          dolinar_batchsize_4096_num_steps_9_max_resources_
                            1.55_ll_False_cl_False_
                            loss_0/plot_Alpha_ProbError.png

                n=8, loss=3

        * - .. figure:: ../examples/dolinar/images/training_loss_6/
                          dolinar_batchsize_4096_num_steps_5_max_
                          resources_1.55_ll_False_cl_False_
                          loss_0/plot_Alpha_ProbError.png

               n=4, loss=6

          - .. figure:: ../examples/dolinar/images/training_loss_6/
                           dolinar_batchsize_4096_num_steps_9_max_
                           resources_1.55_ll_False_cl_False_
                           loss_0/plot_Alpha_ProbError.png

                n=8, loss=6

    The shaded grey areas in the above plot indicate
    the Helstrom bound for the discrimination of
    :math:`|\pm \alpha \rangle`.
                
    The `loss=3` seems to be uniformly superior
    to `loss=6` for every value of :math:`\alpha`.
    The advantage of using the neural network strategy
    is very contained with respect to already known
    strategies for :math:`n=8` but it is significant
    for :math:`n=4`. Instead of a NN a decision tree
    could have also been a viable strategy for controlling
    the beam splitters as done in the module
    :py:mod:`dolinar_three`. As expected the gap
    between the precision of the adaptive and of the
    non-adaptive strategies increases with the number
    of photons in the signal.
                
    Notes
    -----
    The loss used in calling
    :py:func:`~.utils.performance_evaluation` is always
    `loss=0`.

    The resources used in calling
    :py:func:`~.utils.store_input_control`
    are always the number of measurements.

    An application of machine learning
    (decision trees) to the
    Dolinar receiver have been presented also
    by Cui et al [7]_. 

    **Known bugs**: the training on the GPU freezes
    if the parameter `alpha_bound` is set to be
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

    .. [7] C. Cui, W. Horrocks, S. Hao et al.,
           Light Sci Appl. 11, 344 (2022).
    """
    args = parse_args()

    dolinar_receiver(args, num_steps=4, loss=3)

    dolinar_receiver(args, num_steps=8, loss=3)

    dolinar_receiver(args, num_steps=16, loss=3)

    dolinar_receiver(args, num_steps=4, loss=6)

    dolinar_receiver(args, num_steps=8, loss=6)
    
    dolinar_receiver(args, num_steps=16, loss=6)

if __name__ == "__main__":
    main()