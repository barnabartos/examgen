import pytest

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
    logger.debug(f"problem: \n {problem}\n\nsolution:\n{solution}\n")


@pytest.mark.parametrize(
    argnames=["fix_problem_output", "expected_result"],
    argvalues=[
        (
                calc1.PolyRatioLimit(s=0),
                "$$0$$"
        ),
        # todo figure out how to use mocking to eliminate randomness
        # (
        #         calc1.PolyRatioLimit(s=1),
        #         "asdf"
        # ),
        (
                calc1.PolyRatioLimit(s=2),
                "$$\infty$$"
        )
    ],
    ids=[
        "PolyRatioLimit-limZero",
        # "PolyRatioLimit-limFinite",
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
    assert solution == expected_result, \
        f"exercise has solution: {solution}\ninstead of expected: {expected_result}"
