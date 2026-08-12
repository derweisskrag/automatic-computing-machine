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
import os
import sys
import textwrap
from typing import Optional

from dll_pq import PythonDLLPQ


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


# ---------------------------------------------------------------------------
# REPL state
# ---------------------------------------------------------------------------

class REPL:
    def __init__(self) -> None:
        self.queue = PythonDLLPQ()
        self._log: list[str] = []
        self._exec_count: int = 0

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def _record(self, msg: str) -> None:
        self._log.append(msg)

    def _show_logs(self, n: int = 10) -> None:
        if not self._log:
            print(dim("  (no operations yet)"))
            return
        entries = self._log[-n:]
        print(f"\n  {bold('Last')} {len(entries)} {bold('of')} {len(self._log)} log entries:\n")
        for i, entry in enumerate(entries, start=len(self._log) - len(entries) + 1):
            print(f"  {dim(str(i).rjust(4))}  {entry}")
        if len(self._log) > n:
            remaining = len(self._log) - n
            print(dim(f"\n  ... {remaining} earlier entries hidden — use 'logs {len(self._log)}' to see all"))
        print()

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------

    def _cmd_add(self, args: list[str], head: bool = False) -> None:
        if len(args) < 2:
            print(red("  Usage: add <task_name> <priority>"))
            return
        task = args[0]
        try:
            priority = int(args[1])
        except ValueError:
            print(red(f"  Priority must be an integer, got: {args[1]!r}"))
            return
        if head:
            ok = self.queue.push_head(task, priority)
        else:
            ok = self.queue.push_tail(task, priority)
        if not ok:
            print(yellow(f"  Task {task!r} already exists in the queue."))
            return
        pos = "head" if head else "tail"
        print(green(f"  + Added {task!r}  priority={priority}  ({pos})"))
        self._record(f"add  {task!r:30s} priority={priority:6d}  @ {pos}")

    def _cmd_exec(self) -> None:
        result = self.queue.pop_max()
        if result is None:
            print(yellow("  Queue is empty — nothing to execute."))
            return
        task, pri = result
        self._exec_count += 1
        print(green(f"  ✓ [{self._exec_count}] Executed {task!r}  (priority={pri})"))
        self._record(f"exec {task!r:30s} priority={pri:6d}")

    def _cmd_swap(self, args: list[str]) -> None:
        if len(args) < 2:
            print(red("  Usage: swap <task1> <task2>"))
            return
        t1, t2 = args[0], args[1]
        p1_before = self.queue.get_priority(t1)
        p2_before = self.queue.get_priority(t2)
        ok = self.queue.swap_nodes(t1, t2)
        if not ok:
            missing = []
            if not self.queue.contains(t1): missing.append(t1)
            if not self.queue.contains(t2): missing.append(t2)
            print(red(f"  Task(s) not found: {', '.join(missing)}"))
            return
        p1_after = self.queue.get_priority(t1)
        p2_after = self.queue.get_priority(t2)
        print(cyan(f"  ⇄ Swapped priorities:"))
        print(cyan(f"    {t1!r:30s} {p1_before} → {p1_after}"))
        print(cyan(f"    {t2!r:30s} {p2_before} → {p2_after}"))
        self._record(
            f"swap {t1!r} ({p1_before}→{p1_after}) ↔ {t2!r} ({p2_before}→{p2_after})"
        )

    def _cmd_peek(self) -> None:
        result = self.queue.peek()
        if result is None:
            print(yellow("  Queue is empty."))
            return
        task, pri = result
        print(f"  Next up: {bold(task)}  {dim(f'(priority={pri})')}")

    def _cmd_list(self) -> None:
        items = self.queue.to_list()
        if not items:
            print(dim("  Queue is empty."))
            return
        print(f"\n  {bold('Queue')} — {len(items)} task(s), head → tail:\n")
        max_pri = max(p for _, p in items)
        for i, (task, pri) in enumerate(items, 1):
            bar_len = int((pri / max(max_pri, 1)) * 20)
            bar = "▓" * bar_len + dim("░" * (20 - bar_len))
            marker = "◀ next" if pri == max_pri else ""
            print(f"  {dim(str(i).rjust(3))}  {task:<32} {cyan(str(pri).rjust(6))}  {bar}  {yellow(marker)}")
        print()

    def _cmd_benchmark(self, args: list[str]) -> None:
        import benchmark as bm
        n = 20_000
        if args:
            try:
                n = int(args[0])
            except ValueError:
                print(red(f"  n must be an integer, got {args[0]!r}"))
                return
        print(f"  Running benchmarks on {n:,} operations …")
        results = bm.run(n=n)
        print(bm.format_results(results, n))
        self._record(f"benchmark n={n}")

    def _cmd_build(self) -> None:
        print("  Compiling Rust extension with maturin …")

        """
        
        Replit wanted this: 
        _venv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".pythonlibs")
        _activate = os.path.join(_venv, "bin", "activate")
        _todo_dir = os.path.dirname(os.path.abspath(__file__))
        cmd = f"bash -c 'source {_activate} && cd {_todo_dir} && maturin develop --release -q'"
        ret = os.system(cmd)
        """

        """
        Replit origal code:
        _venv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".pythonlibs")
        _activate = os.path.join(_venv, "bin", "activate")
        _todo_dir = os.path.dirname(os.path.abspath(__file__))
        cmd = f"bash -c 'source {_activate} && cd {_todo_dir} && maturin develop --release -q'"
        ret = os.system(cmd)
        if ret == 0:
            print(green("  Rust extension compiled successfully."))
            print(dim("  Run 'benchmark' to compare Python vs Rust."))
        else:
            print(red("  Build failed — check output above."))"""
        
        """Our code from Guide:
        print(" Compiling Rust extension with maturin ...")
        # Use current active python executable & sys.executable to run maturin cleanly
        cmd = [sys.executable, "-m", "maturin", "develop", "--release"]
        try:
            res = subprocess.run(cmd, check=True)
            if res.returncode == 0:
                print(" Rust extension compiled successfully.")
        except Exception as e:
            print(f" Build failed: {e}")
        """

    def _cmd_help(self) -> None:
        help_text = f"""
  {bold('DLL Priority Queue Todo App')}
  {dim('─' * 50)}

  {cyan('add')}  <task> <priority>    Push task at tail  (O(1))
  {cyan('top')}  <task> <priority>    Push task at head  (O(1))
  {cyan('exec')}                      Execute highest-priority task  (O(n) scan)
  {cyan('swap')} <task1> <task2>      Swap priorities  — heapq cannot do this  (O(1))
  {cyan('peek')}                      Peek at the next task without removing it
  {cyan('list')}                      Show the full queue (head → tail order)
  {cyan('logs')} [n]                  Show last n log entries  (default: 10)
  {cyan('benchmark')} [n]             Benchmark Python DLL vs Rust extension
  {cyan('build')}                     Compile the Rust extension (maturin develop)
  {cyan('help')}                      Show this help
  {cyan('exit')} / {cyan('quit')}              Quit

  {dim('Why a DLL instead of heapq?')}
  {dim('  heapq.nlargest / heapify: O(n) to rebuild after any priority change.')}
  {dim('  DLL swap_nodes: O(1) — just two integer assignments in the hash-indexed nodes.')}
"""
        print(help_text)

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        print(f"\n  {bold('DLL Priority Queue — Todo App')}")
        print(dim("  Type 'help' for commands, 'build' to compile the Rust extension.\n"))

        while True:
            try:
                raw = input(bold("  > ")).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                print(dim("  Bye."))
                break

            if not raw:
                continue

            parts = raw.split()
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in ("exit", "quit"):
                print(dim("  Bye."))
                break
            elif cmd == "add":
                self._cmd_add(args, head=False)
            elif cmd == "top":
                self._cmd_add(args, head=True)
            elif cmd in ("exec", "execute", "pop"):
                self._cmd_exec()
            elif cmd == "swap":
                self._cmd_swap(args)
            elif cmd == "peek":
                self._cmd_peek()
            elif cmd in ("list", "ls", "queue"):
                self._cmd_list()
            elif cmd == "logs":
                n = 10
                if args:
                    try: n = int(args[0])
                    except ValueError: pass
                self._show_logs(n)
            elif cmd == "benchmark":
                self._cmd_benchmark(args)
            elif cmd == "build":
                self._cmd_build()
            elif cmd == "help":
                self._cmd_help()
            else:
                print(red(f"  Unknown command: {cmd!r}  — type 'help' for a list."))
