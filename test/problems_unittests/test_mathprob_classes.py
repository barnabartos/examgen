import pytest

from examgen.lib import algebra, calc1

@pytest.mark.parametrize(
    argnames=["fix_problem_output"],
    argvalues=[
        # (
        #         ["empty", "this is an empty worksheet"],
        #         []
        # ),
        (
                algebra.LinearEq()
        ),
        (
                algebra.QuadraticEq()
        ),
        (
                algebra.RationalPolySimplify()
        ),
        (
                calc1.FindDervative()
        ),
        (
                calc1.PolyRatioLimit()
        ),
        (
                calc1.QuotientRule()
        ),
        (
                calc1.ChainRule()
        ),
        (
                calc1.HorizontalTangents()
        )

    ],
    ids=[
        "empty_worksheet"
        "second_run",
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
