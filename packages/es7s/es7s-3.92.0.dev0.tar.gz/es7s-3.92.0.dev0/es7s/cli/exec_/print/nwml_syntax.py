# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ..._base import CliCommand
from ..._base_opts_params import CMDTRAIT_ADAPTIVE, CMDTYPE_BUILTIN
from ..._decorators import catch_and_log_and_exit, cli_command


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="internal es7s markup syntax for command descriptions",
)
@catch_and_log_and_exit
class invoker:
    """
    Display NWML specification and examples. NWML stands for
    "Not-the-Worst-Markup-Language".\n\n
    """
    def __init__(self, **kwargs):
        from es7s.cmd.print_nwml_syntax import action
        action(**kwargs)
