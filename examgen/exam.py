import os
from typing import Callable, Union, List, Tuple

from examgen.lib.docparts import doc_parts, problem, exam_parts
from examgen.lib.algebra import make_quadratic_eq, make_linear_eq, make_rational_poly_simplify
from examgen.lib.calc1 import make_poly_ratio_limit, \
    make_chain_rule_prob, \
    make_quotient_rule_prob, \
    make_horizontal_tangents, \
    make_find_derivative_at_value
from examgen.worksheet import Document, _problems_map


class Exam:
    """
    Class for managing an exam.
    """
    def __init__(self, fname: str, title: str = "", savetex: bool = False):
        """
        fname : file name for the exam
        title : title to be placed in the exam
        savetex : flag to either save or delete the .tex files after compiling
        """

        self.fname = fname
        self.exam = Document(fname, title, savetex, doc_generator=exam_parts)

    def add_problem(
            self,
            problem_type: Union[Callable, str],
            instructions: str,
            points: int = 1,
            vspace: int = 200,
            # todo fix these asap
            args=(),
            kwargs={}
    ) -> None:
        """
        Method for adding a section of problems to an exam & solutions.
        problem_type : name of the type of problem, which is mapped to a
                       problem generating function shown at the top of this file

                                                OR
                       
                       A problem generating function directly. This function
                       must take no arguments, and return a tuple of two strings.
                       The first string gives the problem, the second string it's
                       solution.
        n : the number of problems to generate for this section.
        title : title text for the section
        instructions : text instructions for the section
        """
        # todo not sure about this one
        if hasattr(problem_type, '__call__'):
            prob_generator = problem_type
        else:
            prob_generator = _problems_map[problem_type]

        prob, soln = prob_generator(*args, **kwargs)
        soln = ''.join(soln)
        problem_code = problem(instructions, prob, soln, points)
        problem_code += "\\vspace{%spt}" % vspace
        self.exam.add(problem_code)

    def write(self) -> None:
        self.exam.write_compile(remove_aux=False)
        self.exam.write_compile()
        self.exam.start = self.exam.start.replace("\\noprintanswers", "\\printanswers")
        self.exam.fname += "_solutions"
        self.exam.write_compile(remove_aux=False)
        self.exam.write_compile()
        self.exam.fname = self.fname
        self.exam.start = self.exam.start.replace("\\printanswers", "\\noprintanswers")


# if __name__ == "__main__":
#
#     myexam = Exam("algebra1", "Algebra 101 exam 1", savetex=True)
#     myexam.add_problem(make_linear_eq, "Find all solutions")
#     myexam.add_problem(make_rational_poly_simplify, "Simplify")
#     myexam.add_problem(
#         make_quadratic_eq,
#         "Find all solutions",
#         kwargs={"var": "x", "integer": 1}
#     )
#     myexam.add_problem(
#         make_poly_ratio_limit,
#         "Evaluate",
#         kwargs={"var": "x", "s": 1}
#     )
#     myexam.add_problem(
#         make_chain_rule_prob,
#         "Compute the derivative",
#         kwargs={"var": ["x", "y", "z"]}
#     )
#     myexam.add_problem(
#         make_chain_rule_prob,
#         "Compute the derivative",
#         kwargs={"var": ["x", "y", "z"]}
#     )
#     myexam.add_problem(
#         make_quotient_rule_prob,
#         "Compute the derivative",
#         kwargs={"var": ["x", "y", "z"]}
#     )
#     myexam.add_problem(
#         make_horizontal_tangents,
#         "Find all values in the domain of $f$ where horizontal tangents occur",
#         kwargs={"var": ["x", "y", "z"]}
#     )
#     myexam.add_problem(
#         make_find_derivative_at_value,
#         "Suppose $f\\left(n \\right)$, given below, is the cost for the production of $n$ items. " +
#         "When $n=10$, what is the marginal cost?",
#         kwargs={"var": ["n"], "rhs": 10}
#     )
#     myexam.write()


