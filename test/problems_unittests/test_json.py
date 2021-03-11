from pprint import pformat

from jsonschema import validate

from examgen.lib.algebra import QuadraticEq
from examgen.lib.schema import chapter
from test.constants import logger


def test_json():
    eq = QuadraticEq()
    res = eq.to_json()
    validate(instance=res[0], schema=chapter)
    validate(instance=res[1], schema=chapter)
    logger.debug(f"\n{pformat(res, indent=2)}")
