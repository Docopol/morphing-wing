import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

from utils.other import perftimer
from utils.filereader import files_in_directory


@perftimer
def imageVisualization(file, show_colorbar:bool = False) -> None:
    """
    visualization an image using plt.imshow()
    """
    plt.imshow(file)
    if show_colorbar:
        plt.colorbar()
    plt.show()


@perftimer
def loadRGBandBOOL(file: str, usepil: bool = False) -> list:
    if usepil:
        image_colordata = Image.open(file)
    else:
        image_colordata = plt.imread(file)
    file_bool = np.asarray(np.zeros((np.copy(image_colordata).shape[:2]), dtype=bool))
    return [np.asarray(image_colordata), file_bool]


def cropimage(array: np.ndarray) -> np.ndarray:
    pass


def creategridd():
    pass


images = files_in_directory("Images (BMP) - FOR IMAGE CALIBRATION ONLY", "bmp")
image = loadRGBandBOOL(images[-1])
print(np.unique(image[0], axis=0, return_counts=True))
imageVisualization(image[0])
imageVisualization(image[1])
# print(image[0][1000:1500, 1000:2000])
