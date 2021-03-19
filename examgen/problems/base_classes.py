import random
from typing import List, Optional
from random import choice, randrange, uniform
from datetime import datetime, timedelta

from examgen.constants import ALPHA, logger


class MathProb:
    instructions = "set this to default description in children"
    title = "set this to default title in children"
    var = ALPHA
    TIMEOUT = timedelta(seconds=5)

    def __init__(self, var: Optional[str] = None) -> None:
        self.problems = []
        self.solutions = []
        self.vspace = None
        if var is not None:
            if type(var) != str:
                raise TypeError("var has to be a string")
            if var == "":
                raise ValueError("var should not be an empty string")
            self.var = var

    def get_variable(self) -> str:
        if len(self.var) != 1:
            return choice(self.var)
        else:
            return self.var

    def shuffle(self):
        # todo investigate performance!
        temp = list(zip(self.problems, self.solutions))
        random.shuffle(temp)
        self.problems, self.solutions = zip(*temp)

    def get_coeffs(
            self,
            n: int,
            start: int,
            stop: int,
            integer: Optional[bool] = True,
            include_zero: bool = False,
            unique: bool = False
    ) -> List[float]:
        if type(n) != int:
            raise TypeError(f"type of n should be int, not {type(n)}")
        if n <= 0:
            raise ValueError(f"n must be a positive nonzero integer not {n}")
        if start >= stop:
            raise ValueError(f"start must be smaller than stop")
        ret = []
        deadline = datetime.now() + self.TIMEOUT
        while len(ret) < n:
            if datetime.now() > deadline:
                raise TimeoutError("variable generation timed out")
            if integer:
                num = randrange(start=start, stop=stop+1)
            else:
                num = uniform(a=start, b=stop)
            if not include_zero and num == 0:
                continue
            if unique:
                if num in ret:
                    continue
                if start < 0 and -num in ret:
                    continue
            ret.append(num)
        return ret

    def add_custom_problem(self, problem: str, solution: str):
        logger.warning(
            f"added custom exercise. \n problem: {problem}, solution {solution}\n" +
            "Custom exercises are not checked for correctness or LaTex compatibility, " +
            "by examgen, be careful!"
        )
        self.problems.append(problem)
        self.solutions.append(solution)

    def add_problem(self, n: int):
        raise NotImplementedError("function add_problem is not implemented!")

    def get_problems(self):
        return {
            "title": self.title,
            "main": {
                "description": self.instructions,
                "parts": [{"eq": i, "vspace": self.vspace} for i in self.problems]
            },
            "footer": None
        }

    def get_solutions(self):
        return {
            "title": self.title,
            "main": {
                "description": None,
                "parts": [{"eq": i, "vspace": None} for i in self.solutions]
            },
            "footer": None
        }
