# Installation instructions

## Technical requirements

You must have Python version >= 3.7 installed on your system in order to run and
develop xfuzz. If you don't have Python installed on your system, you can
download it from [python.org](https://www.python.org/downloads/). You should be
able to run `xfuzz` on any operating system (but please keep in mind that for
grading purposes, we will test your code on Linux).

For installing the dependencies, you will also need to have `pip` and `venv`
installed (or a different package manager, like
[Anaconda](https://www.anaconda.com/)). You can check if these are installed on
your system by running

```
$ python3 -m pip --help
$ python3 -m venv --help
```

These should come installed by default if you downloaded Python from
[python.org](https://www.python.org/). In other cases (e.g. if you're using
Linux's default Python installation), you may need to install these manually. On
Debian and Ubuntu, you can run

```
$ apt-get install -y python3-pip python3-venv
```

## Download xfuzz and install dependencies

Download this repository with

```bash
$ git clone https://github.com/kernelmethod/xfuzz
```

or by downloading the source directly as a `.zip` or `.tar.gz` file. Once you
have the code, you should create a [virtual
environment](https://docs.python.org/3/library/venv.html) to install
the dependencies you'll need for `xfuzz` by calling the following from the
command line:

```
$ python3 -m venv ./venv
```

You can then activate your virtual environment with `source ./venv/bin/activate`
(MacOS / Linux) or `venv\Scripts\activate` (Windows). You can now install the
development dependencies for this project in the virtual environment with

```
$ python3 -m pip install -r dev.requirements.txt
```

If you don't like using `pip`, you can try using a different package manager
like [Anaconda](https://www.anaconda.com/) to install these dependencies.

## Running xfuzz

To run `xfuzz` on your machine, run the following in your terminal:

```
$ python3 -m xfuzz --help
```

This will display the default command line arguments available for `xfuzz`, as
well as some examples of how it should be used. Note that you will need to
implement these parts of `xfuzz` first before the example commands will work
correctly.
