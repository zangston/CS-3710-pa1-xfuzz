# Assignment instructions

- [Getting started](#getting-started)
- [Requirements](#requirements)
  - [Program output](#program-output)
  - [Flags](#flags)
  - [Fuzzable parameters](#fuzzable-parameters)
- [Restrictions](#restrictions)
- [References and tips](#references-and-tips)

See [README.md](README.md) for a high-level overview of xfuzz and information on
how to test xfuzz.

## Getting started

Before you start writing any code, you should set up xfuzz and its dependencies
by following the [installation instructions](INSTALL.md).

Once xfuzz is set up, you should start implementing it by working on the
`fuzz()` function defined in [xfuzz/fuzz.py](xfuzz/fuzz.py). This function is
called by xfuzz right after we read in and parse the command line arguments.

## Requirements

In order to get full points on this assignment, you will need to implement all
of the xfuzz features that are shown when you run

```
$ python3 -m xfuzz --help
```

You can use pytest (see [testing instructions](README.md#pytest)) to determine
whether or not you've implemented all of the features that you need.

### Program output

While running `xfuzz`, your program should generate one line of output for each
URL it encounters that returns an HTTP response with one of the status codes
given in `args.match_codes`.

For instance, here's what my toy implementation of `xfuzz` prints out when I
fuzz [http://ffuf.me/cd/basic](http://ffuf.me/cd/basic):

```bash
$ python3 -m xfuzz -u http://ffuf.me/cd/basic/FUZZ -mc 200 -w test/wordlists/common.txt 
Fuzzed value                            Status    
--------------------------------------------------
                                        200       
class                                   200       
development.log                         200       

Processed 4714 items
```

Your fuzzer can include whatever output you feel is appropriate, but at a
minimum you need to print out the value that you fuzzed and the HTTP response
status code.

### Flags

xfuzz will need to be able to understand each of the flags that are displayed.
Here is a quick overview of each of the flags, as well as how you can access
them from the `args` variable passed in to `fuzz()`.  Note that the `xfuzz`
command-line arguments are as close to those of ffuf as possible.

> -u / --url (`args.url`)

The URL that your fuzzer should target.

**Example:** `-u http://example.org`

> -w / --wordlist (`args.wordlist`)

The wordlist that your fuzzer should use.  If `-` is provided as the wordlist,
then you should read data from
[stdin](https://en.wikipedia.org/wiki/Standard_streams#Standard_input_(stdin))
(e.g. using [sys.stdin](https://docs.python.org/3/library/sys.html#sys.stdin))
instead. For example:

```
seq 1 1000 | python3 -m xfuzz -u http://example.org/user?id=FUZZ -w -
```

In this example, `xfuzz` should read its wordlist from the output of `seq 1
1000`, which it can do by reading from `sys.stdin`.

**Examples:**

- `-w /path/to/wordlist.txt`
- `-w -`

> -e / --extension (`args.extensions`)

One or more extensions that should optionally be appended to each value in the
wordlist. For instance, if your wordlist contains

```
index
hello
```

And the command

```
python3 -m xfuzz -w /path/to/wordlist -u http://example.org/FUZZ -e html -e php
```

is run, then the following URLs should be requested:

```
http://example.org/index.html
http://example.org/index.php
http://example.org/hello.html
http://example.org/hello.php
```

If no extensions are provided, then none should be appended to the items in the
wordlist.

**Example:** `-e html -e php`

> -X / --method (`args.method`)

The HTTP method (GET, POST, etc.) that should be used for requests. Note that
aiohttp allows you to specify the HTTP method for a request as a string using
the `ClientSession.request()` function:

```python
async with aiohttp.ClientSession() as sess:
  resp_get = await sess.request("GET", "http://www.example.org")
  resp_post = await sess.request("POST", "http://www.example.org")
```

**Examples:**

- `-X GET`
- `-X PUT`

> -H / --header (`args.headers`)

One or more [HTTP
headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) that should
be sent in the request

**Example:** `-H 'Content-Type: application/json' -H 'Host: www.example.com'`

> -d / --data (`args.data`)

Data to send in the body of the HTTP request.

**Example:** `--data '{"username": "admin", "password": "password123"}'`

> -mc (`args.match_codes`)

HTTP status codes that `xfuzz` should filter in. You should only print
fuzzed values for which the HTTP response you get has a status code in
`args.match_codes`.

**Example:** `-mc 200 -mc 302 -mc 403`

### Fuzzable parameters

In addition to implementing the flags mentioned above, it should be possible to
fuzz one of the parameters by constantly changing it using values from the
wordlist.

The following parameters should be fuzzable:

- The URL (`args.url`)
- The data (`args.data`)
- One of the headers (`args.headers`)

If `xfuzz` sees the term `FUZZ` in any of these values, then that should
indicate that it is a fuzzable parameter. `xfuzz` should repeatedly replace the
substring `FUZZ` with values from the wordlist until there are no more
candidates left to try.

Exactly one parameter should be fuzzable at any given time. If you see two or
more parameters with `FUZZ` in them, or none of the parameters have `FUZZ`, your
program should generate an error.

## Restrictions

In general, you are free to implement `xfuzz` however you see fit. However, to
ensure that your code doesn't break and that we're able to grade your assignment
correctly, there are a few things that you should not change.

In particular, **you should avoid modifying the command existing line arguments
for xfuzz** or their expected behavior (as described above). The [test
harness](README.md#pytest) expects the program to run in a certain way, and will
fail if your program does not behave correctly. The command line arguments for
xfuzz that appear in the output of `python3 -m xfuzz --help` and in the
[flags](#flags) section above are defined in [`cmd.py`](xfuzz/cmd.py) using
Python's [argparse](https://docs.python.org/3/library/argparse.html) library.

If you wish (and are comfortable using argparse), you may add _new_ command line
arguments, but keep in mind that these will not be explicitly supplied during
testing. Otherwise, you should avoid modifying [`cmd.py`](xfuzz/cmd.py).

Otherwise you are free to do as you wish. In general, you _should not_
modifying [`__init__.py`](xfuzz/__init__.py),
[`__main__.py`](xfuzz/__main__.py), or [`_typing.py`](xfuzz/_typing.py), but if
you know what these files do and are sure your changes won't break any tests you
may make modifications to them.

I recommend that you start modifying the code from the `fuzz()` function in
[`fuzz.py`](xfuzz/fuzz.py), which is the first function called after the command
line arguments are parsed.

### Dependencies

In addition to the above, you shouldn't modify the dependencies for `xfuzz`
specified in `requirements.txt` and `dev.requirements.txt`; these will not get
installed when we grade your labs.

In general, the only libraries that you should import in your code should either
be `aiohttp` or something from the [Python Standard
Library](https://docs.python.org/3/library/index.html) (note that we will be
grading your assignments using Python 3.10). If you wish to include
nicely-formatted / colorized output in your program (*not required*), you may
also use the [rich
library](https://rich.readthedocs.io/en/stable/introduction.html), which has
been included alongside `aiohttp` in the `requirements.txt` file.

## References and tips

For this problem you will need to use aiohttp heavily. To accomplish that, you
may want to use Python's built-in asyncio library as well. You can find the
documentation for each of these here:

- [aiohttp](https://docs.aiohttp.org/en/stable/index.html)
  - In particular, you will want to use aiohttp's client-side functionality. The
    [quickstart](https://docs.aiohttp.org/en/stable/client_quickstart.html)
    guide is a good place to check if this is your first time using aiohttp.
  - For maximum performance you should try to use `aiohttp.ClientSession`, but
    as you're just getting started you may find it easier to use the
    [`aiohttp.request`](https://docs.aiohttp.org/en/stable/client_reference.html#basic-api)
    method to make HTTP requests.
- [asyncio](https://docs.python.org/3/library/asyncio.html)

If you've never done asynchronous I/O before (in Python or elsewhere), here's a
quick overview: whenever you computer does any kind of input/output processing
(reading a file, performing an HTTP request, etc.), it has to wait a *loooong*
time (relative to how fast the CPU is going) before it gets back a response.

To speed things up, you perform multiple overlapping I/O operations
simultaneously, so that you aren't waiting as long for each individual I/O
operation to finish. For example, here's how we would make three asynchronous
HTTP requests to `www1.example.com`, `www2.example.com`, and `www3.example.com`
in Python with aiohttp:

```python
import aiohttp
import asyncio
from asyncio import create_task

async def main():
  tasks = []
  async with aiohttp.ClientSession() as sess:
    tasks.append(create_task(sess.get("http://www1.example.com")))
    tasks.append(create_task(sess.get("http://www2.example.com")))
    tasks.append(create_task(sess.get("http://www3.example.com")))
    responses = await asyncio.gather(*tasks)

if __name__ == "__main__":
  asyncio.run(main())
```

Instead of waiting for each of those requests to finish separately, we collected
them into a list and then waited for all of them to finish at the same time. By
using async I/O, we were able to perform more HTTP requests in a shorter period
of time.

If you are not very familiar with asynchronous I/O you shouldn't need to learn
much for this problem; however, it can take some getting used to the rules of
the `async` / `await` keywords. Here are some additional good discussions on the
topic that you can look into:

- https://en.wikipedia.org/wiki/Asynchronous_I/O
- https://realpython.com/async-io-python/
- https://realpython.com/python-async-features/
