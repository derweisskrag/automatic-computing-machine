from typing import TypeVar, Generic, Callable, NoReturn, Any

"""
Please, refer to here: (https://github.com/rust-lang/rust/blob/449c801783ecef2aad3ae03d6c9e4ac007de7d4b/library/core/src/option.rs#L606)

And if you want Python docs: 

tomodachi/docs

"""


# Define a TypeVar for generics, similar to Rust's <T>
T = TypeVar('T')

class Option(Generic[T]):
    """
    Represents an optional value: either a value of type T or no value.
    This is the base class for Some and None.
    """
    def is_some(self) -> bool:
        """
        Returns True if the option is Some, False otherwise.
        """
        raise NotImplementedError

    def is_none(self) -> bool:
        """
        Returns True if the option is None, False otherwise.
        """
        raise NotImplementedError

    def is_some_and(self, predicate: Callable[[T], bool]) -> bool:
        """
        Returns True if the option is Some and the value inside of it
        satisfies the predicate.
        """
        raise NotImplementedError

    def unwrap(self) -> T:
        """
        Unwraps the option, yielding the content of a Some.
        Panics if the value is a None.
        """
        raise NotImplementedError

    def expect(self, msg: str) -> T:
        """
        Unwraps the option, yielding the content of a Some.
        Raises an error with the given message if the value is a None.
        """
        raise NotImplementedError

    def map(self, func: Callable[[T], Any]) -> 'Option[Any]':
        """
        Maps an Option<T> to Option<U> by applying a function to a contained value.
        """
        raise NotImplementedError

    def filter(self, predicate: Callable[[T], bool]) -> 'Option[T]':
        """
        Returns None if the option is None, otherwise calls `predicate`
        with the wrapped value and returns Some(T) if `predicate` returns true,
        and None otherwise.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)



class Some(Option[T]):
    """
    Represents the presence of a value.
    """
    def __init__(self, value: T = None):
        self._value = value

    def is_some(self) -> bool:
        return True

    def is_none(self) -> bool:
        return False

    def is_some_and(self, predicate: Callable[[T], bool]) -> bool:
        return predicate(self._value)

    def unwrap(self) -> T:
        return self._value

    def expect(self, msg: str) -> T:
        return self._value

    def map(self, func: Callable[[T], Any]) -> 'Option[Any]':
        return Some(func(self._value))

    def filter(self, predicate: Callable[[T], bool]) -> 'Option[T]':
        if predicate(self._value):
            return self
        else:
            return None

    def __repr__(self) -> str:
        return f"Some({repr(self._value)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Some) and self._value == other._value


# class None_(Option[T]):
#     """
#     Represents the absence of a value.
#     """
#     def is_some(self) -> bool:
#         return False

#     def is_none(self) -> bool:
#         return True

#     def is_some_and(self, predicate: Callable[[T], bool]) -> bool:
#         return False

#     def unwrap(self) -> NoReturn:
#         raise RuntimeError("called `Option.unwrap()` on a `None` value")

#     def expect(self, msg: str) -> NoReturn:
#         raise RuntimeError(msg)

#     def map(self, func: Callable[[T], Any]) -> 'Option[Any]':
#         return self  # Applying a function to None still results in None

#     def filter(self, predicate: Callable[[T], bool]) -> 'Option[T]':
#         return self # Filtering None still results in None

#     def __repr__(self) -> str:
#         return "None"

#     def __eq__(self, other: Any) -> bool:
#         return isinstance(other, None_)

# # Create a singleton instance for None, similar to Rust's None enum variant
# None_ = None_()