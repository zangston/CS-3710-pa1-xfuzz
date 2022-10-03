import sys

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

    """
    Read in wordlist, depending on parameters supplied
    if "-" is supplied, read wordlist from sys.stdin,
    else read wordlist from file passed in.
    if no wordlist is supplied, then terminal should give an error
    """
    wordlist = []
    if args.wordlist == "-":
        for line in sys.stdin:
            if 'q' == line.rstrip():
                break
            wordlist.append(line)
    else:
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
    tasks = []
    urls = []

    """
    This block handles converting data parameters into a string to be 
    passed into session request
    """
    data = ''
    if args.data:
        data = args.data.replace("{", '"')
        data = data.replace("}", '"')
        data = data.replace(":", "=")
        data = data.replace(",", "&")
    print("data: " + data)

    """
    This block handles converting passed in header parameters into a dictionary
    """
    headers = {}
    keys = []
    values = []
    for h in args.headers:
        x = h.split()
        keys.append(x[0])
        values.append(x[1])
    # print('keys: ' + str(keys))
    # print('values: ' + str(values))
    for i in range(len(keys)):
        headers[keys[i]] = values[i]
    print('headers: ' + str(headers))

    """
    This code block handles all features relating to URL fuzzing
    """
    if fuzzparam == 'url':
        # print(fuzzparam)
        for word in wordlist:
            url = args.url.replace('FUZZ', word)
            urls.append(url)
            if args.extensions:
                for e in args.extensions:
                    if e not in url:
                        urle = url + e
                    urls.append(urle)

        async with aiohttp.ClientSession() as sess:
            for u in urls:
                task = asyncio.create_task(sess.request(args.method, u, data=data, headers=headers))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)

        print('Fuzzed value - Status code')
        for r in responses:
            if r.status in args.match_codes:
                print(str(r.url) + " - " + str(r.status))
        print('Processed ' + str(len(responses)) + ' items')
        return

    """
    This code block handles data fuzzing, brute force login
    """
    """
    if fuzzparam == 'data':
        # print(fuzzparam)
        dataf = []
        for word in wordlist:
            d = data.replace('FUZZ', word)
            print(d)
            dataf.append(d)

        async with aiohttp.ClientSession() as sess:
            for d in dataf:
                task = asyncio.create_task(sess.request(args.method, args.url, data=d))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)

        print('Data combination - Status code')
        for r in responses:
            if r.status in args.match_codes:
                # print(data + " - " + str(r.status))
                print(r)
        print('Processed ' + str(len(responses)) + ' items')
    """

