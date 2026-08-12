"""
Benchmark: Python DLL priority queue vs. Rust extension (via Maturin/PyO3).

Operations compared
-------------------
  push_head   — N insertions at the front
  push_tail   — N insertions at the back
  swap_nodes  — N/2 priority swaps on a pre-filled queue

All timings are wall-clock via time.perf_counter().
"""

from __future__ import annotations
import time
import random
from typing import Dict, Callable, Optional

from dll_pq import PythonDLLPQ

_RUST_AVAILABLE: Optional[bool] = None


def _rust_available() -> bool:
    global _RUST_AVAILABLE
    if _RUST_AVAILABLE is None:
        try:
            import todo_app_rs  # noqa: F401
            _RUST_AVAILABLE = True
        except ImportError:
            _RUST_AVAILABLE = False
    return _RUST_AVAILABLE


def _task(i: int) -> str:
    return f"task_{i:07d}"


# ---------------------------------------------------------------------------
# Benchmark helpers
# ---------------------------------------------------------------------------

def _time(fn: Callable, n: int) -> float:
    t0 = time.perf_counter()
    fn(n)
    return time.perf_counter() - t0


# Python benchmarks --------------------------------------------------------

def _py_push_head(n: int) -> None:
    q = PythonDLLPQ()
    for i in range(n):
        q.push_head(_task(i), random.randint(1, 1_000_000))


def _py_push_tail(n: int) -> None:
    q = PythonDLLPQ()
    for i in range(n):
        q.push_tail(_task(i), random.randint(1, 1_000_000))


def _py_swap(n: int) -> None:
    q = PythonDLLPQ()
    for i in range(n):
        q.push_tail(_task(i), i)
    for i in range(0, n - 1, 2):
        q.swap_nodes(_task(i), _task(i + 1))


# Rust benchmarks ----------------------------------------------------------

def _rs_push_head(n: int) -> None:
    from todo_app_rs import RustDLLPQ
    q = RustDLLPQ()
    for i in range(n):
        q.push_head(_task(i), random.randint(1, 1_000_000))


def _rs_push_tail(n: int) -> None:
    from todo_app_rs import RustDLLPQ
    q = RustDLLPQ()
    for i in range(n):
        q.push_tail(_task(i), random.randint(1, 1_000_000))


def _rs_swap(n: int) -> None:
    from todo_app_rs import RustDLLPQ
    q = RustDLLPQ()
    for i in range(n):
        q.push_tail(_task(i), i)
    for i in range(0, n - 1, 2):
        q.swap_nodes(_task(i), _task(i + 1))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run(n: int = 20_000, seed: int = 42) -> Dict[str, float]:
    """
    Run all benchmarks and return a dict of label → seconds.

    Keys: python_push_head, python_push_tail, python_swap_nodes
          rust_push_head,   rust_push_tail,   rust_swap_nodes  (if available)
    """
    random.seed(seed)

    results: Dict[str, float] = {}

    py_ops = [
        ("python_push_head",  _py_push_head),
        ("python_push_tail",  _py_push_tail),
        ("python_swap_nodes", _py_swap),
    ]
    for label, fn in py_ops:
        results[label] = _time(fn, n)

    if _rust_available():
        rs_ops = [
            ("rust_push_head",  _rs_push_head),
            ("rust_push_tail",  _rs_push_tail),
            ("rust_swap_nodes", _rs_swap),
        ]
        for label, fn in rs_ops:
            results[label] = _time(fn, n)

    return results


def format_results(results: Dict[str, float], n: int) -> str:
    """Render a compact comparison table."""
    ops = ["push_head", "push_tail", "swap_nodes"]
    lines: list[str] = []

    bar_w = 30
    max_time = max(results.values()) if results else 1.0

    lines.append(f"\n  Benchmark — {n:,} operations each\n")
    lines.append(f"  {'Operation':<14}  {'Python':>10}  {'Rust':>10}  {'Speedup':>8}  Bar (Python vs Rust)")
    lines.append("  " + "-" * 72)

    for op in ops:
        py_t = results.get(f"python_{op}")
        rs_t = results.get(f"rust_{op}")

        py_str = f"{py_t*1000:.1f} ms" if py_t is not None else "—"
        rs_str = f"{rs_t*1000:.1f} ms" if rs_t is not None else "n/a"

        if py_t and rs_t and rs_t > 0:
            speedup = f"{py_t / rs_t:.1f}×"
        else:
            speedup = "—"

        if py_t:
            py_bars = int((py_t / max_time) * bar_w)
        else:
            py_bars = 0
        if rs_t:
            rs_bars = int((rs_t / max_time) * bar_w)
        else:
            rs_bars = 0

        py_bar = "█" * py_bars
        rs_bar = "░" * rs_bars
        bar = f"[{py_bar:<{bar_w}}] [{rs_bar:<{bar_w}}]"

        lines.append(f"  {op:<14}  {py_str:>10}  {rs_str:>10}  {speedup:>8}  {bar}")

    if not _rust_available():
        lines.append("\n  (Rust extension not compiled yet — run 'build' to compile it)")

    lines.append(f"\n  █ = Python  ░ = Rust")
    return "\n".join(lines)
