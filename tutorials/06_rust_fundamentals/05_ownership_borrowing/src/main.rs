// ============================================================
// OWNERSHIP, BORROWING, AND MUTABLE REFERENCES
// ============================================================
//
// Rust carefully controls who owns data and who is
// allowed to modify it.
//
// Three important patterns:
//
//     Person      -> ownership
//     &Person     -> immutable borrow
//     &mut Person -> mutable borrow
//
// We'll learn these using infection status.
// ============================================================


struct Person {
    id: i32,
    infected: bool,
}


// ------------------------------------------------------------
// IMMUTABLE BORROW
// ------------------------------------------------------------
//
// &Person means:
//
//     "Let this function temporarily look at the Person."
//
// The function does NOT own the Person.
// It also cannot modify the Person.

fn print_status(person: &Person) {

    println!(
        "Person {} infected: {}",
        person.id,
        person.infected
    );
}


// ------------------------------------------------------------
// MUTABLE BORROW
// ------------------------------------------------------------
//
// &mut Person means:
//
//     "Temporarily borrow this Person AND allow
//      the function to modify it."

fn infect(person: &mut Person) {

    person.infected = true;
}


// ------------------------------------------------------------
// Main program
// ------------------------------------------------------------

fn main() {

    // --------------------------------------------------------
    // Create a mutable Person
    // --------------------------------------------------------
    //
    // `mut` is necessary because this person's state
    // will change during the simulation.

    let mut person = Person {
        id: 1,
        infected: false,
    };


    // --------------------------------------------------------
    // Read the person's state
    // --------------------------------------------------------

    println!("Before infection:");

    print_status(
        &person
    );


    // --------------------------------------------------------
    // Modify the person's state
    // --------------------------------------------------------
    //
    // We give infect() a mutable reference.

    infect(
        &mut person
    );


    // --------------------------------------------------------
    // Read the state again
    // --------------------------------------------------------

    println!("After infection:");

    print_status(
        &person
    );
}