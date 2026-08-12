"""
Console REPL for the DLL Priority Queue Todo App.

Commands
--------
  add  <task> <priority>   Push a task at the tail (default) or head
  top  <task> <priority>   Push a task at the head (highest insertion point)
  exec                     Pop and execute the highest-priority task
  swap <task1> <task2>     Swap the priorities of two tasks  ← heapq can't do this
  peek                     Show the next task without removing it
  list                     Show the full queue (head → tail)
  logs [n]                 Show the last n operation log entries (default 10)
  benchmark [n]            Benchmark Python DLL vs Rust extension on n ops
  build                    Compile the Rust extension with maturin
  help                     Show this help
  exit / quit              Exit

Logs are stored in memory and only shown when you ask — no scrolling noise.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# ANSI helpers (disabled on non-TTY)
# ---------------------------------------------------------------------------

_TTY = sys.stdout.isatty()

def _c(code: str, text: str) -> str:
    if not _TTY:
        return text
    return f"\033[{code}m{text}\033[0m"

def bold(t: str) -> str:   return _c("1", t)
def dim(t: str) -> str:    return _c("2", t)
def green(t: str) -> str:  return _c("32", t)
def yellow(t: str) -> str: return _c("33", t)
def cyan(t: str) -> str:   return _c("36", t)
def red(t: str) -> str:    return _c("31", t)
def magenta(t: str) -> str: return _c("35", t)


"""
    def _unlink(self, node: Node) -> None:
        "Remove *node* from the DLL; caller must handle _index / _size."
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
"""

