fn foo() -> Box<dyn Fn(u32) -> u32> {
    let x = 0u32;
    Box::new(move |y| {
	println!("x = {}, y = {}", x, y);
        x + y
    })
}




fn main() {
    println!("Hello, world!");
    let ex = foo();
    let my_result: u32 = ex(5);
    println!("I got: {}", my_result);
}
