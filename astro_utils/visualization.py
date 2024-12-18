import numpy as np
import matplotlib.pyplot as plt
from skimage.util import montage

def plot_montage(cube, channel_axis=1):
    # add an extra channel needed for sklearn montage function
    cube = cube[:, np.newaxis, :, :]
    im_montage = montage(cube, channel_axis=1)
    # Display the montage
    plt.figure(figsize=(10, 10))
    plt.imshow(im_montage)
    plt.axis('off')
    plt.title(f"Montage of Slices")

class solocube:
    def __init__(self, data:np.ndarray):
        self.data = data
        self.generator = None
        self.frame_num = None
    def montage(self):
        plot_montage(self.data)
    def frame_generator(self, data):
        for i, frame in enumerate(data):
            yield i,frame
    def frame_viewer(self, frame_num=None):
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
            plt.imshow(frame)
            return frame
