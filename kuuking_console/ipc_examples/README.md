IPC terminals example (kuuking_console/ipc_examples)

Overview

This small example demonstrates inter-process communication (IPC) between two terminal processes using TCP sockets on localhost. It shows how two independent consoles (server and client) can exchange messages in real time. Run the server in one terminal and the client in another.

Why TCP sockets here?
- TCP sockets work across operating systems and network stacks and are easy to demo between terminals.
- Alternatives: anonymous pipes (parent-child only), named pipes (Windows) / Unix domain sockets (Unix) for local-only, shared memory for large high-speed data, and message queues for advanced patterns.

Files
- server.py: Accepts a single client, prints messages from the client and sends messages typed into the server terminal.
- client.py: Connects to the server and mirrors the same behavior from the client side.

How to run
1. Open terminal A and run the server:
   python kuuking_console\ipc_examples\server.py

2. Open terminal B and run the client:
   python kuuking_console\ipc_examples\client.py

3. Type messages in either terminal. Messages from the other side appear with a prefix ([CLIENT] or [SERVER]).

4. Type "exit" in either terminal to close the connection cleanly.

Using this with kuuking_console
- The example is placed under kuuking_console/ipc_examples so you can experiment alongside the existing console.
- You can run the server next to the Kuuking console instance and use the client to send commands/messages into the server terminal, or integrate a small client call into Kuuking to spawn a connection if you want automation.

Notes and next steps
- This is a minimal demo. For real-world needs consider:
  - Protocols (JSON, line-based, or binary framing) to avoid ambiguity.
  - Authentication / authorization for cross-machine use.
  - Using Unix domain sockets/named pipes for local-only high-performance IPC.
  - Reconnecting logic and multiple client handling (server currently accepts one client only).

Concept summary: what "inter-process for terminals" means
- Inter-process communication (IPC) is any method that allows separate processes to exchange data. When those processes are run in different terminal windows, IPC lets you coordinate or control one terminal from another.
- Common IPC mechanisms: pipes, named pipes, Unix domain sockets, TCP sockets, shared memory, message queues. The best choice depends on OS, performance, scope (local-only vs network), and complexity.

Enjoy experimenting — open two terminals and try it out!