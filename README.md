# xfuzz

_**NOTE:**_ this is a programming assignment originally designed for CS 3710
*Intro to Cybersecurity* at the University of Virginia. This assignment covers
*web fuzzers*, and asks you to build your own fuzzer from the skeleton
provided here.

## Introduction

*Web fuzzers* are useful tools for exploring and auditing the security of web
applications. They can do any number of things, including

- Finding the pages and directories that are available on a webserver;
- brute-force a login page to try and login as a user;
- enumerate the [virtual hosts](https://en.wikipedia.org/wiki/Virtual_hosting)
  that are available on a webserver;
- and more!

There are many great web fuzzers already out there, like
[ffuf](https://github.com/ffuf/ffuf) and
[wfuzz](https://wfuzz.readthedocs.io/en/latest/). For this assignment, we will
be using the  [aiohttp](https://docs.aiohttp.org/en/stable/index.html) library
to build the fastest web fuzzer we can in the spirit of these other projects.

## Repository layout

The `xfuzz/` directory contains some skeleton code you can use to start building
out your fuzzer. This skeleton code contains the following files:

- `xfuzz/__main__.py`: the "entrypoint" script for `xfuzz`; this is the Python
  script that gets executed when you run `python3 -m xfuzz`.
- `xfuzz/__init__.py`: required to make Python [treat the `xfuzz/` diretory like
  a package](https://docs.python.org/3/tutorial/modules.html#packages).
- `xfuzz/cmd.py`: code for parsing command-line arguments to `xfuzz`.
- `xfuzz/fuzz.py`: contains the `fuzz` function, which takes the command-line
  arguments given to `xfuzz` after they've been parsed and pre-processed by the
  code in `cmd.py`.

Once you've [installed xfuzz](#installation) and its dependencies, you should
run `python3 -m xfuzz --help` to see how it should be used; you can use this to
start guiding your development.

### Modifying the source code

In general, you are free to implement `xfuzz` however you see fit. However,
there are a few things that you _**should not**_ change:

- Don't remove or change any of the command-line arguments specified in
  `xfuzz/cmd.py`. You can add new ones if you like; however, the [test
  harness](#pytest) expects the command line arguments to work in a certain way,
  and if you veer off it won't be able to score the lab correctly. Note that the
  built-in command line arguments are roughly the same as the arguments to
  [`ffuf`](https://github.com/ffuf/ffuf).

- Don't change the location or the function signature of the `fuzz` function in
  `xfuzz/fuzz.py`. This is the function that the test harness will call when it
  runs its tests.

### Dependencies

In addition to the above, you shouldn't modify the dependencies for `xfuzz`
specified in `requirements.txt` and `test.requirements.txt`; these will not get
installed when we grade your labs.

In general, the only libraries that you should import in your code should either
be `aiohttp` or something from the [Python Standard
Library](https://docs.python.org/3/library/index.html) (note that we will be
grading your assignments using Python 3.10). If you wish to include
nicely-formatted / colorized output in your program (*not required*), you may
also use the [rich
library](https://rich.readthedocs.io/en/stable/introduction.html), which has
been included alongside `aiohttp` in the `requirements.txt` file.

## Installation

Download this repository with

```bash
$ git clone https://github.com/kernelmethod/xfuzz
```

or by downloading the source directly as a `.zip` or `.tar.gz` file. Once you
have the code, you should create a [virtual
environment](https://docs.python.org/3/library/venv.html#venv-def) to install
the dependencies you'll need for `xfuzz` by calling the following from the
command line:

```
$ python3 -m venv ./venv
```

You can then download the project and testing dependencies with

```
$ source ./venv/bin/activate
$ pip install -r test.requirements.txt
```

### Running xfuzz

To run `xfuzz` on your machine, run the following in your terminal:

```
$ python3 -m xfuzz --help
```

This will display the default command line arguments available for `xfuzz`, as
well as some examples of how it should be used. Note that you will need to
implement these parts of `xfuzz` first before the example commands will work
correctly.

## Testing

There are two ways that you can test xfuzz: interactively, and with `pytest`. In
either case, you will want to install the dependencies in
`test.requirements.txt`, which you can do with

```
$ pip install -r test.requirements.txt
```

### Interactive testing

After installing the dependencies in `test.requirements.txt`, you can run a test
server for `xfuzz` locally by running the following command:

```
$ uvicorn test.interactive:server --host 0.0.0.0 --port 5000
```

This will run an HTTP server on `http://localhost:5000`. You can then run (in a
different terminal)

```
$ python3 -m xfuzz -u http://localhost:5000
```

along with any other options you want to run xfuzz against this local server.
For instance, once you've implemented the `fuzz()` function, you should be able
to run

```
$ python3 -m xfuzz -u http://localhost:5000/FUZZ
```

to see all of the pages in the top-level directory of the webserver.

### PyTest

For grading purposes, we will use PyTest to ensure that `xfuzz` works correctly.
You can run a series of automated tests for `xfuzz` by simply running

```
$ pytest
```

from your terminal. If all of the tests pass, then you've successfully completed
the assignment! Note that the test suite we use for grading will be slightly
different from the one that appears here, so you should be careful and make sure
that you've implemented everything correctly even after the tests pass.
