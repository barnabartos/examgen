from typing import Tuple
from pylatex import Document, Package, Command, NoEscape, Section
from pylatex.base_classes import Environment
# from pylatex.table import Tabular

# class Tabular(Environment):
#     packages = [Package("tabular"), NoEscape(r"r@{\,}l")]


class Multicols(Environment):
    """A class to wrap LaTeX's multicol environment."""
    packages = [Package('multicol')]
    escape = False
    # content_separator = "\n"


class Enumerate(Environment):
    """A class to wrap LaTeX's enumerate environment."""
    packages = [Package('enumerate')]
    escape = False
    # content_separator = "\n"


class Solution(Environment):
    """A class to wrap LaTeX's enumerate environment."""
    packages = [Package('solution')]
    escape = False
    # content_separator = "\n"


class LatexDoc(Document):
    def __init__(self, title: str):
        super().__init__()
        self.packages.append(Package("amsfonts"))
        self.packages.append(Package("amsmath"))
        self.packages.append(Package("multicol"))
        self.packages.append(Package(NoEscape(f"eso-pic")))
        self.preamble.append(Command("title", NoEscape(title)))
        self.append(NoEscape(r"\maketitle"))

    def add_section(self, title: str, content: str):
        columns = 2
        with self.create(Section(title=title)):
            with self.create(Multicols(arguments=[str(columns)])):
                with self.create(Enumerate()):
                    self.append(NoEscape(content))

    # def add_exercise(self, instructions, problem, solution, points):
    #     self.append(NoEscape(r"\question"))
    #     self.append(NoEscape(instructions))
    #     self.append(NoEscape(problem))
    #     with self.create(Solution()):
    #         self.append(solution)


# def problem(instructions: str, problem: str, solution: str, points: int = 1) -> str:
#     code = """
#     \\question[%s]
#         %s
#         %s
#     \\begin{solution}
#         %s
#     \\end{solution}
#     """ % (str(points), instructions, problem, solution)
#     return code


# def oo_exam():
#     doc = Document(documentclass="exam")
#     doc.packages.append(Package("amsfonts"))
#     doc.packages.append(Package("amsmath"))
#     doc.packages.append(Package("multicol"))
#     doc.packages.append(Package(NoEscape(f"eso-pic")))
#     doc.preamble.append(Command("title", "hello, im a title"))
#     doc.preamble.append(NoEscape(r'\noprintanswers'))
#     doc.preamble.append(NoEscape(r'\addpoints'))
#     doc.preamble.append(
#         Command(
#             "qformat",
#             Command(
#                 "textbf",
#                 NoEscape(r"Question \\ \thequestion \quad(\thepoints)\hfill")
#             )
#         )
#     )
#     doc.packages.append(Package("color"))
#     doc.preamble.append(
#         Command(
#             "definecolor",
#             "SolutionColor rgb 0.8,0.9,1"
#         )
#     )
#     doc.preamble.append(NoEscape(r"\shadedsolutions"))
#     doc.preamble.append(
#         Command(
#             "renewcommand",
#             NoEscape(r"\solutiontitle}{\noindent\textbf{Solution:}\par\noindent")
#         )
#     )
#     doc.append(NoEscape(r'\maketitle'))
#     doc.append(
#         Command(
#             "AddToShipoutPicture",
#             Command(
#                 "AtTextUpperLeft",
#                 Command(
#                     NoEscape("makebox(400,45)"),
#                     "lt",
#                     # NoEscape(r"footnotesize") + \
#
#
#                 )
#             )
#         )
#     )
#     return doc.dumps()
#
#
# def exam_parts(title: str = "", author: str = "") -> Tuple[str, str]:
#     start = """
#     \\documentclass{exam}
#     \\usepackage{amsfonts}
#     \\usepackage{amsmath,multicol,eso-pic}
#     \\noprintanswers
#     \\addpoints
#     \\qformat{\\textbf{Question \\\\ \\thequestion}\\quad(\\thepoints)\\hfill}
#     \\usepackage{color}
#     \\definecolor{SolutionColor}{rgb}{0.8,0.9,1}
#     \\shadedsolutions
#     \\renewcommand{\\solutiontitle}{\\noindent\\textbf{Solution:}\\par\\noindent}
#
#     \\begin{document}
#     \\AddToShipoutPicture{
#         \\AtTextUpperLeft{
#         \\makebox(400,45)[lt]{
#           \\footnotesize
#           \\begin{tabular}{r@{\\,}l}
#             Name:  & \\rule{0.5\\linewidth}{\\linethickness} \\\\[.5cm]
#             Date:  & \\rule{0.5\\linewidth}{\\linethickness} \\\\
#           \\end{tabular}
#     }}}
#     \\begin{minipage}{.8\\textwidth}
#     This exam includes \\numquestions\\ questions. The total number of points is \\numpoints.
#     \\end{minipage}
#     \\begin{questions}
#     """
#
#     end = """\\end{questions}
#     \\end{document}
#     """
#     return start, end


