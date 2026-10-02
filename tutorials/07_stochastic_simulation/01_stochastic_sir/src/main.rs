// ============================================================
// MODULE 07 — STOCHASTIC SIMULATION
// 01_stochastic_sir
// ============================================================
//
// This model is a stochastic version of the SIR model.
//
// Each simulated DAY:
//
// 1. Calculate expected new infections.
// 2. Calculate expected new recoveries.
// 3. Randomly draw actual event counts using Poisson
//    distributions.
// 4. Update S, I, and R.
// 5. Repeat.
//
// This is NOT yet event-driven simulation.
// ============================================================


use rand::rng;
use rand_distr::{Distribution, Poisson};


// ------------------------------------------------------------
// POISSON RANDOM DRAW
// ------------------------------------------------------------
//
// lambda = expected number of events.
//
// Example:
//
//     expected infections = 2.7
//
// Instead of using exactly 2.7 infections, we draw:
//
//     X ~ Poisson(2.7)
//
// which might produce:
//
//     1, 2, 3, 4, ...
//
// This introduces stochasticity into the epidemic.

fn poisson_draw(lambda: f64) -> u64 {

    // A Poisson distribution requires a positive mean.
    //
    // If no events are expected, return zero.

    if lambda <= 0.0 {
        return 0;
    }


    // Create a Poisson distribution with mean lambda.

    let distribution =
        Poisson::new(lambda)
            .expect("Poisson mean must be positive");


    // Create the random-number generator.

    let mut random_generator = rng();


    // Draw one random event count.

    distribution.sample(
        &mut random_generator
    ) as u64
}


// ------------------------------------------------------------
// MAIN STOCHASTIC SIR SIMULATION
// ------------------------------------------------------------

fn main() {

    // --------------------------------------------------------
    // POPULATION SIZE
    // --------------------------------------------------------

    let population: u64 = 10_000;


    // --------------------------------------------------------
    // MODEL PARAMETERS
    // --------------------------------------------------------
    //
    // beta:
    //     transmission rate
    //
    // gamma:
    //     recovery rate

    let beta: f64 = 0.30;
    let gamma: f64 = 0.10;


    // --------------------------------------------------------
    // INITIAL EPIDEMIC STATE
    // --------------------------------------------------------
    //
    // We use integer counts because people are discrete.
    //
    // `mut` is required because these values change
    // throughout the simulation.

    let mut susceptible: u64 = 9_990;
    let mut infected: u64 = 10;
    let mut recovered: u64 = 0;


    // Basic reproduction number for this simple SIR model.

    let r0 = beta / gamma;

    println!(
        "R0 = {:.2}",
        r0
    );


    // --------------------------------------------------------
    // SIMULATE UP TO 60 DAYS
    // --------------------------------------------------------

    for day in 0..60 {

        // Print current epidemic state.

        println!(
            "Day {:2} | S: {:5} | I: {:5} | R: {:5}",
            day,
            susceptible,
            infected,
            recovered
        );


        // ----------------------------------------------------
        // EXPECTED NEW INFECTIONS
        // ----------------------------------------------------
        //
        // Standard SIR transmission equation:
        //
        //                     S × I
        // infections = beta × -----
        //                       N

        let expected_infections =
            beta
            * susceptible as f64
            * infected as f64
            / population as f64;


        // ----------------------------------------------------
        // EXPECTED NEW RECOVERIES
        // ----------------------------------------------------
        //
        // recoveries = gamma × I

        let expected_recoveries =
            gamma * infected as f64;


        // ----------------------------------------------------
        // STOCHASTIC EVENT COUNTS
        // ----------------------------------------------------
        //
        // The equations above give EXPECTED numbers.
        //
        // Now randomly determine what actually happens.

        let drawn_infections =
            poisson_draw(expected_infections);

        let drawn_recoveries =
            poisson_draw(expected_recoveries);


        // ----------------------------------------------------
        // PREVENT IMPOSSIBLE TRANSITIONS
        // ----------------------------------------------------
        //
        // Cannot infect more people than are susceptible.

        let new_infections =
            drawn_infections.min(susceptible);


        // Cannot recover more people than are infected.

        let new_recoveries =
            drawn_recoveries.min(infected);


        // ----------------------------------------------------
        // UPDATE THE SIR STATE
        // ----------------------------------------------------
        //
        // S -> I

        susceptible -= new_infections;


        // Infected population gains new infections.

        infected += new_infections;


        // I -> R

        infected -= new_recoveries;

        recovered += new_recoveries;


        // ----------------------------------------------------
        // EPIDEMIC EXTINCTION
        // ----------------------------------------------------
        //
        // If nobody remains infected, there can be no
        // additional transmission.

        if infected == 0 {

            println!(
                "Epidemic extinct on day {}.",
                day + 1
            );

            break;
        }
    }
}

