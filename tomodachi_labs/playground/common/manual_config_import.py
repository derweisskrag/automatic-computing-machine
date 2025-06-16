"""
This module imports the environmental variable from the configuration (nearby file) and then calls other modules from the tomodachi core.

NB! Please, make sure you installed the tomodachi_core!
"""

from tomodachi_core.tomodachi.services import PandasService
from shared_env_setup import CSV_PATH # different names space?

# What I mean is -> we imported the same variable but in the
# different location & environment.
service = PandasService(CSV_PATH)

with service.connection() as df:
    print(df.head())


# Interesting part: we reuse the config file defined earlier 
# NB! The config is NOT deployed. Our package code does NOT use
# the CONFIG. Only tests. Tests are NOT uploaded to package.
from env_config_locator import config_path, root_dir
import importlib.util
import sys

# import the module and get the path
# sys.path.insert(0, str(config_path.parent)) # because we go from file itself to parent
spec = importlib.util.spec_from_file_location("config", str(config_path))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


# do the same as previously
relative_path = config.CSV_PATH # the string

# get the abs path
absolute_csv = (root_dir / relative_path).resolve()


# try to read the same data frame and log its tail
with PandasService(absolute_csv).connection() as df:
    print(df.tail())
