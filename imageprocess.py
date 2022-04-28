import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import math

from PIL import Image

from utils.other import perftimer
from utils.filereader import files_in_directory
from utils.filereader import load_file


# global variables
cut_left = 0
cut_right = 0
cut_up = 0
cut_down = 0
subgrid_size = 25


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
    """
    :param file: The file path name from the repository root of the image
    :param usepil: True or False value depending on the wish to use the Pil libary or not
    :return: A list containing the image array were every cell contains the rgb code of the pixel,
    the second item is an initialized boolean array with the size of the color array.
    """

    # generate file with methode of choice
    if usepil:
        image_colordata = Image.open(file)
    else:
        image_colordata = plt.imread(file)

    # intialize empty boolean array with the size of the color array
    file_bool = np.asarray(np.zeros((np.copy(image_colordata).shape[:2]), dtype=bool))
    return [np.asarray(image_colordata), file_bool]


def addcamber(array: np.ndarray):

    points = np.argwhere(array == 1)
    x = []
    y = []
    for i in points:
        x.append(i[0])
        y.append(i[1])
    x = np.array(x)
    y = np.array(y)
    plt.plot(x,y,"k.")


# Outdated function used for debugging
def plotBoolpoints(array: np.ndarray, line: list = None) -> None:

    points_x, points_y = genboolxy(array)
    plt.scatter(points_x, points_y)
    if line:
        x = line[0]
        a = line[1]
        b = line[2]
        x_avg = line[3]
        y_avg = line[4]
        plt.plot(x, a*x + b)
        plt.plot(x_avg, y_avg, 'ro')
    plt.show()


def rotate(array: np.ndarray, amount: int = 1) -> np.ndarray:
    """
    :param array: A np.ndarray that is to be rotated
    :param amount: Amount of times the array should be flipped 90degrees (were + is CW)
    :return: Rotated array
    """
    return np.rot90(array, k=amount)


@perftimer
def cropimage(array_color: np.ndarray, array_bool: np.ndarray) -> tuple:
    """
    :param array_color: Color image array to be cropped
    :param array_bool: Boolean array to be cropped
    :return: cropped image(color and bool in a list) based on two anker point,
     found at the bottom left and top right part of the screen.
     The ankerpoints are based on locations were no critical data will be left
     after linear cropping.
    """

    # initialize global variables
    global cut_left
    global cut_right
    global cut_up
    global cut_down

    def ankerpoint2() -> tuple:
        """
        :return: Two anker points in a list/ tuple
        """
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

    print(size)
    print(ankers)

    # save the amount that is going to be cropped on all sides
    cut_left = ankers[1] - 1
    cut_right = size[1] - ankers[3]
    cut_up = ankers[2]
    cut_down = size[0] - ankers[0]

    print(f"{cut_left=}")
    print(f"{cut_right=}")
    print(f"{cut_up=}")
    print(f"{cut_down=}")

    # crop both the color and boolean array
    out_array_color = array_color[ankers[2]:ankers[0]-1, ankers[1]:ankers[3]+1]
    out_array_bool = array_bool[ankers[2]:ankers[0]-1, ankers[1]:ankers[3]+1]

    print(f"{np.shape(out_array_bool)=}")
    return out_array_color, out_array_bool


@perftimer
def creategrid(array_bool: np.ndarray, usedict:bool = False):
    """
    :param array_bool: Cropped or non-cropped boolean array, to be devided into subgrids
    which are later to be used for linear/ or other global contour approximation.
    :param usedict: For debugging perpose, dump the array data as a dictionary.
    :return: A 4 dimensional array containing subgrids(of requested size) on each of the mxn elements.
    """

    # initialize global variable
    global subgrid_size

    def pad_with(vector, pad_width, iaxis, kwargs):
        """
        :param vector: 2 dimension array to be padded
        :param pad_width: Direction to be padded by requested amount
        :param iaxis: /
        :param kwargs: padder = some value <- the value wich is used to pad the array (0, False in this use case)
        :return: A padded array in the requested direction
        """
        pad_value = kwargs.get('padder', 0)
        vector[:pad_width[0]] = pad_value
        if pad_width[1] != 0:
            vector[-pad_width[1]:] = pad_value

    # Find the amount an array should be padded to allow for grid creation based on the requested subgrid size
    size = np.shape(array_bool)

    size_corectionY = subgrid_size - size[0] % subgrid_size
    size_corectionX = subgrid_size - size[1] % subgrid_size

    # Pad the array in vertical and or horizontal direction to allow for grid creation
    if size_corectionY != subgrid_size:
        array_bool = np.pad(array_bool, ((size_corectionY, 0), (0, 0)), pad_with, padder=0)
    if size_corectionX != subgrid_size:
        array_bool = np.pad(array_bool, ((0, 0), (0, size_corectionX)), pad_with, padder=0)

    # Initialize dump and subgrid array
    size = np.shape(array_bool)
    subgrids_dict = {}
    subgrids = []

    # Create and store the subgrids
    for i in range(0, size[0], subgrid_size):
        empty_1 = []
        for j in range(0, size[1], subgrid_size):
            subgrid = array_bool[i:i+subgrid_size, j:j+subgrid_size]
            empty_1.append(subgrid)
            if usedict:
                subgrid_loc = f"{i // subgrid_size}x{j // subgrid_size}"
                subgrids_dict[subgrid_loc] = subgrid
        subgrids.append(empty_1)
    subgrids = np.array(subgrids)
    if usedict:
        return subgrids, subgrids_dict
    return subgrids


@perftimer
def regress(array: np.ndarray) -> np.ndarray:
    """
    :param array: 4 dimensional array containing subgrids,
    using the subgrids the contour of the airfoil can be approximated using a linear approximation.
    linear approximation used: Least squares
    :return: Pyplot containing the approximated airfoil contour
    """

    # initialize global variable
    global subgrid_size

    def genBoolXY(array: np.ndarray) -> list:
        """
        :param array: 2 dimensional boolean array (subgrid).
        :return: A list containing the location of the True values of the specified input array.
        The coordinates are defined from the top left, the x(vertical) and y(horizontal)
        are defined to plot the aifoil on its side.
        """

        points = np.argwhere(array == True)
        x = []
        y = []
        for i in points:
            x.append(i[0])
            y.append(i[1])
        x = np.array(x)
        y = np.array(y)
        return [x, y]

    def setupLS(array: np.ndarray, index: tuple = (0, 0)) -> list:
        """
        :param array: The boolean array(subgrid) of the airfoil LE contour on wich least squares should be performed.
        :param index: current index of subgrid to translate to the correct global location.
        :return: list with unique x values, slope and intercept found from least square,average x and y.
        A global plot of the approximated airfoil LE contour is also contructed in the meantime.
        """

        # initialize global variable
        global subgrid_size

        # get x and y coordinates of True points in array/subgrid
        x, y = genBoolXY(array)

        # Transform x and y to global position
        x += index[0]*subgrid_size
        y += index[1]*subgrid_size

        ##  plt.scatter(x, y) # plot contour points (DEBUG)

        # centroid of array/ subgrid of bool values where True has weight 1 and False 0
        x_avg = np.mean(x)
        y_avg = np.mean(y)

        # Least squares
        A = np.vstack([x, np.ones(len(x))]).T
        a, b = np.linalg.lstsq(A, y, rcond=None)[0]

        x = np.array(list(set(x)))

        plt.plot(x, a * x + b, "black")

        ## plt.plot(x_avg, y_avg, 'ro') # plot centroid points (DEBUG)

        return [x, a, b, x_avg, y_avg]

    size = np.shape(array)[0:2]

    # Initialize arrays containing subgrid values(Weight(amount of True over total items in array/subgrid),
    # slope, centroid) for the ful global contour
    weight = np.zeros(size)
    slope = np.zeros(size)
    centroidX = []
    centroidY = []

    # perform least squares for every subgrid in main global array
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            loc_array = array[i,j]
            if np.count_nonzero(loc_array == True):
                ## some debugging code (DEBUG)
                ## if ok == 5 or ok == 10:
                    # imageVisualization(loc_array)
                    # plotBoolpoints(rotate(loc_array, amount=-1), line=setupLS(rotate(loc_array, amount=-1), index=(i,j), subgrid_size= subgrid_size))
                    # setupLS(rotate(loc_array, amount=-1), index=(i,j), subgrid_size= subgrid_size)
                    # plt.show()
                # Least square
                res = setupLS(rotate(loc_array, amount=0), index=(i, j))

                # data of all the subgrids
                weight[i, j] = np.count_nonzero(loc_array) / subgrid_size
                slope[i, j] = res[1]
                centroidX.append(res[3])
                centroidY.append(res[4])

    centroid = np.vstack((centroidX, centroidY))
    plt.show()
    return centroid


class DeflectionProfiles:

    def __init__(self, camberline, centroid):
        self.camberline = camberline
        self.centroid = centroid
        self.cX = centroid[0,:]
        self.cY = centroid[1,:]
        self.tipX = np.min(self.cX)
        self.tipY = float(self.cY[np.where(self.cX == self.tipX)])
        self.rootY1 = np.min(self.cY)
        self.rootY2 = np.max(self.cY)
        self.rootX1 = float(self.cX[np.where(self.cY == self.rootY1)])
        self.rootX2 = float(self.cX[np.where(self.cY == self.rootY2)])
        self.rootmidpointX = np.abs(self.rootX2 + self.rootX1)/2
        self.rootmidpointY = np.abs(self.rootY2 + self.rootY1)/2
        self.dangle1 = 0
        self.dangle1 = 1
        self.dangle1 = 2
        self.model1()
        self.model2()
        self.model3()

    def model1(self):
        """
        :return: Deflection angle using rootmidpoint and tip point
        """
        self.dangle1 = math.atan2(abs(self.rootmidpointY-self.tipY), abs(self.rootmidpointX-self.tipX))*180/math.pi

    def model2(self):
        pass

    def model3(self):
        pass

    def printsummary(self):
        print("---------- Deflection angles - summary ----------")
        print(f"model1: {self.dangle1}")


# Test array
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

# -----------------
# Main calling code
# -----------------

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
img_bool_file1 = load_file(img_bool_loc[0], separator=",", skip_last=True)
img_bool_file2 = load_file(img_bool_loc[1], separator=",", skip_last=True)

# imageVisualization(img_bool_file)
img_bool_cropped_camber, img_bool_cropped = cropimage(np.array(np.asarray(img_bool_file2), dtype=bool), np.array(np.asarray(img_bool_file1), dtype=bool))
imageVisualization(img_bool_cropped)
imageVisualization(img_bool_cropped_camber)

print(addcamber(img_bool_cropped_camber))
#plotBool(rotate(img_bool_cropped,3))
img_grid = creategrid(img_bool_cropped)
centroid_ = regress(img_grid)

df1 = DeflectionProfiles(None, centroid_)
print(df1.__dict__)


# img_bool_file2 = load_file(img_bool_loc[0], separator=",", skip_last=True)
# img_bool_cropped2 = cropimage(np.array(np.asarray(img_bool_file2), dtype=bool), np.array(np.asarray(img_bool_file2), dtype=bool))[1]
#
# imageVisualization(img_bool_cropped2)

# imageVisualization(img_bool_cropped)
# points = np.argwhere(img_bool_cropped == True)
#
# print(*zip(*points))
# plt.scatter(*zip(*points))
# plt.show()


# sometesting = load_file(img_bool_loc[3], separator=",", skip_last= False)
# sometesting = np.asarray(sometesting)
# for level in range(np.shape(sometesting)[0]):
#     plt.scatter(sometesting[:,2], sometesting[:,1])
# plt.show()