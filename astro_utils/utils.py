#!/bin/env python3
"""
This script provides utility functions for common tasks in astronomy.
Dependencies:
- astropy: A Python library for astronomy-related computations and file handling.

Usage:
Import the `read_fits_single` function from this script to read FITS files in your projects.

Example:
data = read_fits_single("example.fits")
"""

from astropy.io import fits

def read_fits_single(file_path):
    """
    Function to read FITS image containing single image from disk
    Also implements fix for "Too many files open" error 
    read more: https://docs.astropy.org/en/stable/io/fits/appendix/faq.html#id16
    """
    with fits.open(file_path) as hdul:
        data = hdul[0].data.copy()
    del hdul[0].data
    return data