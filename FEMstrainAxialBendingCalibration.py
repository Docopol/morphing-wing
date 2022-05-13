import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import processingFEMData_manualMatrix as processingFEMData

'''
processedFEMData1s and processedFEMData2s are 3dnumpy arrays with [loadstepnumber - 1] [nodenumber - 11651,  strain xx]
e.g. processedFEMData1s [2][:,1] -> gives the strain data from data set 1 for the 3rd loadstep 
- Ask Mick if confused
inside = 2, outside = 1
'''

processedFEMData1s = processingFEMData.processedFEMData1s 
processedFEMData2s = processingFEMData.processedFEMData2s 

#conversion to true strain
processedFEMData1s [:][:,1] = processedFEMData1s [:][:,1] /2
processedFEMData2s [:][:,1] = processedFEMData2s [:][:,1] /2


'''
insideFEMDatas and outsideFEMDatas are 3dnumpy arrays with [loadstepnumber - 1] [nodenumber - 11651,  Axial Strain, Bending strain]
'''
FEMDatas = np.zeros ([np.shape (processedFEMData2s)[0], np.shape (processedFEMData2s)[1], 3])

#calibration
for i in range (1,5):
    processedFEMData1s [i][:,1] -= processedFEMData1s [0] [:,1]
    processedFEMData2s [i][:,1] -= processedFEMData2s [0] [:,1]


for i in range (np.shape (FEMDatas)[0]):
       for j in range (np.shape (FEMDatas)[1]): 
            LHS = [[1,1],[1,-1]]
            RHS = [processedFEMData1s[i][j,1], processedFEMData2s[i][j,1]]
            axialStrain, bendingStrain = np.linalg.solve(LHS,RHS) #output is axial, bending
            FEMDatas [i][j][:] = [processedFEMData2s[i][j][0], axialStrain, bendingStrain]#node number
'''
plt.plot(FEMDatas[1][:,0], FEMDatas[1][:,1])
plt.plot(FEMDatas[1][:,0], FEMDatas[1][:,2])
plt.show()
'''