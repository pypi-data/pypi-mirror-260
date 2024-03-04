# AIPY for EOVSA

[![Build Status](https://github.com/HERA-Team/aipy/workflows/Run%20Tests/badge.svg)](https://github.com/HERA-Team/aipy/actions)
[![Coverage Status](https://codecov.io/gh/HERA-Team/aipy/branch/master/graph/badge.svg?token=Vrr4XFcE8p)](https://codecov.io/gh/HERA-Team/aipy)

AIPY (Astronomical Interferometry in Python) is a library designed to support radio astronomical interferometry. This fork is specifically customized for handling data from the Expanded Owens Valley Solar Array (EOVSA).

## Features

- Pure-python phasing, calibration, imaging, and deconvolution.
- Interfaces to MIRIAD (Fortran interferometry package) and HEALPix (spherical data sets representation).
- Custom modifications to support the large total power data array sizes encountered in EOVSA data.

## Requirements

- Python 3 (3.0.x version series or newer)
- For Python 2 support, please refer to versions prior to 3.0.x.

## Installation

To install AIPY for EOVSA, you can use `pip`:

```bash
pip install aipy-ovsa
```

For development purposes, you can install the source code in editable mode and build extensions in place:

```bash
pip install -e .
python setup.py build_ext --inplace
```

## License

AIPY is licensed under the GNU General Public License (GPL), version 2 or later, ensuring it remains free software for all users. For the complete terms and conditions, refer to the [LICENSE](LICENSE) file.

For specific acknowledgements and licensing details regarding subpackages and included source code (such as "optimize" from SCIPY, the "cephes" Math Library, the HEALPix collaboration, and "miriad"), please see the license section.