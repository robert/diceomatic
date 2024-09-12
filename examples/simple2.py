import random

from sumchef import (
    Add,
    AdditionCrosses10Boundary,
    Equal,
    IsLessThan,
    Lit,
    Multiply,
    expression_string,
    find_bindings,
    uniform_domains,
    variables,
)

var_names = ["a", "b", "c", "d", "e"]
a, b, c, d, e = variables(var_names)

lhs = Add(Multiply(a, b), Multiply(c, d))
rhs = e

constraints = [
    AdditionCrosses10Boundary(Multiply(a, b), Multiply(c, d)),
    IsLessThan(Multiply(a, b), Lit(20)),
    Equal(lhs, rhs),
]
domains = uniform_domains(var_names, range(2, 100))

for bnd in find_bindings(var_names, domains, constraints, 10):
    hold_out = random.choice([a, b, c, d, e])
    lhs_expr = expression_string(lhs, bnd, hold_out=hold_out)
    rhs_expr = expression_string(rhs, bnd, hold_out=hold_out)
    print(f"{lhs_expr} = {rhs_expr}")
