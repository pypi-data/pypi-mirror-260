"""Provides kindly verbs from makefiles with mkhelp docstrings"""

from __future__ import annotations

import dataclasses
import itertools
import pathlib
import subprocess
from typing import Iterable, List

from mkhelp._base import Docstring, Stream, Target


def _find_upwards(start: pathlib.Path, name: str) -> pathlib.Path:
    for parent in itertools.chain([start], start.parents):
        path = parent / name
        if path.exists():
            return path
    raise FileNotFoundError


@dataclasses.dataclass(frozen=True)
class MakefileCommand:
    cwd: pathlib.Path
    name: str
    help: str

    def __call__(self, args: List[str]) -> None:
        subprocess.check_call(("make", self.name), cwd=self.cwd)


class MakefileProvider:
    # pylint: disable=too-few-public-methods

    def __init__(self, cwd: pathlib.Path) -> None:
        self._cwd = cwd

    def v1_commands(self) -> Iterable[MakefileCommand]:
        try:
            makefile = _find_upwards(self._cwd, "Makefile")
        except FileNotFoundError:
            return

        docstrings = Docstring.take_all(Stream(makefile.read_text().splitlines()))
        for docstring in docstrings:
            if isinstance(docstring.ref, Target):
                yield MakefileCommand(
                    makefile.parent, docstring.ref, docstring.lines[0]
                )
