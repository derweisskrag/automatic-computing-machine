"""
This module contains the implementation of reading the file.

It is very similar to `analyze.py` but here, we do not read `.env`, instead,
we read the python file located in the root (you can create any, as I remove any junk files soon).


To run this code, you have to create the file in the root directory
and add the following code to it:

```python
greetings = "Hello, world!"
```
Then, run this file and you should see the output of the `greetings` variable.

You can add any content you want, but in that case, you would have to modify the code.
"""

import pathlib

# get root dir
root_dir = pathlib.Path(__file__).parents[1].resolve()

# So, now you know: we must find the absolute path
# Expect: error again?
# If error: we have to use `sys.path.append` -> it will resolve
# Or we have to use import lib
path_to_test_file = (root_dir / "test_file.py").resolve()

# try to import the file
# from test_file import greetings

# import the `importlib.util`
import importlib.util

# read and load the module using the path to it
# sys.path.insert(0, str(path_to_test_file.parent))
if path_to_test_file.exists():
    spec = importlib.util.spec_from_file_location("test_file", str(path_to_test_file))
    test_file = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_file)

    # print the content
    print(f"Import from 'test_file': {test_file.greetings}")
else:
    print(f"File {path_to_test_file} does not exist.")

