pub fn count_to_billion() -> i32 {
    let mut count = 0;
    for i in 0..=1_000_000_000 {
        count += (i % 2) as i32;
    }
    count
}