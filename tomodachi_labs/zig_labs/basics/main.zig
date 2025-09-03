const std = @import("std");


pub fn print_hello() void {
    var stdout = std.io.getStdOut().writer();
    stdout.writeAll("STDOUT: Hello, world!\n") catch |err| {
        std.debug.print("Error writing to stdout: {}\n", .{err});
        return;
    };
}

pub fn main() !void {
    std.debug.print("Hello, {s}!\n", .{"World"});
    print_hello();
}