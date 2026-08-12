#!/usr/bin/env lua

--[[
    This script is used to increment the version number in the specified file.
    It reads the current version, increments it, and writes the new version back to the file.
]]

-- import the LuaFileSystem library
local lfs = require("lfs")

-- Get the current working directory
-- Because we run it from the root
-- This is the root directory of the project
local current_dir = lfs.currentdir()

-- Go back to the root (two directories up)
-- READ the previous comment.
-- local root_dir = current_dir:gsub("[^/\\]+[/\\][^/\\]+$", "")

-- Debug:
-- print("Current Directory: " .. current_dir)
-- print("Root Directory: " .. root_dir)

-- Find the path & Define the version line schema (how it looks like)
local version_file = "/tomodachi_core/__init__.py"
local version_line = "__version__ = \"0.1.4\""

-- Define the path to the file (relative to the script location)
-- We use string concatenation to build the path to the file
local path_to_file = current_dir .. "/" .. version_file


-- Debug
-- print("Path to file: " .. path_to_file)


-- log the action to the console (we are trying to increment the version)
print("Incrementing version in... ")


-- function to check if the file exist
local function file_exists(path)
    local file = io.open(path, "r")
    if file then
        file:close()
        return true
    else
        return false
    end
end

-- define the function to increment version
local function increment_version(version)
    --[[
        This function takes a version string in the format "major.minor.patch" and increments the patch version.
        It returns the new version string.

        Args:
            version (string): The current version string in the format "major.minor.patch".

        Example:
            Input: "1.2.3"
            Output: "1.2.4"
    ]]


    local major, minor, patch = version:match("(%d+)%.(%d+)%.(%d+)") -- Extract major, minor, and patch versions

    -- Check if the version string is valid
    if not major or not minor or not patch then
        error("Invalid version format: " .. version)
    end

    -- Increment the patch version
    patch = tonumber(patch) + 1

    -- Return the new version string
    return string.format("%s.%s.%s", major, minor, patch)
end


-- check if the file exists
result = file_exists(path_to_file)
if not result then
    error("File does not exist: " .. path_to_file)
else
    print("File exists: " .. path_to_file)
end


-- read the file
local file, err = io.open(path_to_file, "r")
if not file then
    error("Failed to open file for reading: " .. err)
end


-- Read the entire content of the file
-- We use "*a" to read the whole file as a string
local content = file:read("*a")
file:close()


-- Debug:
-- print("File content: " .. content)

-- find the line with the version
-- match the version line
local current_version = content:match("__version__ = \"(.-)\"")

-- increment if found
if current_version then 
    -- increment
    local new_version = increment_version(current_version)

    -- update the content
    -- content = content:gsub(version_line, "__version__ = \"" .. new_version .. "\"")
    content = content:gsub("__version__ = \"(.-)\"", "__version__ = \"" .. new_version .. "\"")

    -- Write the new content back to the file
    file = io.open(path_to_file, "w")
    file:write(content)
    file:close()

    -- Output the new version
    print("Version updated to: " .. new_version)
else
    print("Version line not found in the file.")
end