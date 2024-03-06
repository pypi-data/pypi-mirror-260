# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import click

from ..._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_NONE
from ..._decorators import cli_command, cli_option, catch_and_log_and_exit, cli_argument


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_NONE],
    short_help="print formatted telegram palette contents",
)
@cli_argument("file", type=click.File(mode="r"), required=False)
@cli_option(
    "-d",
    "--demo",
    is_flag=True,
    default=False,
    help="Ignore FILE argument and use built-in example text as input.",
)
@catch_and_log_and_exit
class invoker:
    """
    Read the specified FILE, or stdin if argument is omitted or provided as ''-'',
    parse 'Telegram Desktop' theme specification and display it. The output contains
    color previews and definition inheritance chains.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_tg_theme import action
        action(**kwargs)
