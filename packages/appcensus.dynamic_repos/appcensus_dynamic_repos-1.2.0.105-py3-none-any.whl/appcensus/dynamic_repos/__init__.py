import logging
import sys
from pathlib import Path

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


# hideous workaround for https://github.com/python-poetry/poetry/issues/8157:
# pydantic depends on a more recent typing_extensions than poetry pins
#
# thisisfine.jpg
try:
    from typing_extensions import TypeAliasType

    assert bool(TypeAliasType)
except ImportError:
    sys_path = sys.path
    try:
        sys.path = [x for x in sys.path if not x.endswith("poetry/core/_vendor")]
        del sys.modules["typing_extensions"]
        from typing_extensions import TypeAliasType
    finally:
        sys.path = sys_path

REPO_FILE_PATH: Path = Path("repos.toml")
