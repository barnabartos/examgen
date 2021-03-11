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

    def add_section(self, chapter):
        with self.create(Section(title=chapter["title"])):
            if chapter["main"]["description"] is not None:
                self.append(chapter["main"]["description"])
            with self.create(Enumerate()):
                for eq in chapter["main"]["equations"]:
                    self.append(NoEscape(r"\item $$" + eq + "$$"))
