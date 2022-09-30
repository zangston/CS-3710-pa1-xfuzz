#!/usr/bin/env python

# Short script to benchmark the time required to response to one or more sequential requests
# from aiohttp.

import aiohttp
import argparse
import asyncio
import datetime
from pathlib import Path
from rich import print


async def main(args) -> None:
    async with aiohttp.ClientSession() as sess:
        # Perform a warm-up request
        async with sess.get(args.url) as _:
            ...

        print("[blue]Starting benchmarks")

        start = datetime.datetime.now()
        for _ in range(args.nrequests):
            async with sess.get(args.url) as _:
                ...
        end = datetime.datetime.now()

    total_time = (end - start).total_seconds()
    avg_time = total_time / args.nrequests

    print(f"[blue]Total time to perform requests:    [bold red]{total_time:10.5f}")
    print(f"[blue]Average time per request:          [bold red]{avg_time:10.5f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=Path(__file__).name,
        description="aiohttp benchmarking script",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("url", help="The URL to benchmark against")
    parser.add_argument(
        "-n", "--nrequests", type=int, default=1, help="The number of requests to perform sequentially."
    )

    args = parser.parse_args()
    asyncio.run(main(args))
