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
experimentDatas_axial = [sectionDivisionExpData.ax_str_AC, sectionDivisionExpData.ax_str_BD]
experimentDatas_bend = [sectionDivisionExpData.bd_str_AC, sectionDivisionExpData.bd_str_BD]
index_gaps = [[sectionDivisionExpData.gap_1, sectionDivisionExpData.gap_2, sectionDivisionExpData.gap_3, sectionDivisionExpData.gap_4],[sectionDivisionExpData.gap_1_BD, sectionDivisionExpData.gap_2_BD, sectionDivisionExpData.gap_3_BD, sectionDivisionExpData.gap_4_BD]]

AC_formula_lengths = sectionDivisionExpData.AC_formula_lengths
ax_str_AC = sectionDivisionExpData.ax_str_AC

BD_formula_lengths = sectionDivisionExpData.BD_formula_lengths
ax_str_BD = sectionDivisionExpData.ax_str_BD

timeStamps = [0, 12, 27, 39, 54]
plots = [221]


'''
v v make graphs v v
'''

'''
Axial Strain
'''
index_gaps[0][1]
for i in range (1,5):
    plt.figure(i)
    #inside comparison plots experiment vs fem
    #plt.title('Loadstep vs FEM strains')
    #plt.plot(#experiment x values, #experiment y values, label = 'Experimental Loop C', color = 'lime', ls = '-.')
    plt.plot(AC_formula_lengths[index_gaps[0][0][0]:index_gaps[0][0][1]],[ -x for x in ax_str_AC[i-1][index_gaps[0][0][0]:index_gaps[0][0][1]]], label = 'Experimental Loop AC',  color = 'b', ls = '-.')
    plt.plot(AC_formula_lengths[index_gaps[0][1][0]:index_gaps[0][1][1]],[ -x for x in ax_str_AC[i-1][index_gaps[0][1][0]:index_gaps[0][1][1]]], color = 'b', ls = '-.')
    plt.plot(AC_formula_lengths[index_gaps[0][2][0]:index_gaps[0][2][1]],[ -x for x in ax_str_AC[i-1][index_gaps[0][2][0]:index_gaps[0][2][1]]], color = 'b', ls = '-.')
    plt.plot(AC_formula_lengths[index_gaps[0][3][0]:index_gaps[0][3][1]],[ -x for x in ax_str_AC[i-1][index_gaps[0][3][0]:index_gaps[0][3][1]]], color = 'b', ls = '-.')
    
    plt.plot(np.flip(BD_formula_lengths[index_gaps[1][0][0]:index_gaps[1][0][1]]),[ -x for x in ax_str_BD[i-1][index_gaps[1][0][0]:index_gaps[1][0][1]]], label = 'Experimental Loop BD',  color = 'g', ls = '-.')
    plt.plot(np.flip(BD_formula_lengths[index_gaps[1][1][0]:index_gaps[1][1][1]]),[ -x for x in ax_str_BD[i-1][index_gaps[1][1][0]:index_gaps[1][1][1]]], color = 'g', ls = '-.')
    plt.plot(np.flip(BD_formula_lengths[index_gaps[1][2][0]:index_gaps[1][2][1]]),[ -x for x in ax_str_BD[i-1][index_gaps[1][2][0]:index_gaps[1][2][1]]], color = 'g', ls = '-.')
    plt.plot(np.flip(BD_formula_lengths[index_gaps[1][3][0]:index_gaps[1][3][1]]),[ -x for x in ax_str_BD[i-1][index_gaps[1][3][0]:index_gaps[1][3][1]]], color = 'g', ls = '-.')
    
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