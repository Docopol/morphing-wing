
from cgitb import small
from turtle import shape
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from twoStrainSplitter import check_interval, check_closest

'''
Takes the unprocessed panda dataframe of experimental data.
Turns into a numpy array. Assumes it has 
Divides it into the four main sections as numpy arrays.
'''

def load_file(file: str, skip_rows: int = None):
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows, header=None)
    return data_file




'''
WARNING: 
For the data calibration, the fiber length does not exactly match the path distance of the airfoil.
This means the data had to be squeezed in order to fit with the actual surface of the airfoil.
'''


'''
SectionX:

Takes a timestamp (Starting from 1, 0 is the lengths), the list of fiber lists and array of experimental strains.
returns the corresponding section lengths and strains, both as measured on the fiber cable.

Note that all the segments have different sizes, must first be fitted before matching together.

WARNING: Here the lengths are still uncalibrated, they need to be stretched/squeezed in order to fit the actual contour of the airfoil.
WARNING: The strain data for Sections C and D are given backwards, as in, they start at the "end" of the contour and begin 
'''# I know its redundant but get off my back.

#print(fiberLengths)
def sectionC(timeStamp ,fiberLengths, strainMeasures):
    for i in range(len(fiberLengths)):
        if abs(fiberLengths[i] - 0.190102)<10**(-3):
            firstTerm = i
        if fiberLengths[i] == 1.25324:
            lastTerm = i+1 
            break
    sectionCStrains = [float(a) for a in strainMeasures[timeStamp, firstTerm:lastTerm]]
    sectionCLengths = [float(a) for a in fiberLengths[firstTerm:lastTerm]]
    sectionCLengths[0] = 0.190102
    return sectionCStrains, sectionCLengths

def sectionA(timeStamp ,fiberLengths, strainMeasures):
    for i in range(len(fiberLengths)):
        if fiberLengths[i] == 1.58908:
            firstTerm = i
        if fiberLengths[i] == 2.59791:
            lastTerm = i+1 
            break
    sectionAStrains = [float(a) for a in strainMeasures[timeStamp, firstTerm:lastTerm]]
    sectionALengths = [float(a) for a in fiberLengths[firstTerm:lastTerm]]
    return sectionAStrains, sectionALengths

def sectionB(timeStamp ,fiberLengths, strainMeasures):
    for i in range(len(fiberLengths)):
        if fiberLengths[i] == 2.75864:
            firstTerm = i
        if fiberLengths[i] == 3.77008:
            lastTerm = i+1
            break
    sectionAStrains = [float(a) for a in strainMeasures[timeStamp, firstTerm:lastTerm]]
    sectionALengths = [float(a) for a in fiberLengths[firstTerm:lastTerm]]
    return sectionAStrains, sectionALengths

def sectionD(timeStamp ,fiberLengths, strainMeasures):
    for i in range(len(fiberLengths)):
        if fiberLengths[i] == 4.07065:
            firstTerm = i
        if fiberLengths[i] == 5.17115:
            lastTerm = i+1 
            break
    sectionAStrains = [float(a) for a in strainMeasures[timeStamp, firstTerm:lastTerm]]
    sectionALengths = [float(a) for a in fiberLengths[firstTerm:lastTerm]]
    return sectionAStrains, sectionALengths


'''
fitSection.
Takes the sections lengths, and their appropriate callibration start and end points.
Returns a set of intervals of the same size as the section lengths which has been squeezed to fit the actual contour.
'''

def fitSection(sectionLengths, callibrationStart, callibrationEnd):
    totalLength = callibrationEnd - callibrationStart
    gapNumber = len(sectionLengths) - 1
    gapLength = totalLength/gapNumber

    fittedLength = np.empty([gapNumber+1])
    fittedLength[0]=callibrationStart

    for i in range(gapNumber):
        fittedLength[i+1]=fittedLength[i]+gapLength

    return fittedLength


def noiseRemove(timeZeroStrains, strainMeasures):

    noNoiseStrains = np.empty([len(timeZeroStrains)])

    for i in range(len(timeZeroStrains)):
        noNoiseStrains[i] = float(strainMeasures[i]) - timeZeroStrains[i]

    return noNoiseStrains


'''I hate what happens here but its needed.

This function happens since the callibration points given make the gaps not have the same spacing.

'''


def calibrateSection(secLengths, secCalibFibers, secCalibActual):
    a = 0
    secLengthsActuals = np.empty([1])

    while a < len(secCalibActual)-1:
        #print(secCalibActual[a])
        for i in range(len(secLengths)):
            #print(secCalibFibers[a], ' = ', secLengths[i])
            if secCalibFibers[a] == secLengths[i]:
                firstPt = i
                continue
            if secCalibFibers[a+1] == secLengths[i]:
                lastPt = i 
                continue
        actualLengths = fitSection(secLengths[firstPt:lastPt],secCalibActual[a],secCalibActual[a+1])
        np.delete(secLengthsActuals, -1)
        secLengthsActuals = np.append(secLengthsActuals, actualLengths)
        a=a+1
    return secLengthsActuals


# The number entered on each section function is the timestamp, starting from 1.


'''
Returns a list of numpy arrays, each of which is a different timestamp of the fiber optic strain readings.

Each list element is a different timestamp. (First coordinate)
Each array is made up of two arrays, the lengths and strains. (Second Coordinate)
Each strain or length arrays is made up of the four sections that the fiber can be divided into. (Third Coordinate)

As an example, if you want to call the lengths of section C, at timestamp 24:

experimentalDatas[23][0][2]

'''

def expData(timestamp):

    experimental_strain_rows = pd.DataFrame(load_file("Data/Experimental Strains/Measurements2014_05_22.csv")).to_numpy()
    rows = experimental_strain_rows.shape [0]
    experimental_strain = np.array(np.zeros((rows,4263)),dtype=str)

    for i in range(rows):
        line = np.zeros((1,4263))
        #print(line.shape)
        line = np.array(experimental_strain_rows[i,0].split(sep=','))    
        #print(line)
        #print(line.shape)
        experimental_strain[i] = line


    fiberLengths = [float(i) for i in experimental_strain[0,1:]] # This should not be changed

    zeroAStrains = sectionA(1, fiberLengths, experimental_strain)[0] # Gets time zero values for noise removal.
    AStrains, ALengths = sectionA(timestamp, fiberLengths, experimental_strain)

    zeroCStrains, trash = sectionC(1, fiberLengths, experimental_strain)
    CStrains, CLengths = sectionC(timestamp, fiberLengths, experimental_strain)

    zeroBStrains, trash = sectionB(1, fiberLengths, experimental_strain)
    BStrains, BLengths = sectionB(timestamp, fiberLengths, experimental_strain)

    zeroDStrains, trash = sectionD(1, fiberLengths, experimental_strain)
    DStrains, DLengths = sectionD(timestamp, fiberLengths, experimental_strain)
    '''
    AStrains = noiseRemove(zeroAStrains, AStrains)
    BStrains = noiseRemove(zeroBStrains, BStrains)
    CStrains = noiseRemove(zeroCStrains, CStrains)
    DStrains = noiseRemove(zeroDStrains, DStrains)
    '''
    # C and D Strain will need to be inverted in order to be comparable in bending analysis.
    AStrains = np.flip(AStrains)
    #CStrains = [-x for x in CStrains]

    BStrains = np.flip(BStrains)
    #DStrains = [-x for x in DStrains]

    ACalibrationActuals = [1.05, 0.55, 0.05]
    ACalibrationFibers = [1.58908, 2.09349, 2.59791]

    BCalibrationActuals = [0.05, 0.55, 1.05]
    BCalibrationFibers = [2.75864, 3.26436, 3.77008]

    CCalibrationActuals = [0.07, 0.296, 0.378, 0.54, 0.645, 0.70, 0.759, 1.027] 
    CCalibrationFibers = [0.190102 ,0.414263, 0.510969, 0.673016, 0.793244, 0.848131, 0.984042, 1.25324]

    DCalibrationActuals = [1.024, 0.764, 0.711, 0.650, 0.540, 0.388, 0.297, 0.076]
    DCalibrationFibers = [4.07065, 4.33205, 4.50327, 4.55425, 4.68756, 4.83656, 4.95288, 5.17115]


    CLengthsActual = calibrateSection(CLengths, CCalibrationFibers, CCalibrationActuals)
    ALengthsActual = calibrateSection(ALengths, ACalibrationFibers, ACalibrationActuals)
    ALengthsActual = np.flip(ALengthsActual)

    ALengthsActual = np.delete(ALengthsActual,-1)
    AStrains = np.delete(AStrains,-1)

    CLengths = [float(x) for x in CLengthsActual]
    ALengths = [float(x) for x in ALengthsActual]

    BLengthsActual = calibrateSection(BLengths, BCalibrationFibers, BCalibrationActuals)
    DLengthsActual = calibrateSection(DLengths, DCalibrationFibers, DCalibrationActuals)
    BLengthsActual = np.flip(BLengthsActual)


    DLengthsActual = np.delete(DLengthsActual, 0)
    DStrains = np.delete(DStrains, 0)

    BLengths = [float(x) for x in BLengthsActual]
    DLengths = [float(x) for x in DLengthsActual]

    expStrains = [[ALengths, BLengths, CLengths, DLengths],[AStrains, BStrains, CStrains, DStrains]]
    return expStrains

experimentalDatas = []

for i in range(1,80):
    experimentalDatas.append(expData(i))

'''print(np.size(experimentalDatas[1][0][1]))
print(np.size(experimentalDatas[1][0][3]))

plt.plot(experimentalDatas[1][0][1],experimentalDatas[1][1][1])
plt.plot(experimentalDatas[1][0][3],experimentalDatas[1][1][3])
plt.show()'''

tested_step  = 12


'''
Checks the endpoints of the interval on which the strains (inside/outside) can be compared.
    Inputs: strain_in, strain_out
    Outputs: 
     - interval_min: minimum value of arcsec lenght of interval
     - interval_max: maximum idem.
     - i_range[a][b]: list of cell numbers for a (0: inside(DC), 1: outside(AB) loops) and b (0: start, 1: end of interval)
'''

AC_min_extreme, AC_max_extreme, AC_indexes = check_interval(experimentalDatas[tested_step][0][2][1:], experimentalDatas[tested_step][0][0])

BD_lens_flipped = np.empty([2], dtype='object')

BD_lens_flipped[0] = np.flip(experimentalDatas[tested_step][0][3][1:])
BD_lens_flipped[1] = np.flip(experimentalDatas[tested_step][0][1][1:])

BD_min_extreme, BD_max_extreme, BD_indexes = check_interval(BD_lens_flipped[0], BD_lens_flipped[1])

AC_indexes[0,0] = AC_indexes[0,0] + 1 # For some reason there's a zero in the first term which fucks things up, this fixes that.
BD_indexes[0,0] = BD_indexes[0,0] + 1

'''
print(AC_min_extreme, ' to ', AC_max_extreme)
print(AC_indexes)
print(experimentalDatas[tested_step][0][2][AC_indexes[0,0]], experimentalDatas[tested_step][0][2][AC_indexes[0,1]])
print(experimentalDatas[tested_step][0][0][AC_indexes[1,0]], experimentalDatas[tested_step][0][0][AC_indexes[1,1]])

print()

print(BD_min_extreme, ' to ', BD_max_extreme)
print(BD_indexes)
print(BD_lens_flipped[0][BD_indexes[0,0]], BD_lens_flipped[0][BD_indexes[0,1]])
print(BD_lens_flipped[1][BD_indexes[1,0]], BD_lens_flipped[1][BD_indexes[1,1]])
'''

timeStamps = [0, 12, 27, 39, 54]

def axial_str(inside_str, outside_str):
    return (outside_str + inside_str)/2

def bend_str(inside_str, outside_str):
    return (outside_str - inside_str)/2


# Timestamps here picked randomly since the lengths of the section wont change.
AC_formula_lengths = experimentalDatas[0][0][2][AC_indexes[0,0]:AC_indexes[0,1]]
BD_formula_lengths = np.flip(experimentalDatas[0][0][1])[BD_indexes[0,0]:BD_indexes[0,1]]

print(BD_indexes)

j = 0
# Array of arrays. Index correspond to the five relevant timestamps. (0, 12, 27, 39, 54)
ax_str_AC = np.empty([5], dtype='object') 
bd_str_AC = np.empty([5], dtype='object')
ax_str_BD = np.empty([5], dtype='object') 
bd_str_BD = np.empty([5], dtype='object')

for time in timeStamps:     #Calculates the axial and bending strains with the closest matching perimeter positions.
    A_lens = experimentalDatas[0][0][0][AC_indexes[1,0]:AC_indexes[1,1]]
    placeholder_axial = []
    placeholder_bend = []
    for i in range(AC_indexes[0,0], np.size(experimentalDatas[time][0][2][AC_indexes[0,0]:AC_indexes[0,1]])+1):    
        A_index = check_closest(experimentalDatas[time][0][2][i], A_lens)
        out_str = experimentalDatas[time][1][0][A_index]
        in_str = experimentalDatas[time][1][2][i]

        placeholder_axial = np.append(placeholder_axial, axial_str(in_str, out_str))
        placeholder_bend = np.append(placeholder_bend, bend_str(in_str, out_str)) 
    ax_str_AC[j] = placeholder_axial
    bd_str_AC[j] = placeholder_bend

    B_lens = np.flip(experimentalDatas[0][0][1])[BD_indexes[1,0]:BD_indexes[1,1]]
    placeholder_axial = []
    placeholder_bend = []
    for i in range(BD_indexes[0,0], np.size(experimentalDatas[time][0][1][BD_indexes[0,0]:BD_indexes[0,1]])+1):    
        B_index = check_closest(experimentalDatas[time][0][3][i], B_lens)
        out_str = np.flip(experimentalDatas[time][1][1])[B_index]
        in_str = np.flip(experimentalDatas[time][1][3])[i]

        placeholder_axial = np.append(placeholder_axial, axial_str(in_str, out_str))
        placeholder_bend = np.append(placeholder_bend, bend_str(in_str, out_str)) 
    ax_str_BD[j] = placeholder_axial
    bd_str_BD[j] = placeholder_bend

    j = j + 1    
        

'''
This section checks which parts of the fiber data have to be discarded due to the stiffeners.

The lengths where this had to happen were, honestly, picked by hand. 
Using the graphs of unaltered strain data, the stiffener locations are found around:
    0.31 - 0.38 m
    0.54 - 0.64 m
    0.71 - 0.77 m
The indexes below are the start and end indexes for the gaps.
The gaps here refer to the four gaps in-between the discarded data.
'''

# JUST FOR AC

gap_1 = [0, check_closest(0.31,AC_formula_lengths)]
gap_2 = [check_closest(0.38, AC_formula_lengths), check_closest(0.54, AC_formula_lengths)]
gap_3 = [check_closest(0.64, AC_formula_lengths), check_closest(0.71, AC_formula_lengths)]
gap_4 = [check_closest(0.77, AC_formula_lengths), -1]

gap_1_BD = [0, check_closest(0.31,BD_formula_lengths)]
gap_2_BD = [check_closest(0.38, BD_formula_lengths), check_closest(0.54, BD_formula_lengths)]
gap_3_BD = [check_closest(0.64, BD_formula_lengths), check_closest(0.71, BD_formula_lengths)]
gap_4_BD = [check_closest(0.77, BD_formula_lengths), -1]

'''print(gap_1_BD)
print(gap_2_BD)'''


'''
print(gap_1, 'corresponding lengths:', AC_formula_lengths[gap_1[0]],AC_formula_lengths[gap_1[1]])
print(gap_2, 'corresponding lengths:', AC_formula_lengths[gap_2[0]],AC_formula_lengths[gap_2[1]])
print(gap_3, 'corresponding lengths:', AC_formula_lengths[gap_3[0]],AC_formula_lengths[gap_3[1]])
print(gap_4, 'corresponding lengths:', AC_formula_lengths[gap_4[0]],AC_formula_lengths[gap_4[1]])
'''

'''plt.plot(BD_formula_lengths[gap_1_BD[0]:gap_1_BD[1]],ax_str_BD[1][gap_1_BD[0]:gap_1_BD[1]])
plt.plot(BD_formula_lengths[gap_2_BD[0]:gap_2_BD[1]],ax_str_BD[1][gap_2_BD[0]:gap_2_BD[1]])
plt.plot(BD_formula_lengths[gap_3_BD[0]:gap_3_BD[1]],ax_str_BD[1][gap_3_BD[0]:gap_3_BD[1]])
plt.plot(BD_formula_lengths[gap_4_BD[0]:gap_4_BD[1]],ax_str_BD[1][gap_4_BD[0]:gap_4_BD[1]])


plt.show()'''


