# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from ..._base_opts_params import CMDTRAIT_ADAPTIVE, IntRange
from ..._decorators import catch_and_log_and_exit, cli_argument, cli_command, cli_option, cli_flag


@cli_command(__file__, "Launch a demonstration of Gradient component.", traits=[CMDTRAIT_ADAPTIVE])
@cli_argument("file", type=click.File(mode="r"), nargs=-1, required=False)
@cli_option(
    "-h",
    "--height",
    type=IntRange(1, max_open=True, show_range=False),
    default=1,
    show_default=True,
    help="Gradient scale height in characters.",
)
@cli_option(
    "-x",
    "--extend",
    type=IntRange(0, 3, clamp=True, show_range=False),
    default=0,
    count=True,
    help="Display detailed info about gradient segments. Can be used multiple times to increase "
    "the details amount even further ('-xx', '-xxx').",
)
@cli_flag("-d", "--demo", help="Discard all FILEs and display a few library presets instead.")
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Read data from given FILE, build and display a gradient based on it. The only supported format is
    GIMP gradient (**.ggr*). If FILE is omitted or equals to ''-'', read standard input instead.
    Multiple FILEs supported.
    """
    from es7s.cmd.print_gradient import action
    action(**kwargs)
