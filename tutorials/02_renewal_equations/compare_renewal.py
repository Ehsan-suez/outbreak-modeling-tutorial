import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Model settings
# --------------------------------------------------

R_t = 1.2
generation_interval = np.array([0.2, 0.5, 0.3])
n_days = 30

rng = np.random.default_rng(seed=42)


# --------------------------------------------------
# Initialize both epidemic trajectories
# --------------------------------------------------

deterministic = np.zeros(n_days)
stochastic = np.zeros(n_days, dtype=int)

deterministic[0:3] = [10, 10, 10]
stochastic[0:3] = [10, 10, 10]


# --------------------------------------------------
# Simulate both models
# --------------------------------------------------

for t in range(3, n_days):

    # ----- Deterministic model -----

    past_deterministic = deterministic[t - 3:t][::-1]

    deterministic_infectiousness = (
        past_deterministic * generation_interval
    ).sum()

    deterministic[t] = (
        R_t * deterministic_infectiousness
    )


    # ----- Stochastic model -----

    past_stochastic = stochastic[t - 3:t][::-1]

    stochastic_infectiousness = (
        past_stochastic * generation_interval
    ).sum()

    expected_incidence = (
        R_t * stochastic_infectiousness
    )

    # Draw the actual infection count rather than
    # simply using the expected value.
    stochastic[t] = rng.poisson(
        lam=expected_incidence
    )


# --------------------------------------------------
# Plot both trajectories
# --------------------------------------------------

plt.plot(
    deterministic,
    label="Deterministic",
)

plt.plot(
    stochastic,
    marker="o",
    label="Stochastic",
)

plt.xlabel("Day")
plt.ylabel("Incidence")
plt.title("Deterministic vs stochastic renewal model")
plt.legend()

plt.show()