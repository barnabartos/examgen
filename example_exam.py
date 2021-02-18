from examgen.worksheet import Worksheet
from examgen.lib.calc1 import make_quotient_rule_prob

# make an exam with a filename and title
myexam = Worksheet("algebra1", "Algebra 101 worksheet 1", savetex=True)

# add some problem sections 
myexam.add_section(
    problem_type="Linear equations",
    n=20,
    title="Linear equations",
    instructions="Solve the following equations for the specified variable."
)
myexam.add_section(
    problem_type="Quadratic equations",
    n=20,
    title="Quadratic equations",
    instructions="Solve the following quadratic equations."
)
myexam.add_section(
    # todo fix this
    make_quotient_rule_prob,
    10,
    "Compute the derivative",
    ["x", "y", "z"]
)

# generate the exam and solutions pdf
myexam.write()
