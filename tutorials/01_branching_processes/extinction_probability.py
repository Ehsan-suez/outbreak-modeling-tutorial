import numpy as np

def simulate_outbreak(R, generations, rng, distribution="poisson", k=0.2):
    # Start every simulated outbreak with one infected person.
    infections = 1

    for generation in range(1, generations + 1):

        # Poisson model:
        # Each infected person generates a Poisson(R)
        # number of secondary infections.
        if distribution == "poisson":
            offspring = rng.poisson(
                lam=R,
                size=infections,
            )

        # Negative-binomial model:
        # The mean is still R, but k controls transmission
        # heterogeneity. Smaller k means more overdispersion.
        elif distribution == "negative_binomial":
            # Convert epidemiological parameters R and k
            # to NumPy's negative-binomial probability parameter.
            p = k / (k + R)

            offspring = rng.negative_binomial(
                n=k,
                p=p,
                size=infections,
            )

        # Add all secondary infections to obtain the
        # number of infections in the next generation.
        infections = offspring.sum()

        # Once there are zero infections, the transmission
        # chain is extinct and cannot restart.
        if infections == 0:
            return 0

    # A nonzero value means the outbreak was still active
    # at the end of our simulation horizon.
    return infections

# --------------------------------------------------
# Compare extinction under two offspring distributions
# --------------------------------------------------

R = 1.5
k = 0.2
generations = 20
n_simulations = 100

# Use separate random-number generators so each experiment
# starts from the same reproducible seed.
poisson_rng = np.random.default_rng(seed=42)
negative_binomial_rng = np.random.default_rng(seed=42)

poisson_extinctions = 0
negative_binomial_extinctions = 0


# Simulate many Poisson branching-process outbreaks.
for simulation in range(n_simulations):
    result = simulate_outbreak(
        R=R,
        generations=generations,
        rng=poisson_rng,
        distribution="poisson",
    )

    if result == 0:
        poisson_extinctions += 1


# Simulate many negative-binomial branching-process outbreaks.
for simulation in range(n_simulations):
    result = simulate_outbreak(
        R=R,
        generations=generations,
        rng=negative_binomial_rng,
        distribution="negative_binomial",
        k=k,
    )

    if result == 0:
        negative_binomial_extinctions += 1


# Estimate extinction probabilities using Monte Carlo simulation.
poisson_probability = poisson_extinctions / n_simulations
negative_binomial_probability = (
    negative_binomial_extinctions / n_simulations
)


print("R:", R)
print("k:", k)

print(
    "Poisson extinction probability:",
    poisson_probability,
)

print(
    "Negative-binomial extinction probability:",
    negative_binomial_probability,
)

# --------------------------------------------------
# Explore how the dispersion parameter k affects
# outbreak extinction.
# --------------------------------------------------

# Smaller k means greater transmission heterogeneity.
k_values = [2.0, 1.0, 0.5, 0.2, 0.1]

print("\nEffect of transmission heterogeneity:")

for k_value in k_values:

    # Start a reproducible random-number generator
    # for this value of k.
    rng = np.random.default_rng(seed=42)

    extinctions = 0

    # Simulate many independent outbreaks.
    for simulation in range(n_simulations):

        result = simulate_outbreak(
            R=R,
            generations=generations,
            rng=rng,
            distribution="negative_binomial",
            k=k_value,
        )

        # Count outbreaks that became extinct.
        if result == 0:
            extinctions += 1

    # Monte Carlo estimate of extinction probability.
    extinction_probability = extinctions / n_simulations

    print(
        "k =", k_value,
        "| extinction probability =",
        extinction_probability,
    )