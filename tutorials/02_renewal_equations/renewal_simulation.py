import numpy as np


# --------------------------------------------------
# Model settings
# --------------------------------------------------

# Effective reproduction number.
R_t = 1.2 #change to 08 or 1.2 or 1.0

# Generation-interval distribution.
# Transmission can occur 1, 2, or 3 days after infection.
generation_interval = np.array([0.2, 0.5, 0.3])

# Number of days to simulate.
n_days = 30


# --------------------------------------------------
# Initialize incidence
# --------------------------------------------------

# Create an array containing 30 zeros.
# We will fill this array with simulated incidence.
incidence = np.zeros(n_days)

# Seed the epidemic with infections during the first
# three days so the renewal equation has some history.
incidence[0:3] = [10, 10, 10]


# --------------------------------------------------
# Simulate incidence through time
# --------------------------------------------------

# Start at day 3 because days 0, 1, and 2
# were initialized above.
for t in range(3, n_days):

    # Get incidence from the previous three days.
    #
    # [::-1] reverses the order so that:
    #   first value = 1 day ago
    #   second      = 2 days ago
    #   third       = 3 days ago
    past_incidence = incidence[t - 3:t][::-1]

    # Calculate infectiousness contributed by
    # previous infections.
    infectiousness = (
        past_incidence * generation_interval
    ).sum()

    # Renewal equation:
    #
    #     I_t = R_t * sum(I_{t-s} * w_s)
    incidence[t] = R_t * infectiousness


# --------------------------------------------------
# Display results
# --------------------------------------------------

for day, infections in enumerate(incidence):
    print(
        f"Day {day}: "
        f"{infections:.2f} expected infections"
    )