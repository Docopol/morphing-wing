import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import processFEMStrainData
import mainFEMdisp
from matrixManual import matrixManual
import sectionDivisionExpData


'''
femStrainData1s and femStrainData2s are numpy arrays with [loadstepnumber - 1] [nodenumber - 11651, data column (node number, x, y, z, xy, yz, zx)]
e.g. strainData1s [2][:,2] -> gives the y strain data from data set 1 for the 3rd loadstep 
- Ask Mick if confused
'''
femStrainData1s = processFEMStrainData.strainData1s
femStrainData2s = processFEMStrainData.strainData2s

'''
experimentalDatas[timestamp - 1][0:length along airfoil // 1:strains along airfoil][0,1,2,3: Contours A,B,C,D]
'''

experimentDatas = sectionDivisionExpData.experimentalDatas 

'''
Importing all the finalized postion data from mainFEMdisp.
At this point, if we were to interpolate there might be some errors with the interpolation since the output "equation" has double values for a single x.
We'll need to split the graph into two curves which can be splined. At the tip we assume an infinite derivative? Dunno if this will cause trouble.
'''

loadstep1_coord_x = mainFEMdisp.loadstep1_coord_x
loadstep1_coord_y = mainFEMdisp.loadstep1_coord_y
loadstep2_coord_x = mainFEMdisp.loadstep2_coord_x
loadstep2_coord_y = mainFEMdisp.loadstep2_coord_y
loadstep3_coord_x = mainFEMdisp.loadstep3_coord_x
loadstep3_coord_y = mainFEMdisp.loadstep3_coord_y
loadstep4_coord_x = mainFEMdisp.loadstep4_coord_x
loadstep4_coord_y = mainFEMdisp.loadstep4_coord_y
loadstep5_coord_x = mainFEMdisp.loadstep5_coord_x
loadstep5_coord_y = mainFEMdisp.loadstep5_coord_y


'''
This function takes in the x and y coordinates of an airfoil.
Detects the tip and splits it into two separate curves which have unique xy pairs.

Output:     split_airfoil[1st or 2nd curve][x or y coords]

i.e split_airfoil[0][1] returns the y coordinates of the first curve.
'''
def airfoil_splitter(x_coords, y_coords, ):

    split_airfoil = np.array([[0,0],[0,0]], dtype='object')

    size = len(x_coords)
    for i in range(size):
        if x_coords[i+1] > x_coords[i]:
            break
        if x_coords[i+1] < x_coords[i]:
            smallest_i = i+1
            continue
    
    # This flip here is weird, but its needed for the interpolation function (used later) to work.
    split_airfoil[0][0]=np.flip(x_coords[:smallest_i+1])
    split_airfoil[1][0]=x_coords[smallest_i:]
    split_airfoil[0][1]=np.flip(y_coords[:smallest_i+1])
    split_airfoil[1][1]=y_coords[smallest_i:]

    return split_airfoil, smallest_i

'''
Debugged with propper data as of 05/05/2022
(aka should be working fine)
'''
###        CURRENT APPROACH: Tests using loadstep 2, be consistent in further betas.
split_test, smallest_i = airfoil_splitter(loadstep2_coord_x,loadstep2_coord_y)

'''testx = np.flip(split_test[0][0])
testy = np.flip(split_test[0][1])'''

splined_airfoil_1 = CubicSpline(split_test[0][0], split_test[0][1])
splined_airfoil_2 = CubicSpline(split_test[1][0], split_test[1][1])

theta_1 = np.arctan(splined_airfoil_1(split_test[0][0],1))
theta_2 = np.arctan(splined_airfoil_2(split_test[1][0],1))

# Loadsteps also influence here
strain_xx_1 = []
for i in range(smallest_i+1):
    strain_xx_1 = np.append(strain_xx_1, femStrainData2s[1][:][i][1])

strain_yy_1 = []
for i in range(smallest_i+1):
    strain_yy_1 = np.append(strain_yy_1, femStrainData2s[1][:][i][2])

strain_xy_1 = []
for i in range(smallest_i+1):
    strain_xy_1 = np.append(strain_xy_1, femStrainData2s[1][:][i][4])

strain_xx_2 = []
for i in range(smallest_i,555):
    strain_xx_2 = np.append(strain_xx_2, femStrainData2s[1][:][i][1])

strain_yy_2 = []
for i in range(smallest_i,555):
    strain_yy_2 = np.append(strain_yy_2, femStrainData2s[1][:][i][2])

strain_xy_2 = []
for i in range(smallest_i,555):
    strain_xy_2 = np.append(strain_xy_2, femStrainData2s[1][:][i][4])





print(np.shape (femStrainData2s))


strain_camber_1 = []
for i in range(smallest_i+1):
    strain_camber_1 = np.append(strain_camber_1, matrixManual(theta_1[i], strain_xx_1[i], strain_yy_1[i], strain_xy_1[i])*10**6)
strain_camber_2 = []
for i in range(np.size(strain_xx_2)):
    strain_camber_2 = np.append(strain_camber_2, matrixManual(theta_2[i], strain_xx_2[i], strain_yy_2[i], strain_xy_2[i])*10**6)

length = np.append(split_test[0][0],split_test[1][0]+split_test[0][0][-1]-split_test[0][0][0])
strain_camber = np.append(strain_camber_1,strain_camber_2)



###         MAIN PROBLEM: Plotting over experimental and then doing it for all loadsteps.
#fig, ax = plt.subplots(1)
'''
ax[0].set_title('full curve')
ax[0].plot(split_test[0][0],split_test[0][1],label='unsplit')

ax[1].set_title('first half')
ax[1].plot(split_test[0][0],splined_airfoil_1(split_test[0][0]), label='splined 1st')
ax[1].plot(split_test[1][0],splined_airfoil_2(split_test[1][0]), label='splined 1st')
'''

'''plt.plot(split_test[0][0],strain_camber_1)
plt.plot(split_test[1][0]+split_test[0][0][-1]-split_test[0][0][0],strain_camber_2)'''
plt.plot(length, np.flip(strain_camber))
'''plt.plot([x*10**3 for x in experimentDatas[12][0][0]],experimentDatas[12][1][0],'--')
plt.plot([x*10**3 for x in experimentDatas[12][0][1]],experimentDatas[12][1][1],'--')'''
plt.plot([x*10**3 for x in experimentDatas[12][0][2]],experimentDatas[12][1][2],'--')
plt.plot([x*10**3 for x in experimentDatas[12][0][3]],experimentDatas[12][1][3],'--')

plt.plot()


plt.show()

