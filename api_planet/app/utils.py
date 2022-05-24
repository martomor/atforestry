import os
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2
import matplotlib.pyplot as plt


PLANET_API_KEY = os.environ.get('PLANET_API_KEY')
PLANET_URL = "https://api.planet.com/basemaps/v1/mosaics"

class PlanetAPI():
    def __init__(self, api_key=PLANET_API_KEY, api_url=PLANET_URL):
        self.api_key = api_key
        self.api_url = api_url


# Processing Images
def preprocess_raster_image(raster):
    # Move channels from start of array (e.g. (C, H, W)) to the end (e.g. (H, W, C))
    image_original = np.einsum('ijk->jki', raster.image)[:, :, :3]

    # Stretch each channel to min/max for later converting the image to np.uint8
    image = image_original.astype(float)
    for idx_channel in range(image.shape[-1]):
        image_min = image[..., idx_channel].min()
        image_max = image[..., idx_channel].max()
        image[..., idx_channel] = (image[..., idx_channel] - image_min) * (255 / (image_max - image_min))

    image = cv2.convertScaleAbs(image)

    return image

def imshow(inp, fig_size=4, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)

    fig, ax = plt.subplots(figsize=(fig_size, fig_size))
    ax.imshow(inp)
    
def transform(image, mean, std):
    for channel in range(3):
        image[:,:,channel] = (image[:,:,channel] - mean[channel]) / std[channel]
    return image

def list_files_in_directory(path:str):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles







