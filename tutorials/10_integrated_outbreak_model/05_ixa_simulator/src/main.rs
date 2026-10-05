use ixa::prelude::*;
use std::collections::HashMap;
use std::error::Error;
use std::path::Path;

// ============================================================
// MODULE 10 — INTEGRATED OUTBREAK MODEL
// 05_ixa_simulator
// ============================================================
//
// Goal:
//
// Read parameters produced by Python and use them inside
// a Rust/ixa agent-based epidemic simulation.
//
// Pipeline:
//
// NumPyro
//    ↓
// posterior R
//    ↓
// Python exports CSV
//    ↓
// Rust reads CSV
//    ↓
// ixa simulation
//


// ============================================================
// 1. DEFINE OUR AGENT
// ============================================================

define_entity!(Person);


// ============================================================
// 2. DEFINE DISEASE STATE
// ============================================================

#[derive(Default, Debug, PartialEq, Eq, Hash, Clone, Copy)]
pub enum InfectionStatus {
    #[default]
    Susceptible,
    Infectious,
    Recovered,
}


impl_property!(
    InfectionStatus,
    Person,
    default_const = InfectionStatus::Susceptible
);


// ============================================================
// 3. READ PARAMETERS PRODUCED BY PYTHON
// ============================================================

fn read_parameters(
    path: &Path,
) -> Result<HashMap<String, f64>, Box<dyn Error>> {

    let mut reader = csv::Reader::from_path(path)?;

    let mut parameters = HashMap::new();


    // Our CSV looks like:
    //
    // parameter,value
    // R,1.376
    // contacts_per_day,4.0
    // infectious_days,5.0
    // transmission_probability,0.0688

    for result in reader.records() {

        let record = result?;

        let name = record
            .get(0)
            .ok_or("Missing parameter name")?
            .to_string();

        let value: f64 = record
            .get(1)
            .ok_or("Missing parameter value")?
            .parse()?;

        parameters.insert(
            name,
            value,
        );
    }


    Ok(parameters)
}


// ============================================================
// 4. MAIN
// ============================================================

fn main() -> Result<(), Box<dyn Error>> {

    // --------------------------------------------------------
    // FIND THE CSV CREATED BY PYTHON
    // --------------------------------------------------------
    //
    // CARGO_MANIFEST_DIR points to:
    //
    // .../05_ixa_simulator
    //
    // The parameter CSV is one directory above it.

    let parameter_path = Path::new(
        env!("CARGO_MANIFEST_DIR")
    )
    .join("../ixa_parameters.csv");


    // --------------------------------------------------------
    // READ PARAMETERS
    // --------------------------------------------------------

    let parameters =
        read_parameters(&parameter_path)?;


    let r = *parameters
        .get("R")
        .ok_or("R missing from parameter file")?;


    let contacts_per_day = *parameters
        .get("contacts_per_day")
        .ok_or("contacts_per_day missing")?;


    let infectious_days = *parameters
        .get("infectious_days")
        .ok_or("infectious_days missing")?;


    let transmission_probability = *parameters
        .get("transmission_probability")
        .ok_or("transmission_probability missing")?;


    println!("Parameters received from Python");
    println!("-------------------------------");

    println!("R: {:.3}", r);

    println!(
        "Contacts per day: {:.1}",
        contacts_per_day
    );

    println!(
        "Infectious period: {:.1} days",
        infectious_days
    );

    println!(
        "Transmission probability: {:.4}",
        transmission_probability
    );

    println!();


    // ========================================================
    // 5. CREATE IXA CONTEXT
    // ========================================================

    let mut context = Context::new();


    // ========================================================
    // 6. CREATE THREE AGENTS
    // ========================================================

    let person_0 = context
        .add_entity(with!(Person))
        .expect("Failed to create Person 0");

    let person_1 = context
        .add_entity(with!(Person))
        .expect("Failed to create Person 1");

    let person_2 = context
        .add_entity(with!(Person))
        .expect("Failed to create Person 2");


    // ========================================================
    // 7. INTRODUCE INDEX CASE
    // ========================================================

    context.set_property::<Person, InfectionStatus>(
        person_0,
        InfectionStatus::Infectious,
    );


    println!(
        "Time 0.0: Person 0 starts Infectious."
    );


    // ========================================================
    // 8. SCHEDULE TRANSMISSION
    // ========================================================
    //
    // For this first integrated example, transmission times
    // remain deterministic.
    //
    // The important new feature is that our transmission
    // PARAMETERS came from Python.
    //
    // In the next refinement, this probability could be used
    // in stochastic contact/transmission events.

    context.add_plan(
        2.0,
        move |context| {

            let status =
                context.get_property::<
                    Person,
                    InfectionStatus,
                >(person_1);


            if status == InfectionStatus::Susceptible {

                context.set_property::<
                    Person,
                    InfectionStatus,
                >(
                    person_1,
                    InfectionStatus::Infectious,
                );


                println!(
                    "Time 2.0: Person 0 infects Person 1."
                );
            }
        },
    );


    context.add_plan(
        4.0,
        move |context| {

            let source_status =
                context.get_property::<
                    Person,
                    InfectionStatus,
                >(person_1);


            let target_status =
                context.get_property::<
                    Person,
                    InfectionStatus,
                >(person_2);


            if source_status == InfectionStatus::Infectious
                && target_status == InfectionStatus::Susceptible
            {
                context.set_property::<
                    Person,
                    InfectionStatus,
                >(
                    person_2,
                    InfectionStatus::Infectious,
                );


                println!(
                    "Time 4.0: Person 1 infects Person 2."
                );
            }
        },
    );


    // ========================================================
    // 9. SCHEDULE RECOVERY
    // ========================================================
    //
    // Notice that the recovery times now use the
    // infectious_days parameter that came from Python.

    context.add_plan(
        infectious_days,
        move |context| {

            context.set_property::<
                Person,
                InfectionStatus,
            >(
                person_0,
                InfectionStatus::Recovered,
            );


            println!(
                "Time {:.1}: Person 0 recovers.",
                infectious_days
            );
        },
    );


    context.add_plan(
        2.0 + infectious_days,
        move |context| {

            context.set_property::<
                Person,
                InfectionStatus,
            >(
                person_1,
                InfectionStatus::Recovered,
            );


            println!(
                "Time {:.1}: Person 1 recovers.",
                2.0 + infectious_days
            );
        },
    );


    context.add_plan(
        4.0 + infectious_days,
        move |context| {

            context.set_property::<
                Person,
                InfectionStatus,
            >(
                person_2,
                InfectionStatus::Recovered,
            );


            println!(
                "Time {:.1}: Person 2 recovers.",
                4.0 + infectious_days
            );
        },
    );


    // ========================================================
    // 10. RUN IXA
    // ========================================================

    context.execute();


    // ========================================================
    // 11. FINAL STATES
    // ========================================================

    println!();
    println!("Final agent states");
    println!("------------------");


    println!(
        "Person 0: {:?}",
        context.get_property::<
            Person,
            InfectionStatus,
        >(person_0)
    );


    println!(
        "Person 1: {:?}",
        context.get_property::<
            Person,
            InfectionStatus,
        >(person_1)
    );


    println!(
        "Person 2: {:?}",
        context.get_property::<
            Person,
            InfectionStatus,
        >(person_2)
    );


    Ok(())
}