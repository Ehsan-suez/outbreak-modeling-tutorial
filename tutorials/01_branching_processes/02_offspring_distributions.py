import numpy as np


# Mean number of secondary infections per infected person
R = 1.5

# Dispersion parameter:
# smaller k = more variation between individuals / more overdispersion
k = 0.2

# Create a reproducible random number generator
rng = np.random.default_rng(seed=42)


# --------------------------------------------------
# Poisson offspring distribution
# --------------------------------------------------

# Simulate the number of secondary infections caused by
# 20 infected individuals.
poisson_offspring = rng.poisson(
    lam=R,      # Mean offspring number
    size=20,    # Number of infected individuals to simulate
)

print("Poisson:")
print(poisson_offspring)


# --------------------------------------------------
# Negative-binomial offspring distribution
# --------------------------------------------------

# NumPy parameterizes the negative binomial using n and p,
# rather than the epidemiological parameters R and k.
#
# We use:
#
#     n = k
#     p = k / (k + R)
#
# This gives the offspring distribution:
#
#     mean = R
#     variance = R + R^2 / k

p = k / (k + R)

negative_binomial_offspring = rng.negative_binomial(
    n=k,        # Dispersion parameter
    p=p,        # Probability parameter derived from R and k
    size=20,    # Simulate 20 infected individuals
)

print("\nNegative binomial:")
print(negative_binomial_offspring)

# --------------------------------------------------
# Compare the two offspring distributions
# --------------------------------------------------

# Calculate the sample mean.
# With enough simulated individuals, both means should
# approach R = 1.5.
poisson_mean = poisson_offspring.mean()
negative_binomial_mean = negative_binomial_offspring.mean()

# Calculate the sample variance.
# ddof=1 gives the usual sample variance.
poisson_variance = poisson_offspring.var(ddof=1)
negative_binomial_variance = negative_binomial_offspring.var(ddof=1)

print("\nSummary:")

print(
    "Poisson:",
    "mean =", poisson_mean,
    "variance =", poisson_variance,
)

print(
    "Negative binomial:",
    "mean =", negative_binomial_mean,
    "variance =", negative_binomial_variance,
)