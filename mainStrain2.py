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



timeStamps = [0, 12, 27, 39, 54]
plots = [221]
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