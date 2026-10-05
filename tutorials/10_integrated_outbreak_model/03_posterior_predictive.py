"""
Module 10 — Integrated Outbreak Model
03_posterior_predictive.py

Goal
----
Infer R from observed epidemic data and propagate uncertainty in R
forward to create a probabilistic epidemic forecast.

Workflow:

observed incidence
      ↓
Bayesian inference
      ↓
posterior samples of R
      ↓
future simulations
      ↓
probabilistic forecast
      ↓
median + prediction intervals
"""

import numpy as np

import jax.numpy as jnp
from jax import random

import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS


# ============================================================
# 1. OBSERVED EPIDEMIC
# ============================================================
#
# Same synthetic epidemic from scripts 01 and 02.

incidence = jnp.array(
    [
        10,
        12,
        15,
        20,
        27,
        32,
        28,
        39,
        47,
        51,
        65,
        83,
        98,
        122,
        136,
        150,
        181,
        211,
        228,
        273,
    ]
)


generation_interval = jnp.array(
    [0.2, 0.5, 0.3]
)


# ============================================================
# 2. CALCULATE HISTORICAL INFECTIOUSNESS
# ============================================================

infectiousness = []

for week in range(3, len(incidence)):

    recent_incidence = incidence[
        week - 3 : week
    ][::-1]

    lambda_t = jnp.dot(
        recent_incidence,
        generation_interval,
    )

    infectiousness.append(lambda_t)


infectiousness = jnp.array(infectiousness)

observed_incidence = incidence[3:]


# ============================================================
# 3. BAYESIAN RENEWAL MODEL
# ============================================================

def renewal_model(infectiousness, observed=None):

    # Prior uncertainty about R.
    R = numpyro.sample(
        "R",
        dist.LogNormal(0.0, 0.5),
    )

    # Renewal equation:
    #
    # mu_t = R * Lambda_t

    expected_incidence = (
        R * infectiousness
    )

    # Observation model:
    #
    # I_t ~ Poisson(mu_t)

    numpyro.sample(
        "incidence",
        dist.Poisson(expected_incidence),
        obs=observed,
    )


# ============================================================
# 4. INFER R
# ============================================================

kernel = NUTS(renewal_model)

mcmc = MCMC(
    kernel,
    num_warmup=500,
    num_samples=1000,
)


mcmc.run(
    random.PRNGKey(42),
    infectiousness=infectiousness,
    observed=observed_incidence,
)


posterior_samples = mcmc.get_samples()

R_samples = np.asarray(
    posterior_samples["R"]
)


print()
print("Posterior R")
print("-----------")

print(
    f"Mean: {np.mean(R_samples):.3f}"
)

print(
    f"95% credible interval: "
    f"[{np.quantile(R_samples, 0.025):.3f}, "
    f"{np.quantile(R_samples, 0.975):.3f}]"
)


# ============================================================
# 5. POSTERIOR PREDICTIVE FORECAST
# ============================================================
#
# Now comes the new part.
#
# Instead of forecasting with ONE estimated R:
#
#     R = posterior mean
#
# we repeatedly:
#
#   1. take an R from the posterior
#   2. simulate future incidence
#
# Therefore uncertainty in R propagates into uncertainty
# about future epidemic trajectories.


FORECAST_HORIZON = 6

N_FORECASTS = 1000


# Convert historical incidence to ordinary NumPy because
# the forecasting simulation below uses NumPy's RNG.

historical_incidence = np.asarray(
    incidence,
    dtype=float,
)


generation_interval_np = np.asarray(
    generation_interval
)


# Each row will contain one possible future epidemic.
#
# Shape:
#
#     1000 simulations × 6 future weeks

forecast_trajectories = np.zeros(
    (N_FORECASTS, FORECAST_HORIZON)
)


rng = np.random.default_rng(seed=123)


# ============================================================
# 6. SIMULATE FUTURE TRAJECTORIES
# ============================================================

for simulation in range(N_FORECASTS):

    # --------------------------------------------------------
    # SAMPLE R FROM THE POSTERIOR
    # --------------------------------------------------------
    #
    # Different simulations can therefore use slightly
    # different plausible values of R.

    R = rng.choice(R_samples)


    # Start this simulated future with the observed history.

    trajectory = list(
        historical_incidence
    )


    # --------------------------------------------------------
    # FORECAST ONE WEEK AT A TIME
    # --------------------------------------------------------

    for horizon in range(
        FORECAST_HORIZON
    ):

        # Use the three most recent incidence values.
        #
        # Importantly, after the first forecast week,
        # these can include SIMULATED future values.

        recent_incidence = np.array(
            trajectory[-3:][::-1]
        )


        # Renewal infectiousness:
        #
        # Lambda_t = sum(I_{t-s} * w_s)

        lambda_t = np.dot(
            recent_incidence,
            generation_interval_np,
        )


        # Expected future incidence:
        #
        # E[I_t] = R * Lambda_t

        expected_incidence = (
            R * lambda_t
        )


        # Future observations are stochastic.
        #
        # I_t ~ Poisson(R * Lambda_t)

        future_cases = rng.poisson(
            expected_incidence
        )


        trajectory.append(
            future_cases
        )


        # Save this future observation.

        forecast_trajectories[
            simulation,
            horizon,
        ] = future_cases


# ============================================================
# 7. SUMMARIZE THE PROBABILISTIC FORECAST
# ============================================================
#
# For each future week, calculate:
#
#     2.5% quantile
#     median
#     97.5% quantile
#
# These summarize the distribution across our 1000 possible
# future epidemic trajectories.


lower = np.quantile(
    forecast_trajectories,
    0.025,
    axis=0,
)

median = np.quantile(
    forecast_trajectories,
    0.50,
    axis=0,
)

upper = np.quantile(
    forecast_trajectories,
    0.975,
    axis=0,
)


# ============================================================
# 8. DISPLAY FORECAST
# ============================================================

print()
print("Posterior predictive forecast")
print("-----------------------------")

print(
    "Week | Median | 95% prediction interval"
)

print(
    "---------------------------------------"
)


last_observed_week = (
    len(incidence) - 1
)


for horizon in range(
    FORECAST_HORIZON
):

    week = (
        last_observed_week
        + horizon
        + 1
    )

    print(
        f"{week:4d} | "
        f"{median[horizon]:6.0f} | "
        f"[{lower[horizon]:.0f}, "
        f"{upper[horizon]:.0f}]"
    )