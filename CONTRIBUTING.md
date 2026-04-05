# Contributing to earthcare-dggs

Thank you for your interest in contributing!

## Development setup

```bash
git clone https://github.com/annefou/earthcare-dggs.git
cd earthcare-dggs
pixi install -e dev
pixi run -e dev jupyterlab
```

## Pre-commit hooks

Install pre-commit hooks to automatically strip notebook outputs and lint code:

```bash
pixi run -e dev pre-commit install
```

## Building documentation

```bash
pixi run -e docs build-docs          # Build static site
pixi run -e docs jupyter-book start  # Preview locally
```

## Code style

- Python code is formatted and linted with [ruff](https://github.com/astral-sh/ruff)
- Line length: 100 characters
- Absolute imports only (no relative imports)
- Notebook outputs are stripped before commit via nbstripout

## Reporting issues

Please use the [GitHub issue tracker](https://github.com/annefou/earthcare-dggs/issues).
