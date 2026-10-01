fn main() {
    // ========================================================
    // FIRST RUST EPIDEMIC PROGRAM
    // ========================================================
    //
    // We use familiar epidemiological quantities so that
    // we can focus on Rust syntax rather than a new model.


    //32     → integer
    //f64     → floating-point/decimal number
    //bool    → true/false
    //;       → ends most Rust statements
    //let     → create a variable


    // Integer: total population size.
    let population: i32 = 1_000_000;

    // Integer: number currently infected.
    let infected: i32 = 100;

    // Floating-point number: reproduction number.
    let reproduction_number: f64 = 1.5;

    // Boolean: true if R > 1, otherwise false.
    let epidemic_growing: bool = reproduction_number > 1.0;

    println!("Population: {}", population);
    println!("Currently infected: {}", infected);
    println!("Reproduction number: {}", reproduction_number);
    println!("Is the epidemic growing? {}", epidemic_growing);
}



//cd ../../..

//git add tutorials/06_rust_fundamentals/01_rust_basics
//git commit -m "add Rust basics tutorial"
//git push