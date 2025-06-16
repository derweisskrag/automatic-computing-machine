fn bar(x: &mut i32) {
    
}

fn foo(a: &mut i32) {
    bar(a);
    let y = &a;
    println!("{}", y);
}


fn main() {
    println!("Hello, world!");

    let mut x = 2;

    foo(&mut x);
}
