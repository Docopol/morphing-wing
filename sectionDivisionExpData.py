
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


# This stuff will go into the final code of this section.

experimental_strain_rows = pd.DataFrame(load_file("Data/Experimental Strains/Measurements2014_05_22.csv")).to_numpy()
rows, columns = experimental_strain_rows.shape
experimental_strain = np.array(np.zeros((rows,4263)),dtype=str)



for i in range(rows):
    line = np.zeros((1,4263))
    #print(line.shape)
    line = np.array(experimental_strain_rows[i,0].split(sep=','))    
    #print(line)
    #print(line.shape)
    experimental_strain[i] = line


fiberLengths = [float(i) for i in experimental_strain[0,1:]] # This should not be changed

'''
# To access specific strains at timestamp change the X value in:
# float(i) for i in experimental_strain[X,1:]
strainMeasures = [float(i) for i in experimental_strain[20,1:]] # This will change based on which timestep is wanted
''' # This shit should no longer be needed, just kept in case.


'''
WARNING: 
For the data calibration, the fiber length does not exactly match the path distance of the airfoil.
This means the data had to be squeezed in order to fit with the actual surface of the airfoil.
'''

'''
lengthSectionSplitter:

Takes a list of fiber lengths, splits them into four sections A,B,C,D.
Returns them as an array where each row is a section. A row 0, B row 1, C row 2, D row 3.
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
            firstTerm = i+1
        if fiberLengths[i] == 1.25324:
            lastTerm = i+2 
            break
    sectionCStrains = [float(a) for a in strainMeasures[timeStamp, firstTerm:lastTerm]]
    sectionCLengths = [float(a) for a in fiberLengths[firstTerm:lastTerm]]
    return sectionCStrains, sectionCLengths

def sectionA(timeStamp ,fiberLengths, strainMeasures):
    for i in range(len(fiberLengths)):
        if fiberLengths[i] == 1.58908:
            firstTerm = i+1
        if fiberLengths[i] == 2.59791:
            lastTerm = i+2 
            break
    sectionAStrains = [float(a) for a in strainMeasures[timeStamp, firstTerm:lastTerm]]
    sectionALengths = [float(a) for a in fiberLengths[firstTerm:lastTerm]]
    return sectionAStrains, sectionALengths

def sectionB(timeStamp ,fiberLengths, strainMeasures):
    for i in range(len(fiberLengths)):
        if fiberLengths[i] == 2.75864:
            firstTerm = i+1
        if fiberLengths[i] == 3.77008:
            lastTerm = i+2 
            break
    sectionAStrains = [float(a) for a in strainMeasures[timeStamp, firstTerm:lastTerm]]
    sectionALengths = [float(a) for a in fiberLengths[firstTerm:lastTerm]]
    return sectionAStrains, sectionALengths

def sectionD(timeStamp ,fiberLengths, strainMeasures):
    for i in range(len(fiberLengths)):
        if fiberLengths[i] == 4.07065:
            firstTerm = i+1
        if fiberLengths[i] == 5.17115:
            lastTerm = i+2 
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

# The number entered on each section function is the timestamp, starting from 1.

zeroAStrains, trash= sectionA(1, fiberLengths, experimental_strain) # Gets time zero values for noise removal.
AStrains, ALengths = sectionA(15, fiberLengths, experimental_strain)

zeroCStrains, trash = sectionC(1, fiberLengths, experimental_strain)
CStrains, CLengths = sectionC(15, fiberLengths, experimental_strain)

AStrains = noiseRemove(zeroAStrains, AStrains)
CStrains = noiseRemove(zeroCStrains, CStrains)

AStrains = np.flip(AStrains)
CStrains = [-x for x in CStrains]



BStrains, BLengths = sectionB(1, fiberLengths, experimental_strain)
DStrains, DLengths = sectionD(1, fiberLengths, experimental_strain)
DStrains.reverse()
DStrains = [-x for x in DStrains]

CLengths = fitSection(CLengths, 0.07, 1.027)#0.07; 1.027
ALengths = fitSection(ALengths, 0.05, 1.05)

BLengths = fitSection(BLengths, 0.05, 1.05)
DLengths = fitSection(DLengths, 0.076, 1.024)

ACSections = [ALengths, AStrains, CLengths, CStrains]
BDSections = [BLengths, BStrains, DLengths, DStrains]

#print(CStrain)




 
plt.plot(ACSections[2], ACSections[3], linewidth=0.5) # Inside Graph
plt.plot(ACSections[0], ACSections[1], linewidth=0.5, color='r') # Outside Graph
plt.show()


'''
FiberLocation	ActualLocation
0.190102	0.07
0.414263	0.296
0.510969	0.378
0.673016	0.54
0.793244	0.645
0.848131	0.70
0.984042	0.759
1.25324		1.027
'''

#print(fiberLengths)