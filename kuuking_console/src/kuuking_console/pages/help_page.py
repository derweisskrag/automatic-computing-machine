from src.kuuking_console.pages.styles import (
    bold, cyan, yellow, dim, green, magenta
)

help_page = f"""{bold(cyan("=== Help Information ==="))}
{yellow("change page")}. - Changes your page (home/help/dashboard)
{yellow("1")} - Choose your Tasks (Workspace)
{yellow("2")} - Add Task
{yellow("3")} - Execute Highest Priority
{yellow("4")} - Migrate to Rust
{yellow("5")} - Change Priority
{yellow("6")} - View All Tasks
{yellow("7")} - Exit
{yellow("8")} - {green("NEW!")} Change your task to different PRIORITY

{dim("--------------------------------------------------------------------------------")}

This is a basic kit of the program. Here is what each option does:

{bold(yellow("1 - Choose your Tasks:"))} Allows you to select tasks from the current queue to focus on. You can prioritize which tasks to work on next.
Namely, instead of PriorityQueue and datetime as priorities, we can try handle basic dailies. The idea was that it is difficult to assign tasks based on datetime. That is why I wanted to try using predefined priorities (like 1, 2, 3) to represent high, medium, and low priority tasks. This way, users can easily categorize their tasks without worrying about exact timestamps.
That is, you can choose your workspace.

{bold(yellow("2 - Add Task:"))} Lets you add a new task to the queue with a description and due date. The task will be added to the appropriate priority level based on its due date.

{bold(yellow("3 - Execute Highest Priority:"))} Pops the highest priority task from the queue and marks it as executed. This helps you focus on completing tasks in order of importance.

{bold(yellow("4 - Migrate to Rust:"))} Switches the underlying queue implementation to a Rust-backed priority queue for improved performance. This is part of the Burmese Eating Protocol, which optimizes task management by leveraging Rust's efficiency.

{bold(yellow("5 - Change Priority:"))} Allows you to change the priority of an existing task in the queue. You can specify the task name and the new priority level.

{bold(yellow("6 - View All Tasks:"))} Displays all tasks currently in the queue without modifying the state. This is useful for reviewing your tasks and planning your workflow.

{bold(yellow("7 - Exit:"))} Exits the console application cleanly, saving logs to a file for future reference. The logs will be saved in a file named {magenta("kuuking_logs_YYYY-MM-DD.txt")}, where YYYY-MM-DD is the current date.

{bold(yellow("8 - Change Priority (NEW!):"))} Quick-shift an existing task to a different priority level dynamically.
"""

def render_command_help():
    print(help_page)