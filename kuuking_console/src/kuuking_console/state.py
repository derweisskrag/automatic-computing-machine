from collections import deque
from dsa_kuuking.queues.queue.implementation.queue_list import Queue
from dsa_kuuking.queues.priority_queue.implementation.priority_queue import PriorityQueue
from dsa_kuuking.trees.red_black_tree.implementation.red_black_tree import RBTree

from src.kuuking_console.entities import Todo

class AppState:
    def __init__(self):
        # Custom thesis library is the core database of the application state
        # Do I bloat memory right now? Feeling lazy
        # Cuz later we must try Buckets thing
        # self.buckets = {}
        # Let try it for now, cuz I want to have it 
        # a feature that can change my tasks cluster
        # But treat this like every task
        # Rules:
        # DEQUE - Important tasks (high priority)
        # Queue - Trial (stress test) for low priority tasks (like a backlog)
        # Right now we are using Todo[T] and we mean that our priorities are the keys of our thing
        # So, our tasks are stored in queues/deque that has NO PRIORITY by itself, so we skip our 
        # PriorityQueue[T] for now, but we can use it later if we want to have a more complex priority system. For now, we just use the priority_score property of our Todo class to determine the order of execution.
        self.tasks = { # I avoid using my Queue for now (which uses List[T])
            1: deque(),  # High priority tasks
            2: deque(),  # Medium priority tasks
            3: deque(),   # Low priority tasks
            4: Queue()   # Optional: Extra low priority tasks 
            # Hell, nah we cannot use Rust's queue here because
            # Rust wants the priority, but we cannot fix it
            # Hence, I must create Rust's queue without priority too - later
            # Or: READ and Find Rust's crates that solve this too - gain reading someone else's code
        }

        # MONSTER
        # Experimental: LET'S GO DAMMIT
        self.task_tree = RBTree[Todo]()


        # Treat this like day task cluster boss
        # E.g., handle house choirs (instead of listing all tasks)
        # Because it does not allow to switch priority easily right now
        self.todo_queue = PriorityQueue[Todo]()
        self.logs = []
        self._migrated = 0 # bit to track migration status
