"""
Pure-Python doubly-linked list priority queue.

Design goals
------------
* push_head / push_tail  — O(1)  insert at either end
* swap_nodes             — O(1)  swap priority values of two named tasks
                                 (heapq cannot do this without a full rebuild)
* pop_max                — O(n)  linear scan to find the highest priority node
* peek                   — O(n)  same scan, no removal

The DLL gives us O(1) unlink once we have the node pointer, which is why
swap_nodes is fast: we look up both nodes in a hash table and swap their
`.priority` fields in place — no structural changes needed.
"""

from __future__ import annotations
from typing import Optional, Tuple, List, Dict


class Node:
    """A single node in the doubly-linked list."""

    __slots__ = ("task", "priority", "prev", "next")

    def __init__(self, task: str, priority: int) -> None:
        self.task: str = task
        self.priority: int = priority
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class PythonDLLPQ:
    """
    Doubly-linked list priority queue.

    Invariants
    ----------
    * Nodes are stored in insertion order (head = oldest or most-recently
      pushed to head; tail = most-recently pushed to tail).
    * `_index` maps task-name → Node for O(1) swap and existence checks.
    * There are no duplicate task names.
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._index: Dict[str, Node] = {}
        self._size: int = 0

    # ------------------------------------------------------------------
    # Insertion
    # ------------------------------------------------------------------

    def push_head(self, task: str, priority: int) -> bool:
        """Insert *task* at the front of the list.  O(1)."""
        if task in self._index:
            return False
        node = Node(task, priority)
        self._index[task] = node
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1
        return True

    def push_tail(self, task: str, priority: int) -> bool:
        """Insert *task* at the back of the list.  O(1)."""
        if task in self._index:
            return False
        node = Node(task, priority)
        self._index[task] = node
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1
        return True

    # ------------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------------

    def _unlink(self, node: Node) -> None:
        """Remove *node* from the DLL; caller must handle _index / _size."""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None

    def pop_max(self) -> Optional[Tuple[str, int]]:
        """Remove and return (task, priority) of the highest-priority node.  O(n)."""
        if self.head is None:
            return None
        best = self.head
        cur = self.head.next
        while cur is not None:
            if cur.priority > best.priority:
                best = cur
            cur = cur.next
        self._unlink(best)
        del self._index[best.task]
        self._size -= 1
        return (best.task, best.priority)

    # ------------------------------------------------------------------
    # The key operation heapq cannot do
    # ------------------------------------------------------------------

    def swap_nodes(self, task1: str, task2: str) -> bool:
        """
        Swap the *priority values* of two tasks.  O(1).

        heapq cannot do this because priority determines heap position;
        changing a priority requires removing and re-inserting the element
        (O(log n) per node, plus O(n) if you have to locate it first).
        Here we just flip two integers in the hash-table-reachable nodes.
        """
        n1 = self._index.get(task1)
        n2 = self._index.get(task2)
        if n1 is None or n2 is None:
            return False
        n1.priority, n2.priority = n2.priority, n1.priority
        return True

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def peek(self) -> Optional[Tuple[str, int]]:
        """Return (task, priority) of the max-priority node without removing it.  O(n)."""
        if self.head is None:
            return None
        best = self.head
        cur = self.head.next
        while cur is not None:
            if cur.priority > best.priority:
                best = cur
            cur = cur.next
        return (best.task, best.priority)

    def get_priority(self, task: str) -> Optional[int]:
        """Return the current priority of *task*, or None if not found."""
        node = self._index.get(task)
        return node.priority if node else None

    def contains(self, task: str) -> bool:
        return task in self._index

    def to_list(self) -> List[Tuple[str, int]]:
        """Return all (task, priority) pairs in linked order (head → tail)."""
        result: List[Tuple[str, int]] = []
        cur = self.head
        while cur is not None:
            result.append((cur.task, cur.priority))
            cur = cur.next
        return result

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self.head = self.tail = None
        self._index.clear()
        self._size = 0
