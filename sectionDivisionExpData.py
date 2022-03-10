import numpy as np
import pandas as pd
'''
Takes the unprocessed panda dataframe of experimental data.
Turns into a numpy array. Assumes it has 
Divides it into the four main sections as numpy arrays.
'''

def load_file(file: str, skip_rows: int = None):
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows)
    return data_file
expData = pd.DataFrame(load_file("Data/Experimental Strains/Measurements2014_05_22.csv"))

def divideExpData(expData):
    expData = pd.DataFrame(expData).to_numpy()
    expData = np.vsplit(expData, 4263)
    print(expData)

divideExpData(expData)