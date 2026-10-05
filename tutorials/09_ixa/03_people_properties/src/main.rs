use ixa::prelude::*;

// ============================================================
// MODULE 09 — IXA
// 03_people_properties
// ============================================================
//
// Goal:
// Learn how ixa represents:
//
//   1. An entity type: Person
//   2. A property: InfectionStatus
//   3. An actual individual person
//   4. Reading that person's state
//   5. Changing that person's state
//
// This is our first example where an actual agent's
// epidemiological state changes inside ixa.


// ============================================================
// 1. DEFINE THE AGENT TYPE
// ============================================================
//
// This tells ixa:
//
//     "Our simulation contains entities called Person."
//
// IMPORTANT:
//
// This defines the TYPE of entity.
// It does NOT create an actual person yet.
//
// Think:
//
//     Person = blueprint
//
// Later:
//
//     person = actual agent

define_entity!(Person);


// ============================================================
// 2. DEFINE THE INFECTION STATES
// ============================================================
//
// Each Person can be in one of three states:
//
//     Susceptible
//          ↓
//     Infectious
//          ↓
//     Recovered
//
// This resembles the S, I, and R states from our earlier
// compartmental model.
//
// The difference is:
//
// Compartmental SIR:
//     S = 9990
//     I = 10
//
// Agent-based model:
//     Person 0 = Susceptible
//     Person 1 = Infectious
//     Person 2 = Susceptible
//     ...

#[derive(Default, Debug, PartialEq, Eq, Hash, Clone, Copy)]
pub enum InfectionStatus {
    #[default]
    Susceptible,

    Infectious,

    Recovered,
}


// ============================================================
// 3. CONNECT InfectionStatus TO Person
// ============================================================
//
// This tells ixa:
//
//     "InfectionStatus is a property belonging to Person."
//
// We also specify:
//
//     default = Susceptible
//
// Therefore, if we create a Person without explicitly
// specifying InfectionStatus, ixa uses:
//
//     InfectionStatus::Susceptible

impl_property!(
    InfectionStatus,
    Person,
    default_const = InfectionStatus::Susceptible
);


// ============================================================
// 4. RUN THE SIMULATION EXAMPLE
// ============================================================

fn main() {

    // --------------------------------------------------------
    // CREATE THE IXA SIMULATION WORLD
    // --------------------------------------------------------
    //
    // Context is the central simulation environment.
    //
    // It will eventually contain:
    //
    //     people
    //     properties
    //     events
    //     simulation time
    //     random-number machinery
    //
    // We use `mut` because we are going to modify the context
    // by adding an entity and changing its properties.

    let mut context = Context::new();


    // --------------------------------------------------------
    // CREATE AN ACTUAL PERSON
    // --------------------------------------------------------
    //
    // with!(Person)
    //
    // creates the initialization information for a Person.
    //
    // We do NOT explicitly provide InfectionStatus.
    //
    // Therefore our default applies:
    //
    //     InfectionStatus::Susceptible
    //
    //
    // add_entity(...) returns:
    //
    //     Result<EntityId<Person>, IxaError>
    //
    // Why Result?
    //
    // Because creating an entity could potentially fail.
    //
    // expect(...) says:
    //
    //     "If creation succeeded, give me the Person ID.
    //      If creation failed, stop the program."

    let person = context
        .add_entity(with!(Person))
        .expect("Failed to create person");


    // `person` now contains the unique ID of our actual agent.

    println!("Created person: {:?}", person);


    // --------------------------------------------------------
    // READ THE PERSON'S INITIAL INFECTION STATUS
    // --------------------------------------------------------
    //
    // get_property::<Person, InfectionStatus>(person)
    //
    // can be read as:
    //
    //     Entity type:
    //         Person
    //
    //     Property:
    //         InfectionStatus
    //
    //     Which individual?
    //         person
    //
    // Because we used the default value when creating the
    // person, we expect:
    //
    //     Susceptible

    let status =
        context.get_property::<Person, InfectionStatus>(person);

    println!("Initial infection status: {:?}", status);


    // --------------------------------------------------------
    // INFECT THE PERSON
    // --------------------------------------------------------
    //
    // Now something epidemiologically meaningful happens.
    //
    // We change the person's state:
    //
    //     Susceptible
    //          ↓
    //     Infectious
    //
    // Unlike our previous scheduled-events example, this is
    // NOT merely printing that somebody became infected.
    //
    // We are actually modifying the agent's stored state.

    context.set_property::<Person, InfectionStatus>(
        person,
        InfectionStatus::Infectious,
    );


    // --------------------------------------------------------
    // READ THE PROPERTY AGAIN
    // --------------------------------------------------------
    //
    // Now we ask ixa for the person's current InfectionStatus
    // again.
    //
    // We expect:
    //
    //     Infectious

    let new_status =
        context.get_property::<Person, InfectionStatus>(person);

    println!("After infection: {:?}", new_status);


    // --------------------------------------------------------
    // SUMMARY
    // --------------------------------------------------------
    //
    // Our simulation now contains:
    //
    //     Person
    //        │
    //        └── InfectionStatus
    //
    // And during this program:
    //
    //     Person created
    //          ↓
    //     Susceptible
    //          ↓
    //     set_property()
    //          ↓
    //     Infectious
}