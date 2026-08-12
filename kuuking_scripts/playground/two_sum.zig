const std = @import("std");

pub fn two_sum(nums: []const u8, target: u8) ![2]usize {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    var map = std.AutoHashMap(u8, usize).init(allocator);

    defer {
        map.clearAndFree(); // release all hash map allocations
        map.deinit();
        const cleanup_status = gpa.deinit();
        if (cleanup_status != .ok) {
            std.debug.print("Allocator leak detected: {}\n", .{cleanup_status});
        }
    }

    for (nums, 0..) |num, i| {
        const diff = target - num;
        if(map.get(diff)) |j| {
            return .{j, i};
        }

        try map.put(num, i);
    }

    return error.NotFound;
}

pub fn main() !void {
    const nums = [_]u8{1, 2, 3, 4, 5};
    const target: u8 = 7;
    const result = try two_sum(nums[0..], target);
    std.debug.print("Found indices: {} and {}\n", .{ result[0], result[1] });
}

test "two_sum finds correct indices" {
    const nums = [_]u8{2, 7, 11, 15};
    const target: u8 = 9;
    const result = try two_sum(nums[0..], target);

    try std.testing.expect(result[0] == 0 and result[1] == 1);
}
