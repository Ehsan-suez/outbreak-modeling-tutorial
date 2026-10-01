// ============================================================
// RUST STRUCTS FOR EPIDEMIC MODELING
// ============================================================
//
// A struct lets us group related information together.
//
// Here we will represent a person in an epidemic simulation.
//
// Each person has:
//
//     id
//     age
//     infection status
//
// Later, agent-based models can contain many such people.
// ============================================================


// ------------------------------------------------------------
// 1. Define a Person
// ------------------------------------------------------------

struct Person {
    id: i32,
    age: i32,
    infected: bool,
}


// ------------------------------------------------------------
// 2. Function that examines a Person
// ------------------------------------------------------------
//
// &Person means:
//
//     "borrow a reference to a Person"
//
// We can inspect the person without taking ownership.

fn print_person(person: &Person) {

    println!(
        "Person {} | age {} | infected: {}",
        person.id,
        person.age,
        person.infected
    );
}


// ------------------------------------------------------------
// Main program
// ------------------------------------------------------------

fn main() {

    // --------------------------------------------------------
    // 3. Create one Person
    // --------------------------------------------------------

    let person_1 = Person {
        id: 1,
        age: 35,
        infected: false,
    };


    // --------------------------------------------------------
    // 4. Access fields
    // --------------------------------------------------------

    println!(
        "Person ID: {}",
        person_1.id
    );

    println!(
        "Age: {}",
        person_1.age
    );

    println!(
        "Infected: {}",
        person_1.infected
    );


    // --------------------------------------------------------
    // 5. Pass the person to a function
    // --------------------------------------------------------

    print_person(
        &person_1
    );


    // --------------------------------------------------------
    // 6. Create several people
    // --------------------------------------------------------

    let population: Vec<Person> = vec![
        Person {
            id: 1,
            age: 35,
            infected: false,
        },

        Person {
            id: 2,
            age: 52,
            infected: true,
        },

        Person {
            id: 3,
            age: 18,
            infected: false,
        },
    ];


    // --------------------------------------------------------
    // 7. Loop through our population
    // --------------------------------------------------------

    println!("Population:");

    for person in &population {

        print_person(
            person
        );
    }
}