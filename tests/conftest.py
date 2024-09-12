import pytest
from sumchef import (
    Add,
    Equal,
    IsDivisibleBy,
    IsGreaterThan,
    IsLessThan,
    Multiply,
    Subtract,
    Variable,
)


@pytest.fixture
def variables():
    """Fixture providing common variables"""
    return {
        "a": Variable("a"),
        "b": Variable("b"),
        "c": Variable("c"),
        "x": Variable("x"),
        "y": Variable("y"),
        "z": Variable("z"),
    }


@pytest.fixture
def simple_domains(variables):
    """Fixture providing simple domains for variables"""
    vars = variables
    return {
        vars["a"]: list(range(1, 10)),
        vars["b"]: list(range(1, 10)),
        vars["c"]: list(range(1, 20)),
        vars["x"]: list(range(1, 10)),
        vars["y"]: list(range(1, 10)),
        vars["z"]: list(range(1, 20)),
    }


@pytest.fixture
def addition_expression(variables):
    """Fixture providing a simple addition expression: a + b"""
    vars = variables
    return Add(vars["a"], vars["b"])


@pytest.fixture
def subtraction_expression(variables):
    """Fixture providing a simple subtraction expression: a - b"""
    vars = variables
    return Subtract(vars["a"], vars["b"])


@pytest.fixture
def multiplication_expression(variables):
    """Fixture providing a simple multiplication expression: a * b"""
    vars = variables
    return Multiply(vars["a"], vars["b"])


@pytest.fixture
def complex_expression(variables):
    """Fixture providing a complex expression: (a + b) * c"""
    vars = variables
    return Multiply(Add(vars["a"], vars["b"]), vars["c"])


@pytest.fixture
def simple_equality_constraint(variables):
    """Fixture providing a simple equality constraint: a + b = c"""
    vars = variables
    return Equal(Add(vars["a"], vars["b"]), vars["c"])


@pytest.fixture
def less_than_constraint(variables):
    """Fixture providing a less than constraint: x < y"""
    vars = variables
    return IsLessThan(vars["x"], vars["y"])


@pytest.fixture
def greater_than_constraint(variables):
    """Fixture providing a greater than constraint: x > y"""
    vars = variables
    return IsGreaterThan(vars["x"], vars["y"])


@pytest.fixture
def divisible_by_constraint(variables):
    """Fixture providing a divisibility constraint: x is divisible by y"""
    vars = variables
    return IsDivisibleBy(vars["x"], vars["y"])
