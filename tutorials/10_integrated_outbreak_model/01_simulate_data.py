"""
Module 10 — Integrated Outbreak Model
01_simulate_data.py

Goal
----
Generate a small synthetic epidemic using a stochastic renewal model.

Later we will pretend that we do NOT know the true reproduction
number and ask NumPyro to infer it from these simulated observations.

Module 01
stochasticity
       +
Module 02
renewal equation
       +
Module 03
Python / NumPy
       ↓

SIMULATED EPIDEMIC DATA
"""

import numpy as np


# ============================================================
# MODEL PARAMETERS
# ============================================================

# This is the TRUE reproduction number used to generate data.
# Later, NumPyro will not be told this value.
TRUE_R = 1.4

# Generation-interval distribution.
#
# An infected person contributes:
#
# 20% of their transmission after 1 time step
# 50% after 2
# 30% after 3
#
# The weights sum to 1.
generation_interval = np.array([0.2, 0.5, 0.3])


# ============================================================
# INITIAL INCIDENCE
# ============================================================

# We need a few initial observations because the renewal
# equation depends on previous incidence.

incidence = [10, 12, 15]

N_WEEKS = 20


# ============================================================
# STOCHASTIC RENEWAL SIMULATION
# ============================================================

# Reproducible random-number generator.
rng = np.random.default_rng(seed=42)


for week in range(3, N_WEEKS):

    # Take the previous three incidence observations.
    #
    # Example:
    #
    # incidence = [..., 10, 12, 15]
    #
    # recent_incidence becomes:
    #
    # [15, 12, 10]
    #
    # because generation_interval[0] corresponds to the
    # most recent previous week.

    recent_incidence = np.array(
        incidence[week - 3 : week][::-1]
    )


    # --------------------------------------------------------
    # CALCULATE TOTAL INFECTIOUSNESS
    # --------------------------------------------------------
    #
    # Renewal equation:
    #
    # Lambda_t = sum(I_{t-s} * w_s)

    infectiousness = np.dot(
        recent_incidence,
        generation_interval,
    )


    # --------------------------------------------------------
    # EXPECTED INCIDENCE
    # --------------------------------------------------------
    #
    # E[I_t] = R * Lambda_t

    expected_incidence = TRUE_R * infectiousness


    # --------------------------------------------------------
    # STOCHASTIC OBSERVATION
    # --------------------------------------------------------
    #
    # Instead of using the expectation directly, draw the
    # actual incidence from a Poisson distribution.
    #
    # I_t ~ Poisson(R * Lambda_t)

    new_cases = rng.poisson(expected_incidence)

    incidence.append(new_cases)


# ============================================================
# DISPLAY THE SIMULATED DATA
# ============================================================

print(f"True R used to generate epidemic: {TRUE_R}")
print()

print("Week | Incidence")
print("----------------")

for week, cases in enumerate(incidence):
    print(f"{week:4d} | {cases:9d}")