"""
Module 10 — Integrated Outbreak Model
04_export_parameters.py

Goal
----
Create a simple parameter file that can be consumed by our
Rust/ixa agent-based epidemic simulator.

This demonstrates a clean boundary between:

    Python / statistical inference
              ↓
          CSV file
              ↓
        Rust / ixa ABM

In a production pipeline, these values could come directly
from posterior samples or another fitted model.
"""

from pathlib import Path

import pandas as pd


# ============================================================
# 1. INFERRED TRANSMISSION PARAMETER
# ============================================================
#
# From our NumPyro analysis:
#
# posterior mean R ≈ 1.376
#
# IMPORTANT:
#
# R is NOT a per-contact transmission probability.
#
# R means approximately:
#
#     expected secondary infections
#     produced by one infectious person
#
# The ixa ABM will therefore need to translate R into
# agent-level transmission parameters.

posterior_mean_r = 1.376


# ============================================================
# 2. ABM ASSUMPTIONS
# ============================================================
#
# For our toy agent-based model, assume:
#
#     4 potentially infectious contacts per day
#     5-day infectious period
#
# Therefore:
#
#     total opportunities
#         = contacts_per_day * infectious_days
#
#         = 4 * 5
#         = 20
#
# A simple approximation is:
#
#     transmission_probability
#         = R / total_contact_opportunities
#
# This is intentionally simplified.
#
# A real ABM would usually require calibration because:
#
#     repeated contacts,
#     susceptible depletion,
#     contact heterogeneity,
#     network structure,
#     interventions,
#     and timing
#
# can all change the relationship between agent-level
# transmission probabilities and population-level R.

contacts_per_day = 4.0
infectious_days = 5.0

transmission_probability = (
    posterior_mean_r
    / (contacts_per_day * infectious_days)
)


# ============================================================
# 3. BUILD PARAMETER TABLE
# ============================================================

parameters = pd.DataFrame(
    {
        "parameter": [
            "R",
            "contacts_per_day",
            "infectious_days",
            "transmission_probability",
        ],
        "value": [
            posterior_mean_r,
            contacts_per_day,
            infectious_days,
            transmission_probability,
        ],
    }
)


# ============================================================
# 4. SAVE FOR THE RUST / IXA MODEL
# ============================================================

output_path = Path(
    "tutorials/10_integrated_outbreak_model/"
    "ixa_parameters.csv"
)

parameters.to_csv(
    output_path,
    index=False,
)


# ============================================================
# 5. DISPLAY WHAT WE EXPORTED
# ============================================================

print("Parameters exported for Rust/ixa")
print("--------------------------------")

print(parameters.to_string(index=False))

print()
print(f"Saved to: {output_path}")