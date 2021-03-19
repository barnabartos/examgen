from pylatex import Document, Package, Command, NoEscape
from pylatex.base_classes import Environment
from enum import Enum


class DocumentType(Enum):
    EXAM = "exam"
    SOLSKEY = "solskey"


class Parts(Environment):
    """A base class that represents a Question."""
    omit_if_empty = True

    def __init__(self):
        super(Parts, self).__init__()

    def add_part(self, s: str, points: int = None):
        self.append(Command("part", options=[points]))
        self.append(s)


class Questions(Environment):
    """A base class that represents a Question."""
    omit_if_empty = True

    def __init__(self):
        super(Questions, self).__init__()

    def add_question(self, chapter):
        self.append(Command("question"))
        if chapter["main"]["description"] is not None:
            self.append(NoEscape(chapter["main"]["description"]))
        with self.create(Parts()):
            for part in chapter["main"]["parts"]:
                self.append(NoEscape(r"\part $" + part["eq"] + "$"))
                if part["vspace"] is not None:
                    self.append(Command("vspace", part['vspace']))


class Exam(Document):
    def __init__(
            self,
            title: str,
            mode: DocumentType
    ):
        super().__init__(
            documentclass="exam",
            document_options=["12pt", "addpoints"],
            page_numbers=True,
            geometry_options={"left": "12mm", "right": "15mm", "top": "25mm", "bottom": "30mm"}
        )

        self.brand = Command("textit", "https://github.com/barnabartos/examgen")
        if mode == DocumentType.EXAM:
            self.hright = NoEscape(r"Name: \dotuline{\hspace{40mm}} \vspace{1mm}")
        elif mode == DocumentType.SOLSKEY:
            self.hright = ""
        else:
            raise ValueError(f"mode needs to be DocumentType not {mode}")
        self.headtitle = NoEscape(title + r"\vspace{1mm}")
        self.pgnum = Command("textbf", NoEscape(r"\thepage/\pageref{LastPage}"))
        self.date = Command("textit", Command("today"))

        self.packages.append(Package("amsmath"))
        self.packages.append(Package("ulem", options=["normalem"]))
        self.preamble.append(Command("pagestyle", arguments=["headandfoot"]))
        self.preamble.append(
            Command(
                "renewcommand",
                arguments=[
                    Command("questionlabel"),
                    Command("textbf", Command("thequestion."))
                ]
            )
        )
        self.preamble.append(
            Command(
                "renewcommand",
                arguments=[
                    Command("partlabel"),
                    Command("textbf", Command("thepartno)"))
                ]
            )
        )
        self.preamble.append(Command("firstpageheader", arguments=[self.headtitle, "", self.hright]))
        self.preamble.append(Command("runningheader", arguments=[self.headtitle, "", self.hright]))
        self.preamble.append(NoEscape(r"\runningheadrule"))
        self.preamble.append(NoEscape(r"\firstpageheadrule"))
        self.preamble.append(Command("firstpagefooter", arguments=[self.brand, self.pgnum, self.date]))
        self.preamble.append(Command("runningfooter", arguments=[self.brand, self.pgnum, self.date]))
        self.preamble.append(NoEscape(r"\runningfootrule"))
        self.preamble.append(NoEscape(r"\firstpagefootrule"))
