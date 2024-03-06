# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023-2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from .._base_opts_params import IntRange
from .._decorators import cli_command, catch_and_log_and_exit, cli_argument, cli_option, cli_flag


@cli_command(__file__, short_help="&(fu)sion-&(dra)in, remote image generation neural network")
@cli_argument("prompt", type=str, required=True, nargs=-1)
@cli_option(
    "-w",
    "--width",
    help="Target image width.",
    type=IntRange(128, 1024, clamp=True),
    default=1024,
    show_default=True,
)
@cli_option(
    "-h",
    "--height",
    help="Target image height.",
    type=IntRange(128, 1024, clamp=True),
    default=1024,
    show_default=True,
)
@cli_option(
    "-s",
    "--style",
    help="Select picture style. List of supported styles can be seen with '-v'.",
    default="DEFAULT",
    show_default=True,
)
@cli_option(
    "-n",
    "--times",
    help="How many times each prompt should be queried.",
    type=IntRange(1),
    default=1,
    show_default=True,
)
@cli_option(
    "-T",
    "--threads",
    help="How many threads to perform API calls with (0=auto).",
    type=IntRange(0),
    default=0,
)
@cli_flag(
    "-D",
    "--delete",
    help="Delete image origins (default is to keep both the originals and merged composite).",
)
@cli_flag("-O", "--no-open", help="Do not call 'xdg-open' for merged result.")
@cli_flag("-R", "--no-retry", help="Do not repeat failed (censored) queries.")
@cli_flag("-S", "--stdin", help="Ignore 'PROMPT'S arguments and read from standard input instead.")
@catch_and_log_and_exit
class invoker:
    """
    Query a remote service with 'PROMPT'S describing what should be on the
    picture, wait for completion and fetch the result)). Several arguments in
    quotes treated as a single 'PROMPT', unless there are newlines:\n\n

        fudra \\"Prompt number one\\" \\"still same prompt\\"\n\n

        fudra $\\'Prompt number one\\n prompt number two\\'\n\n

    When '-S' is provided, the arguments are ignored completely, and standard
    input is read instead; expected format is the same -- one prompt per line.
    If a word starts with a hyphen \\"-\\", it is treated like 'negative' prompt.\n\n

    Total amount of result pictures is *P* * *N*, where *P* is prompts amount,
    and *N* is an argument of '--times' option (1 if omitted). Argument of
    '--threads' option does not influence picture amount, rather it controls
    how many jobs will be executed in parallel. There is an embedded retry
    mechanism, which will query the same prompt several times if the service
    answers with a placeholder and "'censored'" flag, or just fails with an
    error; retrying can be switched off with '--no-retry' flag.\n\n

    Successfully fetched results will be merged into one image in an array-like
    pattern, then the label with the original prompt will be added to the bottom
    of merged results. Originals are kept unless '-D' is given. The result will
    then be opened in an image viewer, unless disabled with '-O' option.\n\n

    Remote service is https://fusionbrain.ai. Requires ++gmic++ for image merging.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.fudra import action

        action(**kwargs)
