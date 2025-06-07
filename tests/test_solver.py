from diceomatic import (
    Add,
    AdditionCrosses10Boundary,
    Equal,
    IsLessThan,
    Lit,
    Multiply,
    NOf,
    Subtract,
    Variable,
    expression_string,
    find_bindings,
    uniform_domains,
)


def test_simple_addition():
    """Test simple addition equation solving: a + b = c"""
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")

    # Domains: a, b ∈ [1-9], c ∈ [2-18]
    domains = {a: list(range(1, 10)), b: list(range(1, 10)), c: list(range(2, 19))}

    # Constraint: a + b = c
    constraint = Equal(Add(a, b), c)

    # Find bindings
    bindings = find_bindings([a, b, c], domains, [constraint], n_bindings=5)

    # Verify all solutions
    for binding in bindings:
        assert binding[a] + binding[b] == binding[c]


def test_subtraction():
    """Test subtraction equation solving: a - b = c"""
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")

    # Domains: a ∈ [10-20], b ∈ [1-10], c ∈ [0-19]
    domains = {a: list(range(10, 21)), b: list(range(1, 11)), c: list(range(0, 20))}

    # Constraint: a - b = c
    constraint = Equal(Subtract(a, b), c)

    # Find bindings
    bindings = find_bindings([a, b, c], domains, [constraint], n_bindings=5)

    # Verify all solutions
    for binding in bindings:
        assert binding[a] - binding[b] == binding[c]


def test_multiplication():
    """Test multiplication equation solving: a * b = c"""
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")

    # Domains: a, b ∈ [1-10], c ∈ [1-100]
    domains = {a: list(range(1, 11)), b: list(range(1, 11)), c: list(range(1, 101))}

    # Constraint: a * b = c
    constraint = Equal(Multiply(a, b), c)

    # Find bindings
    bindings = find_bindings([a, b, c], domains, [constraint], n_bindings=5)

    # Verify all solutions
    for binding in bindings:
        assert binding[a] * binding[b] == binding[c]


def test_multiple_constraints():
    """Test solving with multiple constraints"""
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

    # Domains: x, y, z ∈ [1-20]
    domains = uniform_domains([x, y, z], range(1, 21))

    # Constraints:
    # 1. x < y
    # 2. y < z
    # 3. x + y + z = 30
    constraints = [
        IsLessThan(x, y),
        IsLessThan(y, z),
        Equal(Add(Add(x, y), z), Lit(30)),
    ]

    # Find bindings
    bindings = find_bindings([x, y, z], domains, constraints, n_bindings=5)

    # Verify all solutions
    for binding in bindings:
        assert binding[x] < binding[y]
        assert binding[y] < binding[z]
        assert binding[x] + binding[y] + binding[z] == 30


def test_n_of_constraint():
    """Test the NOf constraint"""
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")

    # Domains: a, b, c ∈ [1-5]
    domains = uniform_domains([a, b, c], range(1, 6))

    # Individual constraints
    c1 = Equal(a, Lit(1))
    c2 = Equal(b, Lit(2))
    c3 = Equal(c, Lit(3))

    # Exactly 2 of these constraints must be satisfied
    constraint = NOf([c1, c2, c3], 2)

    # Find bindings
    bindings = find_bindings([a, b, c], domains, [constraint], n_bindings=5)

    # Verify all solutions
    for binding in bindings:
        satisfied_count = 0
        if binding[a] == 1:
            satisfied_count += 1
        if binding[b] == 2:
            satisfied_count += 1
        if binding[c] == 3:
            satisfied_count += 1
        assert satisfied_count == 2


def test_carrying_constraints():
    """Test the carrying constraints"""
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")

    # Domains: a, b ∈ [1-99], c ∈ [1-199]
    domains = {a: list(range(1, 100)), b: list(range(1, 100)), c: list(range(1, 200))}

    # Constraints:
    # 1. a + b = c
    # 2. Adding a and b requires carrying
    constraints = [Equal(Add(a, b), c), AdditionCrosses10Boundary(a, b)]

    # Find bindings
    bindings = find_bindings([a, b, c], domains, constraints, n_bindings=5)

    # Verify all solutions
    for binding in bindings:
        assert binding[a] + binding[b] == binding[c]
        assert (binding[a] % 10 + binding[b] % 10) >= 10


def test_expression_string():
    """Test the expression_string function"""
    a = Variable("a")
    b = Variable("b")

    # Create an expression: a + b
    expr = Add(a, b)

    # Create bindings
    bindings = {a: 5, b: 7}

    # Get the string representation
    expr_str = expression_string(expr, bindings)

    # Check the result
    assert expr_str == "5 + 7"


def test_complex_solving():
    """Test a more complex problem with multiple variables and constraints"""
    # Variables for a quadratic equation: ax² + bx + c = d
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    d = Variable("d")
    x = Variable("x")

    # Domains:
    domains = {
        a: list(range(1, 6)),  # a ∈ [1-5]
        b: list(range(-10, 11)),  # b ∈ [-10-10]
        c: list(range(-10, 11)),  # c ∈ [-10-10]
        d: list(range(-50, 51)),  # d ∈ [-50-50]
        x: list(range(-5, 6)),  # x ∈ [-5-5]
    }

    # Constraint: ax² + bx + c = d
    x_squared = Multiply(x, x)
    ax_squared = Multiply(a, x_squared)
    bx = Multiply(b, x)
    left_side = Add(Add(ax_squared, bx), c)
    constraint = Equal(left_side, d)

    # Find bindings
    bindings = find_bindings([a, b, c, d, x], domains, [constraint], n_bindings=3)

    # Verify all solutions
    for binding in bindings:
        a_val = binding[a]
        b_val = binding[b]
        c_val = binding[c]
        d_val = binding[d]
        x_val = binding[x]

        assert a_val * (x_val**2) + b_val * x_val + c_val == d_val
