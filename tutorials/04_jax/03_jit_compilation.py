import jax


# ------------------------------------------------------------
# A normal numerical function
# ------------------------------------------------------------

def expected_cases(R_t, infectiousness):
    """
    Simple renewal-equation calculation:

        expected incidence = R_t * infectiousness
    """
    return R_t * infectiousness


R_t = 1.2
infectiousness = 19.0


# Run the normal function.
normal_result = expected_cases(
    R_t,
    infectiousness,
)

print(
    "Normal result:",
    normal_result,
)


# ------------------------------------------------------------
# JIT compilation
# ------------------------------------------------------------
#
# jax.jit() takes our function and creates a
# JIT-compiled version of it.
#
# The mathematical calculation does NOT change.


compiled_expected_cases = jax.jit(
    expected_cases
)


# Now call the compiled function.
compiled_result = compiled_expected_cases(
    R_t,
    infectiousness,
)

print(
    "JIT result:",
    compiled_result,
)


# ------------------------------------------------------------
# Decorator syntax
# ------------------------------------------------------------
#
# In real JAX code, you will often see @jax.jit.
#
# This is another way of telling JAX:
#
#     "JIT-compile this function."


@jax.jit
def epidemic_growth(cases, growth_rate):
    return cases * growth_rate


next_cases = epidemic_growth(
    100.0,
    1.2,
)

print(
    "Cases after growth:",
    next_cases,
)


# ------------------------------------------------------------
# Main idea
# ------------------------------------------------------------
#
# jax.grad(function)
#     -> creates a derivative function
#
# jax.jit(function)
#     -> creates a compiled function
#
# JIT changes HOW the calculation is executed.
# It does not change WHAT the model calculates.