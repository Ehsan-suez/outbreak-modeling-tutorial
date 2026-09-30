import numpy as np

R = 1.5
generations = 10

rng = np.random.default_rng(seed=2)

infections = 1

print("Generation 0:", infections)

for generation in range (1, generations + 1):
    infections = rng.poisson(
        lam = R,
        size = infections,
    ).sum()

    print(f"Generation {generation}:", infections)

    if infections==0:
        print("Otbreak went extinct.")
        break
    