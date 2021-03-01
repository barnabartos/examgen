from typing import List

import pytest

from test.constants import logger


@pytest.fixture()
def fix_problem_output(request) -> List[str, str]:
    """creates a Worksheet object"""
    prob = request.param
    logger.debug(f" calling make on {prob}")
    return prob.make()
