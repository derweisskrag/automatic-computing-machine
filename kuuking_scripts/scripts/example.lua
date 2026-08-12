#!/usr/bin/env lua

--[[
    This script is an example of how to use Lua for scripting tasks.

    It demonstrates basic file operations, string manipulation, and error handling.
]]

-- an example function:
local function add(a, b)
    --[[
        This function takes two numbers and returns their sum.

        Args:
            a (number): The first number.
            b (number): The second number.

        Returns:
            number: The sum of a and b.
    ]]
    return a + b
end

-- -- an example of how to use the function:
result = add(5, 10)

-- verify the result
assert(result == 15, "The result should be 15")

-- Log result to the console
print("The result of adding 5 and 10 is: " .. result)


