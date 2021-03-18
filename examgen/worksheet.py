from examgen.lib.docparts import Exam, Questions
from examgen.lib.constants import logger
from pprint import pformat


class Worksheet:
    """
    Class for managing an worksheet.
    """
    def __init__(self, fname: str, title: str = "", cleantex: bool = True) -> None:
        """
        fname : file name for the worksheet
        title : title to be placed in the worksheet
        savetex : flag to either save or delete the .tex files after compiling
        """
        self.cleantex = cleantex
        self.title = title
        self.fname = fname
        self.chapters = []

    def add_section(
            self,
            prob_generator,
    ) -> None:
        self.chapters.append(prob_generator)

    def write(self):
        worksheet = Exam(title=self.title)
        solutions = Exam(title=self.title + " Solutions")
        # todo: investigate performace / mem usage
        with worksheet.create(Questions()) as q:
            for chapter in self.chapters:
                q.add_question(chapter.get_problems())
        with solutions.create(Questions()) as q:
            for chapter in self.chapters:
                q.add_question(chapter.get_solutions())
        worksheet.generate_pdf(filepath=self.fname, clean_tex=self.cleantex)
        solutions.generate_pdf(filepath=f"sols_{self.fname}", clean_tex=self.cleantex)

