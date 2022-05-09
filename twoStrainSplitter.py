
from tabnanny import check
from numpy import empty
import numpy as np
from pandas import array

'''
Checks the endpoints of the interval on which the strains (inside/outside) can be compared.
    Inputs: 
     - in_contour, out_contour: Arrays with the arcsec length values of the strain measurements.
    Outputs: 
     - interval_min: minimum value of arcsec lenght of interval
     - interval_max: maximum idem.
     - i_range[a][b]: list of cell indexes for a (0: inside, 1: outside loops) and b (0: start, 1: end of interval)
'''

def check_interval(in_contour, out_contour):
    extremes_out = [min(out_contour), max(out_contour)]
    extremes_in = [min(in_contour), max(in_contour)]
    i_range = empty([2,2],dtype='int')

    if extremes_out[0] < extremes_in[0]:
        i_range[0][0] = 0
        i_range[1][0] = np.argmin([abs(x-extremes_in[0]) for x in out_contour])

    elif extremes_out[0] > extremes_in[0]:
        i_range[1][0] = 0
        i_range[0][0] = np.argmin([abs(x-extremes_out[0]) for x in in_contour])

    if extremes_out[1] < extremes_in [1]:
        i_range[1][1] = -1
        i_range[0][1] = np.argmin([abs(x-extremes_out[1]) for x in in_contour])

    elif extremes_out[1] > extremes_in [1]:
        i_range[0][1] = -1
        i_range[1][1] = np.argmin([abs(x-extremes_in[1]) for x in out_contour])
    
    return i_range


'''
Finds the closest value, in the input array, to the given value. Returns the index in the input array of the corresponding closest value.
    Inputs:
        - value: value we want to find closest to.
        - val_array: Array of values to sort through.
    Outputs:
        - val_index: Index of the given array which corresponds to the closest value.
'''

def check_closest(value, val_array):
    
    val_index = np.argmin([abs(x - value) for x in val_array])

    return val_index



