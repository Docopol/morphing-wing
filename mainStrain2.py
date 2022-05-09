from tracemalloc import stop
import pandas as pd
import numpy as np
import main
import matplotlib.pyplot as plt
import FEMstrainAxialBendingCalibration
import mainFEMdisp
import sectionDivisionExpData


'''
insideFEMDatas and outsideFEMDatas are 3dnumpy arrays with [loadstepnumber - 1] [nodenumber - 11651,  Axial Strain, Bending strain]
- ask Mick if confused
'''
FEMdatas = FEMstrainAxialBendingCalibration.FEMDatas

'''
femNodeLocations is a 2d numpy array with [loadstepnumber -1] [summation of node positions distances]
- Ask Mick if confused
'''

femNodeLocations = np.array([mainFEMdisp.loadstep1_disp_loc[:-1], mainFEMdisp.loadstep2_disp_loc[:-1],
                            mainFEMdisp.loadstep3_disp_loc[:-1], mainFEMdisp.loadstep4_disp_loc[:-1],
                            mainFEMdisp.loadstep5_disp_loc[:-1]])

'''
experimentDatas is a 3d numpy array with [timeStampNumber] [length along contour (0) or strain (1)] [Loopletter (A,B,C,D)]
note that A and B 
'''
experimentDatas = sectionDivisionExpData.experimentalDatas 

'''
This spaghetti code is mine, I apologize in advance.
- Tom

The indexing is 0 for loop AC and 1 for loop BC, for all the stuff below.
'''

newExpDatas = sectionDivisionExpData.newExpDatas

AC_index = sectionDivisionExpData.AC_index
AC_axial = sectionDivisionExpData.AC_axial
BD_index = sectionDivisionExpData.BD_index
BD_axial = sectionDivisionExpData.BD_axial


'''
v v make graphs v v
'''

'''
Axial Strain
'''

for i in range (1,5):
    plt.figure(i)
    #inside comparison plots experiment vs fem
    #plt.title('Loadstep vs FEM strains')
    #plt.plot(#experiment x values, #experiment y values, label = 'Experimental Loop C', color = 'lime', ls = '-.')
    plt.plot(newExpDatas[0][0][2][AC_index[0][0]:AC_index[0][1]], AC_axial[i], ls = '--', label='AC Axial', color = 'r')
    plt.plot(newExpDatas[0][0][3][BD_index[0][0]:BD_index[0][1]], BD_axial[i], label = 'BD Axial', color = 'b')
    
    plt.plot(np.flip(femNodeLocations[i]), FEMdatas[i][:,1] * 10 ** 6, label = 'FEM', color = 'hotpink')
    
    plt.ylabel('Axial Microstrain [μm/m]')
    plt.xlabel('Length along contour [m]')
    plt.legend()
    print(i)
    

'''
Bending Strain
'''

for i in range (1,5):
    plt.figure(i+4)
    #inside comparison plots experiment vs fem
    #plt.title('Loadstep vs FEM strains')
    #plt.plot(#experiment x values, #experiment y values, label = 'Experimental Loop C', color = 'lime', ls = '-.')
    
    plt.plot(np.flip(femNodeLocations[i]), FEMdatas[i][:,2] * 10 ** 6, label = 'FEM', color = 'hotpink')
    
    plt.ylabel('Bending Microstrain [μm/m]')
    plt.xlabel('Length along contour [m]')
    plt.legend()
    print(i)

plt.show()