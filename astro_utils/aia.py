#!/bin/env python3
"""
Functions for visualizing SDO/AIA (Solar Dynamics Observatory/Atmospheric Imaging Assembly) data.

This module provides utilities for plotting and animating AIA images using the appropriate
SDO color maps for different wavelength passbands.
"""

import sunpy.visualization.colormaps as cm
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def plot_aia_image(data, passband, ax=None, show_colorbar=False, **kwargs):
    """
    Plot a single AIA image with the appropriate colormap for the given passband.

    Parameters
    ----------
    data : numpy.ndarray
        2D array containing the AIA image data
    passband : int or str
        AIA passband wavelength (e.g., 171, 193, 211)
    **kwargs : dict
        Optional keyword arguments:
            vmax : float
                Maximum value for the color scaling
            vmax_percentile : float
                Percentile value (0-100) to use for setting vmax

    Returns
    -------
    None
        Displays the plot using matplotlib
    """
    aia_cmap = matplotlib.colormaps[f'sdoaia{passband}']
    if ax is None:
        fig, ax = plt.subplots()
    if 'vmax_percentile' in kwargs:
        # TODO: validate the vmax_percentile value input
        vmax_percentile = kwargs.pop('vmax_percentile')
        if vmax_percentile is not None:
            kwargs['vmax'] = np.percentile(data, vmax_percentile)
    im = ax.imshow(data, cmap=aia_cmap, origin='lower', **kwargs)
    if show_colorbar:
        plt.colorbar(im, ax=ax)
    ax.axis("off")
    return im

def make_aia_movie(filename, data:np.ndarray, wavelength, timestamps:list = None, 
                   vmin=None, vmax=None, aarp_id=None, label=None):
    """
    Create an animation from a sequence of AIA images.

    Parameters
    ----------
    filename : str
        Output filename for the movie (should end in a valid movie extension)
    data : numpy.ndarray
        3D array containing the sequence of AIA images (time, y, x)
    wavelength : int or str
        AIA passband wavelength
    timestamps : list, optional
        List of timestamp strings for each frame
    vmin : float, optional
        Minimum value for scaling the images
    vmax : float, optional
        Maximum value for scaling the images
    aarp_id : str, optional
        AARP ID to display in the title
    label : str, optional
        Additional label to display in the title

    Returns
    -------
    None
        Saves the animation to the specified filename
    """
    cmap_key = 'sdoaia'+str(wavelength)
    sdoaia_cmap = matplotlib.colormaps[cmap_key]
    nframes = data.shape[0]
    fig, ax = plt.subplots()
    data = np.where(data<0, np.zeros_like(data), data)
    im = ax.imshow(np.sqrt(data[0,:,:]), cmap = sdoaia_cmap, origin='lower')
    def update(frame):
        im.set_array(np.sqrt(data[frame,:,:]))
        if timestamps:
            if aarp_id:
                if label is not None:
                    ax.set_title(f'{timestamps[frame]}_AARP_Id:{aarp_id}_Filter:{wavelength}_label:{label}')
    ani = FuncAnimation(fig, update, frames = nframes, interval=50)
    ani.save(f'{filename}', writer='ffmpeg', fps=1)
