import matplotlib.pyplot as plt
import numpy as np
import processFEMStrainData
import mainFEMdisp
from matrixManual import matrixManual

'''
femStrainData1s and femStrainData2s are numpy arrays with [loadstepnumber - 1] [nodenumber - 11651, data column (node number, x, y, z, xy, yz, zx)]
e.g. strainData1s [2][:,2] -> gives the y strain data from data set 1 for the 3rd loadstep 
- Ask Mick if confused
'''
femStrainData1s = processFEMStrainData.strainData1s
femStrainData2s = processFEMStrainData.strainData2s

'''
posNodes is a numpy arrays with [loadstepnumber - 1] [nodenumber - 11651, data column (Node, x, y, z, dx, dy, dz)]
e.g. strainData1s [2][:,2] -> gives the y strain data from data set 1 for the 3rd loadstep 
- Ask Mick if confused 
'''
posNodes = np.array([mainFEMdisp.loadstep1_disp, mainFEMdisp.loadstep2_disp, mainFEMdisp.loadstep3_disp, mainFEMdisp.loadstep4_disp, mainFEMdisp.loadstep5_disp])

def angleDefinitionQuadraticSpline(loadstepNumber:int, rowNumber:int, femStrainDataSetForLoadsteps:np.ndarray): #rownumber has to be 1 less than the amount of data points since no forward extrapolation can occur
       y0,x0 = posNodes[loadstepNumber][rowNumber-1,1],posNodes[loadstepNumber][rowNumber-1,2]
       y1,x1 = posNodes[loadstepNumber][rowNumber,1], posNodes[loadstepNumber][rowNumber,2]
       y2,x2 = posNodes[loadstepNumber][rowNumber+1,1], posNodes[loadstepNumber][rowNumber+1,2]

       LHS = [[1,x0,x0**2],[1,x1,x1**2],[1,x2,x2**2]]
       RHS = [y0,y1,y2]
       
       c,b,a = np.linalg.solve(LHS,RHS)
       angleAirfoilSurfaceRadians = np.arctan(2*a*x1+b)
       '''
       strainXX = femStrainDataSetForLoadsteps [rowNumber][2]
       strainYY = femStrainDataSetForLoadsteps [rowNumber][1]
       angleStrainRadians = np.arctan2(strainYY,strainXX)
       
       theta = angleAirfoilSurfaceRadians - angleStrainRadians
       
       if abs(theta) > np.pi:
              theta = theta/abs(theta) * (abs(theta)-np.pi)
       '''
       return angleAirfoilSurfaceRadians

def matrixMultiplication (rownumber:int, loadstepNumber:int, femStrainDataSetForLoadsteps:np.ndarray): #include the loadstep specification in the femstraindatasetforloadstep
       '''
       notation taken from tutor's image of the required calculation
       '''
       theta = angleDefinitionQuadraticSpline (loadstepNumber, rownumber, femStrainDataSetForLoadsteps)

       Qs = np.matrix([[np.cos(theta), np.sin(theta), 0], 
              [-np.sin(theta), np.cos(theta),0], 
              [0,0,1]])
       epsilons = np.matrix([[femStrainDataSetForLoadsteps[rownumber,1], femStrainDataSetForLoadsteps[rownumber,4], femStrainDataSetForLoadsteps[rownumber,6]],
              [femStrainDataSetForLoadsteps[rownumber,4], femStrainDataSetForLoadsteps[rownumber,2], femStrainDataSetForLoadsteps[rownumber,5]],
              [femStrainDataSetForLoadsteps[rownumber,6], femStrainDataSetForLoadsteps[rownumber,5], femStrainDataSetForLoadsteps[rownumber,3]]
              ])


       transformationMatrixs = np.matmul(Qs, epsilons, Qs.T)
       return transformationMatrixs


#StrainData1s
processedFEMData1s = np.zeros ([np.shape (femStrainData1s)[0], np.shape (femStrainData1s)[1]-1, 2])#-1 comes from the fact that there is forward linear interpolation which ommits the last data point
for i in range (np.shape (processedFEMData1s)[0]):
       for j in range (np.shape (processedFEMData1s)[1]): 
              processedFEMData1s [i][j][0] = femStrainData1s[i][j][0]
              processedFEMData1s [i][j][1]= float(matrixMultiplication(j,i,femStrainData1s[i])[0,0])

#StrainData2s
processedFEMData2s = np.zeros ([np.shape (femStrainData2s)[0], np.shape (femStrainData2s)[1]-1, 2])#-1 comes from the fact that there is forward linear interpolation which ommits the last data point
for i in range (np.shape (processedFEMData2s)[0]):
       for j in range (np.shape (processedFEMData2s)[1]): 
              processedFEMData2s [i][j][0] = femStrainData2s[i][j][0]
              processedFEMData2s [i][j][1]= float(matrixMultiplication(j,i,femStrainData2s[i])[0,0])



thetaValues = np.zeros ([np.shape (femStrainData1s)[0], np.shape (femStrainData1s)[1]-1, 3])
for i in range (np.shape (processedFEMData1s)[0]):
       for j in range (np.shape (processedFEMData1s)[1]): 
              thetaValues [i][j][0] = femStrainData1s[i][j][0]
              thetaValues [i][j][2] = angleDefinitionQuadraticSpline(i,j,femStrainData1s[i])


print(thetaValues)

plt.plot(thetaValues[1][:,0], thetaValues[1][:,2])
plt.show()
