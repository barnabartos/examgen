from examgen.lib.docparts import LatexDoc


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
            n: int,
            title: str,
            instructions: str,
            cols: int = 2,
    ) -> None:
        """
        Method for adding a section of problems to an worksheet & solutions.
        prob_generator : a problem generating object. Must implement a make() function,
            which returns a tuple of two strings
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
