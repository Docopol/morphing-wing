
from tabnanny import check
from numpy import empty
import numpy as np

'''
Checks the endpoints of the interval on which the strains (inside/outside) can be compared.
    Inputs: 
     - strain_in, strain_out: Arrays with the arcsec length values of the strain measurements.
    Outputs: 
     - interval_min: minimum value of arcsec lenght of interval
     - interval_max: maximum idem.
     - i_range[a][b]: list of cell indexes for a (0: inside, 1: outside loops) and b (0: start, 1: end of interval)
'''

def check_interval(strain_in, strain_out):
    extremes_out = [min(strain_out), max(strain_out)]
    extremes_in = [min(strain_in), max(strain_in)]
    i_range = empty([2,2],dtype='int')

    if extremes_out[0] < extremes_in[0]:
        i_check = 100
        interval_min = extremes_in[0]
        i_range[0][0]=0
        for i in range(np.size(strain_out)):
            if abs(strain_out[i] - strain_in[0]) > i_check:
                i_range[1][0] = i
                break
            else: 
                i_check = abs(strain_out[i] - strain_in[0])
    elif extremes_out[0] > extremes_in[0]:
        i_check = 100
        interval_min = extremes_out[0]
        i_range[1][0]=0
        for i in range(np.size(strain_in)):
            if abs(strain_in[i] - strain_out[0]) > i_check:
                i_range[0][0] = i
                break
            else: 
                i_check = abs(strain_in[i] - strain_out[0])
    elif extremes_out[0] == extremes_in[0]:
        i_range[0][0],i_range[1][0]=0,0
        interval_min = extremes_in[0]
    
    ### For the high end extremes.

    if extremes_out[1] < extremes_in[1]:
        i_check = 100
        interval_max = extremes_out[1]
        i_range[1][1]=-1
        for i in range(np.size(strain_in)-1,0,-1):
            if abs(strain_in[i] - strain_out[-1]) > i_check:
                i_range[0][1] = i
                break
            else: 
                i_check = abs(strain_in[i] - strain_out[-1])
    elif extremes_out[1] > extremes_in[1]:          
        i_check = 100
        interval_max = extremes_in[1]
        i_range[0][1]=-1
        for i in range(np.size(strain_out)-1,0,-1):
            if abs(strain_out[i] - strain_in[-1]) > i_check:
                i_range[1][1] = i
                break
            else: 
                i_check = abs(strain_out[i] - strain_in[-1])
    elif extremes_out[1] == extremes_in[1]:
        i_range[0][1],i_range[1][1]=-1,-1
        interval_min = extremes_in[1]

    return interval_min, interval_max, i_range

'''
Finds the closest value, in the input array, to the given value. Returns the index in the input array of the corresponding closest value.
    Inputs:
        - value: value we want to find closest to.
        - val_array: Array of values to sort through.
    Outputs:
        - val_index: Index of the given array which corresponds to the closest value.
'''

def check_closest(value, val_array):
    smallest_diff, diff = abs(value - val_array[0]) , abs(value - val_array[0]) 
    size_arr = np.size(val_array)
    val_index = -1   # If it doesn't find a value in the whole array it just assumes the last one is the closest.

    for i in range(size_arr):
        diff = abs(value - val_array[i])
        #print(diff)

        if diff < smallest_diff:
            smallest_diff = diff
            val_index = int(i-1)
                           
    return val_index



