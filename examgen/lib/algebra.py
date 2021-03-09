from typing import Union, List, Optional, Tuple
from math import floor

import sympy
from sympy.parsing.sympy_parser import parse_expr
import random

from examgen.lib.base_classes import MathProb
from examgen.lib.constants import render

# i reimplemented the original functions naively as classes, to be initialized before
# passing to Worksheet, eliminating the need for *args and ** quargs, while
# changing the least things possible. a principled
# refactoring will be needed later!


class QuadraticEq(MathProb):
    def __init__(
            self,
            var: str = "x",
            rhs: Optional[float] = None,
            integer: Union[int, List[int]] = None
    ):
        """
        :param var:
            charector for the variable to be solved for. defaults to "x", OR
            a list of possible charectors. A random selection will be made from them.
        todo: implement this later, removing now for simplicity
        :param rhs:
            value to set for the right-hand side. If not given, the
            right-hand side will be a randomly generated polynomial expression
            of degree <= 2, in the same variable.
        :param integer:
            determines whether generated problem will have integer roots or
            not. Default is a random selection.
        """
        super().__init__(var=var)
        self.rhs = rhs
        if integer is not None:
            self.integer = integer
        else:
            self.integer = [0, 1]

    def make(self) -> Tuple[str, str]:
        var = sympy.Symbol(name=self.get_variable())
        if isinstance(self.integer, list):
            self.integer = random.choice(seq=self.integer)
        if self.integer:
            # limits are arbitrary, this is what previous code used
            r1, r2 = self.get_coeffs(n=2, start=-26, stop=26, unique=True)
            lhs = (var - r1) * (var - r2)
            lhs = lhs.expand()
        else:
            # todo: limiting it for exactly 2 radicals for now
            c1, c2 = self.get_coeffs(n=2, start=-26, stop=26, unique=True)
            lhs = c1 * var ** 2 + c2 * var + floor(c2**2/(4*c1))-1
        e = sympy.Eq(lhs=lhs, rhs=0)
        pvar = str(var)
        sols = ', '.join([pvar + " = " + sympy.latex(expr=ex) for ex in sympy.solve(e, var)])
        sols = "$$" + sols + "$$"
        return render(e), sols


class LinearEq(MathProb):
    def __init__(
            self,
            var: str = None,
            rhs: Optional[float] = None,  # this currently just gets overwritten
    ):
        """
        :param var:
            character for the variable to be solved for. defaults to random selection
            from the global list `alpha`. OR a list of possible character.
            A random selection will be made from them.
        todo: implement this!
        :param var_coeffs:
            sets whether we want variables as coefficients in the problem.
            defaults to True. Set to False if you want a problem with strictly
            numerical coefficients.

        """
        super().__init__(var=var)

    def make(self) -> Tuple[str, List[str]]:
        # todo: for consistent behavior, i am limiting this to exactly 1 solution.
        # todo: implement no solution / infinite solution / parametrized later!
        x = self.get_variable()
        x = sympy.Symbol(name=x)
        c1, c2, c3, c4 = self.get_coeffs(n=4, start=-26, stop=26, unique=True)
        e = sympy.Eq(lhs=c1 * x + c2, rhs=c3 * x + c4)
        sol = sympy.solve(e, dict=False)
        return "$$" + sympy.latex(e) + "$$", f"$$ {x}=" + sympy.latex(sol[0]) + "$$"


class RationalPolySimplify(MathProb):
    def __init__(self, var: str = "x"):
        super().__init__(var=var)

    def make(self):
        """
        Generates a rational expression of 4 polynomials, to be simplified.
        Example:
            ( (x**2 + 16*x + 60) / (x**2 - 36)) /
            ( (x**2 - 2*x - 63) / (x**2 - 5*x - 36)

        x : charector for the variable to be solved for. defaults to random selection
            from the global list `alpha`.
                                OR
            a list of possible charectors. A random selection will be made from them.
        """
        var = self.get_variable()
        x = sympy.Symbol(name=var)
        coeffs = self.get_coeffs(n=6, start=-10, stop=10, include_zero=False, unique=True)
        brackets = [(x-i) for i in coeffs]
        e1 = sympy.prod([brackets[0], brackets[1]]).expand()
        e2 = sympy.prod([brackets[0], brackets[2]]).expand()
        e3 = sympy.prod([brackets[3], brackets[4]]).expand()
        e4 = sympy.prod([brackets[3], brackets[5]]).expand()
        e = ((e1 / e2) / (e3 / e4))
        s1 = ''.join(["\\frac{", sympy.latex(e1), "}", "{", sympy.latex(e2), "}"])
        s2 = ''.join(["\\frac{", sympy.latex(e3), "}", "{", sympy.latex(e4), "}"])
        s3 = ''.join(["$$\\frac{", s1, "}", "{", s2, "}$$"])
        pieces = str(e.factor()).split("/")
        num, denom = [parse_expr(i).expand() for i in pieces]
        return s3, render(num / denom)
