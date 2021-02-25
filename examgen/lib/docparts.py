from typing import Optional
from pylatex import Document, Package, Command, NoEscape, Section
from pylatex.base_classes import Environment


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

    def add_section(self, title: str, content: str, cols: Optional[int] = 2, instructions: Optional[str] = None):
        with self.create(Section(title=title)):
            if instructions:
                self.append(instructions)
            with self.create(Multicols(arguments=[str(cols)])):
                with self.create(Enumerate()):
                    self.append(NoEscape(content))
