const std = @import("std");

pub fn main() !void {
    var timer = try std.time.Timer.start();

    var count: u64 = 0;
    var i: u64 = 0;
    while (i < 1_000_000_001) : (i += 1) {
        // Prevent optimization
        std.mem.doNotOptimizeAway(i);
        count += 1;
    }

    const elapsed_ns = timer.read();
    const elapsed_s = @as(f64, @floatFromInt(elapsed_ns)) / 1_000_000_000.0;

    const stdout = std.io.getStdOut().writer();
    try stdout.print("Count: {}\nTime taken: {d:.3} seconds\n", .{count, elapsed_s});
    std.debug.print("Elapsed time: {d:.9} seconds\n", .{elapsed_s});
    std.debug.print("Elapsed time: {} nanoseconds\n", .{elapsed_ns});
    std.debug.print("Count: {}\n", .{count});
}

