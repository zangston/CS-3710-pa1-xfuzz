# Entrypoint script for running the fuzzer. You can start this script
# by running
#
#   python3 -m xfuzz
#
# For instance, ``python3 -m xfuzz --help`` will provide information on
# the different command line parameters that are available by default.

# NOTE: do *not* edit this file! You should start writing your code in fuzz.py.

import asyncio
from xfuzz import fuzz, parse_args

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(fuzz(args))
