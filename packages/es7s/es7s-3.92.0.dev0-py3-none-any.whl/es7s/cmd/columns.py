# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t

import click
from es7s_commons import columns

from es7s.shared import get_stdout, get_demo_columns_text, get_logger
from ._base import _BaseAction


class action(_BaseAction):
    def __init__(self, file: click.File | None, demo: bool, **kwargs):
        if demo:
            file = get_demo_columns_text().open("rt")
        elif file is None:
            file = click.open_file("-", "r")

        try:
            self._run(file, **kwargs)
        finally:
            if not file.closed:
                file.close()

    def _run(self, inp: t.IO, **kwargs):
        result, ts = columns(inp.read().splitlines(), **kwargs)
        get_stdout().echo(result)
        get_logger().debug(ts)
