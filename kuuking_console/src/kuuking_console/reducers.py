import sys
from datetime import datetime, timedelta

# Import the dam class
from src.kuuking_console.entities import (
    Todo,
    Action,
    AddTaskAction,
    AddTodoAction,
    ProcessNextAction,
    ProcessNextTaskAction,
    ViewAllTasksAction,
    ChangePriorityAction
)

from src.kuuking_console.state import AppState
from src.kuuking_console.utils import clear_terminal

def clear_terminal():
    """Flushes the terminal output and clears the screen for a clean display of the current state.

    Alternatively: use os.system('cls' if os.name == 'nt' else 'clear') for a more platform-independent approach, but this method is faster and avoids spawning a new process.
    
    """
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()


# WE PROBABLY NEED SEPARATE REDUCER for this unless 
# I manage to handle both in one but i feel like it will be messy, so let's keep it clean and separate for now. This reducer handles the state transitions based on the dispatched actions, updating the todo_queue and logs accordingly.
def daily_tasks_reducer(state: AppState, action: Action) -> AppState:
    """Reducer for daily tasks cluster, handling actions related to adding tasks to specific priority queues and logging the operations.
    
    """
    match action:
        case AddTaskAction(description, priority):  # let us check definition
            task = Todo(description, datetime.now() + timedelta(days=priority))  # Using priority as days until due
            if priority == 4:
                state.tasks[priority].enqueue(task)
            else:
                state.tasks[priority].append(task)

            # Create Tuple Key - Trying To Save memory
            tree_key = (priority, task.priority_score)
            state.task_tree.add(tree_key, task)
            state.logs.append(f"Added task '{description}' to priority {priority} queue.")
        case ProcessNextTaskAction(priority):
            target_queue = state.tasks.get(priority)

            if not target_queue or len(target_queue) == 0:
                state.logs.append(f"[BURMESE SCOWLS 🐍]: Cannot execute—Cluster {priority} is completely empty!")
                return state
              
            if priority == 4:
                finished_task = target_queue.dequeue().unwrap()
                state.logs.append(f"Just executed {finished_task.description} from Queue")
            else:
                finished_task = target_queue.popleft()
                state.logs.append(f"Just executed {finished_task.description} from {priority} Cluster")

            state.task_tree.remove((priority, finished_task.priority_score))
        case _:
            state.logs.append("Unknown action dispatched to daily_tasks_reducer.")

    
    return state


def todo_reducer(state: AppState, action: Action) -> AppState:
    """Todo reducer for general cluster tasks
    """
    match action:
        case AddTodoAction(description, due_date):
            todo_item = Todo(description, due_date)
            priority = todo_item.priority_score  # Using the optimized property
            
            if state._migrated == 1:
                state.logs.append(f"[BURMESE PROTOCOL]: Adding task '{description}' with priority {priority} to Rust-backed queue.")
                state.todo_queue.push(priority, todo_item.description)  # Assuming the Rust-backed queue has a push method
            else:
                state.todo_queue.enqueue(todo_item, priority)
                
            # Brilliant memory optimization on my part: 
            # Appending strings to logs avoids heavy terminal re-rendering operations!
            state.logs.append(f"Successfully tracked task: {description}")
            
        case ProcessNextAction(): # Now you understand
            # Basically, right now you got idea
            # to change priority
            # Imagine that this is this thing
            # Now you can go ahead and do
            # ProcessNextAction(new_priority=5) or something
            # Basically. It is kinda Rust enum variant, but in Python, we can just use dataclass and pattern
            # So new tasks can be here
            # But we do not need more, so I guess we can add
            # I do not know. I think I nailed it
            # ProcessNextAction(ActionType=CHANGE_PRIORITY, item=Todo, new_priority=5) or something
            
            # BURMESE PROTOCOL
            if state._migrated == 1:
                state.logs.append("[BURMESE PROTOCOL]: Processing next task using Rust-backed queue...")
                completed_task = state.todo_queue.pop()  # Assuming the Rust-backed queue has a pop method
                if completed_task:
                    state.logs.append(f"Executed: {completed_task}")
            else:
                if not state.todo_queue.is_empty():
                    completed_task = state.todo_queue.dequeue()
                    state.logs.append(f"Executed: {completed_task}")
                else:
                    state.logs.append("No pending micro-tasks available in memory.")

            

        case ChangePriorityAction(task_title, new_priority):
            state.todo_queue.change_priority(task_title, new_priority)
            state.logs.append(f"Mutated priority for task: {task_title} to {new_priority}")

        case ViewAllTasksAction():
            if state._migrated == 1:
                state.logs.append("[BURMESE PROTOCOL]: Cannot view all tasks using Rust-backed queue...")
            else:
                # This action is just for viewing all tasks without modifying the state, so we can simply
                # Let us actually modify it now
                # How it was: we call this and program prints the entire logs and then actual content of queue is buried in the logs, which is not ideal for user experience. Instead, we can directly print the queue contents to the console for better visibility.
                # So, let us
                # Does Git Bash let yes.
                # We can do Python's what it was - Sys or os to get access to terminal we are in...
                # But it also means that we may exit the program, right? - Key point to think later
                # It is actually a good point to think about.
                # SO: OUR LOGS are because GLOBAL STATE, we always PRINT LOGS
                # But if we want to look at the contents and avoid LOGS 
                # We can try
                # Nope, it does not work - Python Shell uses Built-in and wrappers around Git Bash, so natively
                # in our code we cannot do it
                # clear() # clear the terminal to avoid clutter and then print the queue contents directly for better visibility. This way, users can focus on the current state of their tasks without being overwhelmed by previous logs.
                # WHAT WE CAN DO is 
                clear_terminal() # Clear the terminal to avoid clutter and then print the queue contents directly for better visibility. This way, users can focus on the current state of their tasks without being overwhelmed by previous logs.
                # NOW WE MAY WANT TO print the queue contents directly for better visibility. This way, users can focus on the current state of their tasks without being overwhelmed by previous logs.
                state.todo_queue.print_queue()

    return state