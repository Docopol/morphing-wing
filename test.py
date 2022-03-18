import matplotlib.pyplot as plt
import numpy as np
import processFEMStrainData
import mainFEMdisp
'''
femStrainData1s and femStrainData2s are numpy arrays with [loadstepnumber - 1] [nodenumber - 11651, data column (node number, x, y, z, xy, yz, zx)]
e.g. strainData1s [2][:,2] -> gives the y strain data from data set 1 for the 3rd loadstep 
- Ask Mick if confused
'''
femStrainData1s = processFEMStrainData.strainData1s
femStrainData2s = processFEMStrainData.strainData2s

posNodes = np.array([mainFEMdisp.loadstep1_disp, mainFEMdisp.loadstep2_disp, mainFEMdisp.loadstep3_disp, mainFEMdisp.loadstep4_disp, mainFEMdisp.loadstep5_disp])

def matrixMultiplication (theta: float, loadstep: int, rownumber:int,femStrainDataSets:np.ndarray):
       '''
       notation taken from tutor's image of the required calculation
       '''
       Qs = [[np.cos(theta), np.sin(theta), 0], [-np.sin(theta), np.cos(theta),0], [0,0,1]]
       epsilons = [femStrainDataSets]
       transformationMatrixs = np
       return transformationMatrixs
