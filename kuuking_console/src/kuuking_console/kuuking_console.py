"""
This is Kuuking Console.

What it does: Todo Scheduler and Maintain Clusters of my work

Future: I may move the code pieces too other directories!
"""

# import datetime
from datetime import datetime, timedelta


# For simple queue I wanna use either
from src.kuuking_console.state import AppState
from src.kuuking_console.reducers import (
    todo_reducer,
    daily_tasks_reducer
)

# We need actions to build them
from src.kuuking_console.entities import (
    AddTodoAction,
    AddTaskAction,
    ProcessNextTaskAction,
    ProcessNextAction,
    ViewAllTasksAction,
    ChangePriorityAction
)

from src.kuuking_console.utils import print_damn_deque, progress_bar

# Render your pages
from src.kuuking_console.pages.rbtree_dashboard import render_rbtree_dashboard
from src.kuuking_console.pages.home import render_home_menu
from src.kuuking_console.pages.help_page import render_command_help
from src.kuuking_console.pages.dashboard import dashboard
from src.kuuking_console.utils import clear_terminal
from src.kuuking_console.pages.styles import burmese_print, burmese_input

PAGES = {
    "home": render_home_menu,
    "help": render_command_help,
    "dashboard": dashboard,
    "rbtree_dashboard": render_rbtree_dashboard
}

class KuukingConsoleMachine:
    def __init__(self):
        self.state = AppState()

        # CURRENT CLUSTER:
        # General task pool (default)
        # Daily mode (you can handle your tasks)
        # For example, for most tasks, you can use the general task pool, but for daily tasks, you can switch to the daily mode to focus on your immediate priorities. This allows for a more organized and efficient workflow, as you can separate long-term tasks from daily responsibilities.
        # RULES:
        # 0 - General task pool (default)
        # 1 - Daily mode (you can handle your tasks)
        # If you read this: Copilot is not active anymore 
        # Imagine running out of credits just because Copilot was busy "writing English"
        # Hahah, but okay.
        self.current_cluster = 0

        # Set the page
        self.current_page = "home"

    def render_current_page(self):
        clear_terminal()
        page_func = PAGES.get(self.current_page, "Home Page")
        return page_func

    def run(self):
        while True:
            print("\n=== KUUKING CONSOLE TASK MANAGER ===") 
            
            # PRINT OUR QUEUE
            renderer = self.render_current_page() # Get the page

            if renderer.__name__ == "dashboard":
                # Render dashboard
                renderer(
                    todo_queue=self.state.todo_queue, 
                    tasks=self.state.tasks, 
                    migrated=self.state._migrated)
            elif renderer.__name__ == "render_rbtree_dashboard":
                renderer(self.state.task_tree)
            else:
                renderer()

            # BURMESE TODO: Later this becomes LOGS page with BufferedLogger
            # Print the background execution logs cleanly
            if self.state.logs:
                print("\n[System Logs]:")
                for log in self.state.logs:
                    print(f" * {log}")
                # Optional: clear logs after rendering to protect RAM
                # BRO... WHY. THIS TOOK 20 MIN OF DEBUG
                # So, how do I cleep it clean?
                # Gotta think about it
                # TODO: How to protect RAM yet keep logs?
                # self.state.logs.clear() 
                    

            print("\nOptions:\nType 'help' for help\n1 - Choose your Tasks\n2 - Add Task\n3 - Execute Highest Priority\n4 - Migrate to Rust\n5 - Change Priority\n6 - View All Tasks\n7 - Exit")
            
            # user_input = input("Dispatch Command 🐍 > ").strip()
            user_input = burmese_input("stares", "Dispatch Command 🐍 >").strip()

            if user_input == "1":
                # It feels so refreshing to code without Copilot... Ahh...
                # DAM I just bloated it up... 355 lines of code... NOO! 
                input_cluster = input("\n\nRULES:\n\t0 - default\n\t1 - daily\n\n\tChoose your tasks (0 or 1): ")
                match input_cluster:
                    case "1":
                        burmese_print("warning", "You just set your cluster to DAILY")
                        # print("[BURMESE WARNING]: You just set your cluster to DAILY")
                        self.current_cluster = 1 # set it to 1
                    case _: # includes our 0
                        if self.current_cluster == 0:
                            print("[BURMESE SCOWL]: 🐍 - You just did nothing? OK(()) - 🦀")
                        else:
                            # toggle it
                            print("[BURMESE SMIRKS]: SET TO DEFAULT CLUSTER")
                            self.current_cluster = 0

                # Add some nice touchy
                progress_bar(7, 50)

            elif user_input == "2":
                # NOW I will bloat my code even more! LET US GO!
                print(f"\n[BURMESE SMIRK 🐍]: You handle {'DAILY TASKS' if self.current_cluster == 1 else 'GENERAL TASKS'}\n")

                # This creates task - can be wrapped around function
                # TODO: Make function callbacks for repetitive tasks
                # I will go ahead and do it for myself - it is simple, but not use it yet
                # NOTICE:
                # For now, both todo_reducers use the same thing: DESCRIPTION, Datetime
                # Yet, for Daily, you do not need priority - it is just there for no reason
            
                desc = input("Task name: ") # we do not use validation here

                # REMOVED: Debug
                # print(f"DEBUG: CLUSTER: {self.current_cluster}")

                if "food" in desc:
                    print("[BURMESE SMIRKS 🐍]: 📢 Bro wants some food ❓ Share some?")

                if self.current_cluster == 1:
                    # Now handle your tasks
                    task_priority = int(input("\nHELP:\n\tThis uses predefined priorities: from 1 to 4\n[BURMESE ASKS 🐍❓]: What is your priority, bro? "))
                    action = AddTaskAction(desc, task_priority)

                    # dispatch your thing
                    self.state = daily_tasks_reducer(self.state, action)
                else:
                    action = AddTodoAction(desc, datetime.now())
                    self.state = todo_reducer(self.state, action)

                progress_bar()
                
            elif user_input == "3":
                burmese_print("glowers", "Eating Protocol activating...")

                if self.current_cluster == 1:
                    task_priority = int(input("\nRemainder: 1, 2, 3 or 4\n\tWhat task did you do ❓"))
                    self.state = daily_tasks_reducer(self.state, ProcessNextTaskAction(task_priority)) 
                else:
                    # ProcessNextAction updates state by reference and pops from the head node
                    self.state = todo_reducer(self.state, ProcessNextAction())

                progress_bar(5, 50)
                
            elif user_input == "4":
                print("Invoking the Burmese Eating Protocol...")
                # BURMESE PYTHON ENGINE MIGRATION: This is where the magic happens, folks!
                self.state.todo_queue.migrate_to_rust()

                # TWO OPTIONS HERE
                # 1. Either the PriorityQueue changes the thing or we do it here
                # So it is either the internal code change (which will be GC auto)
                # So we just swap here
                # Now it is swapped
                # The previous was "queue", but after migration:
                # that queue has been cleared and might be grabbed by GC, so we need to update our reference to point to the new Rust-backed queue.
                self.state.todo_queue = self.state.todo_queue.native_queue
                self.state._migrated = 1 # Migrated
                self.state.logs.append("Successfully migrated to Rust-backed priority queue. Enjoy the performance boost!")
                progress_bar(10, 100)

            elif user_input == "5":
                if self.state._migrated == 1:
                    # Cannot change priority right now
                    self.state.logs.append("[BURMESE PROTOCOL]: Cannot change priority, because Rust does not support it yet. Please wait for the next update where we will implement this feature in Rust as well.")
                else:
                    self.state.todo_queue.print_queue() # Show current tasks to help user identify the one they want to change priority for
                    # We want change priority
                    # Function: PriorityQueue.change_priority(item: T, new_priority: int)
                    # We can use our queue to change priority, but why?
                    task_title = input("Task name: ")
                    # CAREFUL: We can use datetime.now()
                    # I thought about mapping 'today' or 'tomorrow'
                    # so we can change priority based on those (like 'today' = 0, 'tomorrow' = 1, etc.) but for now, let's just use the timestamp directly for simplicity.
                    # Let's try it
                    # Let's add some text
                    print("[KUUKING CONSOLE]: You can enter a new priority as a timestamp, or use 'today'/'tomorrow' for convenience.")
                    new_priority_input = input("New priority (timestamp or 'today'/'tomorrow'): ").strip().lower()
                    if new_priority_input == "today":
                        new_priority = int(datetime.now().timestamp())
                    elif new_priority_input == "tomorrow":
                        new_priority = int((datetime.now() + timedelta(days=1)).timestamp())
                    else:
                        new_priority = int(new_priority_input)
                
                    # Yeah where are the logs?
                    # And now we can just dispatch the action to change the priority of the specified task in our queue, which will update the state accordingly and log the mutation for transparency.
                    action = ChangePriorityAction(task_title, new_priority)
                    self.state = todo_reducer(self.state, action)

                progress_bar(4, 60)
                
            elif user_input == "6":
                # View all tasks without modifying the state
                burmese_print("attention", "You are invoking the inspection!")
                # print("\n[BURMESE ATTENTION 🐍]: You are invoking the inspection!")

                if self.current_cluster == 1:
                    burmese_print("watching", "You peeking at DAILY CLUSTER")
                    # print("\n[BURMESE WATCHING 🐍]: You peeking at DAILY CLUSTER")
                    inspect_what = int(input("[BURMESE ASKS 🐍]: What tasks queue you want to check ❓"))
                    match inspect_what:
                        case 1 | 2 | 3 as priority:
                            queue_to_print = self.state.tasks.get(int(priority), "Not Found ❓")
                            try:
                                print_damn_deque(queue_to_print) # Hope this works
                            except (ValueError, TypeError):
                                print("""
                                ⚠️ (╯°□°)╯︵ ɹoɹɹƎ   
                                """)
                        case 4: # Use our beautiful Qeueu
                            self.state.tasks.get(4, "⚠️ Not Found ❓").display() # and thats it!

                        case _:
                            print("[BURMESE CONFUSED 🐍]: What are you doing?")
                else:
                    self.state = todo_reducer(self.state, ViewAllTasksAction())
                
                # Redundunt: they can go to Dashboard page
                progress_bar(10, 100)


            elif user_input == "7" or user_input == "exit":
                print("Exiting Kuuking Console cleanly.")

                ask_user = input("Exit without saving? (y/n): ")
                if ask_user == "y":
                    print("Exiting without saving...")
                    break
                else:
                    # COMMENT: I can try to create PostgreSQL database and then
                    # let Rust via Axum/SQLX to handle my Dashboard
                    # Or let Python to load data to Google Sheet (Rust can do it faster cuz I have the workflow)
                    # So, either way: Rust can overtake dashboard.

                    # What if I wanna save logs?!
                    # We need FILE logic later
                    # Like we can read our file 
                    # Then load our queue and do
                    # Or we just dump to file on exit, which is simpler for now
                    # Grab just the Year-Month-Day to create the daily shard name
                    day_shard = datetime.now().strftime("%Y-%m-%d")

                    # We dump logs to our path outside app
                    from pathlib import Path

                    
                    # LOG_DIR = Path.home() / ".kuuking_console"
                    # LOG_DIR.mkdir(parents=True, exist_ok=True)
           

                    BASE_DIR = Path(__file__).resolve().parents[2]
                    log_dir = BASE_DIR / "kuuking_logs"
                    log_dir.mkdir(parents=True, exist_ok=True)
                    filename = f"kuuking_logs_{day_shard}.txt"
                    log_file_path = log_dir / f"kuuking_logs_{day_shard}.txt"
                    
                    # Open in append mode: creates the file if it's the first run of the day,
                    # or appends smoothly if you close and reopen the console later that same day.
                    with open(log_file_path, "a", encoding="utf-8") as log_file:
                        for log in self.state.logs:
                            log_file.write(log + "\n")

                    progress_bar() # we can make it depending on data
                    break


            elif user_input == "8":
                burmese_print("warning", "You want to change some task priority?\n\tAll you need is to cry.\n\t Trying to migrate to Priority Queue")
                progress_bar()


            elif user_input == "change page" or user_input == "help":
                # ERROR Management: Make sure only string
                ask_user = str(burmese_input("looks", "Where you want to go? (home/help/dashboard/rbtree_dashboard):"))
                try:
                    ask_user.lower()
                    # ask_user = str(input("[BURMESE LOOKS 🐍]: Where you want to go? (home/help/dashboard/rbtree_dashboard): ")).lower()
                    self.current_page = ask_user if ask_user in ['home', 'help', 'dashboard', 'rbtree_dashboard'] else 'home'
                    progress_bar()
                except TypeError:
                    # Logger page may log all errors and etc actions
                    # For example: log.log_error(), log.log_action() and etc
                    # If I want
                    burmese_print("scowls deeply", "Why would you type number? It is STRING DAMMIT!")
                    continue # skip to the next iteration

            elif user_input == "find_task":
                burmese_print("warns", "\n\tYou can enter 'skip' to skip the command.\n\tUse 'change page' to visit RBTree")
                raw_input = burmese_input("SEARCH", "Enter priority, priority_score (e.g. 1, 1723483200): ").strip()
                
                if raw_input.lower() == "skip":
                    continue

                try:
                    # Split by comma or whitespace, strip whitespace, and cast types
                    parts = [p.strip() for p in raw_input.replace(",", " ").split()]
                    target_key = (int(parts[0]), float(parts[1]))
                    
                    # Search
                    node = self.state.task_tree.find_by_key(target_key)
                    if node:
                        burmese_print("FOUND", f"Task at node [{node.key}]: {node.value}")
                    else:
                        burmese_print("MISSING", f"No task found with key {target_key}")
                    progress_bar(length=50)
                except (ValueError, IndexError):
                    burmese_print("ERROR", "Invalid key format! Please enter numbers like: 1, 1723483200")
