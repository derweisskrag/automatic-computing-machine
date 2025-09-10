# Finding the path of my config or importing the local env?

This was an interesting problem to tackle on. So far I found two solutions to this problem:

- re-read the .env
- don't re-read the .env, but instead find the config.py and import from there

The second one is more tricker, but boils down to the same trick.

## Problem 

We wanna to play with our code and execute it within `py` module or `.ipynb` Jupyter book. Our code 
is located in the different scope: `tomodachi_core.tomodachi`. There we find the code. However, we 
attempt to run the code in `./playground` or `./analysis` - a different directory. We can use the built-in module for this purpose: ***importlib.uitl***. Once we load the module, we want to resolve the path for, say, path variables if there are any (e. g., the path to the **csv** file needs to be combined with the root path as shown in the `./playground/consume_config.py` and `./playground/asb_path`). If it is a function or a class, I believe it will work just fine. We will attempt it later - I test it tomorrow.

In other words, we want to import the .env from the config inside the core directory.

## Solution found 

The solution is present in those files. As such, we can import and test the code without releasing, and if released, it simplifies things to just import. The only problem was getting the .env

```python
# import the pathlib to work with paths
import pathlib
from dotenv import load_dotenv

# get the root directory
root_dir = pathlib.Path(__file__).parents[1].resolve()

# re-read the .env
load_dotenv(root_dir / ".env.local")

# get the csv path
CSV_PATH = os.getenv("CSV_PATH", "Fallback: No file named CSV_PATH was found")

# Combine the paths - it works:
absolute_path_to_csv = (root_dir / CSV_PATH).resolved()

# You can use this absolute path now
# We re-read the env file efficiently
```

However, if we do not want to re-read the .env file (for some reason), we can find the config and import from there, and then again, we would have to use the same logic (combining the root directory and relative one):

```python
import pathlib
import importlib.util
import sys

# get root
root_dir = pathlib.Path(__file__).parents[1].resolve()

# specify path to the module
config_path = (root_dir / "tomodachi_core" / "config_development" / "config.py").resolve()

# From this point, we have to use the sys and importlib:
sys.path.insert(0, str(config_path.parent))
spec = importlib.util.spec_from_file_location("config", str(config_path))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

# get the path from the config
CSV_PATH = config.CSV_PATH

# get the absolute path
absolute_path_to_csv = (root_dir / CSV_PATH).resolve()

```

That is the entire logic here.I would prefer the first approach, as it sounds easier to me, and the second approach if I did not want to re-deploy everytime. 

## Conclusion

If we want to just read the path from .env: re-read the env and that is fine.

If you want to load your module, use importlib.util

