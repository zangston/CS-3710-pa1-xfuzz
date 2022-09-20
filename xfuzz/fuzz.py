import aiohttp


async def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""

    # TODO: your code here!

    # ex: print the arguments that were passed in to this function
    print(f"args = {args}")

    # ex: make an HTTP request to the input URL
    async with aiohttp.ClientSession() as session:
        async with session.get(args.url) as resp:
            print(f"{args.url} - Status {resp.status}")
