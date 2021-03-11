import random
from typing import Tuple
from functools import partial

import sympy

from examgen.lib.base_classes import MathProb
from examgen.lib.constants import digits_nozero, render, logger


def get_polynomial(n, x):
    coeffs = []
    for i in range(n):
        c = random.choice(digits_nozero)
        if random.randint(0, 1):
            c = 0
        coeffs.append(c)
    if coeffs[0] == 0:
        coeffs[0] = random.choice(digits_nozero)
    return sum([k*x**i for i, k in enumerate(reversed(coeffs))])


_functions = [
    sympy.sin,
    sympy.cos,
    sympy.tan,
    sympy.ln,
    sympy.sqrt,
    sympy.exp,
    lambda a: a,
    partial(get_polynomial, 2),
    partial(get_polynomial, 3),
    partial(get_polynomial, 4)
]


class FindDerivative(MathProb):
    title = "Derivation of Polynomials"
    instructions = "find the derivative of the following polynomials"

    def __init__(self, var: str = "x", rhs: str = "4"):
        super().__init__(var=var)
        self.rhs = rhs

    def make(self) -> Tuple[str, str]:
        func = sympy.Function("f")
        var = sympy.Symbol(self.get_variable())
        f = sympy.prod([var - i for i in self.get_coeffs(n=random.randint(2, 3), start=-10, stop=10)]).expand()
        df = sympy.diff(f, var)
        eq = sympy.latex(sympy.Derivative(func(), var))
        eq = r'd'.join(eq.split(r"\partial"))
        eq = eq + "=" + sympy.latex(df)
        fx = fr"f \left({var} \right)={sympy.latex(f)}"
        # todo: f() in answer instead of f(x)
        return fx, eq


class HorizontalTangents(MathProb):
    title = "Horizontal Tangents"
    instructions = "Calculate the tangents"

    def __init__(self, var: str = "x"):
        super().__init__(var=var)

    def make(self) -> Tuple[str, str]:
        var = sympy.Symbol(self.get_variable())
        df = sympy.prod([var - random.choice(digits_nozero) for i in range(random.randint(2, 3))])
        f = sympy.integrate(df, var)
        eqn = sympy.Eq(sympy.diff(f, var), 0)
        fx = fr"f\left({var.name}\right)={sympy.latex(f)}"
        return fx, ', '.join([str(var) + "=" + str(i) for i in sympy.solve(eqn)])


class ChainRule(MathProb):
    title = "Differentiation - Chain Rule"
    instructions = "calculate the derivatives of the following expressions"

    def __init__(
            self,
            var: str = "x",
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
        # todo: what is this all about
        if not self.partial:
            eq = r'd'.join(eq.split(r"\partial"))
        return eq, sol


class QuotientRule(MathProb):
    title = "Differentiation - Quotient Rule"
    instructions = "calculate the derivatives of the following expressions"

    def __init__(self, var: str = "x", partial: bool = False):
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
            eq = r'd'.join(eq.split(r"\partial"))
        return eq, sol


class PolyRatioLimit(MathProb):
    title = "Limits"
    instructions = "calculate the limits of the following expressions"

    def __init__(self, var: str = "x", s=None):
        super().__init__(var=var)
        if s is not None:
            self.s = s
        else:
            self.s = [0, 1, 2]

    def get_limit_mode(self) -> Tuple[int, int]:
        """
            0 : limit at infinity is zero
            1 : limit as infinity is a nonzero finite number
            2 : limit at infinity is either +infinity or -infinity
            default: one of the above is randomly selected
        """
        if isinstance(self.s, list):
            s = random.choice(self.s)
        else:
            s = self.s
        if s == 2:  # infinity
            p2 = random.randint(2, 4)
            p1 = p2 + 1
            logger.debug(f"generated expression will have a limit of infinity")
        elif s == 1:  # ratio of leading coefficients
            p1 = random.randint(2, 4)
            p2 = p1
            logger.debug(f"generated expression will have a finite limit")
        elif s == 0:  # zero
            p1 = random.randint(2, 4)
            p2 = random.randint(p1+1, p1 + 2)
            logger.debug(f"generated expression will have a limit of zero")
        else:
            raise ValueError(f"invalid value for s: {s}")
        return p1, p2

    def make(self) -> Tuple[str, str]:
        """
        Generates a ratio of two polynomials, and evaluates them at infinity.

        x : charector for the variable to be solved for. defaults to "x".
                                OR
            a list of possible charectors. A random selection will be made from them.

        """
        var = sympy.Symbol(self.get_variable())
        p1, p2 = self.get_limit_mode()
        # this is so that the fraction doesnt cancel to 1
        last_coeffs = self.get_coeffs(n=2, start=-26, stop=26, unique=True)
        num_coeffs = [last_coeffs[0]]
        if p1 != 1:
            num_coeffs += self.get_coeffs(n=p1-1, start=0, stop=9, unique=True, include_zero=False)
        num = sum([k * var ** i for i, k in enumerate(num_coeffs)])
        denom_coeffs = [last_coeffs[1]]
        if p2 != 1:
            denom_coeffs += self.get_coeffs(n=p2-1, start=0, stop=9, unique=True, include_zero=False)
        denom = sum([k * var ** i for i, k in enumerate(denom_coeffs)])
        e = num / denom
        s = sympy.limit(e, var, sympy.oo)
        e = r"\lim_{x \to \infty}" + sympy.latex(e)
        return e, sympy.latex(s)
