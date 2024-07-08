import pytest
import sys

sys.path.append('../')

def inc(x):
    return x + 1


def test_answer():
    print(sys.path)
    assert inc(3) == 5