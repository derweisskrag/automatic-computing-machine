from functools import wraps
from dataclasses import fields, is_dataclass

from tomodachi_core.common_types.test_people import TestPeople
from tomodachi_core.tomodachi.utils.contexts.contexts import json_ctx

def validate(data_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if not is_dataclass(data_type):
                raise TypeError(f"{data_type} is not a dataclass")

            expected_fields = {f.name for f in fields(data_type)}

            if not isinstance(result, dict):
                raise ValueError("Expected a dictionary as result")

            missing = expected_fields - result.keys()
            if missing:
                raise ValueError(f"Missing fields in data: {missing}")

            return result
        return wrapper
    return decorator


@validate(data_type=TestPeople)
def load_test_people_json(path: str) -> dict:
    with json_ctx(path) as ctx:
        return ctx.load_data()

