"""
todo: refactor this whole thing
"""

import random
import logging
from string import ascii_letters
from sys import stdout

import sympy


# gather up alphanumeric charectors we might want to use for variable names
ALPHA = list(ascii_letters)
# remove the ones that might be confusing in a problem
ALPHA.remove("l")
ALPHA.remove("o")
ALPHA.remove("O")
ALPHA.remove("I")
ALPHA.remove("i")
# gather up numerical digits we might want to use for coefficients
# nothing special about -26 to 26, other than it matches the number of chars
# above
digits = range(-26, 26)
# make a list of the nums above, but with zero removed. This way we know we
# can always guarantee selection of a non-zero digit (so the degree of a
# polynomial in an equation is at least a certain value)
digits_nozero = [i for i in range(-26, 26)]
digits_nozero.remove(0)


logger = logging.getLogger("examgen")
logger.setLevel(logging.ERROR)  # set to logging.DEBUG for more information.
handler = logging.StreamHandler(stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(handler)
handler.setFormatter(formatter)


def shuffle(x) -> list:
    # todo not sure about this one
    x = list(x)
    random.shuffle(x)
    return x


def render(expr, lhs=""):
    """
    Puts $ at the beginning and end of a latex expression.
    lhs : if we want to render something like: $x = 3 + 5$, set the left hand 
          side here
    """
    left = "$$"
    if lhs:
        left = f"$${lhs} ="
    return ''.join([left, sympy.latex(expr), "$$"])
