from examgen.lib.docparts import LatexDoc
from examgen.lib.constants import logger
from pprint import pformat


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
        self.worksheet = LatexDoc(title=title)
        self.solutions = LatexDoc(title=title + " Solutions")

    def add_section(
            self,
            prob_generator,
    ) -> None:
        """
        Method for adding a section of problems to an worksheet & solutions.
        prob_generator : a problem generating object. Must implement a make() function,
            which returns a tuple of two strings
        n : the number of problems to generate for this section.
        title : title text for the section
        instructions : text instructions for the section
        """
        p, sols = prob_generator.to_json()
        logger.debug(pformat(p, indent=2))
        logger.debug(pformat(sols, indent=2))
        self.worksheet.add_section(chapter=p)
        self.solutions.add_section(chapter=sols)

    def write(self):
        self.worksheet.generate_pdf(filepath=self.fname, clean_tex=False)
        self.solutions.generate_pdf(filepath=f"sols_{self.fname}", clean_tex=False)
