import os
from typing import Callable, Union

from examgen.lib.docparts import LatexDoc
from examgen.lib.algebra import make_quadratic_eq, make_linear_eq, make_rational_poly_simplify
from examgen.lib.calc1 import make_poly_ratio_limit, make_chain_rule_prob

_problems_map = {
    "Quadratic equations": make_quadratic_eq,
    "Linear equations": make_linear_eq,
    "Simplify quadratic ratio": make_rational_poly_simplify,
    "Limit of polynomial ratio": make_poly_ratio_limit
}


class Worksheet:
    """
    Class for managing an worksheet.
    """
    def __init__(self, fname: str, title: str = "", savetex: bool = False) -> None:
        """
        fname : file name for the worksheet
        title : title to be placed in the worksheet
        savetex : flag to either save or delete the .tex files after compiling
        """
        self.fname = fname
        self.worksheet = LatexDoc(title)
        self.solutions = LatexDoc(title + " Solutions")

    def add_section(
            self, problem_type: Union[Callable, str],
            n: int,
            title: str,
            instructions: str,
            cols: int = 2,
            *args,
            **kwargs
    ) -> None:
        """
        Method for adding a section of problems to an worksheet & solutions.
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
        if hasattr(problem_type, '__call__'):
            prob_generator = problem_type
        else:
            prob_generator = _problems_map[problem_type]

        # start, end = section_parts(title, instructions, cols)
        # sol_start, sol_end = section_parts(title, "", cols=1)
        s_probs, s_sols = [], []
        for i in range(n):
            p, sols = prob_generator(*args, **kwargs)
            if not isinstance(sols, list):
                sols = [sols]
            prob = "\\item " + p
            sols = "\\item" + ', '.join(sols)
            s_sols.append(sols)
            s_probs.append(prob)

        s_probs = '\n'.join(s_probs)
        s_sols = '\n'.join(s_sols)
        self.worksheet.add_section(title="problems", content=s_probs)
        self.solutions.add_section(title="solutions", content=s_sols)
        # prob_code = ''.join([start, s_probs, end])

        # sol_code = ''.join([sol_start, s_sols, sol_end])
        
        # self.worksheet.add(prob_code)
        # self.solutions.add(sol_code)

    def write(self):
        self.worksheet.generate_pdf(filepath=self.fname)
        self.solutions.generate_pdf(filepath=f"sols_{self.fname}")


if __name__ == "__main__":

    myworksheet = Worksheet("algebra1", "Algebra 101 worksheet 1", savetex=True)
    myworksheet.add_section(
        "Linear equations",
        10,
        "Linear equations",
        "Solve the following equations for the specified variable."
    )
    # myworksheet.add_section(
    #     "Simplify quadratic ratio",
    #     10,
    #     "Simplify each expression",
    #     ""
    # )
    # myworksheet.add_section(
    #     make_quadratic_eq,
    #     10,
    #     "Quadratic equations",
    #     "Solve the following quadratic equations.",
    #     ["x", "y", "z"]
    # )
    # myworksheet.add_section(
    #     "Limit of polynomial ratio",
    #     10,
    #     "Determine each limit",
    #     ""
    # )
    # myworksheet.add_section(
    #     make_chain_rule_prob,
    #     10,
    #     "Evaluate",
    #     ""
    # )
    myworksheet.write()
