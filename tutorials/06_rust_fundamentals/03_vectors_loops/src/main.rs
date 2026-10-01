
// ============================================================
// RUST VECTORS AND LOOPS
// ============================================================
//
// Goal:
// Learn how Rust stores a collection of values and
// how we iterate through those values.
//
// Epidemiological example:
// daily incidence over several days.
// ============================================================


fn main() {

    // --------------------------------------------------------
    // 1. Create a vector
    // --------------------------------------------------------
    //
    // Vec<i32> means:
    //
    //     a vector containing i32 integers
    //
    // This is somewhat analogous to:
    //
    // Python:
    //     incidence = [10, 15, 21, 30, 43]
    //
    // R:
    //     incidence <- c(10, 15, 21, 30, 43)

    let incidence: Vec<i32> = vec![
        10,
        15,
        21,
        30,
        43,
    ];


    // --------------------------------------------------------
    // 2. Print the entire vector
    // --------------------------------------------------------
    //
    // {:?} is useful for printing structures such as vectors.

    println!(
        "Incidence: {:?}",
        incidence
    );


    // --------------------------------------------------------
    // 3. Access one element
    // --------------------------------------------------------
    //
    // Rust uses zero-based indexing, just like Python.
    //
    // incidence[0] = first value

    println!(
        "First day incidence: {}",
        incidence[0]
    );


    // --------------------------------------------------------
    // 4. Loop through the vector
    // --------------------------------------------------------

    println!("Daily incidence:");

    for cases in &incidence {

        println!(
            "{}",
            cases
        );
    }


    // --------------------------------------------------------
    // 5. Loop with both day and cases
    // --------------------------------------------------------
    //
    // enumerate() gives us:
    //
    //     index + value
    //
    // Similar to Python:
    //
    //     for day, cases in enumerate(incidence):

    println!("Incidence by day:");

    for (day, cases) in incidence.iter().enumerate() {

        println!(
            "Day {}: {} cases",
            day,
            cases
        );
    }


    // --------------------------------------------------------
    // 6. Calculate total incidence
    // --------------------------------------------------------

    let total_cases: i32 =
        incidence.iter().sum();

    println!(
        "Total cases: {}",
        total_cases
    );
}

//cd ../../..

//git add tutorials/06_rust_fundamentals/03_vectors_loops
//git commit -m "add Rust vectors and loops tutorial"
// git push