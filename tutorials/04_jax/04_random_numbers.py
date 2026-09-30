import jax
import jax.numpy as jnp


# ============================================================
# RANDOM NUMBERS IN JAX
# ============================================================
#
# JAX uses explicit random keys.
#
# The key determines the pseudorandom numbers that JAX
# generates. This makes randomness explicit and reproducible.
# ============================================================


# ------------------------------------------------------------
# 1. Create a random key
# ------------------------------------------------------------

key = jax.random.PRNGKey(42)

print("Random key:")
print(key)


# ------------------------------------------------------------
# 2. Epidemiological example
# ------------------------------------------------------------
#
# Suppose the number of secondary infections caused by
# one infected person follows:
#
#     X ~ Poisson(R)
#
# where R = 1.5.


R = 1.5

secondary_infections = jax.random.poisson(
    key,
    lam=R,
)

print(
    "\nSecondary infections:",
    secondary_infections,
)


# ------------------------------------------------------------
# 3. Reusing the SAME key
# ------------------------------------------------------------
#
# JAX does not automatically change the key.
#
# Therefore, using exactly the same key again produces
# exactly the same pseudorandom result.


draw_1 = jax.random.poisson(
    key,
    lam=R,
)

draw_2 = jax.random.poisson(
    key,
    lam=R,
)

print("\nUsing the same key:")

print(
    "Draw 1:",
    draw_1,
)

print(
    "Draw 2:",
    draw_2,
)


# ------------------------------------------------------------
# 4. Split the key
# ------------------------------------------------------------
#
# If we want different random draws, we create new keys
# using jax.random.split().
#
# This pattern appears frequently in JAX code.


key_1, key_2 = jax.random.split(key)

draw_1 = jax.random.poisson(
    key_1,
    lam=R,
)

draw_2 = jax.random.poisson(
    key_2,
    lam=R,
)

print("\nUsing different keys:")

print(
    "Draw 1:",
    draw_1,
)

print(
    "Draw 2:",
    draw_2,
)


# ------------------------------------------------------------
# 5. Simulate multiple infected individuals
# ------------------------------------------------------------
#
# Now imagine 10 infected individuals.
#
# Each individual independently generates a Poisson(R)
# number of secondary infections.


key_many = jax.random.PRNGKey(123)

offspring = jax.random.poisson(
    key_many,
    lam=R,
    shape=(10,),
)

print("\nOffspring counts:")
print(offspring)

print(
    "Total secondary infections:",
    jnp.sum(offspring),
)

print(
    "Mean secondary infections:",
    jnp.mean(offspring),
)