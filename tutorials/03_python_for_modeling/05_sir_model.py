import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Model parameters
# --------------------------------------------------

parameters = {
    "population": 1_000_000,
    "beta": 0.30,
    "gamma": 0.10,
    "initial_infected": 10,
    "n_days": 160,
}


# --------------------------------------------------
# SIR simulation function
# --------------------------------------------------

def simulate_sir(params):
    # Extract model parameters from the dictionary.
    population = params["population"]
    beta = params["beta"]
    gamma = params["gamma"]
    initial_infected = params["initial_infected"]
    n_days = params["n_days"]

    # Create arrays that will store the number of people
    # in each compartment on every simulated day.
    susceptible = np.zeros(n_days)
    infected = np.zeros(n_days)
    recovered = np.zeros(n_days)

    # Initial conditions.
    infected[0] = initial_infected
    susceptible[0] = population - initial_infected
    recovered[0] = 0

    # --------------------------------------------------
    # Simulate the epidemic through time
    # --------------------------------------------------

    for t in range(n_days - 1):

        # Expected number of susceptible people who
        # become infected during this time step.
        new_infections = (
            beta
            * susceptible[t]
            * infected[t]
            / population
        )

        # Expected number of infected people who recover
        # during this time step.
        new_recoveries = (
            gamma * infected[t]
        )

        # Update each compartment for the next day.
        susceptible[t + 1] = (
            susceptible[t] - new_infections
        )

        infected[t + 1] = (
            infected[t]
            + new_infections
            - new_recoveries
        )

        recovered[t + 1] = (
            recovered[t] + new_recoveries
        )

    # Return all three epidemic trajectories.
    return susceptible, infected, recovered


# --------------------------------------------------
# Run the model
# --------------------------------------------------

susceptible, infected, recovered = simulate_sir(
    parameters
)


# --------------------------------------------------
# Calculate R0
# --------------------------------------------------

R0 = (
    parameters["beta"]
    / parameters["gamma"]
)

print("R0:", R0)

# Find the day containing the largest number
# of currently infected people.
peak_day = np.argmax(infected)

print("Peak infection day:", peak_day)
print(
    "Peak infected:",
    infected[peak_day],
)


# --------------------------------------------------
# Check population conservation
# --------------------------------------------------

# S + I + R should always equal the total population.
total_population = (
    susceptible + infected + recovered
)

print(
    "Population at beginning:",
    total_population[0],
)

print(
    "Population at end:",
    total_population[-1],
)


# --------------------------------------------------
# Visualize the epidemic
# --------------------------------------------------

plt.plot(
    susceptible,
    label="Susceptible",
)

plt.plot(
    infected,
    label="Infected",
)

plt.plot(
    recovered,
    label="Recovered",
)

plt.xlabel("Day")
plt.ylabel("People")
plt.title("Simple deterministic SIR model")
plt.legend()

plt.show()
