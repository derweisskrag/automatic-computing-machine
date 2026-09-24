"""
Simple IPC example: server side (terminal A)
Listen on localhost:6000 and accept one client connection.
Messages typed into server terminal are sent to the client; messages from the client are printed.
Type "exit" in either terminal to close the connection cleanly.
"""

import socket
import threading
import argparse
import sys

HOST = "127.0.0.1"
PORT = 6000


def recv_thread(conn, stop_event):
    try:
        with conn:
            while not stop_event.is_set():
                data = conn.recv(4096)
                if not data:
                    print("[CLIENT] connection closed")
                    stop_event.set()
                    break
                text = data.decode("utf-8", errors="replace").rstrip("\n")
                print(f"[CLIENT] {text}")
                if text.strip().lower() == "exit":
                    print("[CLIENT] asked to exit")
                    stop_event.set()
                    break
    except Exception as e:
        print(f"Recv thread error: {e}")
        stop_event.set()


def main(host, port):
    stop_event = threading.Event()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        print(f"Server listening on {host}:{port}")
        try:
            conn, addr = s.accept()
        except KeyboardInterrupt:
            print("Interrupted, exiting")
            return

        print(f"Connected by {addr}")

        rt = threading.Thread(target=recv_thread, args=(conn, stop_event), daemon=True)
        rt.start()

        try:
            # Main thread reads local stdin and sends to client
            while not stop_event.is_set():
                try:
                    line = input().rstrip("\n")
                except EOFError:
                    # Ctrl-D / input closed
                    stop_event.set()
                    break

                if not line:
                    continue

                try:
                    conn.sendall((line + "\n").encode("utf-8"))
                except BrokenPipeError:
                    print("Broken pipe: client disconnected")
                    stop_event.set()
                    break

                if line.strip().lower() == "exit":
                    print("[SERVER] asked to exit")
                    stop_event.set()
                    break

        except KeyboardInterrupt:
            print("Keyboard interrupt, shutting down")
            stop_event.set()

        print("Waiting for recv thread to finish...")
        rt.join(timeout=2)
        print("Server exiting")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IPC terminal server (simple)")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    main(args.host, args.port)
