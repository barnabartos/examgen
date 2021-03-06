import os
from itertools import chain
from typing import Union, List, Optional, Tuple

import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.polys.polytools import degree
import random

from examgen.lib.base_classes import MathProb
from examgen.lib.constants import alpha, digits_nozero, render, shuffle

# i reimplemented the original functions naively as classes, to be initialized before
# passing to Worksheet, eliminating the need for *args and ** quargs, while
# changing the least things possible. a principled
# refactoring will be needed later!


class QuadraticEq(MathProb):
    def __init__(
            self,
            var: Union[str, List[str]] = "x",
            rhs: Optional[float] = None,
            integer: Union[int, List[int]] = None
    ):
        """
        :param var:
            charector for the variable to be solved for. defaults to "x", OR
            a list of possible charectors. A random selection will be made from them.
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
            r1, r2 = self.get_coeffs(n=2, start=-26, stop=26)
            lhs = (var - r1) * (var - r2)
            lhs = lhs.expand()
            rhs = 0
        else:
            c1, c2, c3 = self.get_coeffs(n=3, start=-26, stop=26)
            lhs = c1 * var ** 2 + c2 * var + c3

        if self.rhs is None:
            c4, c5, c6 = self.get_coeffs(n=3, start=-26, stop=26)
            rhs = c4 * var ** 2 + c5 * var + c6

        e = sympy.Eq(lhs=lhs, rhs=self.rhs)
        pvar = str(var)
        sols = ', '.join([pvar + " = " + sympy.latex(expr=ex) for ex in sympy.solve(e, var)])
        sols = "$$" + sols + "$$"
        if len(sols) == 0:
            # todo is this the best way to do this?
            return self.make()
        return render(e), sols


class LinearEq(MathProb):
    def __init__(
            self,
            x: Optional[Union[str, List[str]]] = None,
            rhs: Optional[float] = None,  # this currently just gets overwritten
    ):
        """
        :param x:
            character for the variable to be solved for. defaults to random selection
            from the global list `alpha`. OR a list of possible character.
            A random selection will be made from them.
        todo: implement this!
        :param var_coeffs:
            sets whether we want variables as coefficients in the problem.
            defaults to True. Set to False if you want a problem with strictly
            numerical coefficients.

        """
        super().__init__(var=x)

    def make(self) -> Tuple[str, List[str]]:
        x = self.get_variable()
        x = sympy.Symbol(name=x)
        c1, c2, c3, c4 = self.get_coeffs(n=4, start=-26, stop=26)
        e = sympy.Eq(lhs=c1 * x + c2, rhs=c3 * x + c4)
        return sympy.latex(e), [f"$$ {x}=" + sympy.latex(i) + " $$" for i in sympy.solve(e, dict=False)]


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
        exclude = [var.upper(), var.lower()]
        x = sympy.Symbol(name=var)
        # todo : think this through maybe
        select = shuffle(chain(range(-10, -1), range(1, 10)))[:6]
        e1 = sympy.prod([x - i for i in shuffle(select)[:2]]).expand()
        e2 = sympy.prod([x - i for i in shuffle(select)[:2]]).expand()
        e3 = sympy.prod([x - i for i in shuffle(select)[:2]]).expand()
        e4 = sympy.prod([x - i for i in shuffle(select)[:2]]).expand()
        length = len({e1, e2, e3, e4})
        e = ((e1 / e2) / (e3 / e4))
        s1 = ''.join(["\\frac{", sympy.latex(e1), "}", "{", sympy.latex(e2), "}"])
        s2 = ''.join(["\\frac{", sympy.latex(e3), "}", "{", sympy.latex(e4), "}"])
        s3 = ''.join(["$$\\frac{", s1, "}", "{", s2, "}$$"])
        pieces = str(e.factor()).split("/")
        # todo fix this asap
        try:
            num, denom = [parse_expr(i).expand() for i in pieces]
        except:
            return self.make()
        if len(pieces) != 2 or length < 4 or degree(num) > 2 or degree(denom) > 2:
            return self.make()
        return s3, render(num / denom)

