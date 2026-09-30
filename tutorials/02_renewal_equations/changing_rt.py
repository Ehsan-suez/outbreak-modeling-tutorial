import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Model settings
# --------------------------------------------------

n_days = 30

generation_interval = np.array([0.2, 0.5, 0.3])

# Create one R_t value for every simulated day.
R_t = np.ones(n_days)

# Transmission is relatively high during the
# first half of the simulation.
R_t[:15] = 1.4

# Transmission drops beginning on day 15.
R_t[15:] = 0.7


# --------------------------------------------------
# Initialize incidence
# --------------------------------------------------

incidence = np.zeros(n_days)

# Seed the first three days with infections.
incidence[0:3] = [10, 10, 10]


# --------------------------------------------------
# Renewal simulation
# --------------------------------------------------

for t in range(3, n_days):

    # Previous incidence ordered as:
    # 1 day ago, 2 days ago, 3 days ago.
    past_incidence = incidence[t - 3:t][::-1]

    # Calculate total infectiousness from past cases.
    infectiousness = (
        past_incidence * generation_interval
    ).sum()

    # Unlike our previous model, R_t now depends on time.
    incidence[t] = R_t[t] * infectiousness


# --------------------------------------------------
# Display results
# --------------------------------------------------

for day in range(n_days):
    print(
        f"Day {day}: "
        f"R_t = {R_t[day]:.1f}, "
        f"incidence = {incidence[day]:.2f}"
    )

# --------------------------------------------------
# Visualize incidence and R_t
# --------------------------------------------------

# Plot expected incidence through time.
plt.plot(
    range(n_days),
    incidence,
    marker="o",
)

# Mark the day when R_t changes from 1.4 to 0.7.
plt.axvline(
    x=15,
    linestyle="--",
    label="R_t changes",
)

plt.xlabel("Day")
plt.ylabel("Expected infections")
plt.title("Renewal model with changing R_t")
plt.legend()

plt.show()