# ANODI

This is the Python library **ANODI** for Time Series Anomaly Detection. It offers easy access to algorithms and benchmark data.

Github: [Anodi](https://gitlab.fachschaften.org/timonius/anodi)

## Usage

- the core of the ANODI is the wrapper class ```algorithm``` which contains an specific algorithm and the data the algorithm should be fit on. 
- Each algorithm object offers functions like ```fit```, ```predict``` or ```getAnomalies```
- for example usage, have a look at the [test notebooks](https://gitlab.fachschaften.org/timonius/anodi/-/tree/dev/anodi/tests?ref_type=heads)
   - _! make sure you put a_ ```anodilib.``` _prefix before any anodi-specific import !_

## Dev Installation

This package is built using poetry, run the following code to install an editable version of the package for development
```
pip install poetry
poetry install
```

## Extenstions installation

Look for VSCode Flake8 extension to make sure pipeline doesn't fail at the lint stage