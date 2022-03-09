import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

from main import perftimer
from main import files_in_directory


@perftimer
def imageVisualization(file, show_colorbar:bool = False, grayscale: bool = False) -> None:
    """
    visualization an image using plt.imshow()
    """
    if grayscale:
        plt.imshow(file, cmap="gray", vmin=0, vmax=255)
    else:
        plt.imshow(file)
    if show_colorbar:
        plt.colorbar()
    plt.show()


@perftimer
def loadRGBandBOOL(file: str, grayscale: bool = False, usepil: bool = False) -> list:
    if grayscale:
        image_colordata = Image.open(file).convert("L")
    elif usepil:
        image_colordata = Image.open(file)
    else:
        image_colordata = plt.imread(file)
    file_bool = np.asarray(np.zeros((np.copy(image_colordata).shape[:2]), dtype=bool))
    return [np.asarray(image_colordata), file_bool]


images = files_in_directory("Images (BMP) - FOR IMAGE CALIBRATION ONLY", "bmp")
image = loadRGBandBOOL(images[-1])

imageVisualization(image[0])
imageVisualization(image[1])
print(np.asarray(image[0]))
# print(image[0][1000:1500, 1000:2000])
