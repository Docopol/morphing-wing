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

AC_lengths = sectionDivisionExpData.AC_lengths
AC_axial = sectionDivisionExpData.AC_axial
AC_bending = sectionDivisionExpData.AC_bending
BD_lengths = sectionDivisionExpData.BD_lengths
BD_axial = sectionDivisionExpData.BD_axial
BD_bending = sectionDivisionExpData.BD_bending


'''
v v make graphs v v
'''

'''
Axial Strain
'''

for i in range (1,5):
    plt.figure(i)
    #inside comparison plots experiment vs fem
    #plt.title('Loadstep ' + str(i+1) + ' Experimental vs FEM axial strains')
    #plt.plot(#experiment x values, #experiment y values, label = 'Experimental Loop C', color = 'lime', ls = '-.')
    plt.plot(AC_lengths[i][0], AC_axial[i][0], ls = '--', label='Experimental', color = 'b')
    #plt.plot(BD_lengths[i][0], BD_axial[i][0], ls = '--', label = 'BD Axial', color = 'b')
    for j in range(2,8,2):
        plt.plot(AC_lengths[i][j], AC_axial[i][j], ls = '--', color = 'b')
        #plt.plot(BD_lengths[i][j], BD_axial[i][j], ls = '--', color = 'b')
    
    plt.plot(np.flip(femNodeLocations[i]), FEMdatas[i][:,1] * 10 ** 6, label = 'FEM', color = 'r')
    
    plt.ylabel('Axial Microstrain [μm/m]')
    plt.xlabel('Length along contour [m]')
    plt.legend()
    plt.ylim((-600,500))
    plt.savefig('Axial_' + str(i+1))

    

'''
Bending Strain
'''

for i in range (1,5):
    plt.figure(i+4)
    #plt.title('Loadstep ' + str(i+1) + ' Experimental vs FEM bending strains')
    #inside comparison plots experiment vs fem
    #plt.title('Loadstep vs FEM strains')
    #plt.plot(#experiment x values, #experiment y values, label = 'Experimental Loop C', color = 'lime', ls = '-.')
    plt.plot(AC_lengths[i][0], AC_bending[i][0], ls = '--', label='Experimental', color = 'b')
    #plt.plot(BD_lengths[i][0], BD_bending[i][0], ls = '--',label = 'BD Bending', color = 'b')
    for j in range(2,8,2):
        plt.plot(AC_lengths[i][j], AC_bending[i][j], ls = '--', color = 'b')
        #plt.plot(BD_lengths[i][j], BD_bending[i][j], ls = '--', color = 'b')
    
    plt.plot(np.flip(femNodeLocations[i]), FEMdatas[i][:,2] * 10 ** 6, label = 'FEM', color = 'r')
    
    plt.ylabel('Bending Microstrain [μm/m]')
    plt.xlabel('Length along contour [m]')
    plt.legend()
    plt.ylim((-5000,4000))

    plt.savefig('Bending_' + str(i+1))


plt.show()