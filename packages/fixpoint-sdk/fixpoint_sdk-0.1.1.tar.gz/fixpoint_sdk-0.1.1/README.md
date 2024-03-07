# Fixpoint Python SDK

The `FixpointClient` wraps the OpenAI API Client. You can call it just like OpenAI API Client. The sdk will intercept calls to certain OpenAI APIs, record input / outputs and forward that information to Fixpoint's api server.

## Installation

You can view the package on [pypi](https://pypi.org/project/fixpoint-sdk/). To install:

`pip install fixpoint-sdk`

## Usage

To use the sdk make sure that you have the following variables set in your environment: `FIXPOINT_API_KEY` and `OPENAI_API_KEY`.

## Development

### Virtual Env

To create a virtual environment called `venv` from your terminal run `python3 -m venv venv`.

#### Activate

`source venv/bin/activate`

#### Install packages

To install packages from `requirements.txt` in your virtual environment using
`pip` run: `pip install -r requirements.txt`.

If you want to install from the dependencies in `pyproject.toml` and not from
the `requirement.txt`, you can run:

```
pip install .

# or in "editable mode" so your install changes as you update the source code:
pip install -e .

# and to install dev dependencies
pip install -e '.[dev]'
```

#### Deactivate

`deactivate`

### Git hooks

Set up your Githooks via:

```
git config core.hooksPath githooks/
```

## Examples

You can find examples of how to use the API in `examples`.
