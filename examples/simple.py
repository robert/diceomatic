from sumchef import *

# Declare the variables
vars = variables(["a", "b", "c", "d", "e"])
a, b, c, d, e = vars

# Declare the form of the equation
lhs = Add(Multiply(a, b), Multiply(c, d))
rhs = e

# Declare the constraints
constraints = [
    AdditionCrosses10Boundary(Multiply(a, b), Multiply(c, d)),
    IsLessThan(Multiply(a, b), Lit(20)),
    Equal(lhs, rhs),
]
domains = uniform_domains(vars, range(2, 100))

# Find variable bindings that form a valid equation
bindings = find_bindings(vars, domains, constraints, 10)

# Print each set of bindings as an equation with a value held out
for bnd in bindings:
    print(f"{bnd=}")
    hold_out = random.choice(vars)
    lhs_expr = expression_string(lhs, bnd, hold_out=hold_out)
    rhs_expr = expression_string(rhs, bnd, hold_out=hold_out)
    print(f"{lhs_expr} = {rhs_expr}")
