
from cgitb import small
from tabnanny import check
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


'''
Data for sections B and D are reversed, meaning they start at the end arclength and go to the start.
Below, these are reversed and assigned new variables in order to do the axial/bending stuff.
It also just takes the necessary timestamps instead of the whole thing again.

New variables in order not to break the stuff that's already done.
'''

timeStamps = [0, 12, 27, 39, 54]
newExpDatas = np.empty([5,2,4], dtype='object')

for i in range(5):
    ''' contours '''
    newExpDatas[i][0][0] = experimentalDatas[timeStamps[i]][0][0]
    newExpDatas[i][0][1] = np.flip(experimentalDatas[timeStamps[i]][0][1])
    newExpDatas[i][0][2] = experimentalDatas[timeStamps[i]][0][2]
    newExpDatas[i][0][3] = np.flip(experimentalDatas[timeStamps[i]][0][3])

    ''' strains '''
    newExpDatas[i][1][0] = experimentalDatas[timeStamps[i]][1][0]
    newExpDatas[i][1][1] = np.flip(experimentalDatas[timeStamps[i]][1][1])
    newExpDatas[i][1][2] = experimentalDatas[timeStamps[i]][1][2]
    newExpDatas[i][1][3] = np.flip(experimentalDatas[timeStamps[i]][1][3])

    ''' deletes problematic first elements from B and C '''
    newExpDatas[i][0][1] = np.delete(newExpDatas[i][0][1],0)
    newExpDatas[i][1][1] = np.delete(newExpDatas[i][1][1],0)
    newExpDatas[i][0][2] = np.delete(newExpDatas[i][0][2],0)
    newExpDatas[i][1][2] = np.delete(newExpDatas[i][1][2],0)

'''
Indexes are arrays where Index[(0,1) depending on (inside,outside)][(0,1) depending on (start,end)]
'''

AC_index = check_interval(newExpDatas[0][0][2],newExpDatas[0][0][0])
BD_index = check_interval(newExpDatas[0][0][3],newExpDatas[0][0][1])

'''
Commented here because I have no idea how to do it properly. Just copy paste whenever you want to index the slices.

A_index = AC_index[1][0]:AC_index[1][1]
B_index = BD_index[1][0]:BD_index[1][1]
C_index = AC_index[0][0]:AC_index[0][1]
D_index = BD_index[0][0]:BD_index[0][1]
'''

ax_str = []
bd_str = []


def axial_strain(contour_in, contour_out, str_in, str_out):
    ax_str = []
    for i in range(np.size(contour_in)):
        index = check_closest(contour_in[i], contour_out)
        e_ax = (str_out[index] + str_in[i])/2
        ax_str = np.append(ax_str, e_ax)

    return ax_str

def bending_strain(contour_in, contour_out, str_in, str_out):
    bd_str = []
    for i in range(np.size(contour_in)):
        index = check_closest(contour_in[i], contour_out)
        b_ax = (str_out[index] - str_in[i])/2
        bd_str = np.append(bd_str, b_ax)

    return bd_str

AC_axial = np.empty([5], dtype = 'object')
AC_bending = np.empty([5], dtype = 'object')
BD_axial = np.empty([5], dtype = 'object')
BD_bending = np.empty([5], dtype = 'object')

for i in range(5):
    AC_axial[i] = axial_strain(newExpDatas[i][0][2][AC_index[0][0]:AC_index[0][1]], newExpDatas[i][0][0][AC_index[1][0]:AC_index[1][1]], newExpDatas[i][1][2][AC_index[0][0]:AC_index[0][1]], newExpDatas[i][1][0][AC_index[1][0]:AC_index[1][1]])
    AC_bending[i] = bending_strain(newExpDatas[i][0][2][AC_index[0][0]:AC_index[0][1]], newExpDatas[i][0][0][AC_index[1][0]:AC_index[1][1]], newExpDatas[i][1][2][AC_index[0][0]:AC_index[0][1]], newExpDatas[i][1][0][AC_index[1][0]:AC_index[1][1]])

    BD_axial[i] = axial_strain(newExpDatas[i][0][3][BD_index[0][0]:BD_index[0][1]], newExpDatas[i][0][1][BD_index[1][0]:BD_index[1][1]], newExpDatas[i][1][3][BD_index[0][0]:BD_index[0][1]], newExpDatas[i][1][1][BD_index[1][0]:BD_index[1][1]])
    BD_bending[i] = bending_strain(newExpDatas[i][0][3][BD_index[0][0]:BD_index[0][1]], newExpDatas[i][0][1][BD_index[1][0]:BD_index[1][1]], newExpDatas[i][1][3][BD_index[0][0]:BD_index[0][1]], newExpDatas[i][1][1][BD_index[1][0]:BD_index[1][1]])


'''
for i in range(3):
    bad_indexes[0]=np.append(bad_indexes[0],range(check_closest(bad_lengths[i][0],newExpDatas[0][0][0]),check_closest(bad_lengths[i][1],newExpDatas[0][0][0])))
    bad_indexes[1]=np.append(bad_indexes[1],range(check_closest(bad_lengths[i][0],newExpDatas[0][0][1]),check_closest(bad_lengths[i][1],newExpDatas[0][0][1])))
    bad_indexes[2]=np.append(bad_indexes[2],range(check_closest(bad_lengths[i][0],newExpDatas[0][0][2]),check_closest(bad_lengths[i][1],newExpDatas[0][0][2])))
    bad_indexes[3]=np.append(bad_indexes[3],range(check_closest(bad_lengths[i][0],newExpDatas[0][0][3]),check_closest(bad_lengths[i][1],newExpDatas[0][0][3])))

bad_indexes[0] = np.delete(bad_indexes[0],0).astype(int)
bad_indexes[1] = np.delete(bad_indexes[1],0).astype(int)
bad_indexes[2] = np.delete(bad_indexes[2],0).astype(int)
bad_indexes[3] = np.delete(bad_indexes[3],0).astype(int)
'''


AC_lengths = np.empty([5], dtype='object')
BD_lengths = np.empty([5], dtype='object')
for i in range(5):
    AC_lengths[i] = newExpDatas[i][0][2][AC_index[0][0]:AC_index[0][1]]
    BD_lengths[i] = newExpDatas[i][0][3][BD_index[0][0]:BD_index[0][1]]


'''
bad_indexes[(0,1) for sections (AC, BD)][(0,1,2) for 1st, 2nd and 3rd stiffener gaps]
'''

bad_lengths = np.array([[0.28,0.39],[0.54,0.65],[0.70,0.77]])
bad_indexes = np.empty([2], dtype='object')

for i in range(3):
    bad_indexes[0]=np.append(bad_indexes[0],[check_closest(bad_lengths[i][0],AC_lengths[0]),check_closest(bad_lengths[i][1],AC_lengths[0])]) # This one
    bad_indexes[1]=np.append(bad_indexes[1],[check_closest(bad_lengths[i][0],BD_lengths[0]),check_closest(bad_lengths[i][1],BD_lengths[0])]) # And this one

bad_indexes[0] = np.delete(bad_indexes[0],0)
bad_indexes[1] = np.delete(bad_indexes[1],0)

'''
^^ Above should be working correctly ^^
'''

for i in range(5):
    AC_lengths[i] = np.split(AC_lengths[i], bad_indexes[0])
    AC_axial[i] = np.split(AC_axial[i], bad_indexes[0])
    AC_bending[i] = np.split(AC_bending[i], bad_indexes[0])
    BD_lengths[i] = np.split(BD_lengths[i], bad_indexes[1])
    BD_axial[i] = np.split(BD_axial[i], bad_indexes[1])
    BD_bending[i] = np.split(BD_bending[i], bad_indexes[1])


'''
Plots should have the format displayed below, in order to not show the unusable gaps.

for i in range(0,8,2):
    plt.plot(AC_lengths[2][i], AC_axial[2][i], color='b')
    
'''



