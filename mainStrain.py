import pandas as pd
import numpy as np
import main
import pandas as pd
import matplotlib.pyplot as plt
import processFEMStrainData 


'''
femStrainData1s and femStrainData2s are numpy arrays with [loadstepnumber - 1] [nodenumber - 11651, data column (node number, x, y, z, xy, yz, zx)]
e.g. strainData1s [2][:,2] -> gives the y strain data from data set 1 for the 3rd loadstep 
- Ask Mick if confused
'''
femStrainData1s = processFEMStrainData.strainData1s
femStrainData2s = processFEMStrainData.strainData2s



'''
v v make graphs v v
'''
# symmetry (bending analysis), FEm vs experimental, time vs asymetry (optional)
fig, ax = plt.subplots(2,2)

# symmetry analyis plot FEM
ax[0,0].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')

ax[0,0].set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

ax[0,0].set_title('Bending Analyis FEM')

# symmetry analyis plot Experiment
ax[0,1].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')

ax[0,1].set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

ax[0,1].set_title('Bending Analyis Experiment')

# FEM vs experimental data
ax[1,0].plot(x1, y1, linewidth=2.0, label = 'sin', color = 'orange')
ax[1,0].plot(x1, y2, linewidth=2.0, label = 'cos',  color = 'blue' ) 

#ax[1,0].set(xlim=(0, 8), xticks=np.arange(1, 8), ylim=(0, 8), yticks=np.arange(1, 8))

ax[1,0].legend(['FEM','Experiment'])

ax[1,0].set_title('FEM vs experimental analysis')

#asymmetry over time (optional)
ax[1,1].plot(x1, y2, linewidth=2.0, label = 'cos', color = 'blue')

ax[1,1].set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

ax[1,2].set_title('Bending Analyis over Time Experiment')


plt.show()
