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
def test_math_problem(
    fix_problem_output
):
    # todo: logging output for manual evaluation, assertions needed
    problem, solution = fix_problem_output
    logger.debug(f"problem: \n {problem}\n\nsolution:\n{solution}\n")
