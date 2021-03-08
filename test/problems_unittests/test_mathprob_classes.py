import pytest
import re

from test.constants import logger
from examgen.lib import algebra, calc1


@pytest.mark.parametrize(
    argnames=["fix_problem_output"],
    argvalues=[
        # todo: sort this out when expected functionality is more clear!
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
                [calc1.FindDervative()]
        ),
        (
                [calc1.PolyRatioLimit()]
        ),
        (
                [calc1.QuotientRule()]
        ),
        (
                [calc1.ChainRule()]
        ),
        (
                [calc1.HorizontalTangents()]
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
def test_manual_eval(
    fix_problem_output
):
    """logs output for manual evaluation"""
    problem, solution = fix_problem_output
    logger.debug(f"\nproblem: {problem}\nsolution: {solution}\n")


@pytest.mark.parametrize(
    argnames=["fix_problem_output", "expected_result"],
    argvalues=[
        (
                calc1.PolyRatioLimit(s=0),
                r"^\$\$0\$\$$"
        ),
        (
                calc1.PolyRatioLimit(s=1),
                r"^\$\$(\\frac{[0-9]+}{[0-9]+}|[0-9]+)\$\$$"
        ),
        (
                calc1.PolyRatioLimit(s=2),
                r"^\$\$-?\\infty\$\$$"
        )
    ],
    ids=[
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
        expected_result
):
    problem, solution = fix_problem_output
    expr = re.compile(expected_result)
    assert re.match(pattern=expr, string=solution), \
        f"exercise has solution: {solution}\ninstead of expected: {expected_result}"
