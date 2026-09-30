import numpy as np
import jax.numpy as jnp


# --------------------------------------------------
# NumPy vs JAX NumPy
# --------------------------------------------------

# Standard NumPy array.
numpy_cases = np.array([
    10.0,
    20.0,
    30.0,
])

# JAX array.
jax_cases = jnp.array([
    10.0,
    20.0,
    30.0,
])

print("NumPy:")
print(numpy_cases)

print("\nJAX:")
print(jax_cases)


# --------------------------------------------------
# Basic array operations
# --------------------------------------------------

# JAX syntax looks very similar to NumPy.
doubled_cases = jax_cases * 2

print("\nDoubled:")
print(doubled_cases)


# --------------------------------------------------
# Renewal-equation calculation with JAX
# --------------------------------------------------

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

# Calculate infectiousness using a dot product.
infectiousness = jnp.dot(
    past_incidence,
    generation_interval,
)

# Renewal equation:
#
# I_t = R_t * sum(I_{t-s} * w_s)
expected_incidence = (
    R_t * infectiousness
)

print(
    "\nInfectiousness:",
    infectiousness,
)

print(
    "Expected incidence:",
    expected_incidence,
)


# --------------------------------------------------
# Inspect the array types
# --------------------------------------------------

print(
    "\nNumPy type:",
    type(numpy_cases),
)

print(
    "JAX type:",
    type(jax_cases),
)
