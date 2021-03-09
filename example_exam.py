from examgen.worksheet import Worksheet
from examgen.lib.calc1 import QuotientRule, \
    ChainRule, \
    FindDervative, \
    HorizontalTangents, \
    PolyRatioLimit
from examgen.lib.algebra import LinearEq, QuadraticEq, RationalPolySimplify

# make an exam with a filename and title
myexam = Worksheet("example_worksheet", "Example worksheet 1", savetex=True)

# add some problem sections 
myexam.add_section(
    prob_generator=LinearEq(var="xyz"),
    n=20,
    title="Linear equations",
    instructions="Solve the following equations for the specified variable."
)
myexam.add_section(
    prob_generator=QuadraticEq(var="xyz"),
    n=20,
    title="Quadratic equations",
    instructions="Solve the following quadratic equations."
)
myexam.add_section(
    prob_generator=RationalPolySimplify(var="xyz"),
    n=5,
    title="simplify the expressions",
    instructions=""
)
myexam.add_section(
    prob_generator=QuotientRule(var="xyz"),
    n=10,
    title="Compute the derivative",
    instructions=""
)
myexam.add_section(
    prob_generator=ChainRule(var="xyz"),
    n=10,
    title="Compute the derivative",
    instructions=""
)
myexam.add_section(
    prob_generator=FindDervative(var="xyz"),
    n=10,
    title="Compute the derivative",
    instructions=""
)
myexam.add_section(
    prob_generator=PolyRatioLimit(var="xyz"),
    n=10,
    title="Find the limit",
    instructions=""
)
myexam.add_section(
    prob_generator=HorizontalTangents(var="xyz"),
    n=10,
    title="asdf",
    instructions=""
)

# generate the exam and solutions pdf
myexam.write()
