import pytest
import re

from test.constants import logger
from examgen.lib import algebra, calc


@pytest.mark.parametrize(
    argnames=["fix_problem_output"],
    argvalues=[
        (
                [algebra.LinearEq()]
        ),
        (
                [algebra.QuadraticEq()]
        ),
        (
                [algebra.RationalPolySimplify()]
        ),
        (
                [calc.FindDerivative()]
        ),
        (
                [calc.PolyRatioLimit()]
        ),
        (
                [calc.QuotientRule()]
        ),
        (
                [calc.ChainRule()]
        ),
        (
                [calc.HorizontalTangents()]
        )

    ],
    ids=[
        "linear_equation",
        "quadratic_equation",
        "rational_polynomial",
        "derivation",
        "poly_limit_ratio",
        "quotient_rule",
        "chain_rule",
        "horizontal_tangents"
    ],
    indirect=[
        "fix_problem_output"
    ]
)
@pytest.mark.skip("use for manual testing")
def test_manual_eval(
    fix_problem_output
):
    """logs output for manual evaluation"""
    problem, solution = fix_problem_output
    logger.debug(f"\nproblem: {problem}\nsolution: {solution}\n")


@pytest.mark.parametrize(
    argnames=[
        "fix_problem_output",
        "expected_problem",
        "expected_solution"
    ],
    argvalues=[
        (
                algebra.LinearEq(var="x"),
                r"^\$\$.+=.+\$\$$",
                r"^\$\$x=-?([0-9]+|\\frac{[0-9]+}{[0-9]+})\$\$$"
        ),
        (
                algebra.QuadraticEq(var="x"),
                r"^\$\$.+=0\$\$$",
                r"^\$\$x=-?.+,x=-?.+\$\$$"
        ),
        (
                algebra.RationalPolySimplify(var="x"),
                r"^\$\$\\frac{\\frac{.+}{.+}}{\\frac{.+}{.+}}\$\$$",
                r"^\$\$\\frac{.+}{.+}\$\$$"
        ),
        (
                calc.FindDerivative(),
                r"^\$\$f\\left\(x\\right\)=.+\$\$$",
                r"^\$\$\\frac{d}{dx}f{\\left\(\\right\)}=.+\$\$$"
        ),
        (
                calc.HorizontalTangents(),
                r"^\$\$f\\left\(x\\right\)=.+\$\$$",
                r"^\$\$\\mathtt{\\text{.+}}\$\$$"
        ),
        (
                # todo: this is quite weak
                calc.ChainRule(),
                r"^\$\$\\frac{d}{dx}.+\$\$$",
                r"^\$\$.+\$\$$"
        ),
        (
                # todo: this is quite weak
                calc.QuotientRule(),
                r"^\$\$\\frac{d}{dx}.+\$\$$",
                r"^\$\$.+\$\$$"
        ),
        (
                calc.PolyRatioLimit(s=0),
                r"^\$\$\\lim_{x\\to\\infty}\\frac{.+}{.+}\$\$$",
                r"^\$\$0\$\$$"
        ),
        (
                calc.PolyRatioLimit(s=1),
                r"^\$\$\\lim_{x\\to\\infty}\\frac{.+}{.+}\$\$$",
                r"^\$\$(\\frac{[0-9]+}{[0-9]+}|[0-9]+)\$\$$"
        ),
        (
                calc.PolyRatioLimit(s=2),
                r"^\$\$\\lim_{x\\to\\infty}\\frac{.+}{.+}\$\$$",
                r"^\$\$-?\\infty\$\$$"
        )
    ],
    ids=[
        "LinearEq",
        "QuadraticEq",
        "RationalPolySimplify",
        "FindDerivative",
        "HorizontalTangents",
        "ChainRule",
        "QuotientRule",
        "PolyRatioLimit-limZero",
        "PolyRatioLimit-limFinite",
        "PolyRatioLimit-limInfinite"
    ],
    indirect=[
        "fix_problem_output"
    ]
)
def test_expected_solution(
        fix_problem_output,
        expected_problem,
        expected_solution
):
    problem, solution = fix_problem_output
    problem = problem.replace(" ", "")
    solution = solution.replace(" ", "")
    prob = re.compile(expected_problem)
    sol = re.compile(expected_solution)
    assert re.match(pattern=prob, string=problem), \
        f"\nproblem: {problem} \ndoesn't match expected pattern: {prob}"
    assert re.match(pattern=sol, string=solution), \
        f"\nsolution: {solution} \ndoesn't match expected pattern: {sol}"
