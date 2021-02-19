import logging
from sys import stdout

logger = logging.getLogger("examgen_pytest")
logger.setLevel(logging.DEBUG)  # set to logging.DEBUG for more information.
handler = logging.StreamHandler(stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(handler)
handler.setFormatter(formatter)
