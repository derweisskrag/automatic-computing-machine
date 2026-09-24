"""
Simple IPC example: client side (terminal B)
Connects to server on localhost:6000. Messages typed in client terminal are sent to the server; messages from the server are printed.
Type "exit" in either terminal to close the connection cleanly.
"""

import socket
import threading
import argparse
import sys

HOST = "127.0.0.1"
PORT = 6000


def recv_thread(sock, stop_event):
    try:
        while not stop_event.is_set():
            data = sock.recv(4096)
            if not data:
                print("[SERVER] connection closed")
                stop_event.set()
                break
            text = data.decode("utf-8", errors="replace").rstrip("\n")
            print(f"[SERVER] {text}")
            if text.strip().lower() == "exit":
                print("[SERVER] asked to exit")
                stop_event.set()
                break
    except Exception as e:
        print(f"Recv thread error: {e}")
        stop_event.set()


def main(host, port):
    stop_event = threading.Event()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
        except Exception as e:
            print(f"Could not connect to {host}:{port}: {e}")
            return

        print(f"Connected to server {host}:{port}")

        rt = threading.Thread(target=recv_thread, args=(s, stop_event), daemon=True)
        rt.start()

        try:
            while not stop_event.is_set():
                try:
                    line = input().rstrip("\n")
                except EOFError:
                    stop_event.set()
                    break

                if not line:
                    continue

                try:
                    s.sendall((line + "\n").encode("utf-8"))
                except BrokenPipeError:
                    print("Broken pipe: server disconnected")
                    stop_event.set()
                    break

                if line.strip().lower() == "exit":
                    print("[CLIENT] asked to exit")
                    stop_event.set()
                    break

        except KeyboardInterrupt:
            print("Keyboard interrupt, shutting down")
            stop_event.set()

        print("Waiting for recv thread to finish...")
        rt.join(timeout=2)
        print("Client exiting")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IPC terminal client (simple)")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    main(args.host, args.port)
