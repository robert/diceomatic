from sumchef import (
    Add,
    Equal,
    IsDivisibleBy,
    IsGreaterThan,
    IsLessThan,
    Lit,
    Multiply,
    Subtract,
    Variable,
    filter_variables,
    find_bindings,
    uniform_domains,
    variables,
)


def test_variable_creation():
    var = Variable("x")
    assert var.name == "x"
    assert var.variables() == [var]


def test_lit_creation():
    lit = Lit(5)
    assert lit.val == 5
    assert lit.variables() == []


def test_variable_evaluation():
    x = Variable("x")
    y = Variable("y")

    bindings = {x: 10, y: 20}
    assert x.evaluate(bindings) == 10
    assert y.evaluate(bindings) == 20


def test_add_operation():
    x = Variable("x")
    y = Variable("y")
    z = Add(x, y)

    bindings = {x: 10, y: 20}
    assert z.evaluate(bindings) == 30
    assert set(z.variables()) == {x, y}


def test_subtract_operation():
    x = Variable("x")
    y = Variable("y")
    z = Subtract(x, y)

    bindings = {x: 30, y: 20}
    assert z.evaluate(bindings) == 10
    assert set(z.variables()) == {x, y}


def test_multiply_operation():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)

    bindings = {x: 10, y: 20}
    assert z.evaluate(bindings) == 200
    assert set(z.variables()) == {x, y}


def test_complex_expression():
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")

    # Expression: (a + b) * c
    expr = Multiply(Add(a, b), c)

    bindings = {a: 5, b: 7, c: 2}
    assert expr.evaluate(bindings) == 24
    assert set(expr.variables()) == {a, b, c}


def test_equal_constraint():
    x = Variable("x")
    y = Variable("y")
    constraint = Equal(x, y)

    # Should be satisfied
    assert constraint.is_satisfied({x: 10, y: 10})

    # Should not be satisfied
    assert not constraint.is_satisfied({x: 10, y: 20})


def test_less_than_constraint():
    x = Variable("x")
    y = Variable("y")
    constraint = IsLessThan(x, y)

    # Should be satisfied
    assert constraint.is_satisfied({x: 10, y: 20})

    # Should not be satisfied
    assert not constraint.is_satisfied({x: 20, y: 10})
    assert not constraint.is_satisfied({x: 10, y: 10})


def test_greater_than_constraint():
    x = Variable("x")
    y = Variable("y")
    constraint = IsGreaterThan(x, y)

    # Should be satisfied
    assert constraint.is_satisfied({x: 20, y: 10})

    # Should not be satisfied
    assert not constraint.is_satisfied({x: 10, y: 20})
    assert not constraint.is_satisfied({x: 10, y: 10})


def test_divisible_by_constraint():
    x = Variable("x")
    y = Variable("y")
    constraint = IsDivisibleBy(x, y)

    # Should be satisfied
    assert constraint.is_satisfied({x: 10, y: 2})
    assert constraint.is_satisfied({x: 10, y: 5})

    # Should not be satisfied
    assert not constraint.is_satisfied({x: 10, y: 3})


def test_filter_variables():
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")

    lit = Lit(5)

    # Should filter out duplicates and non-variables
    values = [a, b, a, lit, c]
    filtered = filter_variables(values)

    assert set(filtered) == {a, b, c}


def test_uniform_domains():
    a = Variable("a")
    b = Variable("b")

    domain = [1, 2, 3]

    domains = uniform_domains([a, b], domain)

    assert domains[a] == [1, 2, 3]
    assert domains[b] == [1, 2, 3]


def test_find_bindings_simple():
    x = Variable("x")
    y = Variable("y")

    # Domain: x, y can be 1, 2, or 3
    domains = uniform_domains([x, y], [1, 2, 3])

    # Constraint: x + y = 4
    constraint = Equal(Add(x, y), Lit(4))

    # Find bindings
    bindings = find_bindings([x, y], domains, [constraint])

    # There should be some solutions
    assert len(bindings) > 0

    # All solutions should satisfy the constraint
    for binding in bindings:
        assert binding[x] + binding[y] == 4
