# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import importlib.resources
from collections.abc import Iterator
from importlib.abc import Traversable
from pathlib import Path
from random import randint

from .path import DATA_PACKAGE


def get_res_dir(subpath: str | Path = None) -> Traversable:
    result = importlib.resources.files(DATA_PACKAGE)
    if subpath:
        return result.joinpath(subpath)
    return result


def get_demo_highlight_num_text() -> Traversable:
    return get_res_dir(Path("demo", "demo-hilight.txt"))


def get_demo_columns_text() -> Traversable:
    return get_res_dir(Path("demo", "demo-columns.txt"))


def get_demo_wrap_text() -> Traversable:
    return get_res_dir(Path("demo", "demo-wrap.txt"))


def get_demo_telegram_palette(idx: int = None) -> Traversable:
    if idx is None:
        idx = randint(1, 2)
    return get_res_dir(Path("demo", f"demo-tg-{idx}.tdesktop-palette"))


class DemoGradients:
    @classmethod
    def iter(cls) -> Iterator[Traversable]:
        for file in get_res_dir("demo").iterdir():
            if file.name.startswith("demo-gradient"):
                yield file
