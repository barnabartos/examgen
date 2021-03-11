from typing import List, Tuple

import pytest

from test.constants import logger
from examgen.lib.base_classes import MathProb


@pytest.fixture()
def fix_problem_object(request) -> MathProb:
    """creates a Worksheet object"""
    return request.param


@pytest.fixture()
def fix_problem_method(
        request,
        fix_problem_object: MathProb
) -> Tuple[str]:
    """creates a Worksheet object"""
    logger.debug(f"recieved object {fix_problem_object}")
    method = getattr(fix_problem_object, request.param[0])
    logger.debug(f" calling method: {method}, with args: {request.param[1]}")
    method(*request.param[1])
    prob_json, sol_json = fix_problem_object.to_json()
    assert len(prob_json["main"]["equations"]) == 1, "please add only one problem"
    assert len(sol_json["main"]["equations"]) == 1, "please add only one problem"
    prob = prob_json["main"]["equations"][0]
    sol = sol_json["main"]["equations"][0]
    return prob, sol
