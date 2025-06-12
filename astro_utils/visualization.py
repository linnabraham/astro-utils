
"""
This script provides utilities for visualizing and interacting with 3D data arrays, 
such as image stacks or volumetric data. It includes functions and a class for 
creating montages of slices, viewing individual frames, and iterating through 
frames of the data.

Modules:
    - numpy: Used for numerical operations on arrays.
    - matplotlib.pyplot: Used for plotting and visualizing data.
    - skimage.util.montage: Used for creating montages of 3D data slices.

Functions:
    - plot_montage: Generates and displays a montage of slices from a 3D data cube.

Classes:
    - solocube: A class for visualizing and interacting with 3D data arrays. It 
      provides methods for creating montages, iterating through frames, and 
      displaying individual frames with customizable plotting options.

Usage:
    This script is designed to be imported as a module. Users can utilize the 
    `plot_montage` function for quick visualization of 3D data or create an 
    instance of the `solocube` class for more interactive exploration of the data.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from skimage.util import montage

def plot_image_grid(images, cols=5, cmap='viridis', gap=0, dpi=100, show=False):
    """
    Plots a compact grid of images using fig.add_axes, returning the figure.

    Parameters:
    - images: np.ndarray of shape [n, H, W]
    - cols: Number of columns
    - cmap: Colormap
    - gap: Space (in pixels) between images
    - dpi: Dots per inch for sizing

    Returns:
    - fig: Matplotlib Figure object (not shown by default)
    """
    n, H, W = images.shape
    rows = math.ceil(n / cols)

    # Compute figure size in inches
    total_width_px = cols * W + (cols - 1) * gap
    total_height_px = rows * H + (rows - 1) * gap
    figsize = (total_width_px / dpi, total_height_px / dpi)

    fig = plt.figure(figsize=figsize, dpi=dpi)

    for idx in range(n):
        row = idx // cols
        col = idx % cols

        # Position in figure coordinates [0,1]
        left = (col * (W + gap)) / total_width_px
        bottom = 1 - ((row + 1) * H + row * gap) / total_height_px
        width = W / total_width_px
        height = H / total_height_px

        ax = fig.add_axes([left, bottom, width, height])
        ax.imshow(images[idx], cmap=cmap)
        ax.axis('off')
    if show:
        plt.show()
    else:
        plt.close(fig)
        return fig

def plot_montage(cube, channel_axis=1):
    """
    Generates and displays a montage of slices from a 3D data cube.

    This function takes a 3D data cube, adds an extra channel dimension 
    required by the montage function, and creates a montage of the slices 
    along the specified channel axis. The montage is then displayed using 
    Matplotlib.

    Parameters:
        cube (numpy.ndarray): A 3D array representing the data cube to be visualized.
        channel_axis (int, optional): The axis along which the slices are arranged 
            for the montage. Default is 1.

    Returns:
        None: The function displays the montage but does not return any value.
    """
    # add an extra channel needed for sklearn montage function
    cube = cube[:, np.newaxis, :, :]
    im_montage = montage(cube, channel_axis=1)
    # Display the montage
    plt.figure(figsize=(10, 10))
    plt.imshow(im_montage)
    plt.axis('off')
    plt.title(f"Montage of Slices")

class solocube:
    """
    A class for visualizing and interacting with 3D data arrays (e.g., image stacks or volumetric data).

    Attributes:
        data (np.ndarray): The 3D data array to be visualized.
        colormap (str): The colormap used for visualization. Default is 'virdis'.
        generator (generator): A generator object for iterating through frames of the data.
        frame_num (int): The starting frame number for the generator.

    Methods:
        __init__(data: np.ndarray, colormap='virdis'):
            Initializes the solocube object with the given data and colormap.

        montage():
            Displays a montage of the 3D data using the `plot_montage` function.

        frame_generator(data):
            A generator function that yields frames from the 3D data along with their indices.

        frame_viewer(frame_num=None, plot_func=None, **kwargs):
            Displays a single frame of the data. If a frame number is provided, it starts from that frame.
            Optionally, a custom plotting function can be used.

        plot_frame(frame):
            Plots a single frame using matplotlib with the specified colormap.
    """
    def __init__(self, data:np.ndarray, colormap='virdis'):
        self.data = data
        self.colormap = colormap
        self.generator = None
        self.frame_num = None
    def montage(self):
        plot_montage(self.data)
    def frame_generator(self, data):
        for i, frame in enumerate(data):
            yield i,frame
    def frame_viewer(self, frame_num=None, plot_func=None, **kwargs):
        if not frame_num is None:
            if self.frame_num is None:
                self.generator = self.frame_generator(self.data[frame_num:])
                self.frame_num = frame_num
        if self.generator is None:
            self.generator = self.frame_generator(self.data)
        try:
            i, frame = next(self.generator)
        except StopIteration:
            print("Generator is exhausted")
        else:
            print(f"Internal frame:{i}")
            print(f"{self.frame_num=}")
            if plot_func:
                plot_func(frame, **kwargs)
            else:
                self.plot_frame(frame)
            return frame
    def plot_frame(self, frame):
        plt.imshow(frame, cmap="virdis")
        plt.colorbar()
        plt.show()
