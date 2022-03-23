
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

    fittedLength = np.zeros(gapNumber+1)
    fittedLength[0]=callibrationStart

    for i in range(gapNumber):
        fittedLength[i+1]=fittedLength[i]+gapLength

    return fittedLength


def noiseRemove(timeZeroStrains, strainMeasures):

    noNoiseStrains = np.zeros(len(timeZeroStrains))

    for i in range(len(timeZeroStrains)):
        noNoiseStrains[i] = float(strainMeasures[i]) - timeZeroStrains[i]

    return noNoiseStrains


'''I hate what happens here but its needed.

This function happens since the callibration points given make the gaps not have the same spacing.

'''


def calibrateSection(secLengths, secCalibFibers, secCalibActual):
    a = 0
    secLengthsActuals = np.zeros(1)

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
    
    AStrains = noiseRemove(zeroAStrains, AStrains)
    BStrains = noiseRemove(zeroBStrains, BStrains)
    CStrains = noiseRemove(zeroCStrains, CStrains)
    DStrains = noiseRemove(zeroDStrains, DStrains)
    
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

#print(np.size(DLengthsActual))
#print(np.size(DStrains))


'''
plt.plot(CLengths, CStrains,linewidth=0.5) # Inside Graph
plt.plot(ALengths, AStrains, 'r--', linewidth=0.5) # Outside Graph
plt.show()
'''

'''
plt.plot(DLengths, DStrains,linewidth=0.5) # Inside Graph
plt.plot(BLengths, BStrains, 'r--', linewidth=0.5) # Outside Graph
plt.show()
'''

'''
UNCOMMENT IF NEEDED

BStrains, BLengths = sectionB(28, fiberLengths, experimental_strain)
DStrains, DLengths = sectionD(28, fiberLengths, experimental_strain)
DStrains.reverse()
DStrains = [-x for x in DStrains]



BLengths = fitSection(BLengths, 0.05, 1.05)
DLengths = fitSection(DLengths, 0.076, 1.024)

ACSections = [ALengths, AStrains, CLengths, CStrains]
BDSections = [BLengths, BStrains, DLengths, DStrains]


 '''

'''plt.plot(ACSections[2], ACSections[3],linewidth=0.5) # Inside Graph
plt.plot(ACSections[0], ACSections[1], 'r--', linewidth=0.5) # Outside Graph
plt.show()'''

#print(fiberLengths)