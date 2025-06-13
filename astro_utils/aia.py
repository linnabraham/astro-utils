#!/bin/env python3
"""
Functions for visualizing SDO/AIA (Solar Dynamics Observatory/Atmospheric Imaging Assembly) data.

This module provides utilities for plotting and animating AIA images using the appropriate
SDO color maps for different wavelength passbands.
"""

import math
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


def plot_aia_image_grid(images, passbands, cols=4, gap=0, dpi=100, vmax_percentile=None, show=False):
    """
    Plot a grid of AIA images, each with its corresponding colormap based on passband.

    Parameters
    ----------
    images : np.ndarray
        Array of shape [n, H, W] where each [H, W] image corresponds to a passband
    passbands : list of int or str
        List of AIA wavelengths matching the order of `images`
    cols : int
        Number of columns in the image grid
    gap : int
        Pixel gap between images
    dpi : int
        Resolution of the output figure
    vmax_percentile : float or None
        If given, compute vmax for each image from this percentile
    show : bool
        If True, displays the figure; otherwise returns it

    Returns
    -------
    fig : matplotlib.figure.Figure or None
        The resulting figure if show=False; otherwise None
    """
    assert images.shape[0] == len(passbands), "Number of images and passbands must match"
    n, H, W = images.shape
    rows = math.ceil(n / cols)

    total_width_px = cols * W + (cols - 1) * gap
    total_height_px = rows * H + (rows - 1) * gap
    figsize = (total_width_px / dpi, total_height_px / dpi)

    fig = plt.figure(figsize=figsize, dpi=dpi)

    for idx, (image, passband) in enumerate(zip(images, passbands)):
        row = idx // cols
        col = idx % cols

        left = (col * (W + gap)) / total_width_px
        bottom = 1 - ((row + 1) * H + row * gap) / total_height_px
        width = W / total_width_px
        height = H / total_height_px

        ax = fig.add_axes([left, bottom, width, height])
        plot_aia_image(image, passband, ax=ax, show_colorbar=False, vmax_percentile=vmax_percentile)

    if show:
        plt.show()
    else:
        plt.close(fig)
        return fig

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
