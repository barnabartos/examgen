from typing import Optional
from pylatex import Document, Package, Command, NoEscape, Section
from pylatex.base_classes import Environment
from pylatex.position import Center


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


class Questions(Environment):
    """A class to wrap exam class' question environment."""
    pass


class Parts(Environment):
    """A class to wrap exam class' question environment."""
    pass


class Exam(Document):
    def __init__(self, title: str):
        super().__init__()
        self.documentclass = Command(
            "documentclass",
            options=["12pt", "addpoints"],
            arguments=["exam"]
        )
        self.packages.append(Package("amsmath"))
        self.packages.append(Package("lastpage"))
        self.packages.append(
            Package(
                "geometry",
                options=[NoEscape("left = 12mm, right = 15mm, top = 20mm, bottom = 30mm")]
            )
        )
        self.preamble.append(Command("pagestyle", arguments=["headandfoot"]))
        self.preamble.append(
            Command(
                "renewcommand",
                arguments=[
                    Command("questionlabel"),
                    Command("textbf", Command("thequestion"))
                ]
            )
        )
        self.preamble.append(
            Command(
                "renewcommand",
                arguments=[
                    Command("partlabel"),
                    Command("textbf", Command("thepartno"))
                ]
            )
        )
        self.preamble.append(
            Command(
                "firstpageheader",
                arguments=[
                    NoEscape(title),
                    "",
                    NoEscape(r"Name: \underline{\hspace{2.5in}}")
                ]
            )
        )
        self.preamble.append(
            Command(
                "runningheader",
                arguments=[
                    NoEscape(title),
                    "",
                    NoEscape(r"Name: \underline{\hspace{2.5in}}")
                ]
            )
        )
        self.preamble.append(NoEscape(r"\runningheadrule"))
        self.preamble.append(NoEscape(r"\firstpageheadrule"))
        self.preamble.append(
            Command(
                "firstpagefooter",
                arguments=[
                    Command("textit", "https://github.com/barnabartos/examgen"),
                    Command("textbf", NoEscape(r"\thepage/\pageref{LastPage}")),
                    Command("textit", Command("today"))
                ]
            )
        )
        self.preamble.append(
            Command(
                "runningfooter",
                arguments=[
                    Command("textit", "https://github.com/barnabartos/examgen"),
                    Command("textbf", NoEscape(r"\thepage/\pageref{LastPage}")),
                    Command("textit", Command("today"))
                ]
            )
        )
        self.preamble.append(NoEscape(r"\runningfootrule"))
        self.preamble.append(NoEscape(r"\firstpagefootrule"))

    def add_sections(self, chapters):
        with self.create(Questions()):
            for chapter in chapters:
                self.append(Command("question"))
                if chapter["main"]["description"] is not None:
                    self.append(NoEscape(chapter["main"]["description"]))
                with self.create(Parts()):
                    for eq in chapter["main"]["equations"]:
                        self.append(NoEscape(r"\part $$" + eq + "$$"))

# with self.create(Center()):
#     self.append(
#         Command(
#             "fbox",
#             Command(
#                 "fbox",
#                 Command(
#                     "parbox",
#                     arguments=[
#                         "6in",
#                         NoEscape(r"\centering No notes, calculators, or other aids are allowed.")
#                     ]
#                 )
#             )
#         )
#     )
# self.packages.append(Package("amssymb"))
# self.packages.append(Package("amsfonts"))
# self.packages.append(Package("amsthm"))
# self.packages.append(Package("multicol"))
# self.packages.append(Package("graphicx"))
# self.packages.append(Package("systeme"))
# self.packages.append(Package("pgf"))
# self.packages.append(Package("tikz"))
# self.packages.append(Package("pgfplots"))
# self.packages.append(Package("mathrsfs"))

# self.preamble.append(Command("pgfplotsset", arguments=["compat=1.15"]))
# self.preamble.append(Command("usepgfplotslibrary", arguments=["fillbetween"]))
# self.preamble.append(Command("usetikzlibrary", arguments=["arrows"]))
# self.preamble.append(Command("usetikzlibrary", arguments=["calc"]))

# ex = Exam(title="title")
# ex.generate_pdf(filepath="asdf")
