import pandas as pd
import numpy as np
import main
import matplotlib.pyplot as plt
import processFEMStrainData
import mainFEMdisp


'''
femStrainData1s and femStrainData2s are numpy arrays with [loadstepnumber - 1] [nodenumber - 11651, data column (node number, x, y, z, xy, yz, zx)]
e.g. strainData1s [2][:,2] -> gives the y strain data from data set 1 for the 3rd loadstep 
- Ask Mick if confused
'''
femStrainData1s = processFEMStrainData.strainData1s
femStrainData2s = processFEMStrainData.strainData2s

loadstep1_disp_loc = mainFEMdisp.loadstep1_disp_loc
loadstep2_disp_loc = mainFEMdisp.loadstep2_disp_loc
loadstep3_disp_loc = mainFEMdisp.loadstep3_disp_loc
loadstep4_disp_loc = mainFEMdisp.loadstep4_disp_loc
loadstep5_disp_loc = mainFEMdisp.loadstep5_disp_loc

loadstep1_node_orientation = mainFEMdisp.loadstep1_node_orientation
loadstep2_node_orientation = mainFEMdisp.loadstep2_node_orientation
loadstep3_node_orientation = mainFEMdisp.loadstep3_node_orientation
loadstep4_node_orientation = mainFEMdisp.loadstep4_node_orientation
loadstep5_node_orientation = mainFEMdisp.loadstep5_node_orientation

# ____Plot the the orientations for each node___
# plt.plot(loadstep1_disp_loc, loadstep1_node_orientation)
# plt.plot(loadstep2_disp_loc, loadstep2_node_orientation)
# plt.plot(loadstep3_disp_loc, loadstep3_node_orientation)
# plt.plot(loadstep4_disp_loc, loadstep4_node_orientation)
# plt.plot(loadstep5_disp_loc, loadstep5_node_orientation)
# plt.show()

print(loadstep1_node_orientation)

def load_file(file: str, skip_rows: int = None):
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows)
    return data_file

data2 = load_file("Data/FEM/shell_loadstep3_str.out")
data2 = pd.DataFrame(data2).to_numpy()

# print(data2)




#expData = np.genfromtxt("Data/Experimental Strains/Measurements2014_05_22.csv", delimiter=',')
expData = pd.DataFrame(load_file("Data/Experimental Strains/Measurements2014_05_22.csv")).to_numpy
# print(expData)


'''
v v make graphs v v
'''
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

# strain data 1
plt.subplot(2, 2, 1)
plt.plot(loadstep1_disp_loc, femStrainData1s[1-1][2:, 4], label = "loadstep 1.1")
plt.plot(loadstep2_disp_loc, femStrainData1s[2-1][2:, 4], label = "loadstep 2.1")
plt.plot(loadstep3_disp_loc, femStrainData1s[3-1][2:, 4], label = "loadstep 3.1")
plt.plot(loadstep4_disp_loc, femStrainData1s[4-1][2:, 4], label = "loadstep 4.1")
plt.plot(loadstep5_disp_loc, femStrainData1s[5-1][2:, 4], label = "loadstep 5.1")
plt.legend()


# strain data 2
plt.subplot(2,2,2)
plt.plot(loadstep1_disp_loc, femStrainData2s[1-1][2:, 4], label = "loadstep 1.2")
plt.plot(loadstep2_disp_loc, femStrainData2s[2-1][2:, 4], label = "loadstep 2.2")
plt.plot(loadstep3_disp_loc, femStrainData2s[3-1][2:, 4], label = "loadstep 3.2")
plt.plot(loadstep4_disp_loc, femStrainData2s[4-1][2:, 4], label = "loadstep 4.2")
plt.plot(loadstep5_disp_loc, femStrainData2s[5-1][2:, 4], label = "loadstep 5.2")
plt.legend()

# strain data difference of data 1 and 2
plt.subplot(2,2,3)
plt.plot(loadstep1_disp_loc, abs(abs(femStrainData1s[1-1][2:, 4])-femStrainData2s[1-1][2:, 4]), label = "loadstep 1")
plt.plot(loadstep2_disp_loc, abs(femStrainData1s[2-1][2:, 4]-femStrainData2s[2-1][2:, 4]), label = "loadstep 2")
plt.plot(loadstep3_disp_loc, abs(femStrainData1s[3-1][2:, 4]-femStrainData2s[3-1][2:, 4]), label = "loadstep 3")
plt.plot(loadstep4_disp_loc, abs(femStrainData1s[4-1][2:, 4]-femStrainData2s[4-1][2:, 4]), label = "loadstep 4")
plt.plot(loadstep5_disp_loc, abs(femStrainData1s[5-1][2:, 4]-femStrainData2s[5-1][2:, 4]), label = "loadstep 5")
plt.legend()
plt.show()



# FEM vs experimental data
ax[1,0].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')
ax[1,0].plot(x1, y2, linewidth=2.0, label = 'cos',  color = 'blue' ) 

ax[1,0].set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

ax[1,0].legend(['sin','cos'])


#asymmetry over time (optional)
ax[1,1].plot(x1, y2, linewidth=2.0, label = 'cos', color = 'blue')


ax[1,1].set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))


plt.show()
