import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

from utils.other import perftimer
from utils.filereader import files_in_directory


@perftimer
def imageVisualization(file, show_colorbar:bool = False, name:str = "") -> None:
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


@perftimer
def cropimage(array_color: np.ndarray, array_bool: np.ndarray) -> list:
    """
    cropped the image based on an anker point found at the bottom left part of the screen
    """
    size = np.shape(array_bool)

    def ankerpoint():
        for y in range(size[0] - 1, 3*(size[0]//5), -1):
            for x in range(0, size[1]//2):
                if array_bool[y,x]:
                    print(f"Found first True at ({y}x{x})")
                    return y, x

    def ankerpoint2():
        for y in range(size[0] - 1, 3*(size[0]//5), -1):
            if np.any(array_bool[y: 250:size[1]//2]):
                break
        for x in range(0, size[1]//2):
            if np.any(array_bool[3*(size[0]//5):size[0],x]):
                break
        return y, x

    ankers = ankerpoint()
    out_array_color = array_color[0:ankers[0] + 1, ankers[1]:size[1]]
    out_array_bool = array_bool[0:ankers[0] + 1, ankers[1]:size[1]]
    return [out_array_color, out_array_bool]


def creategrid(array_color: np.ndarray, array_bool: np.ndarray, subgrid_size: int = 12):

    def pad_with(vector, pad_width, iaxis, kwargs):
        pad_value = kwargs.get('padder', 0)
        vector[:pad_width[0]] = pad_value
        if pad_width[1] != 0:  # <-- the only change (0 indicates no padding)
            vector[-pad_width[1]:] = pad_value

    size = np.shape(array_bool)

    size_corectionY = subgrid_size - size[0] % subgrid_size
    size_corectionX = subgrid_size - size[1] % subgrid_size


    if size_corectionY != 0:
        array_bool = np.pad(array_bool, ((size_corectionY, 0), (0, 0)), pad_with, padder=0)
    if size_corectionX != 0:
        array_bool = np.pad(array_bool, ((0, 0), (0, size_corectionX)), pad_with, padder=0)

    size = np.shape(array_bool)

    for i in range(0, size[1], subgrid_size):
        for j in range(0, size[1], subgrid_size):
            pass

    print(array_bool)


a = np.array([[False, False, False, False, False, False, False, False, False, False, False, False],
     [False, False, False, False, False, False, False, False, False, False, False, True],
     [False, False, False, False, False, False, False, False, False, False, False, False],
     [False, False, False, False, False, False, False, False, False, False, False, False],
     [False, False, False, False, False, False, False, True, False, False, False, False],
     [False, False, False, False, False, False, False, False, False, False, False, False],
     [False, False, False, False, False, False, False, False, False, False, False, False],
     [False, False, False, False, False, False, False, False, False, False, False, False],
     [False, False, False, True, False, False, False, False, False, False, False, False],
     [False, False, True, False, False, False, False, False, False, False, False, False],
     [False, False, False, True, False, False, False, False, False, False, False, False],
     [False, False, False, True, False, False, False, False, True, False, False, False],
     [False, False, False, False, False, False, True, False, False, False, False, False],
     [False, False, False, False, False, False, False, True, False, False, False, False],
     [False, False, False, False, False, False, False, False, False, False, False, False]
     ])
imageVisualization(a)
imageVisualization(cropimage(a, a)[1])
creategrid(np.array([[1,2],[2,3]]), np.array([[1,2],[2,3]]))


images = files_in_directory("Images (BMP) - FOR IMAGE CALIBRATION ONLY", "bmp")
image = loadRGBandBOOL(images[-1])

imageVisualization(image[0])
imageVisualization(image[1])
