from examgen.worksheet import Worksheet
from examgen.lib.algebra import LinearEq, RationalPolySimplify, QuadraticEq
from examgen.lib.calc import PolyRatioLimit, \
    ChainRule, \
    FindDerivative, \
    HorizontalTangents, \
    QuotientRule


def test_example():
    ws = Worksheet("example_worksheet", "Example worksheet 1", cleantex=False)

    lin = LinearEq(var="A")
    lin.add_problem(n=4)

    quad = QuadraticEq(var="B")
    quad.add_integer_radicals(n=2)
    quad.add_real_radicals(n=2)
    quad.shuffle()

    poly = RationalPolySimplify(var="C")
    poly.add_problem(n=4)

    der1 = FindDerivative(var="D")
    der1.add_problem(n=4)

    der2 = ChainRule(var="E")
    der2.add_problem(n=4)

    der3 = QuotientRule(var="F")
    der3.add_problem(n=4)

    tangents = HorizontalTangents(var="G")
    tangents.add_problem(n=4)

    limit = PolyRatioLimit(var="H")
    limit.add_problem(n=4)

    ws.add_section(prob_generator=lin)
    ws.add_section(prob_generator=quad)
    ws.add_section(prob_generator=poly)
    ws.add_section(prob_generator=der1)
    ws.add_section(prob_generator=der2)
    ws.add_section(prob_generator=der3)
    ws.add_section(prob_generator=tangents)
    ws.add_section(prob_generator=limit)
    # generate the exam and solutions pdf
    ws.write()

