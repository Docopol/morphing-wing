import pandas as pd
import numpy as np

def load_file(file: str, skip_rows: int = None):
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows)
    return data_file


'''
data2 = load_file("Data/FEM/shell_loadstep3_str.out")
data2 = pd.DataFrame(data2).to_numpy()

print(data2)

'''
#expData = np.genfromtxt("Data/Experimental Strains/Measurements2014_05_22.csv", delimiter=',')
expData = pd.DataFrame(load_file("Data/Experimental Strains/Measurements2014_05_22.csv")).to_numpy
print(expData)