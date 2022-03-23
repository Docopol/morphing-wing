import pandas as pd
import numpy as np
import main
import matplotlib.pyplot as plt
import processingFEMData
import mainFEMdisp
import sectionDivisionExpData

'''
processedFEMData1s and processedFEMData2s are 3dnumpy arrays with [loadstepnumber - 1] [nodenumber - 11651,  strain xx]
e.g. processedFEMData1s [2][:,1] -> gives the strain data from data set 1 for the 3rd loadstep 
- Ask Mick if confused
'''
processedFEMData1s = processingFEMData.processedFEMData1s
processedFEMData2s = processingFEMData.processedFEMData2s

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


'''
v v make graphs v v
'''

#colorblindness
for i in range (5):
    fig, ax = plt.subplots(2,2)
    
    #inside comparison plots experiment vs fem
    ax[0,0].set_title('Inside Experimental vs FEM strains')
    ax[0,0].plot(experimentDatas[timeStamps[i]][0][2], experimentDatas[timeStamps[i]][1][2], label = 'Experimental Loop C', color = 'lime', ls = '-.') 
    ax[0,0].plot(experimentDatas[timeStamps[i]][0][3], experimentDatas[timeStamps[i]][1][3], label = 'Experimental Loop D', color = 'darkred', ls = '--') 
    ax[0,0].plot(np.flip(femNodeLocations[i]), processedFEMData2s [i][:,1] * 10 ** 6, label = 'FEM', color = 'hotpink')
    
    ax[0,0].set_ylabel('Microstrain [μm/m]')
    ax[0,0].set_xlabel('Length along contour [m]')
    plt.legend()



    #outside comparison plots experiment vs fem
    ax[0,1].set_title('Outside Experimental vs FEM strains')
    ax[0,1].plot(experimentDatas[timeStamps[i]][0][0], experimentDatas[timeStamps[i]][1][0], label = 'Experimental Loop A', color = 'lime', ls = '-.') 
    ax[0,1].plot(experimentDatas[timeStamps[i]][0][1], experimentDatas[timeStamps[i]][1][1], label = 'Experimental Loop B', color = 'darkred', ls = '--') 
    ax[0,1].plot(femNodeLocations[i], processedFEMData1s [i][:,1]* 10 ** 6, label = 'FEM', color = 'hotpink')
    
    ax[0,1].set_ylabel('Microstrain [μm/m]')
    ax[0,1].set_xlabel('Length along contour [m]')
    plt.legend()
    

    #symmetry analysis experiment (bending analysis) A-C
    ax[1,0].set_title('Symmetry Analysis A-C')
    ax[1,0].plot (experimentDatas[timeStamps[i]][0][0], experimentDatas[timeStamps[i]][1][0],label = 'Outside', color = 'lime', ls = '-.')
    ax[1,0].plot (experimentDatas[timeStamps[i]][0][2], [-x for x in experimentDatas[timeStamps[i]][1][2]], label = 'Inside', color = 'cyan', ls = '--')

    ax[1,0].set_ylabel('Difference in Microstrain between Inside and Outside [μm/m]')
    ax[1,0].set_xlabel('Length along contour [m]')
    plt.legend()

    #symmetry analysis experiment (bending analysis) #negative has to be taken
    ax[1,1].set_title('Symmetry Analysis B-D')
    ax[1,1].plot (experimentDatas[timeStamps[i]][0][1], experimentDatas[timeStamps[i]][1][1],label = 'Outside', color = 'lime', ls = '-.')
    ax[1,1].plot (experimentDatas[timeStamps[i]][0][3], [-x for x in experimentDatas[timeStamps[i]][1][3]], label = 'Inside', color = 'cyan', ls = '--')

    ax[1,1].set_ylabel('Difference in Microstrain between Inside and Outside [μm/m]')
    ax[1,1].set_xlabel('Length along contour [m]')
    plt.legend()



#asymmetry over time
#plt.plot (label = 'Loop A-C', color = 'lime', ls = '-.') )
#plt.plot (label = 'Loop B-D', color = 'cyan', ls = '--') )

ax[1,0].set_ylabel('Difference in Microstrain between Inside and Outside [μm/m]')
ax[1,0].set_xlabel('Length along contour [m]')
plt.legend()

    
plt.show()


# ax[1, 1].set(xlim=(0, 8), xticks=np.arange(1, 8),
#              ylim=(0, 8), yticks=np.arange(1, 8))
