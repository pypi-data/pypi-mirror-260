# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from es7s.shared.enum import MarginMode, QuoteMode
from ..._base import CliCommand
from ..._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_ADAPTIVE, EnumChoice, HelpPart
from ..._decorators import cli_argument, cli_command, catch_and_log_and_exit, cli_option


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="system/stdin env variables",
    epilog=[
        HelpPart(
            "There is a support for result filtering; by default FILTERs are treated as extended regular "
            "expressions, but this can be altered with '--literal' option. Considerations:",
            "Filters:",
        ),
        HelpPart(
            "⏺ When there are two or more FILTERs specified, a key is considered matching if *any* of these "
            "filters do (i.e. OR operand is applied). Use '--and' to change this behaviour: with the option the "
            "variable will be printed only if *all* filters consequently match the var name.",
            indent_shift=1,
        ),
        HelpPart(
            "⏺ Search is case-insensitive unless any of filters contain one or more capital letters, in which "
            "case the search will be case-sensitive (however, this does not apply to literal mode, which is "
            "always case-sensitive).",
            indent_shift=1,
        ),
    ],
    command_examples=[
        "// @TODO",
    ],
)
@cli_option(
    "-S",
    "--stdin",
    is_flag=True,
    default=False,
    help="Read values from standard input instead of system environment (useful "
    "for redirecting output of '/bin/env' executed in a docker container or on "
    "a remote host).",
)
@cli_option(
    "-z",
    "--null",
    is_flag=True,
    default=False,
    help="Expect input values to be separated by `0x00` (NUL) bytes "
    "[default: by \\n], implies '--stdin'.",
)
@cli_option(
    "-l",
    "--literal",
    is_flag=True,
    default=False,
    help="Treat specified FILTERs as plain strings [default: as extended regexs].",
)
@cli_option(
    "-a",
    "--and",
    is_flag=True,
    default=False,
    help="Require *all* specified FILTERs to match the variable key [default: *any* FILTER].",
)
@cli_option(
    "-m",
    "--margin",
    type=EnumChoice(MarginMode, inline_choices=True),
    default=MarginMode.FULL,
    show_default=True,
    metavar="SIZE",
    help="Horizontal space around the output:",
)
@cli_option(
    "-q",
    "--quote",
    type=EnumChoice(QuoteMode, inline_choices=True),
    default=QuoteMode.AUTO,
    show_default=True,
    metavar="WHEN",
    help="Wrap values in quotes:",
)
@cli_option(
    "-n",
    "--no-prefix",
    is_flag=True,
    default=False,
    help="Do not prepend variable names with context-dependant prefixes.",
)
@cli_option(
    "-k",
    "--keep-sgr",
    is_flag=True,
    default=False,
    help="Do not remove SGRs from values even when '--no-color' is active.",
)
@cli_argument("filter", nargs=-1, required=False)
@catch_and_log_and_exit
class invoker:
    """
    One more environment variable list pretty-printer. Default mode: run '/bin/env',
    format its output and print the result. '--stdin' flag switches the application
    to reading and formatting standard input instead.\n\n

    Correctly processes `key = \"value\"\\n`... format. Therefore, other configs or settings
    files formatted similarly (e.g., 'mc' config or 'php.ini') can be pretty-printed as well.\n\n

    This command requires ++/bin/env++ to be present and available.\n\n
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_env import action
        action(**kwargs)
