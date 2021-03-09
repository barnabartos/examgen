from collections import namedtuple

import pytest

from examgen.lib.algebra import LinearEq, RationalPolySimplify, QuadraticEq
from examgen.lib.calc import PolyRatioLimit, \
    HorizontalTangents, \
    ChainRule, \
    FindDerivative, \
    HorizontalTangents, \
    QuotientRule

worksheet_args = namedtuple("worksheet_args", ["prob_generator", "n", "cols", "title", "instructions"])


@pytest.mark.parametrize(
    argnames=["fix_worksheet", "fix_sections"],
    argvalues=[
        # (
        #         ["empty", "this is an empty worksheet"],
        #         []
        # ),
        (
            ["full_worksheet", "Algebra 101 worksheet 1"],
            [
                worksheet_args(
                    prob_generator=LinearEq(),
                    n=10,
                    cols=2,
                    title="Linear equations",
                    instructions="Solve the following equations for the specified variable."
                ),
                worksheet_args(
                    prob_generator=RationalPolySimplify(),
                    n=10,
                    cols=1,
                    title="Simplify each expression",
                    instructions=""
                ),
                worksheet_args(
                    prob_generator=QuadraticEq(var="xyz"),
                    n=10,
                    cols=2,
                    title="Quadratic equations",
                    instructions="Solve the following quadratic equations.",
                ),
                worksheet_args(
                    prob_generator=PolyRatioLimit(),
                    n=10,
                    cols=2,
                    title="Determine each limit",
                    instructions=""
                ),
                worksheet_args(
                    prob_generator=ChainRule(),
                    n=10,
                    cols=2,
                    title="chain_rule",
                    instructions=""
                ),
                worksheet_args(
                    prob_generator=FindDerivative(),
                    n=10,
                    cols=2,
                    title="derivation",
                    instructions=""
                ),
                worksheet_args(
                    prob_generator=HorizontalTangents(),
                    n=10,
                    cols=2,
                    title="tangents",
                    instructions=""
                ),
                worksheet_args(
                    prob_generator=QuotientRule(),
                    n=10,
                    cols=2,
                    title="quotient_rule",
                    instructions=""
                )
            ]
        )
    ],
    ids=[
        "empty_worksheet"
        # "second_run",
        "multichapter worksheet"
    ],
    indirect=[
        "fix_worksheet",
        "fix_sections"
    ]
)
def test_example(
        fix_worksheet,
        fix_sections
):
    fix_worksheet.write()

