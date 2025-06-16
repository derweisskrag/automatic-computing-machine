"""
This is a basic test for the pytest to see. Please, do not mind it. I should refine
my approach to pipelines, but now it is linear: modify as I go
"""

import pytest

def add(a, b):
    return a + b
    
def test_add():
    assert add(2, 3) == 5
    assert add(6, 4) == 10
    assert add(8, 1) == 9
