from sys import stdout

from src.kuuking_console.entities import Todo
from typing import Deque

# HELPER METHOD: I place it here for now
# To avoid UTILITY CLASS MEME!!!
def print_damn_deque(your_deque: Deque) -> Todo:
    for _, todo in enumerate(your_deque):
        yield todo # Yikes


def clear_terminal():
    """Flushes output, clears visible screen, AND purges the scrollback buffer."""
    # \033[H  -> Move cursor to top-left (0,0)
    # \033[2J -> Clear entire visible screen
    # \033[3J -> Clear scrollback buffer (prevents duplication on small windows)
    stdout.write("\033[H\033[2J\033[3J")
    stdout.flush()


# Import time and styles
import time
from src.kuuking_console.pages.styles import bold, cyan, green, dim

def progress_bar(duration: float = 5.0, length: int = 30) -> None:
    """Displays a smooth ANSI progress bar over a given duration in seconds."""
    start_time = time.time()
    
    while True:
        elapsed = time.time() - start_time
        progress = min(1.0, elapsed / duration)
        
        filled_length = int(length * progress)
        # Use simple ASCII characters: '=' for filled, '-' for remaining
        bar = "=" * filled_length + "-" * (length - filled_length)
        percent = int(progress * 100)
        
        # '\r' resets the cursor to the start of the line without starting a new line
        stdout.write(
            f"\r{dim('[')}{green(bar)}{dim(']')} {bold(cyan(f'{percent:3d}%'))}"
        )
        stdout.flush()
        
        if progress >= 1.0:
            break
            
        time.sleep(0.05)  # Update ~20 times per second for smooth rendering
        
    print()  # Move to the next line when finished