import logging
from typing import List, Optional
from random import choice, randrange, uniform
from datetime import datetime, timedelta

from examgen.lib.constants import ALPHA, logger


class MathProb:
    INSTRUCTIONS = "set this to default description in children"
    TITLE = "set this to default title in children"
    var = ALPHA
    TIMEOUT = timedelta(seconds=5)

    def __init__(self, var: Optional[str] = None) -> None:
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
            if unique and num in ret:
                continue
            ret.append(num)
        return ret

    def make(self):
        raise NotImplementedError("function make is not implemented!")

    # def from_json(self):
    #     raise NotImplementedError
    #
    # def to_json(self):
    #     raise NotImplementedError

