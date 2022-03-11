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
data2 = load_file("Data/FEM/shell_loadstep3_str.out")
data2 = pd.DataFrame(data2).to_numpy()

print(data2)
'''

#expData = np.genfromtxt("Data/Experimental Strains/Measurements2014_05_22.csv", delimiter=',')
experimental_strain_rows = pd.DataFrame(load_file("Data/Experimental Strains/Measurements2014_05_22.csv")).to_numpy()
print(experimental_strain_rows.shape)
rows, columns = experimental_strain_rows.shape
experimental_strain = np.array(np.zeros((rows,4263)),dtype=str)

for i in range(rows):
    line = np.zeros((1,4263))
    #print(line.shape)
    line = np.array(experimental_strain_rows[i,0].split(sep=','))    
    #print(line)
    #print(line.shape)
    experimental_strain[i] = line

print(experimental_strain.shape)

fiberLengths = [float(i) for i in experimental_strain[0,1:]] # This should not be changed
strainMeasures = [float(i) for i in experimental_strain[25,1:]] # This will change based on which timestep is wanted



#plt.style.use('_mpl-gallery')
plt.plot(fiberLengths,strainMeasures,linewidth=0.5)
plt.show()

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

def lengthSectionSplitter(fiberLengths):
    sections = np.zeros((4,))
    for i in range(len(fiberLengths)):
        # Section C
        if abs(fiberLengths[i] - 0.190102)<10**(-3):
            startC = fiberLengths[i]
        


    return sections

'''
addStrainTimestamp_X:

Takes a timestamp (In seconds from start of test), a list of strain measures and a list of fiber lengths.
Adds a new row to a pre-existing sectionC numpy array of timestamps and strains of sectionX.

WARNING: Since this adds the new timestamp at the bootom, 
it assumes that this will be done in the proper order before the function is called.
'''

#print(fiberLengths)
def splitSections_C(timeStamp ,fiberLengths, strainMeasures, sectionC):
    for i in range(len(fiberLengths)):
        '''if abs(fiberLengths[i] - 0.190102)<10**(-3):
            sectionC = np.zeros((80,1))
            sectionC[,0]=testStamps
            sectionC[]

testStamps = np.ones((80,1))
splitSections_C(testStamps, fiberLengths,strainMeasures)
'''
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
print(fiberLengths)