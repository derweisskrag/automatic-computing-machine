import importlib.util

def load_config(config_path):
    try:
        spec = importlib.util.spec_from_file_location("config", str(config_path))
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        return config
    except Exception as e:
        raise RuntimeError(f"Error loading config from {config_path}: {str(e)}")