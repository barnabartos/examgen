import pytest
import re

from jsonschema import validate

from test.constants import logger
from examgen.lib import algebra, calc
from examgen.lib.schema import chapter


@pytest.mark.parametrize(
    argnames="fix_problem_object",
    argvalues=[
        (algebra.LinearEq, {"var": "x"}),
        (algebra.QuadraticEq, {}),
        (algebra.RationalPolySimplify, {"var": "x"}),
        (calc.FindDerivative, {}),
        (calc.PolyRatioLimit, {}),
        (calc.QuotientRule, {}),
        (calc.ChainRule, {}),
        (calc.HorizontalTangents, {})
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
        "fix_problem_object"
    ]
)
def test_output_schema(
    fix_problem_object
):
    """logs output for manual evaluation"""
    problem, solution = fix_problem_object.to_json()
    logger.debug(problem)
    logger.debug(solution)
    validate(instance=problem, schema=chapter)
    validate(instance=solution, schema=chapter)


@pytest.mark.parametrize(
    argnames=[
        "fix_problem_object",
        "fix_problem_method",
        "expected_problem",
        "expected_solution"
    ],
    argvalues=[
        (
                (algebra.LinearEq, {"var": "x"}),
                ("add_problem", [1]),
                r"^(\+?-?([0-9]+)?x?)+=(\+?-?([0-9]+)?x?)+$",
                r"^x=-?([0-9]+|\\frac{[0-9]+}{[0-9]+})$"
        ),
        (
                (algebra.QuadraticEq, {}),
                ("add_integer_radicals", [1]),
                r"^-?([0-9]+)?x\^\{2\}\+?-?([0-9]+)?x\+?-?([0-9]+)?=0$",
                r"^x=-?[0-9]+,x=-?[0-9]+$"
        ),
        (
                (algebra.QuadraticEq, {}),
                ("add_real_radicals", [1]),
                r"^-?([0-9]+)?x\^\{2\}\+?-?([0-9]+)?x\+?-?([0-9]+)?=0$",
                r"^x=(-?\+?([0-9]|\\sqrt{[0-9]+}))+,x=(-?\+?([0-9]|\\sqrt{[0-9]+}))+$"
        ),
        (
                (algebra.RationalPolySimplify, {"var": "x"}),
                ("add_problem", [1]),
                r"^\\frac{\\frac{-?([0-9]+)?x\^\{2\}\+?-?([0-9]+)?x\+?-?([0-9]+)?}" +
                r"{-?([0-9]+)?x\^\{2\}\+?-?([0-9]+)?x\+?-?([0-9]+)?}}" +
                r"{\\frac{-?([0-9]+)?x\^\{2\}\+?-?([0-9]+)?x\+?-?([0-9]+)?}" +
                r"{-?([0-9]+)?x\^\{2\}\+?-?([0-9]+)?x\+?-?([0-9]+)?}}$",
                r"^\\frac{-?([0-9]+)?x\^\{2\}\+?-?([0-9]+)?x\+?-?([0-9]+)?}" +
                r"{-?([0-9]+)?x\^\{2\}\+?-?([0-9]+)?x\+?-?([0-9]+)?}$"
        ),
        (
                (calc.FindDerivative, {}),
                ("add_problem", [1]),
                r"^f\\left\(x\\right\)=.+$",
                r"^\\frac{d}{dx}f{\\left\(\\right\)}=.+$"
        ),
        (
                (calc.HorizontalTangents, {}),
                ("add_problem", [1]),
                r"^f\\left\(x\\right\)=.+$",
                r"^.+$"
        ),
        (
                # todo: this is quite weak
                (calc.ChainRule, {}),
                ("add_problem", [1]),
                r"^\\frac{d}{dx}.+$",
                r"^.+$"
        ),
        (
                # todo: this is quite weak
                (calc.QuotientRule, {}),
                ("add_problem", [1]),
                r"^\\frac{d}{dx}.+$",
                r"^.+$"
        ),
        (
                (calc.PolyRatioLimit, {"s": 0}),
                ("add_problem", [1]),
                r"^\\lim_{x\\to\\infty}\\frac{.+}{.+}$",
                r"^0$"
        ),
        (
                (calc.PolyRatioLimit, {"s": 1}),
                ("add_problem", [1]),
                r"^\\lim_{x\\to\\infty}\\frac{.+}{.+}$",
                r"^(\\frac{[0-9]+}{[0-9]+}|[0-9]+)$"
        ),
        (
                (calc.PolyRatioLimit, {"s": 2}),
                ("add_problem", [1]),
                r"^\\lim_{x\\to\\infty}\\frac{.+}{.+}$",
                r"^-?\\infty$"
        )
    ],
    ids=[
        "LinearEq",
        "QuadraticEq-add_integer_radicals",
        "QuadraticEq-add_real_radicals",
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
        "fix_problem_object",
        "fix_problem_method"
    ]
)
def test_expected_solution(
        fix_problem_method,
        expected_problem,
        expected_solution
):
    problem, solution = fix_problem_method
    problem = problem.replace(" ", "")
    solution = solution.replace(" ", "")
    prob = re.compile(expected_problem)
    sol = re.compile(expected_solution)
    assert re.match(pattern=prob, string=problem), \
        f"\nproblem: {problem} \ndoesn't match expected pattern: {prob}"
    assert re.match(pattern=sol, string=solution), \
        f"\nsolution: {solution} \ndoesn't match expected pattern: {sol}"
