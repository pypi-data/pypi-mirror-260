#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import pathlib
import sys

from kindly import _cli


def main() -> None:
    _cli.cli(pathlib.Path.cwd(), sys.argv[1:])
