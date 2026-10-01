import jax
import numpyro
import numpyro.distributions as dist

#numpyro  allows describing uncertain quantitites  using prob distribution
# instead of R =1.5, we say R~ Normal(1.5, 0.5)

# ------------------------------------------------------------
# 1. Define a probabilistic model
# ------------------------------------------------------------

def epidemic_model():
    """
    A tiny probabilistic model for a reproduction number.

    R is not fixed. Instead, we describe our uncertainty
    about R using a probability distribution.
    """

    R = numpyro.sample(
        "R",
        dist.LogNormal(
            0.0,
            0.5,
        ),
    )

    return R



# ------------------------------------------------------------
# 2. Generate a random key
# ------------------------------------------------------------
#
# This is why we learned JAX random keys.
#
# NumPyro uses JAX underneath, so random-number generation
# also requires a JAX key.



key = jax.random.PRNGKey(42)



# ------------------------------------------------------------
# 3. Draw from the model
# ------------------------------------------------------------
#
# handlers.seed() gives our NumPyro model a random key.
#
# We then call the seeded model and obtain one possible
# value of R.



seeded_model = numpyro.handlers.seed(
    epidemic_model,
    key,
)

R_sample = seeded_model()

print(
    "Sampled R:",
    R_sample,
)