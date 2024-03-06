# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from copy import copy
from dataclasses import dataclass
from typing import TextIO

import click
import pytermor as pt

from es7s.shared import get_logger, Styles, get_stdout
from es7s.shared.demo import get_demo_telegram_palette
from ._base import _BaseAction


@dataclass
class _ColorDef:
    raw_val: str | None
    chain: list[str]
    comment: str | None


class action(_BaseAction):
    def __init__(self, file: TextIO, demo: bool):
        if demo:
            file = get_demo_telegram_palette().open("rt")
        elif file is None:
            file = click.open_file("-", "r")
            get_stdout().echo("> ", nl=False)

        try:
            self._run(file)
        finally:
            if not file.closed:
                file.close()

    def _run(self, file: TextIO):
        self._defs: dict[str, tuple[str, str | None]] = dict()
        self._links = dict()

        for line in file:
            if ":" not in line or line.startswith("//"):
                continue
            comment = None
            if "//" in line:
                line, _, comment = line.partition("//")
                comment = comment.strip()

            try:
                name, val = line.split(":")
                self._defs.update({name.strip(): (val.strip().removesuffix(";"), comment)})
            except ValueError:
                get_logger().warning(f"Malformed color definition: {line!r}")

        M = max(map(len, self._defs.keys()))

        results: dict[str, _ColorDef] = dict()
        for k in self._defs:
            cdef = self._resolve(k)
            results.update({k: cdef})

        for k, cdef in results.items():
            cc = int(cdef.raw_val, 16)
            a = 255
            if len(cdef.raw_val) > 6:
                a = cc & 0xFF
                cc >>= 8

            smpst = pt.Style(fg=cc)
            fgst = pt.Style(bg=cc).flip().autopick_fg()
            if fgst.fg.hsv.value < 0.3:
                fgst.fg = pt.NOOP_COLOR

            links_num = self._links.get(cdef.chain[0], 0)

            prim_col = pt.NOOP_COLOR
            links_col = pt.NOOP_COLOR
            if links_num > 0:
                if len(cdef.chain) > 1:
                    prim_col = pt.cvr.METALLIC_BLUE
                    links_col = pt.cv.YELLOW
                else:
                    prim_col = pt.cvr.AIR_SUPERIORITY_BLUE
            elif len(cdef.chain) > 1:
                prim_col = Styles.TEXT_DEFAULT.fg

            chain: list[str] = copy(cdef.chain)
            for idx, key in enumerate(chain):
                if idx == 0:
                    chain[idx] = pt.Fragment(key.rjust(M), pt.Style(fg=prim_col, bold=True))
                else:
                    chain[idx] = " ← " + key

            links_w = 4
            if links_num > 0:
                links_fg = pt.Composite(
                    pt.Fragment(f" +{links_num}".ljust(links_w), pt.Style(fg=links_col))
                )
            else:
                links_fg = pt.pad(links_w)
            chain.insert(1, links_fg)

            if a == 0:
                samplech = " "
            elif a < 64:
                samplech = "░"
            elif a < 128:
                samplech = "▒"
            elif a < 192:
                samplech = "▓"
            else:
                samplech = "█"

            frags = [
                f" {a/2.55:>2.0f}% " if a < 255 else pt.pad(5),
                (samplech * 2, smpst),
                (f" {cc:06x} ", fgst),
                pt.Fragment("│", Styles.TEXT_DISABLED),
                *chain,
                pt.Fragment(pt.pad(2) + "// " + cdef.comment or "", Styles.TEXT_LABEL)
                if cdef.comment
                else "",
            ]
            pt.echo(pt.Text(*frags))

    def _resolve(self, k, stack=None) -> _ColorDef:
        if not stack:
            stack: list[str] = []
        stack.append(k)

        if k not in self._defs.keys():
            return _ColorDef(None, stack, None)

        v, com = self._defs.get(k)
        if v.startswith("#"):
            return _ColorDef(v[1:], stack, com)

        if v not in self._links.keys():
            self._links[v] = 0
        self._links[v] += 1

        return self._resolve(v, stack)
