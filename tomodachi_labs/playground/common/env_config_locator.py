"""
This module tries to use pathlib to actually reuse the configuration file, 
that we use for the tests.

However, I must assume that different environemnts inside our codebase may 
need different configuration files, and as such, it is not always possible
to reuse the config.py
"""

import pathlib

# get the root directory
root_dir = pathlib.Path(__file__).parents[2].resolve()

# from root we must find the config file
config_path = (root_dir / "tomodachi_core" / "config_development" / "config.py").resolve()

# resolve can throw an error: file does NOT exist or Location
# let us print
# print(config_path)
