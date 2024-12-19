#!/bin/env python3
import sunpy.visualization.colormaps as cm
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def plot_aia_image(data, passband, **kwargs):
    aia_cmap = matplotlib.colormaps[f'sdoaia{passband}']
    plt.figure()
    plot_params = {}
    if 'vmax' in kwargs:
        plot_params['vmax'] = kwargs['vmax']
    elif 'vmax_percentile' in kwargs:
        # TODO: validate the vmax_percentile value input
        plot_params['vmax'] = np.percentile(data, kwargs['vmax_percentile'])
    else:
        # this has no effect other than showing a preferred default value
        vmax_percentile = np.percentile(data, 99)
    plt.imshow(data, cmap=aia_cmap, origin='lower', **plot_params)
    plt.colorbar()
    plt.axis("off")

def make_aia_movie(filename, data:np.ndarray, wavelength, timestamps:list = None, vmin=None, vmax=None, aarp_id=None, label=None):

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
