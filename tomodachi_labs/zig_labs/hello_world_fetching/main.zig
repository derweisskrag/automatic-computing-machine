const std = @import("std");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    const stdout = std.io.getStdOut().writer();

    var client = std.http.Client{ .allocator = allocator };
    defer client.deinit();

    // Prepare request
    const url = "http://127.0.0.1:3000/api/test";
    const headers = &[_]std.http.Header{ .{ .name = "Accept", .value = "application/json" } };

    // Perform a GET request
    const response = try getRequest(url, headers, &client, allocator);

    // Parse JSON into struct
    const Result = struct { message: []const u8 };
    const parsed = try std.json.parseFromSlice(Result, allocator, response.items, .{ .ignore_unknown_fields = true });

    try stdout.print("Message: {s}\n", .{parsed.value.message});
}

fn getRequest(
    url: []const u8,
    headers: []const std.http.Header,
    client: *std.http.Client,
    allocator: std.mem.Allocator,
) !std.ArrayList(u8) {
    var body = std.ArrayList(u8).init(allocator);
    const resp = try client.fetch(.{
        .method = .GET,
        .location = .{ .url = url },
        .extra_headers = headers,
        .response_storage = .{ .dynamic = &body },
    });
    return body;
}
