# Python SDK for the TruSTAR API

## API/SDK Documentation

See https://docs.trustar.co/ for the official documentation to the TruSTAR Python SDK.

## Installation

### Install
To install, run

```bash
pip install trustar
```

### Upgrade
If the package has been previously installed, upgrade to the latest version with

```bash
pip install --upgrade trustar
```

### Uninstall
To uninstall, simply run

```bash
pip uninstall trustar
```

## Tutorial and Examples

For a quick tutorial on using this package, follow the guide at https://docs.trustar.co/sdk/quick_start.html.

More examples can be found within this repository under `trustar/examples`

## Development

To setup this project for development, you need to have [pipenv](https://pipenv.pypa.io/en/latest/) installed and follow the next instructions:

1. Setup a virtual environment:
    ```bash
    pipenv install --dev
    ```

2. Activate the virtualenv:
    ```bash
    pipenv shell
    ```
3. Install this package in editable mode:
    ```bash
    pip install -e .
    ```

## Tests

This repository is built using tox to test the code with diferrent python versions. If you want to set up your development environment follow the instructions.

### Setup instructions

1. If you don't have tox installed in your system, do the following:

`pip install tox`

2. `tox --devenv <virtualenv_name> -e <python_environment>`

Where virtualenv_name is the name you choose for your virtual environment and python_environment is one of the supported python version `py39`.

For example:

`tox --devenv .venv-py39 -e py39`
`tox --devenv .venv-py310 -e py310`

3. Activate your virtual environment:

`source .venv-py39/bin/activate`

### Running tests

If you want to test all available environments:, just do:

`tox` in project's root

If you want to run a specific environment:

`tox -e py39` or `tox -e py310`


## Python 2 Compatibility
This package is no longer compatible with both `Python 2.7` (EOL 2020-01-01)

## Python 3 Compatibility
This package is no longer compatible with `Python 3.7` (EOL 2023-06-27). Minimum compatible version is `Python 3.9`
