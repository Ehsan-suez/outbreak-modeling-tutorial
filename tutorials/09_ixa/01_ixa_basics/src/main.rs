use ixa::prelude::Context;

fn main() {
    // Create the central ixa simulation context.
    let context = Context::new();

    println!("Created an ixa simulation context.");

    // Explicitly consume the context.
    // This is only for this tiny introductory example.
    drop(context);

    println!("Simulation finished.");
}