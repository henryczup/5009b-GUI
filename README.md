# Valon 5009 Python GUI

The files in this directory deomstrate a simple Python/Tk GUI interface for the Valon 5009 synthesizer.

## Installation

This section contains basic instructions for the installation of this package in an isolated environment.

### Pip

```shell
python3 -m venv venv
source venv/bin/activate
pip install ./
```

## Usage

Once the package is installed, the GUI can be started using the `v5009cm` command followed by the serial port.
For example, when using `COM5`: 

To find out the port go into your device manager

```shell
v5009cm COM5
```
