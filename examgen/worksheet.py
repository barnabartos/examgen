import os
from typing import Callable, Union

from examgen.lib.docparts import LatexDoc
from examgen.lib.algebra import make_quadratic_eq, make_linear_eq, make_rational_poly_simplify
from examgen.lib.algebra import QuadraticEq, LinearEq, RationalPolySimplify
from examgen.lib.calc1 import make_poly_ratio_limit, make_chain_rule_prob
from examgen.lib.calc1 import PolyRatioLimit, ChainRule


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
            self,
            prob_generator,
            n: int,
            title: str,
            instructions: str,
            cols: int = 2,
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
        s_probs, s_sols = [], []
        for i in range(n):
            p, sols = prob_generator.make()
            if not isinstance(sols, list):
                sols = [sols]
            prob = "\\item " + p
            sols = "\\item" + ', '.join(sols)
            s_sols.append(sols)
            s_probs.append(prob)

        s_probs = '\n'.join(s_probs)
        s_sols = '\n'.join(s_sols)
        self.worksheet.add_section(title=title, instructions=instructions, content=s_probs, cols=cols)
        self.solutions.add_section(title=title, content=s_sols, cols=cols)

    def write(self):
        self.worksheet.generate_pdf(filepath=self.fname)
        self.solutions.generate_pdf(filepath=f"sols_{self.fname}")


if __name__ == "__main__":

    myworksheet = Worksheet("algebra1", "Algebra 101 worksheet 1", savetex=True)
    myworksheet.add_section(
        prob_generator=LinearEq(),
        n=10,
        title="Linear equations",
        instructions="Solve the following equations for the specified variable."
    )
    myworksheet.add_section(
        prob_generator=RationalPolySimplify(),
        n=10,
        cols=1,
        title="Simplify each expression",
        instructions=""
    )
    myworksheet.add_section(
        prob_generator=QuadraticEq(var=["x", "y", "z"]),
        n=10,
        title="Quadratic equations",
        instructions="Solve the following quadratic equations.",
    )
    myworksheet.add_section(
        prob_generator=PolyRatioLimit(),
        n=10,
        title="Determine each limit",
        instructions=""
    )
    myworksheet.add_section(
        prob_generator=ChainRule(),
        n=10,
        title="Evaluate",
        instructions=""
    )
    myworksheet.write()
