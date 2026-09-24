"""
producer.py — the "Kuuking Console" half that SENDS tasks out to another
process instead of just appending them to a local Deque.

Run this AFTER consumer.py is already waiting (see README).
"""

import os
import time
from datetime import datetime

FIFO_PATH = "/tmp/kuuking_pipe"


def ensure_fifo_exists():
    # mkfifo just creates the special file; it doesn't open it.
    # It's cheap to call every run and skip if it's already there.
    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)


def main():
    ensure_fifo_exists()

    print("[producer] Opening pipe for writing...")
    print("[producer] (this call BLOCKS until a reader connects)")

    # <-- the rendezvous moment. Nothing after this line runs
    # until consumer.py has its own `open(FIFO_PATH, 'r')` call ready.
    pipe = open(FIFO_PATH, "w")
    print("[producer] Reader connected. Pipe is live.\n")

    task_id = 0
    try:
        while True:
            name = input("New task name (empty to quit): ").strip()
            if not name:
                break

            task_id += 1
            timestamp = datetime.now().strftime("%H:%M:%S")

            # Dead simple wire format: id|timestamp|name
            # Real systems would use JSON, protobuf, etc. — but the pipe
            # itself doesn't care, it just moves bytes.
            line = f"{task_id}|{timestamp}|{name}\n"

            pipe.write(line)
            pipe.flush()  # <-- without this the OS may buffer it and
                          #     the consumer won't see it right away
            print(f"[producer] sent -> {line.strip()}")

    except (BrokenPipeError, KeyboardInterrupt):
        print("\n[producer] Consumer disconnected or interrupted.")
    finally:
        pipe.close()
        print("[producer] Pipe closed.")


if __name__ == "__main__":
    main()
