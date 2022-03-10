import numpy as np
import pandas as pd

def load_file(file: str, skip_rows: int = None): #to be deleted once the code works
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows, header=None) #header= None part needed to read file properly 
    return data_file

data1 = load_file("Data/FEM/shell_loadstep4_str.out") #call function to insert data
data2 = data1.to_numpy() #convert into numpy arraw with 1 column

def processFEMStrainData (data2:np.ndarray): #convert into numpy array with several columns
    data3 = np.zeros((np.shape(data1)[0],7))
    for i in range(np.shape(data1)[0]):
        data3 [i] = [data2[i][0][3:8], data2[i][0][9:21], data2[i][0][21:33], data2[i][0][33:45], data2[i][0][45:57], data2[i][0][57:69], data2[i][0][69:81]]
    
    return data3#:numpy.ndarray

print (processFEMStrainData(data2)[0][0])
#print (data2)