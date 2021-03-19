from examgen.worksheet import Worksheet
from examgen.problems.calc import QuotientRule, \
    ChainRule, \
    FindDerivative, \
    HorizontalTangents, \
    PolyRatioLimit
from examgen.problems.algebra import LinearEq, QuadraticEq, RationalPolySimplify

# make an exam with a filename and title
ws = Worksheet(fname="example_worksheet", title="Example worksheet 1")

lin = LinearEq(var="A")
lin.add_problem(n=2)
lin.add_custom_problem(
    problem=r"2*r*\pi = 6.28",
    solution=r"r=1"
)

quad = QuadraticEq(var="B")
quad.add_integer_radicals(n=2)
quad.add_real_radicals(n=2)
quad.shuffle()

poly = RationalPolySimplify(var="C")
poly.add_problem(n=3)

der1 = FindDerivative(var="D")
der1.add_problem(n=3)

der2 = ChainRule(var="E")
der2.add_problem(n=2)

der3 = QuotientRule(var="F")
der3.add_problem(n=2)

tangents = HorizontalTangents(var="G")
tangents.add_problem(n=2)

limit = PolyRatioLimit(var="H")
limit.add_problem(n=2)

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
