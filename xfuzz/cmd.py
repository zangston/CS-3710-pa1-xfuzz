# Methods for setting up command line argument parsing.

import argparse
import typing as _t

# Default list of HTTP response status codes that we should match if the -mc argument
# is not passed in.
DEFAULT_MATCH_CODES: _t.Final[_t.List[int]] = [200, 301, 302, 401, 403]


def setup_argument_parser() -> argparse.ArgumentParser:
    """Create a new ``ArgumentParser`` instance to parse command-line arguments
    passed in to the script."""

    # NOTE: you may *not* change any of the command line arguments that are here by
    # default! These are needed to make the tests work correctly.

    parser = argparse.ArgumentParser(
        prog="xfuzz",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Add required arguments
    parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="The URL to fuzz",
    )

    # Add optional arguments
    parser.add_argument(
        "-w",
        "--wordlist",
        help=(
            "The wordlist to use (provided as a path to a local file). If not provided, xfuzz will "
            "read from stdin instead."
        ),
    )
    parser.add_argument(
        "-e",
        "--extension",
        action="append",
        help=(
            "One or more extensions to append (e.g. php, html, etc.). Multiple extensions "
            "may be provided."
        ),
    )
    parser.add_argument(
        "-X",
        "--method",
        default="GET",
        help="HTTP method to use (GET, POST, PUT, etc.)",
    )
    parser.add_argument(
        "-H",
        "--header",
        action="append",
        help=(
            'One or more HTTP headers to add to requests, in the form `"HeaderName: HeaderValue"` '
            '(e.g. `"Content-Type: application/json"` or `"Host: FUZZ.example.com"`). May be '
            "specified one or more times."
        ),
    )
    parser.add_argument(
        "-d",
        "--data",
        help="Data to send in the body of the HTTP request."
    )
    parser.add_argument(
        "-mc",
        type=int,
        action="append",
        help=(
            "Match HTTP response codes. May be specified multiple times. If let unspecified, "
            f"defaults to the following response codes: {DEFAULT_MATCH_CODES}"
        ),
    )

    # TODO: add any additional (optional) arguments that you want! However, note that these
    # arguments will not be supplied to the program during testing.

    return parser


def parse_args(argv=None) -> argparse.Namespace:
    """Parse command-line arguments and return them in an ``argparse.Namespace`` instance."""

    # NOTE: do *not* edit this function! The test harness expects arguments to be passed in to
    # the fuzz() function in a certain way.

    parser = setup_argument_parser()
    args = parser.parse_args(args=argv)

    # Set defaults for arguments with action="append"
    args.extensions = (
        [] if args.extension is None else [f".{ext}" for ext in args.extension]
    )
    args.headers = [] if args.header is None else args.header
    args.mc = DEFAULT_MATCH_CODES if args.mc is None else args.mc

    return args
