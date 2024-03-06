# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from .._base_opts_params import IntRange, CMDTYPE_BUILTIN, CMDTRAIT_ADAPTIVE
from .._decorators import catch_and_log_and_exit, cli_command, cli_argument, cli_option


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="rephrase input text preserving the semantics",
)
@cli_argument("file", type=click.File(mode="r"), required=False)
@cli_option(
    "-I",
    "--input",
    help="Ignore FILE argument and use TEXT as an input.",
)
@cli_option(
    "-T",
    "--threads",
    type=IntRange(0),
    default=0,
    help="How many threads to perform API calls with (0=auto).",
)
@cli_option(
    "-f",
    "--full",
    is_flag=True,
    help="Display all query results instead of a few ones.",
)
@cli_option(
    "-a",
    "--all",
    is_flag=True,
    help="Query all languages, not only the ones specified in preset list. Implies '-f'.",
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Rephrase input text from given FILE preserving the semantics (more or less).
    Under the hood queries translations API and perform double translation from
    ORIGIN language to one of the preset list and then from the currently
    processed language back to ORIGIN. ORIGIN language can be customized with
    <general.default-lang-code> config option, while preset list is defined as
    <cmd.transmorph.preset-lang-codes> option.\n\n

    If FILE is omitted or equals to ''-'', read standard input instead, unless
    there is a '-I' option, in which case use its argument as an input and
    ignore FILE.\n\n

    '-T0' instructs the program to use optimal number of threads equal to number
    of logical CPU cores. This can be limited by <cmd.transmorph.auto-threads-limit>
    config option.
    """
    from es7s.cmd.transmorph import action

    action(*args, **kwargs)
