// benches/bench_billion.rs
use criterion::{criterion_group, criterion_main, Criterion};
use std::hint::black_box;
use count_billion::count_to_billion;

fn bench_count(c: &mut Criterion) {
    c.bench_function("count_to_billion", |b| {
        b.iter(|| black_box(count_to_billion()))
    });
}

criterion_group! {
    name = benches;
    config = Criterion::default().sample_size(10); // Reduce sample count
    targets = bench_count
}
criterion_main!(benches);
