import random
from typing import Union, List, Tuple

import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.polys.polytools import degree

from examgen.lib.base_classes import MathProb
from examgen.lib.constants import alpha, digits_nozero, get_coefficients, render, shuffle


def poly1(x: float) -> float:
    vals = sum([k*x**i for i, k in enumerate(reversed(get_coefficients(2)))])
    return vals


def poly2(x: float) -> float:
    vals = sum([k*x**i for i, k in enumerate(reversed(get_coefficients(3)))])
    return vals


def poly3(x: float) -> float:
    vals = sum([k*x**i for i, k in enumerate(reversed(get_coefficients(4)))])
    return vals


_functions = [sympy.sin, sympy.cos, sympy.tan, sympy.ln, sympy.sqrt, sympy.exp,
              lambda a: a, poly1, poly2, poly3]


# i reimplemented the original functions naively as classes, to be initialized before
# passing to Worksheet, eliminating the need for *args and ** quargs, while
# changing the least things possible. a principled
# refactoring will be needed later!


class FindDervative(MathProb):
    def __init__(self, var: Union[str, List[str]] = "x", rhs: str = "4"):
        super().__init__(var=var)
        self.rhs = rhs

    def make(self) -> Tuple[str, str]:
        func = sympy.Function("f")
        var = sympy.Symbol(self.get_variable())
        df = sympy.prod([var - random.choice(digits_nozero) for i in range(random.randint(2, 3))])
        f = poly3(var)
        df = int(sympy.diff(f, var).evalf(subs={var: int(self.rhs)}))
        eq = sympy.latex(sympy.Derivative(func(self.rhs), var))
        eq = 'd'.join(eq.split("\\partial"))
        eq = eq + "=" + str(df)
        fx = "f \\left(%s \\right)" % str(var)
        return render(f, fx), render(eq)


class HorizontalTangents(MathProb):
    def __init__(self, var="x"):
        super().__init__(var=var)

    def make(self) -> Tuple[str, str]:
        var = sympy.Symbol(self.get_variable())
        df = sympy.prod([var - random.choice(digits_nozero) for i in range(random.randint(2, 3))])
        f = sympy.integrate(df, var)
        eqn = sympy.Eq(sympy.diff(f, var), 0)
        fx = "f \\left(%s \\right)" % str(var)
        return render(f, fx), render(', '.join([str(var) + "=" + str(i) for i in sympy.solve(eqn)]))


class ChainRule(MathProb):
    def __init__(
            self,
            var: Union[str, List[str]] = "x",
            partial: bool = False
    ):
        super().__init__(var=var)
        self.partial = partial

    def make(self) -> Tuple[str, str]:
        var = sympy.Symbol(self.get_variable())
        f1 = random.choice(_functions)
        f2 = random.choice(_functions)
        f3 = random.choice(_functions)

        eq = f2(f1(var)) + f3(var)

        sol = sympy.latex(sympy.diff(eq, var))
        eq = sympy.latex(sympy.Derivative(eq, var))
        if not self.partial:
            eq = 'd'.join(eq.split("\\partial"))
        eq = "$$" + eq + "$$"
        sol = "$$" + sol + "$$"
        return eq, sol


class QuotientRule(MathProb):
    def __init__(self, var: Union[str, List[str]] = "x", partial: bool = False):
        super().__init__(var=var)
        self.partial = partial

    def make(self):
        var = sympy.Symbol(self.get_variable())
        f1 = random.choice(_functions)
        f2 = random.choice(_functions)
        f3 = random.choice(_functions)

        eq = (f1(var) + f2(var)) / f3(var)

        sol = sympy.latex(sympy.diff(eq, var))
        eq = sympy.latex(sympy.Derivative(eq, var))
        if not self.partial:
            eq = 'd'.join(eq.split("\\partial"))
        eq = "$$" + eq + "$$"
        sol = "$$" + sol + "$$"
        return eq, sol


class PolyRatioLimit(MathProb):
    def __init__(self, var: Union[str, List[str]] = "x", s=None):
        super().__init__(var=var)
        if s is not None:
            self.s = s
        else:
            self.s = [0, 1, 2]

    def make(self) -> Tuple[str, str]:
        """
        Generates a ratio of two polynomials, and evaluates them at infinity.

        x : charector for the variable to be solved for. defaults to "x".
                                OR
            a list of possible charectors. A random selection will be made from them.

        s : selects the kind of solution
            0 : limit at infinity is zero
            1 : limit as infinity is a nonzero finite number
            2 : limit at infinity is either +infinity or -infinity

            default: one of the above is randomly selected
        """
        var = sympy.Symbol(self.get_variable())
        if isinstance(self.s, list):
            s = random.choice(self.s)
        else:
            s = self.s
        if s == 2:  # infinity
            p1 = random.randint(2, 4)
            p2 = p1 - 1
        elif s == 1:  # ratio of leading coefficients
            p1 = random.randint(2, 4)
            p2 = p1
        elif s == 0:  # zero
            p1 = random.randint(2, 4)
            p2 = random.randint(p1, p1 + 2)
        select = [shuffle(digits_nozero)[0]] + shuffle(range(10)[:p1 - 1])
        num = sum([(k + 1) * var ** i for i, k in enumerate(select)])
        select = [shuffle(digits_nozero)[0]] + shuffle(range(10)[:p2 - 1])
        denom = sum([(k + 1) * var ** i for i, k in enumerate(select)])
        e = num / denom
        s = sympy.limit(e, var, sympy.oo)

        e = "\\lim_{x \\to \\infty}" + sympy.latex(e)
        return render(e), render(s)

