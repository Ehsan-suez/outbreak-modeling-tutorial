// ============================================================
// STOCHASTIC SIR SIMULATION
// ============================================================
//
// Deterministic SIR:
//
//     new infections = beta * S * I / N
//     new recoveries = gamma * I
//
// Those equations give EXPECTED numbers of events.
//
// In this stochastic version, we use those expectations
// as the means of Poisson distributions and randomly draw
// the actual number of events.
//
// Example:
//
//     expected infections = 2.7
//
// does NOT mean exactly 2.7 people are infected.
//
// Instead:
//
//     new infections ~ Poisson(2.7)
//
// might produce 1, 2, 3, 4, ... actual infections.
// ============================================================

use rand::rng;
use rand_distr::{Distribution, Poisson};


// ------------------------------------------------------------
// Draw a random event count from a Poisson distribution
// ------------------------------------------------------------
//
// lambda = expected number of events.
//
// Example:
//
//     poisson_draw(3.0)
//
// could return:
//
//     1, 2, 3, 4, 5, ...
//
// Different runs can produce different values.

fn poisson_draw(lambda: f64) -> u64 {

    // A Poisson mean must be positive.
    //
    // If the expected number of events is zero,
    // simply return zero events.

    if lambda <= 0.0 {
        return 0;
    }

    // Create a Poisson distribution with mean lambda.

    let distribution =
        Poisson::new(lambda)
            .expect("Poisson mean must be positive");


    // Create the random-number generator.

    let mut random_generator = rng();


    // Draw one random number from the distribution.

    distribution.sample(
        &mut random_generator
    ) as u64
}


// ------------------------------------------------------------
// Main simulation
// ------------------------------------------------------------

fn main() {

    // --------------------------------------------------------
    // POPULATION
    // --------------------------------------------------------

    let population: u64 = 10_000;


    // --------------------------------------------------------
    // MODEL PARAMETERS
    // --------------------------------------------------------

    let beta: f64 = 0.30;
    let gamma: f64 = 0.10;


    // --------------------------------------------------------
    // INITIAL EPIDEMIC STATE
    // --------------------------------------------------------
    //
    // Unlike our deterministic model, we use whole numbers
    // because people are discrete individuals.

    let mut susceptible: u64 = 9_990;
    let mut infected: u64 = 10;
    let mut recovered: u64 = 0;


    println!(
        "R0 = {:.2}",
        beta / gamma
    );


    // --------------------------------------------------------
    // SIMULATE 60 DAYS
    // --------------------------------------------------------

    for day in 0..60 {

        println!(
            "Day {:2} | S: {:5} | I: {:5} | R: {:5}",
            day,
            susceptible,
            infected,
            recovered
        );


        // ----------------------------------------------------
        // EXPECTED INFECTIONS
        // ----------------------------------------------------
        //
        // Same equation as deterministic SIR:
        //
        //            S * I
        // beta * -----------
        //              N

        let expected_infections =
            beta
            * susceptible as f64
            * infected as f64
            / population as f64;


        // ----------------------------------------------------
        // EXPECTED RECOVERIES
        // ----------------------------------------------------

        let expected_recoveries =
            gamma * infected as f64;


        // ----------------------------------------------------
        // RANDOM EVENT COUNTS
        // ----------------------------------------------------
        //
        // Instead of directly using the expected values,
        // draw actual event counts.

        let drawn_infections =
            poisson_draw(expected_infections);

        let drawn_recoveries =
            poisson_draw(expected_recoveries);


        // ----------------------------------------------------
        // KEEP EVENTS PHYSICALLY POSSIBLE
        // ----------------------------------------------------
        //
        // We cannot infect more people than are susceptible.

        let new_infections =
            drawn_infections.min(susceptible);


        // We cannot recover more people than are infected.

        let new_recoveries =
            drawn_recoveries.min(infected);


        // ----------------------------------------------------
        // UPDATE SIR STATE
        // ----------------------------------------------------

        susceptible -= new_infections;

        infected += new_infections;
        infected -= new_recoveries;

        recovered += new_recoveries;


        // ----------------------------------------------------
        // EXTINCTION
        // ----------------------------------------------------
        //
        // If nobody remains infected, transmission stops.

        if infected == 0 {

            println!(
                "Epidemic extinct on day {}.",
                day + 1
            );

            break;
        }
    }
}