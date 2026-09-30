# --------------------------------------------------
# Basic Python objects used in modeling
# --------------------------------------------------

# Integer: a whole-number count.
infected = 25

# Float: a number that can contain decimals.
R_t = 1.3

# Boolean: True or False.
intervention_active = True

# String: text.
pathogen = "influenza"

print(type(infected))
print(type(R_t))
print(type(intervention_active))
print(type(pathogen))


# --------------------------------------------------
# Lists
# --------------------------------------------------

# A list stores multiple values in order.
daily_cases = [10, 15, 21, 30, 42]

print("Cases:", daily_cases)

# Python uses zero-based indexing.
print("First day:", daily_cases[0])

# -1 means the final element.
print("Most recent day:", daily_cases[-1])

# Extract positions 1, 2, and 3.
# The right endpoint is NOT included.
print("Middle days:", daily_cases[1:4])


# --------------------------------------------------
# Dictionaries
# --------------------------------------------------

# A dictionary stores information as key-value pairs.
parameters = {
    "R_t": 1.3,
    "generation_interval": 4.5,
    "population": 1_000_000,
}

print("Parameters:", parameters)

# Retrieve a value using its key.
print("R_t:", parameters["R_t"])


# --------------------------------------------------
# Conditional logic
# --------------------------------------------------

if R_t > 1:
    print("Incidence tends to grow.")
elif R_t < 1:
    print("Incidence tends to decline.")
else:
    print("Incidence is approximately stable.")


# --------------------------------------------------
# Loops
# --------------------------------------------------

for day, cases in enumerate(daily_cases):
    print(f"Day {day}: {cases} cases")