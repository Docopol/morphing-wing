import pandas as pd
import numpy as np
import main
import matplotlib.pyplot as plt
import processingFEMData
import mainFEMdisp

'''
processedFEMData1s and processedFEMData2s are numpy arrays with [loadstepnumber - 1] [nodenumber - 11651,  strain xx]
e.g. processedFEMData1s [2][:,1] -> gives the strain data from data set 1 for the 3rd loadstep 
- Ask Mick if confused
'''
processedFEMData1s = processingFEMData.processedFEMData1s
processedFEMData2s = processingFEMData.processedFEMData2s

'''
femNodeLocations is a 2d array with [loadstepnumber -1] [summation of node positions distances]
- Ask Mick if confused
'''

femNodeLocations = np.array([mainFEMdisp.loadstep1_disp_loc[:-1], mainFEMdisp.loadstep2_disp_loc[:-1],
                            mainFEMdisp.loadstep3_disp_loc[:-1], mainFEMdisp.loadstep4_disp_loc[:-1],
                            mainFEMdisp.loadstep5_disp_loc[:-1]])



'''
v v make graphs v v
'''
#colorblindness
for i in range (5):
    fig, ax = plt.subplots(2,2)
    
    #inside comparison plots experiment vs fem
    ax[0,0].set_title('Inside Experimental vs FEM strain plots over the length airfoil')
    #ax[0,0].plot(x1, y1, linewidth=2.0, label = 'Experimental', color = 'orange') 
    ax[0,0].plot(femNodeLocations[i], processedFEMData1s [i][:,1] * 10 ** 6, label = 'FEM', color = 'Blue')
    
    ax[0,0].set_ylabel('Microstrain [μm/m]')
    ax[0,0].set_xlabel('Length along airfoil [m]')
    plt.legend()



    #outside comparison plots experiment vs fem
    ax[0,1].set_title('Outside Experimental vs FEM strain plots over the length airfoil')
    #ax[0,1].plot(x1, y1, linewidth=2.0, label = 'Experimental', color = 'orange') 
    ax[0,1].plot(femNodeLocations[i], processedFEMData2s [i][:,1]* 10 ** 6, label = 'FEM', color = 'Blue')
    plt.legend()
    

    #symmetry analysis experiment (bending analysis)

    fig.delaxes(ax[1,1])
    
plt.show()

#asymmetry over time


#synmmetry, time, 

# symmetry (bending analysis), FEm vs experimental, time vs asymetry (optional)
# fig, ax = plt.subplots(2,2)
#
# # symmetry analyis plot FEM
# ax[0,0].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')
#
# ax[0,0].set(xlim=(0, 8), xticks=np.arange(1, 8),
#        ylim=(0, 8), yticks=np.arange(1, 8))

# ax[0,0].set_title('Bending Analyis FEM')

# symmetry analyis plot FEM
# ax[0,1].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')
#
# ax[0,1].set(xlim=(0, 8), xticks=np.arange(1, 8),
#        ylim=(0, 8), yticks=np.arange(1, 8))
#
# ax[0,1].set_title('Bending Analyis FEM')
'''
# strain data 1
plt.subplot(2, 2, 1)
plt.plot(femNodeLocation[1 - 1], femStrainData1s[1 - 1][:, 4], label="loadstep 1.1")
plt.plot(femNodeLocation[2 - 1], femStrainData1s[2 - 1][:, 4], label="loadstep 2.1")
plt.plot(femNodeLocation[3 - 1], femStrainData1s[3 - 1][:, 4], label="loadstep 3.1")
plt.plot(femNodeLocation[4 - 1], femStrainData1s[4 - 1][:, 4], label="loadstep 4.1")
plt.plot(femNodeLocation[5 - 1], femStrainData1s[5 - 1][:, 4], label="loadstep 5.1")
plt.legend()

# strain data 2
plt.subplot(2, 2, 2)
plt.plot(femNodeLocation[1 - 1], femStrainData2s[1 - 1][:, 4], label="loadstep 1.2")
plt.plot(femNodeLocation[2 - 1], femStrainData2s[2 - 1][:, 4], label="loadstep 2.2")
plt.plot(femNodeLocation[3 - 1], femStrainData2s[3 - 1][:, 4], label="loadstep 3.2")
plt.plot(femNodeLocation[4 - 1], femStrainData2s[4 - 1][:, 4], label="loadstep 4.2")
plt.plot(femNodeLocation[5 - 1], femStrainData2s[5 - 1][:, 4], label="loadstep 5.2")
plt.legend()

# strain data difference of data 1 and 2
plt.subplot(2, 2, 3)
plt.plot(femNodeLocation[1 - 1], abs(abs(femStrainData1s[1 - 1][:, 4]) - abs(femStrainData2s[1 - 1][:, 4])),
         label="loadstep 1")
plt.plot(femNodeLocation[2 - 1], abs(abs(femStrainData1s[2 - 1][:, 4]) - abs(femStrainData2s[2 - 1][:, 4])), label="loadstep 2")
plt.plot(femNodeLocation[3 - 1], abs(abs(femStrainData1s[3 - 1][:, 4]) - abs(femStrainData2s[3 - 1][:, 4])), label="loadstep 3")
plt.plot(femNodeLocation[4 - 1], abs(abs(femStrainData1s[4 - 1][:, 4]) - abs(femStrainData2s[4 - 1][:, 4])), label="loadstep 4")
plt.plot(femNodeLocation[5 - 1], abs(abs(femStrainData1s[5 - 1][:, 4]) - abs(femStrainData2s[5 - 1][:, 4])), label="loadstep 5")
plt.legend()
plt.show()

# # FEM vs experimental data
# ax[1, 0].plot(x1, y1, linewidth=2.0, label='sin', color='orange')
# ax[1, 0].plot(x1, y2, linewidth=2.0, label='cos', color='blue')
#
# ax[1, 0].set(xlim=(0, 8), xticks=np.arange(1, 8),
#              ylim=(0, 8), yticks=np.arange(1, 8))
#
# ax[1, 0].legend(['sin', 'cos'])
#
# # asymmetry over time (optional)
# ax[1, 1].plot(x1, y2, linewidth=2.0, label='cos', color='blue')
#
# ax[1, 1].set(xlim=(0, 8), xticks=np.arange(1, 8),
#              ylim=(0, 8), yticks=np.arange(1, 8))
#
# plt.show()
'''