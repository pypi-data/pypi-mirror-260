# Format iPython Cells

[![Tests](https://github.com/janosh/format-ipy-cells/actions/workflows/test.yml/badge.svg)](https://github.com/janosh/format-ipy-cells/actions/workflows/test.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/janosh/format-ipy-cells/main.svg)](https://results.pre-commit.ci/latest/github/janosh/format-ipy-cells/main)
[![Requires Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://python.org/downloads)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![PyPI](https://img.shields.io/pypi/v/format-ipy-cells?logo=pypi&logoColor=white)](https://pypi.org/project/format-ipy-cells)

Python code formatter (and [`pre-commit`](https://pre-commit.com) hook) for cell delimiters (`# %%`) in [VS Code-style interactive Python notebooks](https://code.visualstudio.com/docs/python/jupyter-support-py).

This formatter ensures

- cell delimiters are preceded by two empty lines:

    ```py
    # %% before
    foo='bar'
    # %%
    ```

    ```py
    # %% after
    foo='bar'


    # %%
    ```

- empty cells are removed:

    ```py
    # %% before

    # %%
    ```

    ```py
    # %% after
    ```

- comments on the same line as cell delimiters are separated by a single space:

    ```py
    # %%some comment before
    foo = 'bar'
    # %%    another comment
    ```

    ```py
    # %% some comment after
    foo = 'bar'
    # %% another comment
    ```

## Installation

```sh
pip install format-ipy-cells
```

## Usage

### CLI

```sh
format-ipy-cells path/to/file.py
# or
format-ipy-cells **/*.py
```

### As `pre-commit` hook

```yml
# .pre-commit-config.yaml

repos
  - repo: https://github.com/janosh/format-ipy-cells
    rev: v0.1.10
    hooks:
      - id: format-ipy-cells
```
