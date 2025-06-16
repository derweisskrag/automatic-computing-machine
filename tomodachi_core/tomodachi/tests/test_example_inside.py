import pytest

def add(a, b):
    return a + b

def test_add():
    assert add(1, 1) == 2
    assert add(2, 2) == 4
    assert add(3, 5) == 8
    assert add(1, 2) == 3
