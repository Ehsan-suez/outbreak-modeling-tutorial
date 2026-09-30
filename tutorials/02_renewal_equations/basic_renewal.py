# Branching processes describe transmission chains; 
# renewal equations describe how those chains appear as incidence through time.

import numpy as np


# --------------------------------------------------
# Basic renewal equation
# --------------------------------------------------

# Incidence from the previous three days.
#
# The order is:
#   1 day ago, 2 days ago, 3 days ago
past_incidence = np.array([30, 20, 10])

# Generation-interval weights.
#
# These describe how much infections from each previous
# day contribute to transmission today.
#
# The weights sum to 1.
generation_interval = np.array([0.2, 0.5, 0.3])

# Effective reproduction number today.
R_t = 0.8


# --------------------------------------------------
# Calculate total infectiousness
# --------------------------------------------------

# Multiply incidence from each previous day by its
# corresponding generation-interval weight.
weighted_infections = past_incidence * generation_interval

print("Weighted infections:", weighted_infections)

# Add the weighted contributions together.
infectiousness = weighted_infections.sum()

print("Total infectiousness:", infectiousness)


# --------------------------------------------------
# Apply the renewal equation
# --------------------------------------------------

# Renewal equation:
#
#     I_t = R_t * sum(I_{t-s} * w_s)
#
# This gives the expected incidence today.
incidence_today = R_t * infectiousness

print("Expected incidence today:", incidence_today)
