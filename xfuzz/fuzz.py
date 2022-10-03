import aiohttp
import asyncio

async def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""

    # TODO: your code here!

    # ex: print the arguments that were passed in to this function
    print(f"args = {args}")

    '''
    # ex: make an HTTP request to the input URL
    async with aiohttp.ClientSession() as session:
        async with session.get(args.url) as resp:
            print(f"{args.url} - Status {resp.status}")
    '''

    # Read in wordlist from args in an array
    wordlist = []
    with open(args.wordlist) as file:
        for line in file:
            wordlist.append(line)

    '''
    # Print wordlist array
    for word in wordlist:
        print(word)
    '''

    '''
    This is to handle the parameter that's being fuzzed
    xfuzz should return an error if no parameter is supplied, or if too many parameters are supplied
    '''
    fuzzcount = 0;
    fuzzparam = ''

    if 'FUZZ' in args.url:
        fuzzcount += 1
        fuzzparam = 'url'
    if 'FUZZ' in args.headers:
        fuzzcount += 1
        fuzzparam = 'headers'
    if args.data is not None:
        if 'FUZZ' in args.data:
            fuzzcount += 1
            fuzzparam = 'data'
    if fuzzcount == 0:
        print("Error - no parameter supplied. You haven't told us what to fuzz!.")
        return
    else:
        if fuzzcount > 1:
            print("Error - too many parameters supplied. Only one parameter can be fuzzed at a time")
            return

    '''
    The fuzzing part
    '''
    tasks =[]
    urls = []
    if fuzzparam == 'url':
        for word in wordlist:
            url = args.url.replace('FUZZ', word)
            urls.append(url)

        async with aiohttp.ClientSession() as sess:
            for u in urls:
                task = asyncio.create_task(sess.request("GET", u))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)

        print('Fuzzed value - Status code')
        for r in responses:
            if r.status in args.match_codes:
                print(str(r.url) + " - " + str(r.status))
        print('Processed ' + str(len(responses)) + ' items')