import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Model settings
# --------------------------------------------------

# Mean number of secondary infections per infected person.
R = 1.5

# Different levels of transmission heterogeneity.
# Smaller k means greater heterogeneity.
k_values = [2.0, 1.0, 0.5, 0.2, 0.1]

# Number of independent outbreaks to simulate for each k.
n_simulations = 100

# Maximum number of transmission generations.
generations = 20

# Reproducible random-number generator.
rng = np.random.default_rng(seed=42)


# --------------------------------------------------
# Simulate one negative-binomial branching process
# --------------------------------------------------

def simulate_outbreak(R, k, generations, rng):
    # Begin with one infected person.
    infections = 1

    for generation in range(1, generations + 1):

        # Convert epidemiological parameters R and k
        # to NumPy's negative-binomial parameterization.
        p = k / (k + R)

        # Generate one offspring count for every currently
        # infected person.
        offspring = rng.negative_binomial(
            n=k,
            p=p,
            size=infections,
        )

        # Total offspring become the next generation.
        infections = offspring.sum()

        # Stop immediately if the transmission chain dies out.
        if infections == 0:
            return 0

    # Nonzero means the outbreak survived through our horizon.
    return infections


# --------------------------------------------------
# Estimate extinction probability for each k
# --------------------------------------------------

extinction_probabilities = []

for k in k_values:
    extinctions = 0

    for simulation in range(n_simulations):
        result = simulate_outbreak(
            R=R,
            k=k,
            generations=generations,
            rng=rng,
        )

        if result == 0:
            extinctions += 1

    # Estimate P(extinction) using Monte Carlo simulation.
    probability = extinctions / n_simulations

    extinction_probabilities.append(probability)

    print(
        "k =", k,
        "| extinction probability =", probability,
    )


# --------------------------------------------------
# Visualize the results
# --------------------------------------------------

plt.plot(
    k_values,
    extinction_probabilities,
    marker="o",
)

plt.xlabel("Dispersion parameter (k)")
plt.ylabel("Extinction probability")
plt.title("Transmission heterogeneity and outbreak extinction")

plt.show()