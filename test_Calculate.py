import pytest
from Calculate import add, divide
def test_add():
    assert add(10, 20) == 30

def test_divide():
    assert divide(20, 4) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)