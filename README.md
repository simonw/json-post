# json-post

[![PyPI](https://img.shields.io/pypi/v/json-post.svg)](https://pypi.org/project/json-post/)
[![Changelog](https://img.shields.io/github/v/release/simonw/json-post?include_prereleases&label=changelog)](https://github.com/simonw/json-post/releases)
[![Tests](https://github.com/simonw/json-post/workflows/Test/badge.svg)](https://github.com/simonw/json-post/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/json-post/blob/master/LICENSE)

Tool for posting JSON to an API, broken into pages

## Installation

Install this tool using `pip`:

    $ pip install json-post

## Usage

Run `json-post --help` for options.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd json-post
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
