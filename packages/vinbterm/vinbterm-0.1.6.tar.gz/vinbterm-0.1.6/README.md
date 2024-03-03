[![Build Status](https://github.com/davidbrochart/nbterm/workflows/CI/badge.svg)](https://github.com/davidbrochart/nbterm/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# vinbterm

vinbterm is [nbterm](https://github.com/davidbrochart/nbterm) with some keybinding modifications, and setting edit mode as default.

The command is remained as `nbterm`, instead of "vinbterm".

Lets you view, edit and execute Jupyter Notebooks in the terminal.

## Install

```
pip install vinbterm
```


## Usage

Open an interactive notebook:

```
$ nbterm my_notebook.ipynb
```

Run a notebook in batch mode:

```
$ nbterm --run my_notebook.ipynb
```

## Key bindings

There are two modes: edit mode, and command mode.

- `i`: enter the edit mode, allowing to type into the cell.
- `esc`: exit the edit mode and enter the command mode.

In command mode:

- `k` or `up`: select cell above.
- `j` or `down`: select cell below.
- `ctrl-k` or `ctrl-up`: move cell above.
- `ctrl-j` or `ctrl-down`: move cell below.
- `a`: insert cell above.
- `b`: insert cell below.
- `d`: cut the cell.
- `y`: copy the cell.
- `ctrl-p`: paste cell above.
- `p`: paste cell below.
- `c`: set as code cell.
- `r`: set as raw cell.
- `m`: set as Markdown cell.
- `l`: clear cell outputs.
- `ctrl-e`: run cell.
- `enter` or `ctrl-r`: run cell and select below.
- `ctrl-w` or `ctrl-s`: save.
- `ctrl-q`: exit.
- `ctrl-h`: show help.
