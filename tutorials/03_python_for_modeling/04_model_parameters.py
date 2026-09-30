# --------------------------------------------------
# Organizing model parameters
# --------------------------------------------------

# A dictionary is a convenient way to keep related
# model parameters together.
parameters = {
    "population": 1_00000,
    "beta": 0.30,
    "gamma": 0.10,
    "initial_infected": 10,
}

print("Model parameters:")
print(parameters)


# --------------------------------------------------
# Access individual parameters
# --------------------------------------------------

population = parameters["population"]
beta = parameters["beta"]
gamma = parameters["gamma"]

print("Population:", population)
print("Beta:", beta)
print("Gamma:", gamma)


# --------------------------------------------------
# Calculate R0
# --------------------------------------------------

# In a simple SIR model:
#
#     R0 = beta / gamma
#
# beta  = transmission rate
# gamma = recovery rate
R0 = beta / gamma

print("R0:", R0)


# --------------------------------------------------
# Pass a parameter dictionary into a function
# --------------------------------------------------

def calculate_R0(params):
    # Retrieve the values needed by this function.
    beta = params["beta"]
    gamma = params["gamma"]

    return beta / gamma


R0_from_function = calculate_R0(parameters)

print(
    "R0 from function:",
    R0_from_function,
)


# --------------------------------------------------
# Modify a parameter
# --------------------------------------------------

# Imagine an intervention reduces transmission.
intervention_parameters = parameters.copy()

intervention_parameters["beta"] = 0.08

intervention_R0 = calculate_R0(
    intervention_parameters
)

print(
    "R0 after intervention:",
    intervention_R0,
)


# --------------------------------------------------
# Compare scenarios
# --------------------------------------------------

if intervention_R0 < 1:
    print(
        "After the intervention, "
        "transmission is expected to decline."
    )
else:
    print(
        "After the intervention, "
        "transmission can still grow."
    )