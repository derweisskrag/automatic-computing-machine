#!/usr/bin/env lua
--[[
    Solves the classic two sum problem in Lua.
]]

local function two_sum(nums, target)
    local hash_map = {}

    -- loop over
    for i, num in ipairs(nums) do
        local difference = target - num

        if hash_map[difference] then
            return {hash_map[difference], i}
        end

        hash_map[num] = i
    end

    return nil -- as the failure value? 
end


nums = {1, 2, 3, 4, 5}
local result = two_sum(nums, 3)

if result ~= nil then
    print("The result is " .. table.concat(result, " "))
else
    print("The result was not found in the table")
end

-- test
assert("1 2" == table.concat(result, " "), "In this case, the sum of 1 + 2 is 3")
assert("3 4" == table.concat(two_sum(nums, 7), " "), "The sum of 3 + 4 is 7")
