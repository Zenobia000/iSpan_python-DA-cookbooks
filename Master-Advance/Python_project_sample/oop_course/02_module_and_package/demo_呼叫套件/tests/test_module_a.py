import pytest
from my_package.module_a import func_a, another_func_a

def test_func_a():
    """Test that func_a returns the expected string."""
    assert func_a() == "Hello from module A"
    
def test_another_func_a():
    """Test that another_func_a returns the expected string."""
    assert another_func_a() == "Another greeting from module A" 