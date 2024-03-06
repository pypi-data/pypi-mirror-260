# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t
from dataclasses import dataclass

import pytermor as pt
from pytermor import FT, RT, Align, IRenderer


Size = int | float | None


class _Size:
    def __init__(self, val: Size):
        if isinstance(val, (int, float)) and val <= 0:
            val = 0
        self._val = val

    def to_chars(self, base: int):
        if isinstance(self._val, int):
            return self._val
        if isinstance(self._val, float):
            return round(base * self._val)
        return self._val


AUTO = _Size(None)


@dataclass(frozen=True)
class ElasticSetup:
    min_width: _Size = AUTO
    max_width: _Size = AUTO
    basis: float = 1.00
    shrink: float = 1.00
    grow: float = 0.00
    align: pt.Align = pt.Align.LEFT
    keep: pt.Align = pt.Align.LEFT


class ElasticFragment(pt.Fragment):
    def __init__(
        self,
        es: ElasticSetup,
        string: str = "",
        fmt: FT = None,
        *,
        close_this: bool = True,
        close_prev: bool = False,
    ):
        self._elastic_setup = es
        super().__init__(string, fmt, close_this=close_this, close_prev=close_prev)

    @property
    def elastic_setup(self) -> ElasticSetup:
        return self._elastic_setup


class ElasticContainer(pt.Composite):
    def __init__(self, width: Size = None, gap: Size = 2, *parts: RT):
        super().__init__(*parts)
        self._width: _Size = _Size(width)
        self._gap: _Size = _Size(gap)
        self.set_width(width)

    def render(self, renderer: IRenderer | t.Type[IRenderer] = None) -> str:
        if self._width.to_chars() < 1:
            return ""
        return super().render(renderer)

# @TEMP
@
class Elastic:
    @classmethod
    def compute(cls, container: ElasticContainer, elements: t.Iterable[ElasticFragment]):
        avail_width = container.width
        occupied_width_base = sum(len(el) for el in elements)
