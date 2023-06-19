# Valon 5009 Python GUI

The files in this directory deomstrate a simple Python/Tk GUI interface for the Valon 5009 synthesizer.

## Installation

This section contains basic instructions for the installation of this package in an isolated environment.

### Nix

This project uses [Nix](https://nixos.org/) Flakes to manage its environment and packages.
To start the default development shell:

```shell
nix develop
```

### Pip

If Nix is not your thing, this project can be installed (in a venv) using pip:

```shell
python3 -m venv venv
source venv/bin/activate
pip install ./
```

## Usage

Once the package is installed, the GUI can be started using the `v5009cm` command followed by the serial port.
For example, when using `/dev/ttyUSB0`:

```shell
v5009cm /dev/ttyUSB0
```
