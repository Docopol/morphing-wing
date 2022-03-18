import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy

from PIL import Image

from utils.other import perftimer
from utils.filereader import files_in_directory
from utils.filereader import load_file


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

    def ankerpoint():
        for y in range(size[0] - 1, 3*(size[0]//5), -1):
            for x in range(0, size[1]//2):
                if array_bool[y,x]:
                    return y, x

    def ankerpoint2():
        for y in range(size[0] - 1, 3*(size[0]//5), -1):
            if np.any(array_bool[y, 250:size[1]//2]):
                break
        for x in range(0, size[1]//2):
            if np.any(array_bool[3*(size[0]//5):size[0],x]):
                break
        for y2 in range(0, 2*(size[0]//5)):
            if np.any(array_bool[y2,:]):
                break
        for x2 in range(size[1] - 1, 2*(size[1]//5), -1):
            if np.any(array_bool[2*(size[0]//5):size[0],x2]):
                break
        return y, x, y2, x2

    size = np.shape(array_bool)
    ankers = ankerpoint2()
    out_array_color = array_color[ankers[2]-1:ankers[0]-1 , ankers[1]:ankers[3]+1]
    out_array_bool = array_bool[ankers[2]-1:ankers[0]-1, ankers[1]:ankers[3]+1]
    return [out_array_color, out_array_bool]

@perftimer
def creategrid(array_color: np.ndarray, array_bool: np.ndarray, subgrid_size: int = 12, usedict:bool = False):

    def pad_with(vector, pad_width, iaxis, kwargs):
        pad_value = kwargs.get('padder', 0)
        vector[:pad_width[0]] = pad_value
        if pad_width[1] != 0:
            vector[-pad_width[1]:] = pad_value

    size = np.shape(array_bool)

    size_corectionY = subgrid_size - size[0] % subgrid_size
    size_corectionX = subgrid_size - size[1] % subgrid_size

    if size_corectionY != subgrid_size:
        array_bool = np.pad(array_bool, ((size_corectionY, 0), (0, 0)), pad_with, padder=0)
    if size_corectionX != subgrid_size:
        array_bool = np.pad(array_bool, ((0, 0), (0, size_corectionX)), pad_with, padder=0)

    size = np.shape(array_bool)
    subgrids_dict = {}
    subgrids = []

    for i in range(0, size[0], subgrid_size):
        empty_1 = []
        for j in range(0, size[1], subgrid_size):
            subgrid = array_bool[i:i+subgrid_size, j:j+subgrid_size]
            empty_1.append(subgrid)
            if usedict:
                subgrid_loc = f"{i // subgrid_size}x{j // subgrid_size}"
                subgrids_dict[subgrid_loc] = subgrid
        subgrids.append(empty_1)
    if usedict:
        return subgrids, subgrids_dict
    return subgrids


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
# imageVisualization(a)
# imageVisualization(cropimage(a, a)[1])
# creategrid(np.array([[1,2],[2,3]]), np.array([[1,2],[2,3]]))
# creategrid(a,a, subgrid_size=4)
#
#
# images = files_in_directory("Images (BMP) - FOR IMAGE CALIBRATION ONLY", "bmp")
# image = loadRGBandBOOL(images[-1])
#
# imageVisualization(image[0])
# imageVisualization(image[1])

img_bool_loc = files_in_directory("csv_bool", "csv")
img_bool_file = load_file(img_bool_loc[1], separator=",", skip_last=True)
imageVisualization(img_bool_file)
img_bool_cropped = cropimage(np.array(np.asarray(img_bool_file), dtype=bool), np.array(np.asarray(img_bool_file), dtype=bool))[1]
imageVisualization(img_bool_cropped)
points = np.argwhere(img_bool_cropped == True)
plt.scatter(*zip(*points))
plt.show()