import os
from dotenv import load_dotenv
import pathlib

# File path to the .env.local file
my_path = pathlib.Path(__file__).parents[2].resolve() 

# check if the path exists (safety)
if not my_path.exists():
    raise FileNotFoundError(f"The path {my_path} does not exist.")
else:
    print(f"Path {my_path} exists.")

# Load environment variables from .env.local file
load_dotenv(my_path / ".env.local")

CSV_PATH = os.getenv("CSV_PATH")
SAVE_TO_PATH = os.getenv("SAVE_TO_PATH")

# Load the test path
TEST_PATH = os.getenv("TEST_PATH")
