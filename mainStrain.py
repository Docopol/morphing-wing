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



def load_file(file: str, skip_rows: int = None):
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows)
    return data_file

data2 = load_file("Data/FEM/shell_loadstep3_str.out")
data2 = pd.DataFrame(data2).to_numpy()

print(data2)



#expData = np.genfromtxt("Data/Experimental Strains/Measurements2014_05_22.csv", delimiter=',')
expData = pd.DataFrame(load_file("Data/Experimental Strains/Measurements2014_05_22.csv")).to_numpy
print(expData)
