import grpc
import sys
import os

# Load environment variables from .env.local file
from dotenv import load_dotenv
load_dotenv(".env.local")

# --- CRUCIAL CHANGE TO SYS.PATH HANDLING ---
# Get the directory where this client.py script is located
current_script_dir = os.path.dirname(__file__)

# Construct the full path to the 'gen' directory
generated_code_dir = os.path.join(current_script_dir, "gen")

# Add the 'gen' directory itself to Python's sys.path
# This makes modules directly inside 'gen' (like hello_pb2.py)
# importable by their base name (e.g., 'hello_pb2')
sys.path.append(generated_code_dir)

# Now, import the generated modules directly by their base names
# because their containing directory ('gen') is now in sys.path
import hello_pb2 as hello_pb2           # Note: No 'gen.' prefix here
import hello_pb2_grpc as hello_pb2_grpc # Note: No 'gen.' prefix here
# -------------------------------------------

RUST_SERVER = os.getenv("RUST_SERVER")

def main():
    if RUST_SERVER is None:
        print("Error: RUST_SERVER environment variable not set.")
        return
    else:
        channel = grpc.insecure_channel(RUST_SERVER)
        stub = hello_pb2_grpc.GreeterStub(channel) # Now hello_pb2_grpc is the module, not gen.hello_pb2_grpc
        request = hello_pb2.HelloRequest(name="Alice from Python 🐍")
        response = stub.SayHello(request)
        print(f"Response from Rust server: {response.message}")

if __name__ == "__main__":
    main()