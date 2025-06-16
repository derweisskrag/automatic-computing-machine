"""
This module demonstrates how to import another Python module by 
modifying `sys.path` manually using `os.path.join(os.getcwd(), "..")`.

This approach is sometimes referred to as a "magic method" because it
lets Python dynamically discover sibling or parent directories at runtime.

Use case: perfect for quick CLI tools, local testing, or scripting
when you don't want to configure full package paths or use `importlib`.
"""

import os
import sys

# Get the current working directory — i.e., where the script is launched from
cwd = os.getcwd()
print(f"📁 Current working directory: {cwd}")

# Assume the target module is located two levels up from current directory
# For example, if you're in 'playground/common', we want to reach project root
# Run from vim: :!python %
# Run from CLI: cd playground/common && python use_sys_path_append.py
parent_dir = os.path.abspath(os.path.join(cwd, "../.."))
sys.path.append(parent_dir)  # Make the parent directory discoverable for imports

# Try importing a module from that parent directory
# The file should be named `test_file.py` and contain a variable `greetings`
try:
    import test_file
    print(f"✅ Successfully imported: {test_file.greetings}")
except ImportError as e:
    print(f"❌ Import failed: {e}")
except AttributeError:
    print("⚠️ Module 'test_file' imported, but 'greetings' was not found.")
finally:
    if parent_dir in sys.path:
        print(f"🧹 Removing {parent_dir} from sys.path")
        sys.path.remove(parent_dir)
    else:
        print(f"⚠️ {parent_dir} not found in sys.path")
