from enum import Enum

import sympy
from sympy.parsing.sympy_parser import parse_expr
import random

from examgen.problems.base_classes import MathProb


class NumType(Enum):
    ZERO = 1
    ONE = 2
    INT = 3
    NON_ZERO_INT = 4
    FRAC = 5
    RANDOM = 6
    INF = 7


class SignType(Enum):
    POSITIVE = 1
    NEGATIVE = 2
    NON_NEGATIVE = 3
    NON_POSITIVE = 4
    RANDOM = 6


class QuadraticEq(MathProb):
    title = "Quadratic Equations"
    instructions = "Solve these quadratic equations"

    def __init__(
            self,
            var: str = "x",
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
        self.vspace = "3cm"

    def add_integer_radicals(self, n: int):
        """
        generates equations of form (x-x1)(x-x2)=0
        exactly 2 integer radicals
        """
        for i in range(n):
            var = sympy.Symbol(name=self.get_variable())
            # limits are arbitrary, this is what previous code used
            r1, r2 = self.get_coeffs(n=2, start=-26, stop=26, unique=True)
            lhs = (var - r1) * (var - r2)
            lhs = lhs.expand()
            e = sympy.Eq(lhs=lhs, rhs=0)
            self.problems.append(sympy.latex(e))
            self.solutions.append(
                ', '.join([var.name + " = " + sympy.latex(expr=ex) for ex in sympy.solve(e, var)])
            )

    def add_real_radicals(self, n: int):
        """
        generates equations based on x^2-(x1+x2)+x1*x2 = 0
        where x1=a+sqrt(b), x2=a-sqrt(b), where b is a positive prime
        exactly 2 non-integer radicals
        """
        # todo: this is buggy!!!
        for i in range(n):
            var = sympy.Symbol(name=self.get_variable())
            # todo: limiting it for exactly 2 radicals for now
            c1 = self.get_coeffs(n=1, start=-10, stop=10, unique=True)[0]
            c2 = sympy.randprime(a=2, b=9)
            lhs = var**2 - 2*c1*var + c1**2-c2
            e = sympy.Eq(lhs=lhs, rhs=0)
            self.problems.append(sympy.latex(e))
            self.solutions.append(
                ', '.join([var.name + " = " + sympy.latex(expr=ex) for ex in sympy.solve(e, var)])
            )

    def add_problem(self, n: int):
        mode = [random.choice(seq=[0, 1]) for i in range(n)]
        for i in mode:
            # todo: is this faster than shuffling the exercises after?
            if random.choice(seq=[0, 1]):
                self.add_real_radicals(n=1)
            else:
                self.add_integer_radicals(n=1)


class LinearEq(MathProb):
    title = "Linear Equations"
    instructions = "Solve the following linear equations"

    def __init__(
            self,
            var: str = None,
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
        self.vspace = "3cm"

    def add_simple_const_right(
            self,
            var_multiplied: bool = True,
            coeff_mode: NumType = NumType.NONZERO_INT,
            radical_mode: NumType = NumType.INT,
            radical_sign: SignType = SignType.RANDOM
    ):
        if type(var_multiplied) != bool:
            raise TypeError(f"var_multiplied should be of type bool, not {type(coeff_mode)}")
        if type(coeff_mode) != NumType:
            raise TypeError(f"coeff_mode should be of type NumType, not {type(coeff_mode)}")
        if type(radical_mode) != NumType:
            raise TypeError(f"radical_mode should be of type NumType, not {type(coeff_mode)}")
        if type(radical_sign) != SignType:
            raise TypeError(f"radical_sign should be of type SignType, not {type(coeff_mode)}")
        if coeff_mode in [
            NumType.ONE,
            NumType.INF
        ]:
            raise NotImplementedError(f"coeff_mode {coeff_mode} is not supported")
        if radical_mode in [
            NumType.ONE,
            NumType.INF
        ]:
            raise NotImplementedError(f"radical_mode {radical_mode} is not supported")
        if radical_sign in [
            SignType.NON_NEGATIVE,
            SignType.NON_POSITIVE
        ]:
            raise NotImplementedError(f"radical_sign {radical_mode} is not supported")

        if radical_mode == NumType.RANDOM:
            radical_mode = random.choice([NumType.INT, NumType.NON_ZERO_INT, NumType.FRAC])

        if radical_mode == NumType.NON_ZERO_INT:
            sol = self.get_coeffs(n=1, start=1, stop=10)
        elif radical_mode == NumType.INT:
            sol = self.get_coeffs(n=1, start=0, stop=10)
        elif radical_mode == NumType.FRAC:
            p, q = self.get_coeffs(n=2, start=1, stop=10, unique=True)
            sol = sympy.Rational(p=p, q=q)
        elif radical_mode == NumType.ZERO:
            sol = 0
        else:
            raise ValueError(f"oops, radical mode {radical_mode} is not supported")

        if radical_sign == (SignType.RANDOM and random.choice([0, 1])) or radical_sign == SignType.NEGATIVE:
            sol = -sol

        x = self.get_variable()
        x = sympy.Symbol(name=x)
        if var_multiplied:
            if coeff_mode == NumType.FRAC:
                p, q = self.get_coeffs(n=2, start=1, stop=10, unique=True)
                c1 = sympy.Rational(p=p, q=q)
            else:
                c1 = self.get_coeffs(n=2, start=1, stop=10)[0]
            ls = c1 * x
        else:
            ls = x

        if coeff_mode == NumType.FRAC:
            p, q = self.get_coeffs(n=2, start=-10, stop=10)
            c2 = sympy.Rational(p=p, q=q)
        else:
            c2 = self.get_coeffs(n=2, start=-10, stop=10)[0]

        eq = sympy.Eq(lhs=ls+c2, rhs=sol+c2)

        self.problems.append(sympy.latex(eq))
        self.solutions.append(f"{x.name}={sol}")

    def add_problem(
            self,
            n: int,
    ):
        # todo: for consistent behavior, i am limiting this to exactly 1 solution.
        # todo: implement no solution / infinite solution / parametrized later!
        for i in range(n):
            x = self.get_variable()
            x = sympy.Symbol(name=x)
            c1, c2, c3, c4 = self.get_coeffs(n=4, start=-26, stop=26, unique=True)
            e = sympy.Eq(lhs=c1 * x + c2, rhs=c3 * x + c4)
            sol = sympy.solve(e, dict=False)
            self.problems.append(sympy.latex(e))
            self.solutions.append(f"{x}=" + sympy.latex(sol[0]))


class RationalPolySimplify(MathProb):
    title = "Simplifying Polynomials"
    instructions = "simplify the following expressions"

    def __init__(self, var: str = "x"):
        super().__init__(var=var)
        self.vspace = "3cm"

    def add_problem(self, n: int):
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
        for i in range(n):
            coeffs = self.get_coeffs(n=6, start=-10, stop=10, include_zero=False, unique=True)
            brackets = [(x-i) for i in coeffs]
            e1 = sympy.prod([brackets[0], brackets[1]]).expand()
            e2 = sympy.prod([brackets[0], brackets[2]]).expand()
            e3 = sympy.prod([brackets[3], brackets[4]]).expand()
            e4 = sympy.prod([brackets[3], brackets[5]]).expand()
            e = ((e1 / e2) / (e3 / e4))
            s1 = ''.join([r"\frac{", sympy.latex(e1), "}", "{", sympy.latex(e2), "}"])
            s2 = ''.join([r"\frac{", sympy.latex(e3), "}", "{", sympy.latex(e4), "}"])
            s3 = ''.join([r"\frac{", s1, "}", "{", s2, "}"])
            pieces = str(e.factor()).split("/")
            num, denom = [parse_expr(i).expand() for i in pieces]
            self.problems.append(s3)
            self.solutions.append(sympy.latex(num / denom))
