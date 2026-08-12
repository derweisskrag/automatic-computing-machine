import json
from contextlib import contextmanager

@contextmanager
def json_ctx(file_path: str, mode='r'):
    try:
        if mode == 'r':  # Reading the file
            with open(file_path, 'r') as file:
                data = json.load(file)
            yield data
        elif mode == 'w':  # Writing to the file
            with open(file_path, 'w') as file:
                yield file  # Give the file object to the code for writing
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Finished with the JSON context.")