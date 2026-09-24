"""
consumer.py — a second, independent process that renders tasks as they
arrive from producer.py, in the same ANSI-terminal style as your
`burmese_timer` / `progress_bar` helpers.

Run this FIRST (see README) — it will sit blocked waiting for a writer.
"""

import os
import sys
import time

FIFO_PATH = "/tmp/kuuking_pipe"


def ensure_fifo_exists():
    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)


def render_incoming_bar(seconds: float = 0.6, length: int = 20):
    """Same idea as your progress_bar(): '\\r' redraws in place."""
    steps = 20
    for i in range(steps + 1):
        filled = int(length * i / steps)
        bar = "=" * filled + "-" * (length - filled)
        sys.stdout.write(f"\r  ingesting [{bar}] {int(i / steps * 100):3d}%")
        sys.stdout.flush()
        time.sleep(seconds / steps)
    sys.stdout.write("\n")


def main():
    ensure_fifo_exists()

    print("[consumer] Opening pipe for reading...")
    print("[consumer] (this call BLOCKS until a writer connects)")

    # <-- the other half of the rendezvous. This line does not return
    # until producer.py calls open(FIFO_PATH, 'w').
    pipe = open(FIFO_PATH, "r")
    print("[consumer] Writer connected. Listening for tasks...\n")

    try:
        # A blocking readline() loop: the OS parks this process (uses ~0
        # CPU) until bytes actually show up on the pipe. No polling.
        for line in pipe:
            line = line.strip()
            if not line:
                continue

            task_id, timestamp, name = line.split("|", 2)
            print(f"[consumer] task #{task_id} @ {timestamp} :: {name}")
            render_incoming_bar()
            print(f"  \033[1;32m✓ processed:\033[0m {name}\n")

    except KeyboardInterrupt:
        print("\n[consumer] Interrupted.")
    finally:
        pipe.close()
        print("[consumer] Pipe closed — producer disconnected.")


if __name__ == "__main__":
    main()
