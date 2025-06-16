from typing import Callable, Union
from functools import wraps

class Result[T, E]:
    def __init__(self, value: Union[T, None] = None, error: Union[T, None] = None):
        self.value = value
        self.error = error


    def is_ok(self) -> bool:
        return self.error is None
    

    def is_err(self) -> bool:
        return self.error is not None
    

    def unwrap(self) -> T:
        if self.error:
            raise Exception(self.error)
        return self.value
    
    def unwrap_or(self, default_value: T) -> T:
        return self.value if self.is_ok() else default_value
    
    def map(self, func: Callable[[T], T]) -> 'Result[T, E]':
        if self.is_ok():
            try:
                return Ok(value=func(self.value))
            except Exception as e:
                return Err(error=e)
        else:
            return Err(error=self.error)
    

    def map_err(self, func: Callable[[E], E]) -> 'Result[T, E]':
        if self.is_err():
            return Err(error=func(self.error))
        return self
    

    def and_then(self, func: Callable[[T], 'Result[T, E]']) -> 'Result[T, E]':
        if self.is_ok():
            try:
                result = func(self.value)
                return Ok(result) if not isinstance(result, Result) else result
            except Exception as e:
                return Err(error=e)
        else:
            return Err(error=self.error)
    

    def expect(self, msg: str) -> T:
        if self.is_err():
            raise Exception(f"{msg}: {self.error}")
        return self.value


    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return self.value if self.is_ok() else func()


    def __repr__(self):
        return f"Ok({self.value})" if self.is_ok() else f"Err({self.error})"
    
    
    def __str__(self):
        return self.__repr__()
    

class Ok[T](Result[T, None]):
    def __init__(self, value: T) -> None:
        super().__init__(value=value)

class Err[T](Result[None, T]):
    def __init__(self, error: T) -> None:
        super().__init__(error=error)


def result_wrapper[T, E](func: Callable[..., T]) -> Callable[..., Result[T, E]]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Result[T, Exception]:
        try:
            return Ok(func(*args, **kwargs))
        except Exception as e:
            return Err(e)
    return wrapper