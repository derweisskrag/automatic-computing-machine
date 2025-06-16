"""
This tries to consume the tomodachi core and use it without 
accessing the config.py. The challenge is to set up environmental 
variables in one place to make it accessible to the all of the 
codebase.
"""

from dotenv import load_dotenv
import pathlib
import os

# find the path to the root directory
path_to_env = pathlib.Path(__file__).parents[2].resolve()

# we can use this fail and load the env
load_dotenv(path_to_env / ".env.local")

# try to call & get error and fix it
CSV_PATH = os.getenv("CSV_PATH", "Fallback: No ENV was found")

# Use the absolute path
CSV_PATH = (path_to_env / CSV_PATH).resolve()

# Uncomment the following line to print the path to the CSV file if you try to run it from console
# print the path to the CSV file
# print(f"CSV_PATH: {CSV_PATH}")
