import jax
import jax.numpy as jnp
import numpy as np

import numpyro
import numpyro.distributions as dist

from numpyro.infer import MCMC, NUTS


# ============================================================
# BAYESIAN INFERENCE WITH A RENEWAL MODEL
# ============================================================
#
# Instead of manually providing:
#
#     infectiousness = 20
#
# we calculate infectiousness from past incidence using
# the generation-interval distribution.
#
#
# Renewal model:
#
#     infectiousness_t
#         = sum(past incidence × generation weights)
#
#     expected_cases_t
#         = R × infectiousness_t
#
#     observed_cases_t
#         ~ Poisson(expected_cases_t)
#
# We will use NumPyro to infer R.
# ============================================================


# ------------------------------------------------------------
# Observed incidence
# ------------------------------------------------------------
#
# Imagine these are daily observed infections.
#
# The first three values give us the history needed
# to calculate infectiousness for day 3.

incidence = jnp.array(
    [
        10.0,
        12.0,
        15.0,
        18.0,
        21.0,
        25.0,
        30.0,
        35.0,
        40.0,
        47.0,
    ]
)


# ------------------------------------------------------------
# Generation-interval distribution
# ------------------------------------------------------------
#
# Interpretation:
#
# infections 1 day ago contribute weight 0.2
# infections 2 days ago contribute weight 0.5
# infections 3 days ago contribute weight 0.3

generation_interval = jnp.array(
    [
        0.2,
        0.5,
        0.3,
    ]
)


# ------------------------------------------------------------
# Calculate infectiousness
# ------------------------------------------------------------

def calculate_infectiousness(
    incidence,
    generation_interval,
):
    """
    Calculate infectiousness for each day after the
    initial three-day history.
    """

    infectiousness_values = []

    for t in range(
        len(generation_interval),
        len(incidence),
    ):
        # Example for t = 3:
        #
        # incidence[:3] gives:
        #
        #     [10, 12, 15]
        #
        # We reverse it:
        #
        #     [15, 12, 10]
        #
        # so that:
        #
        #     15 gets the 1-day weight
        #     12 gets the 2-day weight
        #     10 gets the 3-day weight.

        past_incidence = incidence[
            t - len(generation_interval):t
        ][::-1]

        infectiousness_t = jnp.dot(
            past_incidence,
            generation_interval,
        )

        infectiousness_values.append(
            infectiousness_t
        )

    return jnp.array(
        infectiousness_values
    )


infectiousness = calculate_infectiousness(
    incidence,
    generation_interval,
)


# ------------------------------------------------------------
# Observations corresponding to those infectiousness values
# ------------------------------------------------------------
#
# The first three incidence values were used as history.
#
# Therefore our likelihood starts with day 3.

observed_cases = incidence[
    len(generation_interval):
]


# ------------------------------------------------------------
# NumPyro model
# ------------------------------------------------------------

def renewal_model(
    infectiousness,
    observed_cases=None,
):
    """
    Infer a constant reproduction number R using
    the renewal equation.
    """

    # PRIOR
    #
    # R is unknown and must be positive.

    R = numpyro.sample(
        "R",
        dist.LogNormal(
            0.0,
            0.5,
        ),
    )

    # RENEWAL EQUATION
    #
    # We now have several infectiousness values rather
    # than the single value of 20 used previously.

    expected_cases = (
        R * infectiousness
    )

    # LIKELIHOOD
    #
    # Each observed daily case count is modeled as a
    # Poisson observation around its expected value.

    numpyro.sample(
        "cases",
        dist.Poisson(expected_cases),
        obs=observed_cases,
    )


# ------------------------------------------------------------
# Bayesian inference using NUTS
# ------------------------------------------------------------

kernel = NUTS(
    renewal_model
)

mcmc = MCMC(
    kernel,
    num_warmup=100,
    num_samples=200,
)

key = jax.random.PRNGKey(42)

mcmc.run(
    key,
    infectiousness=infectiousness,
    observed_cases=observed_cases,
)


# ------------------------------------------------------------
# Examine posterior R
# ------------------------------------------------------------

R_samples = np.array(
    mcmc.get_samples()["R"]
)

print(
    "Infectiousness:",
    infectiousness,
)

print(
    "Observed cases:",
    observed_cases,
)

print(
    "Posterior mean R:",
    np.mean(R_samples),
)

print(
    "95% posterior interval:",
    np.quantile(R_samples, 0.025),
    "to",
    np.quantile(R_samples, 0.975),
)

print(
    "P(R > 1):",
    np.mean(R_samples > 1.0),
)