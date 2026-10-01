// ============================================================
// A SIMPLE EPIDEMIC SIMULATION IN RUST
// ============================================================
//
// We simulate an epidemic using three compartments:
//
//     S = susceptible
//     I = infected
//     R = recovered
//
// This is the same basic SIR logic we previously implemented
// in Python.
//
// The goal here is NOT to learn a new epidemiological model.
//
// The goal is to see how familiar epidemic logic is written
// in Rust.
// ============================================================


// ------------------------------------------------------------
// Calculate new infections
// ------------------------------------------------------------
//
// SIR transmission equation:
//
//                     S × I
// new infections = β × -----
//                       N
//
// beta controls the transmission rate.

fn calculate_new_infections(
    susceptible: f64,
    infected: f64,
    population: f64,
    beta: f64,
) -> f64 {

    beta * susceptible * infected / population
}


// ------------------------------------------------------------
// Calculate new recoveries
// ------------------------------------------------------------
//
// Recovery equation:
//
// new recoveries = gamma × infected

fn calculate_new_recoveries(
    infected: f64,
    gamma: f64,
) -> f64 {

    gamma * infected
}


// ------------------------------------------------------------
// Main simulation
// ------------------------------------------------------------

fn main() {

    // Total population size.
    let population: f64 = 1_000_000.0;


    // --------------------------------------------------------
    // MODEL PARAMETERS
    // --------------------------------------------------------

    let beta: f64 = 0.30;
    let gamma: f64 = 0.10;


    // --------------------------------------------------------
    // INITIAL EPIDEMIC STATE
    // --------------------------------------------------------
    //
    // These variables change every day.
    //
    // Therefore they must be declared with `mut`.

    let mut susceptible: f64 = 999_990.0;
    let mut infected: f64 = 10.0;
    let mut recovered: f64 = 0.0;


    // --------------------------------------------------------
    // BASIC REPRODUCTION NUMBER
    // --------------------------------------------------------

    let r0 = beta / gamma;

    println!(
        "R0 = {:.2}",
        r0
    );


    // --------------------------------------------------------
    // RUN THE SIMULATION
    // --------------------------------------------------------
    //
    // 0..30 means:
    //
    //     0, 1, 2, ..., 29
    //
    // So this loop runs for 30 simulated days.

    for day in 0..30 {

        // Print the epidemic state at the beginning
        // of the current day.

        println!(
            "Day {:2} | S: {:10.0} | I: {:10.0} | R: {:10.0}",
            day,
            susceptible,
            infected,
            recovered
        );


        // Calculate today's transitions.

        let new_infections =
            calculate_new_infections(
                susceptible,
                infected,
                population,
                beta,
            );

        let new_recoveries =
            calculate_new_recoveries(
                infected,
                gamma,
            );


        // ----------------------------------------------------
        // UPDATE THE EPIDEMIC STATE
        // ----------------------------------------------------
        //
        // Susceptible people become infected.

        susceptible -= new_infections;


        // Infected people gain new infections but lose
        // people who recover.

        infected +=
            new_infections
            - new_recoveries;


        // Recovered people accumulate.

        recovered += new_recoveries;
    }
}

