# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from .._decorators import catch_and_log_and_exit, cli_argument, cli_command, cli_flag


@cli_command(__file__, "highlight numbers in text")
@cli_argument("file", type=click.File(mode="r"), required=False)
@cli_flag(
    "-d",
    "--demo",
    default=False,
    help="Ignore FILE argument and use built-in example text as input.",
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Read text from given FILE and highlight all occurrences of numbers with [prefixed] units. Color
    depends on value OOM (order of magnitude). If FILE is omitted or equals to ''-'', read standard
    input instead.\n\n

    Is used by es7s 'ls'.
    """
    from es7s.cmd.hilight_num import action

    action(*args, **kwargs)
