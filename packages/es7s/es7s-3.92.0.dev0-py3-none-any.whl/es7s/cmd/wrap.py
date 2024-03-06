# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t

import click
import pytermor as pt

from es7s.shared import get_stdout, get_demo_wrap_text
from ._base import _BaseAction


class action(_BaseAction):
    PRIVATE_REPLACER = "\U000E5750"

    def __init__(
        self,
        file: click.File | None,
        demo: bool,
        force_width: int = None,
        max_width: int = None,
        **kwargs,
    ):
        if force_width is not None:
            width = force_width
        else:
            width = pt.get_terminal_width(pad=0)
            if max_width:
                width = min(max_width, width)

        if demo:
            file = get_demo_wrap_text().open("rt")
        elif file is None:
            file = click.open_file("-", "r")

        try:
            self._run(file, width)
        finally:
            if not file.closed:
                file.close()

    def _run(self, inp: t.IO, width: int):
        result = pt.wrap_sgr(inp.readlines(), width)
        get_stdout().echo(result)
