import pytest

from count_to_billion import count_to_billion


def test_count_to_billion(benchmark):
    benchmark(count_to_billion)
    

