"""
Astro Utils
===========

A collection of utilities for astrophysics data processing and visualization.

Available modules:
----------------
aia : Functions for SDO/AIA image processing
flare : Solar flare data downloading and analysis
general : General FITS file handling utilities

Example usage:
-------------
>>> from astro_utils import read_fits_single
>>> from astro_utils.aia import plot_aia_image
>>> from astro_utils.flare import fetch_goes_data
"""

from .utils import read_fits_single

__all__ = [
    'read_fits_single',
]
