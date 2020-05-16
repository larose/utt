# Development

**Table of Contents**

- [System dependencies](#system-dependencies)
- [Python dependencies](#python-dependencies)
- [Formatting code](#formatting-code)
- [Code quality](#code-quality)
- [Executing `utt` from source](#executing-utt-from-source)
- [Tests](#tests)
    - [Unit tests](#unit-tests)
        - [Integration Tests](#integration-tests)



## System dependencies

You will need the following tools on your system to work on utt:

- [Python](https://www.python.org/)
- [Make](https://www.gnu.org/software/make/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)


## Python dependencies

Once the dependencies above have been installed on your system, you
can install utt's Python dependencies with this command:

`$ make bootstrap`


## Formatting code

All code must be properly formatted to be accepted in utt. You can
format the code with this command:

`$ make format`


## Code quality

We run a few checks to enforce a minimum code quality. You can run
them with this command:

`$ make lint`

It checks that the code is properly formatted (it shouldn't be an
issue if you ran `make format`) and a few other checks such as unused
imports, unused variables, etc.


## Executing `utt` from source

To run utt from local source:

`$ poetry run utt`


## Tests

This section is very important as most code changes need tests.

There are two kinds of tests: unit and integration tests.

You can run both with this command:

`$ make test`


### Unit tests

Unit tests are in-memory tests (i.e. no I/O) that runs very fast. They
are located in [../test/unit](../test/unit).

To run them:

`$ make test.unit`


#### Integration Tests

Integration tests test the entire system. They

1. build utt
2. build and start a docker container
3. install utt in the container
4. run tests in the container


Integration tests test the entire system. They 1) build utt, 2) build
and start a docker container, 3) install utt in the container, and 4)
run tests in the container.

Integration tests are located in
[../test/integration](../test/integration)


To run them:

`$ make test.integration`

The tests are listed in this [Makefile](../test/integration/Makefile)

You can also run a specific test. For example, to run the `hello`
test:

`$ make test.integration INTEGRATION_CMD=hello`

You can also spawn a shell in the container:

`$ make test.integration INTEGRATION_CMD=shell`

And, then you can run a specific test:

`$ make hello`

Note that the previous command must be run inside the container.
