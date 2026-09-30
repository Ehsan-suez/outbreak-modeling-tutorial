import numpy as np


# --------------------------------------------------
# Python list vs NumPy array
# --------------------------------------------------

python_cases = [10, 20, 30]

numpy_cases = np.array([10, 20, 30])

print("Python list:", python_cases)
print("NumPy array:", numpy_cases)


# --------------------------------------------------
# Element-wise arithmetic
# --------------------------------------------------

# NumPy performs arithmetic on every element.
doubled_cases = numpy_cases * 2

print("Doubled:", doubled_cases)

# Be careful: multiplying a Python list does NOT
# perform numerical element-wise multiplication.
print("Python list * 2:", python_cases * 2)


# --------------------------------------------------
# Vectorization
# --------------------------------------------------

past_incidence = np.array([30, 20, 10])

generation_interval = np.array([0.2, 0.5, 0.3])

# NumPy multiplies corresponding elements:
#
# 30 * 0.2
# 20 * 0.5
# 10 * 0.3
weighted_incidence = (
    past_incidence * generation_interval
)

print("Weighted incidence:", weighted_incidence)

# Sum the weighted contributions.
infectiousness = weighted_incidence.sum()

print("Infectiousness:", infectiousness)


# --------------------------------------------------
# Dot product
# --------------------------------------------------

# The same calculation can be written as a dot product.
#
# 30*0.2 + 20*0.5 + 10*0.3
infectiousness_dot = np.dot(
    past_incidence,
    generation_interval,
)

print("Dot product:", infectiousness_dot)


# --------------------------------------------------
# Array indexing and slicing
# --------------------------------------------------

incidence = np.array([
    10,
    12,
    15,
    18,
    25,
    31,
])

print("First value:", incidence[0])
print("Last value:", incidence[-1])

# Positions 1, 2, and 3.
print("Slice:", incidence[1:4])

# Last three values.
print("Last three:", incidence[-3:])

# Reverse the array.
print("Reversed:", incidence[::-1])


# --------------------------------------------------
# Boolean indexing
# --------------------------------------------------

# Create a True/False array.
high_incidence = incidence > 20

print("Above 20:", high_incidence)

# Use that Boolean array to select only values > 20.
print(
    "Values above 20:",
    incidence[high_incidence],
)


# --------------------------------------------------
# Useful summary operations
# --------------------------------------------------

print("Mean:", incidence.mean())
print("Minimum:", incidence.min())
print("Maximum:", incidence.max())
print("Total:", incidence.sum())