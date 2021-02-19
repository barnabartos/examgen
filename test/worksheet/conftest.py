import pytest
from test.constants import logger

from examgen.worksheet import Worksheet


@pytest.fixture()
def fix_worksheet(request) -> Worksheet:
    """creates a Worksheet object"""
    ws = Worksheet(fname=request.param[0], title=request.param[1])
    logger.debug(f"created worksheet{ws}")
    return ws


@pytest.fixture()
def fix_sections(
        request,
        fix_worksheet
):
    """adds sections for each item in request"""
    ws = Worksheet(fname="test", title="test")
    for section in request.param:
        fix_worksheet.add_section(*section)
        logger.debug(f"added section {section}")
    return ws
