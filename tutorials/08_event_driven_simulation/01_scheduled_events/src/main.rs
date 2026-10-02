// ============================================================
// MODULE 08 — EVENT-DRIVEN SIMULATION
// 01_scheduled_events
// ============================================================
//
// Instead of updating the entire epidemic every day,
// an event-driven simulation processes individual events
// at the exact times when they occur.
//
// Each event answers:
//
//     WHEN does something happen?
//     WHO does it happen to?
//     WHAT happens?
//
// The simulation:
//
//     1. Looks at the event queue.
//     2. Finds the next event.
//     3. Advances to that event's time.
//     4. Processes the event.
//     5. Possibly schedules future events.
//     6. Repeats until no events remain.
// ============================================================


// ------------------------------------------------------------
// EVENT TYPES
// ------------------------------------------------------------
//
// An enum defines the possible kinds of events.
//
// For this simple example, a person can:
//
//     become infected
//     recover

enum EventType {
    Infection,
    Recovery,
}


// ------------------------------------------------------------
// EVENT
// ------------------------------------------------------------
//
// Every event stores:
//
//     time       -> WHEN?
//     person_id  -> WHO?
//     event_type -> WHAT?

struct Event {
    time: f64,
    person_id: usize,
    event_type: EventType,
}


// ------------------------------------------------------------
// PRINT AN EVENT
// ------------------------------------------------------------
//
// &Event means that this function borrows the event
// for reading.
//
// It does not take ownership of the event.

fn print_event(event: &Event) {

    // `match` lets us perform different logic depending
    // on which EventType we have.

    let event_name = match event.event_type {

        EventType::Infection => "infection",

        EventType::Recovery => "recovery",
    };


    println!(
        "Time {:.1}: Person {} -> {}",
        event.time,
        event.person_id,
        event_name
    );
}


// ------------------------------------------------------------
// MAIN EVENT-DRIVEN SIMULATION
// ------------------------------------------------------------

fn main() {

    // --------------------------------------------------------
    // EVENT QUEUE
    // --------------------------------------------------------
    //
    // We start with one scheduled infection:
    //
    //     time 1.0
    //     Person 7
    //     becomes infected
    //
    // `events` is our simple event queue.

    let mut events = vec![

        Event {
            time: 1.0,
            person_id: 7,
            event_type: EventType::Infection,
        },

    ];


    // --------------------------------------------------------
    // KEEP RUNNING WHILE EVENTS EXIST
    // --------------------------------------------------------

    while !events.is_empty() {

        // ----------------------------------------------------
        // FIND THE NEXT EVENT
        // ----------------------------------------------------
        //
        // Sort events according to their scheduled time.
        //
        // The earliest event becomes events[0].

        events.sort_by(
            |a, b| a.time.partial_cmp(&b.time).unwrap()
        );


        // ----------------------------------------------------
        // REMOVE NEXT EVENT FROM QUEUE
        // ----------------------------------------------------
        //
        // remove(0) takes the earliest event out of
        // the queue so we can process it.

        let event = events.remove(0);


        // Conceptually, simulation time has now advanced
        // to event.time.

        print_event(
            &event
        );


        // ----------------------------------------------------
        // PROCESS THE EVENT
        // ----------------------------------------------------

        match event.event_type {


            // =================================================
            // INFECTION EVENT
            // =================================================

            EventType::Infection => {

                println!(
                    "    Person {} is now infected.",
                    event.person_id
                );


                // ---------------------------------------------
                // SCHEDULE A FUTURE RECOVERY
                // ---------------------------------------------
                //
                // For this toy example, everyone recovers
                // exactly four time units after infection.
                //
                // If infection occurs at:
                //
                //     time = 1.0
                //
                // recovery will occur at:
                //
                //     time = 5.0

                let recovery_event = Event {

                    time: event.time + 4.0,

                    person_id: event.person_id,

                    event_type: EventType::Recovery,
                };


                // Put the new future event into the
                // event queue.

                events.push(
                    recovery_event
                );


                println!(
                    "    Recovery scheduled for time {:.1}",
                    event.time + 4.0
                );
            },


            // =================================================
            // RECOVERY EVENT
            // =================================================

            EventType::Recovery => {

                println!(
                    "    Person {} is now recovered.",
                    event.person_id
                );

                // Recovery does not schedule another event
                // in this simple example.
            },
        }
    }


    // --------------------------------------------------------
    // SIMULATION FINISHED
    // --------------------------------------------------------
    //
    // If the event queue is empty, there is nothing
    // left for the simulation to process.

    println!(
        "No events remain. Simulation finished."
    );
}
