import jax
import jax.numpy as jnp


# ============================================================
# SIMPLE EPIDEMIC MODEL WITH JAX
# ============================================================
#
# We return to the renewal equation:
#
#     I_t = R_t * Lambda_t
#
# where:
#
#     I_t      = expected incidence
#     R_t      = reproduction number
#     Lambda_t = infectiousness from previous infections
#
# This script combines:
#
#     jax.numpy
#     jax.grad()
#     jax.jit()
#
# in one epidemiological example.
# ============================================================


# ------------------------------------------------------------
# 1. Calculate infectiousness
# ------------------------------------------------------------

def calculate_infectiousness(
    past_incidence,
    generation_interval,
):
    """
    Calculate total infectiousness from past incidence.

    Lambda_t = sum(I_{t-s} * w_s)
    """

    return jnp.dot(
        past_incidence,
        generation_interval,
    )


# ------------------------------------------------------------
# 2. Renewal equation
# ------------------------------------------------------------

def expected_incidence(
    R_t,
    past_incidence,
    generation_interval,
):
    """
    Calculate expected incidence:

        I_t = R_t * Lambda_t
    """

    infectiousness = calculate_infectiousness(
        past_incidence,
        generation_interval,
    )

    return R_t * infectiousness


# ------------------------------------------------------------
# 3. Define epidemic data
# ------------------------------------------------------------

past_incidence = jnp.array([
    30.0,
    20.0,
    10.0,
])

generation_interval = jnp.array([
    0.2,
    0.5,
    0.3,
])

R_t = 1.2


# ------------------------------------------------------------
# 4. Calculate expected incidence
# ------------------------------------------------------------

incidence = expected_incidence(
    R_t,
    past_incidence,
    generation_interval,
)

print(
    "Expected incidence:",
    incidence,
)


# ------------------------------------------------------------
# 5. Calculate sensitivity to R_t
# ------------------------------------------------------------
#
# jax.grad() differentiates with respect to the first
# argument by default.
#
# Therefore we calculate:
#
#     d I_t
#     -----
#     d R_t


incidence_gradient = jax.grad(
    expected_incidence
)

sensitivity = incidence_gradient(
    R_t,
    past_incidence,
    generation_interval,
)

print(
    "Sensitivity to R_t:",
    sensitivity,
)


# ------------------------------------------------------------
# 6. JIT-compile the model
# ------------------------------------------------------------
#
# JIT changes how the calculation is executed,
# not the epidemiological equation itself.


compiled_model = jax.jit(
    expected_incidence
)

compiled_incidence = compiled_model(
    R_t,
    past_incidence,
    generation_interval,
)

print(
    "JIT-compiled incidence:",
    compiled_incidence,
)