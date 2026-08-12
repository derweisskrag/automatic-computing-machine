#!/usr/bin/env python3
"""
Entry point for the DLL Priority Queue Todo App.

Run directly:   python main.py
Or from repo:   python todo_app/main.py
"""

import sys
import os

# Ensure this package directory is on the path when invoked as a script
_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

from repl import REPL # HA REPLIT DAMMIT <- this should be at the top of file.

if __name__ == "__main__":
    REPL().run()
