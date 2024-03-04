# OGC API Test Client

A black box verifier for OGC API specifications

## Installation

This package is available on PyPi and can be installed with pip

```bash
$ python -m pip install ogctests
```

## Usage

### Command Line Interface

The test suite is designed to be run from the command line. At least one scope and an instance URL must be provided.
```bash
$ python -m ogctests <scope_1> [<scope_2>] -i <instance_url>
```

### Python callable

The test suite can also be called from within your python code by importing the `run_ogctests` function from 
the main module
```python
from ogctests.main import run_ogctests

scope = "features/core"
run_ogctests(scope)
```

You can optionally override the HTTP client used by the ogc test suite by passing a value to the `test_client`
argument.
This is especially useful if you want to integrate the ogctests into your own test suite, and have it use
your own test client.

```python
from fastapi import FastAPI
from fastapi.testing import TestClient

from ogctests.main import run_ogctests
app = FastAPI()
client = TestClient(app)

scope = "features/core"
run_ogctests(scope, client)
```

Thus, all requests made by the ogctests test suite will be done using the fastapi.testing.TestClient instead
of the default httpx.Client declared in the ogc test suite.

### Scoping

For instructions on how to scope the tests, call the package with the `-h` flag.

```bash
$ python -m ogctests -h
```

## Reporting

Reporting to stdout is as per normal pytest output. To increase the verbosity of the output set the `-v` flag to `True`.
To create a detailed report of the test run, set the `-r` flag to `True`. This will create a junitxml report in the users
home folder under `ogctestsReporting/<date>.xml`

## What it Does

In line with the
[Official OGC test suite](https://github.com/opengeospatial/ets-ogcapi-features10)
(written in Java), this Python-based test suite will verify the compliance of a
given endpoint with the
[OGC API - Features - Part 1: Core](https://docs.ogc.org/is/17-069r3/17-069r3.html)
specification.

The test suite only tests against the **OGC API - Features - Part 1:
Core** specification, But may be expanded in the future.

## See also

**An introduction to the OGC API specification**

- https://ogcapi-workshop.ogc.org/

**OGC API — Features — Part 1: Core**

- https://docs.ogc.org/is/17-069r3/17-069r3.html

**Official OGC test suite**

- https://github.com/opengeospatial/ets-ogcapi-features10

### Implementors
https://github.com/opengeospatial/ogcapi-features/tree/master/implementations/servers
