// ============================================================
// MODULE 09 — IXA
// 02_scheduled_events
// ============================================================
//
// Goal:
// Learn how ixa schedules actions in simulation time.
//
// In Module 08 we manually:
//   1. created an event queue
//   2. sorted events by time
//   3. removed the next event
//   4. processed it
//
// ixa's Context handles that event-scheduling machinery for us.

use ixa::prelude::*;

fn main() {
    // --------------------------------------------------------
    // CREATE THE SIMULATION
    // --------------------------------------------------------

    let mut context = Context::new();


    // --------------------------------------------------------
    // SCHEDULE FUTURE ACTIONS
    // --------------------------------------------------------
    //
    // add_plan(time, action)
    //
    // means:
    //
    // "At this simulation time, execute this function."
    //
    // Notice that these are intentionally added OUT OF ORDER.
    // ixa will execute them according to simulation time.

    context.add_plan(5.0, |_context| {
        println!("Time 5.0: Person 7 recovers.");
    });

    context.add_plan(1.0, |_context| {
        println!("Time 1.0: Person 7 becomes infected.");
    });

    context.add_plan(3.0, |_context| {
        println!("Time 3.0: Person 7 is still infected.");
    });


    // --------------------------------------------------------
    // RUN THE SIMULATION
    // --------------------------------------------------------
    //
    // execute() tells ixa:
    //
    // "Process scheduled actions in chronological order
    //  until there is nothing left to process."

    context.execute();


    println!("Simulation finished.");
}