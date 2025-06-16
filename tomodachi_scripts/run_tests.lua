#!/usr/bin/env lua
--[[
    Run all tests for the python using LuaJIT and Lua 5.1.
    This script is intended to be run from the command line.

    To simplify path handling, I placed the script in the bin directory
    where the Bash script is located.
]]

-- Locate the Bash Script
local bash_script_path = "bin/run_unittests.sh" 


-- write the function to handle the script
local function run_bash_script(script_path)
    -- Check if the script exists
    local file = io.open(script_path, "r")

    -- If the file does not exist, print an error message and return false
    if not file then
        print("Error: Script not found: " .. script_path)
        return false
    end

    -- Debug: Print a message indicating the script was found
    -- print("Script found: " .. script_path)

    -- Close the file after checking
    file:close()

    -- Run the script using os.execute
    local command = 'bash "' .. script_path .. '" --testing=pytest --use-coverage'

    -- Debug: Print the command that will be executed
    -- print("Executing command: " .. command)

    -- Execute the command and capture the result
    local ok, exit_type, code = os.execute(command)

    if not ok or (exit_type == "exit" and code ~= 0) then
        print("Error: Failed to run the script.")
        return false
    end

    return true
end

-- Call the function to run the script
run_bash_script(bash_script_path)
