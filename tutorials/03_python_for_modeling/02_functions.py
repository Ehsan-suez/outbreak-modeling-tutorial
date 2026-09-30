# --------------------------------------------------
# Functions in Python
# --------------------------------------------------
#def function_name(input1, input2):
#    result = input1 * input2
#    return result


# A function packages reusable logic.
#
# This function takes two inputs:
#   R_t            = reproduction number
#   infectiousness = infectiousness from past cases
#
# It returns expected incidence.
def expected_incidence(R_t, infectiousness):
    incidence = R_t * infectiousness
    return incidence


# Call the function.
result = expected_incidence(
    R_t=1.2,
    infectiousness=19,
)

print("Expected incidence:", result)


# --------------------------------------------------
# Functions can call other functions
# --------------------------------------------------

def calculate_infectiousness(
    past_incidence,
    generation_interval,
):
    # zip() pairs corresponding values:
    #
    # incidence: 30   20   10
    # weights:   0.2  0.5  0.3
    #
    # giving:
    # (30, 0.2), (20, 0.5), (10, 0.3)

    infectiousness = 0

    for cases, weight in zip(
        past_incidence,
        generation_interval,
    ):
        infectiousness += cases * weight

    return infectiousness


past_incidence = [30, 20, 10]
generation_interval = [0.2, 0.5, 0.3]

infectiousness = calculate_infectiousness(
    past_incidence,
    generation_interval,
)

incidence = expected_incidence(
    R_t=1.2,
    infectiousness=infectiousness,
)

print("Infectiousness:", infectiousness)
print("Expected incidence:", incidence)
