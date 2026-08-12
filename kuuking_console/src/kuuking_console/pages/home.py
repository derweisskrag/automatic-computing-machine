from src.kuuking_console.pages.styles import (
    bold, cyan, yellow, green, dim, red
)

def render_home_menu(current_backend: str = "Python DLL") -> str:
    backend_badge = green(f"[{current_backend}]") if "Rust" in current_backend else yellow(f"[{current_backend}]")
    
    header = f"{bold(cyan('Kuuking Console Task Manager'))} {backend_badge}"
    separator = dim("=" * 50)
    
    menu = f"""{header}
{separator}
  {yellow("change page")}. - Changes your page (home/help/dashboard)
  {yellow("1")}. Choose your Tasks (Workspace)
  {yellow("2")}. Add Task
  {yellow("3")}. Execute Highest Priority
  {yellow("4")}. Migrate to Rust
  {yellow("5")}. Change Priority
  {yellow("6")}. View All Tasks
  {yellow("7")}. Exit
  {yellow("8")}. {green("NEW!")} Change your task to different PRIORITY
{separator}
Enter choice {dim("(1-8, or 'help')")}: """
    print(menu)


# MUGGED REPLIT AGENT!
def render_command_help() -> None:
    help_text = f"""
{bold(cyan("Console REPL Commands"))}
{dim("--------------------------------------------------------------------------------")}
  {green("add")} <task> <priority>   Push a task at the tail (default)
  {green("top")} <task> <priority>   Push a task at the head (highest insertion point)
  {green("exec")}                    Pop and execute the highest-priority task
  {green("swap")} <task1> <task2>    Swap priorities of two tasks {dim("(heapq can't do this!)")}
  {green("peek")}                  Show next task without removing it
  {green("list")}                  Show full queue {dim("(head -> tail)")}
  {green("logs")} [n]               Show last n operation log entries {dim("(default 10)")}
  {green("benchmark")} [n]          Benchmark Python DLL vs Rust extension on n ops
  {green("build")}                  Compile Rust extension with maturin
  {green("help")}                  Show this help screen
  {red("exit / quit")}           Exit cleanly
{dim("--------------------------------------------------------------------------------")}
"""
    print(help_text)



