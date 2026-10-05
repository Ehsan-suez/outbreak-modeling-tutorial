use ixa::prelude::*;

// ============================================================
// MODULE 09 — IXA
// 04_ixa_epidemic_model
// ============================================================
//
// Goal:
// Combine everything from the previous ixa tutorials:
//
//   09.01 -> Context
//   09.02 -> scheduled actions
//   09.03 -> Person + InfectionStatus
//
// into a tiny agent-based epidemic.
//
// This is intentionally simple.
// We are learning the architecture of an ixa epidemic model,
// not yet trying to build a realistic transmission model.


// ============================================================
// 1. DEFINE THE AGENT TYPE
// ============================================================

define_entity!(Person);


// ============================================================
// 2. DEFINE THE DISEASE STATE
// ============================================================
//
// Each individual person has their OWN infection status.
//
// This is what makes the model agent-based:
//
// Person 0 -> Infectious
// Person 1 -> Susceptible
// Person 2 -> Susceptible

#[derive(Default, Debug, PartialEq, Eq, Hash, Clone, Copy)]
pub enum InfectionStatus {
    #[default]
    Susceptible,
    Infectious,
    Recovered,
}


// InfectionStatus belongs to Person.
//
// Newly created people are Susceptible unless we explicitly
// change their state.

impl_property!(
    InfectionStatus,
    Person,
    default_const = InfectionStatus::Susceptible
);


// ============================================================
// 3. MAIN SIMULATION
// ============================================================

fn main() {

    // --------------------------------------------------------
    // CREATE THE SIMULATION WORLD
    // --------------------------------------------------------

    let mut context = Context::new();


    // --------------------------------------------------------
    // CREATE THREE PEOPLE
    // --------------------------------------------------------
    //
    // Each call creates an actual agent.
    //
    // Because InfectionStatus defaults to Susceptible:
    //
    // Person 0 -> Susceptible
    // Person 1 -> Susceptible
    // Person 2 -> Susceptible

    let person_0 = context
        .add_entity(with!(Person))
        .expect("Failed to create Person 0");

    let person_1 = context
        .add_entity(with!(Person))
        .expect("Failed to create Person 1");

    let person_2 = context
        .add_entity(with!(Person))
        .expect("Failed to create Person 2");


    // --------------------------------------------------------
    // INTRODUCE THE FIRST INFECTION
    // --------------------------------------------------------
    //
    // Person 0 becomes our index case.

    context.set_property::<Person, InfectionStatus>(
        person_0,
        InfectionStatus::Infectious,
    );

    println!("Time 0.0: Person 0 starts Infectious.");


    // --------------------------------------------------------
    // TIME 2: PERSON 0 INFECTS PERSON 1
    // --------------------------------------------------------
    //
    // add_plan() schedules something to happen at a future
    // simulation time.
    //
    // person_1 is captured by the closure so that when time
    // reaches 2.0, we know which person to modify.

    context.add_plan(2.0, move |context| {

        let current_status =
            context.get_property::<Person, InfectionStatus>(person_1);

        // Only infect Person 1 if they are still susceptible.
        if current_status == InfectionStatus::Susceptible {

            context.set_property::<Person, InfectionStatus>(
                person_1,
                InfectionStatus::Infectious,
            );

            println!(
                "Time 2.0: Person 0 transmits infection to Person 1."
            );
        }
    });


    // --------------------------------------------------------
    // TIME 4: PERSON 1 INFECTS PERSON 2
    // --------------------------------------------------------

    context.add_plan(4.0, move |context| {

        let source_status =
            context.get_property::<Person, InfectionStatus>(person_1);

        let target_status =
            context.get_property::<Person, InfectionStatus>(person_2);

        // Transmission happens only if:
        //
        // source = Infectious
        // target = Susceptible

        if source_status == InfectionStatus::Infectious
            && target_status == InfectionStatus::Susceptible
        {
            context.set_property::<Person, InfectionStatus>(
                person_2,
                InfectionStatus::Infectious,
            );

            println!(
                "Time 4.0: Person 1 transmits infection to Person 2."
            );
        }
    });


    // --------------------------------------------------------
    // TIME 5: PERSON 0 RECOVERS
    // --------------------------------------------------------

    context.add_plan(5.0, move |context| {

        context.set_property::<Person, InfectionStatus>(
            person_0,
            InfectionStatus::Recovered,
        );

        println!("Time 5.0: Person 0 recovers.");
    });


    // --------------------------------------------------------
    // TIME 7: PERSON 1 RECOVERS
    // --------------------------------------------------------

    context.add_plan(7.0, move |context| {

        context.set_property::<Person, InfectionStatus>(
            person_1,
            InfectionStatus::Recovered,
        );

        println!("Time 7.0: Person 1 recovers.");
    });


    // --------------------------------------------------------
    // TIME 9: PERSON 2 RECOVERS
    // --------------------------------------------------------

    context.add_plan(9.0, move |context| {

        context.set_property::<Person, InfectionStatus>(
            person_2,
            InfectionStatus::Recovered,
        );

        println!("Time 9.0: Person 2 recovers.");
    });


    // --------------------------------------------------------
    // RUN THE EVENT-DRIVEN SIMULATION
    // --------------------------------------------------------
    //
    // Until execute() is called, we have only scheduled the
    // future actions.
    //
    // execute() processes them in chronological order:
    //
    // 2 -> 4 -> 5 -> 7 -> 9

    context.execute();


    // --------------------------------------------------------
    // CHECK FINAL STATES
    // --------------------------------------------------------

    let status_0 =
        context.get_property::<Person, InfectionStatus>(person_0);

    let status_1 =
        context.get_property::<Person, InfectionStatus>(person_1);

    let status_2 =
        context.get_property::<Person, InfectionStatus>(person_2);


    println!();
    println!("Final states:");
    println!("Person 0: {:?}", status_0);
    println!("Person 1: {:?}", status_1);
    println!("Person 2: {:?}", status_2);
}