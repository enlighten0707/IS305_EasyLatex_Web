from sympy import *

str_expr = 'x**2 + 2*x + 1'
expr = sympify(str_expr)
# solveset(Eq(x**2 - x, 0), x, domain = S.Reals)
print(latex(expr))
