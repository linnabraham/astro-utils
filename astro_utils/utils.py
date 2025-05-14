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

from datetime import datetime, timedelta
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

def time_convert(timestamp_str):
    """    
    Function originally written by Aryan - https://github.com/AryanVainala/

    Converts a given timestamp string into a Python `datetime` object. 
    The function attempts to parse the input string using a predefined list of 
    date and time formats. If the input does not match any of the formats, 
    a `ValueError` is raised.

    Args:
        timestamp_str (str): The timestamp string to be converted.

    Returns:
        datetime.datetime: A `datetime` object representing the parsed timestamp.

    Raises:
        ValueError: If the input string does not match any of the predefined formats.

    Supported Formats:
        - "%Y-%m-%dT%H:%M:%SZ"
        - "%Y.%m.%d_T%H:%M:%SZ"
        - "%Y-%m-%d %H:%M:%S"
        - "%Y-%m-%d"
        - "%d-%m-%Y"
        - "%m/%d/%Y"
        - "%Y/%m/%d"
        - "%d %B %Y"
        - "%B %d, %Y"
    """

    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y.%m.%d_T%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%d %B %Y",
        "%B %d, %Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError as e:
            print(f"Failed to parse '{timestamp_str}' with format '{fmt}': {e}")
    raise ValueError("Invalid date/timestamp format. Please try again.")

def get_start_and_end_time(timestamp, time_window_minutes):
    """
    Function originally written by Aryan - https://github.com/AryanVainala/

    Calculate the start and end time based on the central timestamp and time window.

    Args:
        timestamp (datetime.datetime): The reference timestamp.
        time_window_minutes (int): The time window in minutes to calculate the start and end times.

    Returns:
        tuple: A tuple containing two datetime.datetime objects:
            - start_time (datetime.datetime): The timestamp minus the time window.
            - end_time (datetime.datetime): The timestamp plus the time window.

    Example:
        >>> from datetime import datetime, timedelta
        >>> timestamp = datetime(2024, 12, 1, 12, 0, 0)
        >>> time_window_minutes = 30
        >>> get_start_and_end_time(timestamp, time_window_minutes)
        (datetime.datetime(2024, 12, 1, 11, 30), datetime.datetime(2024, 12, 1, 12, 30))
    """
    delta = timedelta(minutes=time_window_minutes)
    start_time = timestamp - delta
    end_time = timestamp + delta
    return start_time, end_time
