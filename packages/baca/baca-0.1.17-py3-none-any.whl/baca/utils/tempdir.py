import tempfile
from pathlib import Path

from baca import __appname__


def create_tempdir() -> Path:
    return Path(tempfile.mkdtemp(prefix=f"{__appname__}-"))
