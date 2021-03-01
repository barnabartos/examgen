import random
from typing import Union, List, Optional
from random import choice, randrange, uniform
from itertools import chain

from examgen.lib.constants import alpha


class MathProb:
    INSTRUCTIONS = "set this to default description in children"
    TITLE = "set this to default title in children"
    var = alpha

    def __init__(self, var: Optional[str] = None) -> None:
        if var is not None:
            if var == "":
                raise ValueError("var should not be an empty string")
            self.var = var

    def get_variable(self) -> str:
        if len(self.var) != 1:
            return choice(self.var)
        else:
            return self.var

    @staticmethod
    def get_coeffs(
            n: int,
            start: int,
            stop: int,
            integer: Optional[bool] = True,
            include_zero: bool = False
    ) -> List[float]:
        ret = []
        if not include_zero and start < 0 and stop > 0:
            while len(ret) < n:
                if integer:
                    num = randrange(start=start, stop=stop)
                else:
                    num = uniform(a=start, b=stop)
                if num != 0:
                    ret.append(num)
            return ret
        else:
            if integer:
                return [randrange(start=start, stop=stop) for i in range(n)]
            else:
                return [uniform(a=start, b=stop) for i in range(n)]

    def make(self):
        raise NotImplementedError("function make is not implemented!")

    # def from_json(self):
    #     raise NotImplementedError
    #
    # def to_json(self):
    #     raise NotImplementedError
