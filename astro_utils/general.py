#!/bin/env python3
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
