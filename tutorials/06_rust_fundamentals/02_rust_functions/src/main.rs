// ============================================================
// RUST FUNCTIONS FOR EPIDEMIC MODELING
// ============================================================
//
// Familiar epidemiological equation:
//
//     expected incidence = R × infectiousness
//
// Our goal here is not to learn a new epidemic model.
// We're learning how to express familiar model logic
// as Rust functions.
// ============================================================


// ------------------------------------------------------------
// Function 1: Calculate expected incidence
// ------------------------------------------------------------
//
// Python equivalent:
//
// def expected_incidence(r, infectiousness):
//     return r * infectiousness
//
// Rust requires us to specify the types of the inputs
// and the type of value returned.
//
//     r: f64
//     infectiousness: f64
//
// The:
//
//     -> f64
//
// means:
//
//     "this function returns an f64"
//

fn expected_incidence(
    r: f64,
    infectiousness: f64,
) -> f64 {

    // IMPORTANT RUST FEATURE:
    //
    // The final expression has NO semicolon.
    //
    // Rust automatically returns the value of the
    // final expression from the function.

    r * infectiousness
}


// ------------------------------------------------------------
// Function 2: Determine whether epidemic is growing
// ------------------------------------------------------------
//
// This function takes an f64 and returns a bool.

fn epidemic_is_growing(
    r: f64,
) -> bool {

    r > 1.0
}


// ------------------------------------------------------------
// Main program
// ------------------------------------------------------------

fn main() {

    let r: f64 = 1.5;
    let infectiousness: f64 = 20.0;

    // Call our function.
    let expected_cases =
        expected_incidence(
            r,
            infectiousness,
        );

    let growing =
        epidemic_is_growing(r);

    println!(
        "R: {}",
        r
    );

    println!(
        "Infectiousness: {}",
        infectiousness
    );

    println!(
        "Expected cases: {}",
        expected_cases
    );

    println!(
        "Is epidemic growing? {}",
        growing
    );
}


//cd ../../..

//git add tutorials/06_rust_fundamentals/02_rust_functions
//git commit -m "add Rust functions tutorial"
//git push