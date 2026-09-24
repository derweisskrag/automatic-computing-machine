# Kuuking IPC Demo — Named Pipe (FIFO) Producer/Consumer

## The concept, briefly

A **process** owns its own memory. Two threads inside one process can just
share a variable (that's why your `kuuking_console` works fine as a single
script — the Todo deque, the terminal renderer, the timer all live in one
address space). Two **processes** cannot do that. `producer.py` and
`consumer.py` below are two separate Python interpreters, each with their
own PID, each blind to the other's memory. The only way they exchange data
is if the **kernel** gives them a shared channel. That channel is IPC.

There are several kernel-level channels: anonymous pipes (`os.pipe`, only
useful between a parent and its own fork/child), named pipes / FIFOs
(`os.mkfifo`, any two unrelated processes can open the same path), sockets
(TCP/Unix domain — works across machines, most flexible), shared memory
(`multiprocessing.shared_memory`, fastest, no syscall per message), and
signals (`os.kill`, one bit of information, not really a data channel).

This demo uses a **named pipe**, because it's the clearest to reason about:
it's a special file on disk (`/tmp/kuuking_pipe`) that behaves like an
in-memory queue instead of storing bytes on disk.

## The interesting part: rendezvous blocking

`open(FIFO_PATH, 'w')` in the producer **blocks** until some other process
opens that same path for reading. `open(FIFO_PATH, 'r')` in the consumer
blocks until a writer shows up. Neither side has to poll or sleep-loop to
wait for the other — the kernel suspends both processes and wakes them
the instant they're paired up. That's a real scheduling primitive, not a
busy-wait like your `progress_bar()` frame loop.

## Running it

Two separate terminals, same machine (FIFOs are Linux/macOS — no Windows
support without WSL):

```bash
# Terminal 1 — starts first, will block until Terminal 2 connects
python3 consumer.py

# Terminal 2
python3 producer.py
```

Type task names into the producer terminal. Each one gets serialized as
one line and pushed through the pipe; the consumer terminal renders them
arriving with a small ANSI progress bar, same visual language as your
`burmese_timer`/`progress_bar` helpers.

## Where this maps onto your stack

- **Rust equivalent**: `tokio::net::UnixListener` / `interprocess` crate
  gets you the same rendezvous semantics but async instead of blocking —
  worth looking at once `DSA Kuuking` grows a networked component.
- **If you outgrow one machine**: swap `os.mkfifo` for a `socket.socket()`
  pair (`AF_INET` instead of the FIFO path) — the producer/consumer logic
  barely changes, only the "how do I get a byte stream" part does.
