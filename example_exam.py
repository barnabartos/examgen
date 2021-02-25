from examgen.worksheet import Worksheet
from examgen.lib.calc1 import QuotientRule
from examgen.lib.algebra import LinearEq, QuadraticEq

# make an exam with a filename and title
myexam = Worksheet("algebra1", "Algebra 101 worksheet 1", savetex=True)

# add some problem sections 
myexam.add_section(
    prob_generator=LinearEq(),
    n=20,
    title="Linear equations",
    instructions="Solve the following equations for the specified variable."
)
myexam.add_section(
    prob_generator=QuadraticEq(),
    n=20,
    title="Quadratic equations",
    instructions="Solve the following quadratic equations."
)
myexam.add_section(
    prob_generator=QuotientRule(var=["x", "y", "z"]),
    n=10,
    title="Compute the derivative",
    instructions=""
)

# generate the exam and solutions pdf
myexam.write()
