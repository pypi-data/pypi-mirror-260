import json
import sys
from pathlib import Path
from typing import Any, Generator


def parse_incremental(data) -> Generator[Any, None, None]:
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(data):
        try:
            obj, pos = decoder.raw_decode(data, pos)
            yield obj
        except json.JSONDecodeError:
            pos += 1


def read_input(file: Path = None) -> Generator[Any, None, None]:
    """
    Read data from stdin or from a file.
    """
    if file:
        with open(file, "r") as f:
            return parse_incremental(f.read())
    else:
        return parse_incremental(sys.stdin.read())
