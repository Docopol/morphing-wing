import numpy as np
import pandas as pd

def load_file(file: str, skip_rows: int = None): #to be deleted once the code works
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows, header=None) #header= None part needed to read file properly 
    return data_file

dataFileNames = ['loadstep1_str', 'loadstep2_str', 'loadstep3_str', 'loadstep4_str', 'loadstep5_str']


exampleDatas = load_file("Data/FEM/shell_loadstep4_str.out") #call function to insert data
exampleDatas = exampleDatas.to_numpy() #convert into numpy arraw with 1 column

def processFEMStrainData (datas:np.ndarray): #convert into numpy array with several columns
    returnedArray = np.zeros((np.shape(datas)[0],7))
    for i in range(np.shape(datas)[0]):
        if i %
        returnedArray [i] = [datas[i,0][3:8], datas[i,0][9:21], datas[i,0][21:33], datas[i,0][33:45], datas[i,0][45:57], datas[i,0][57:69], datas[i,0][69:81]]
    return returnedArray #:numpy.ndarray

'''
strainData1s and strainData2s are numpy arraws with [loadstepnumber - 1] [nodenumber - 11651, data column (node number, x, y, z, xy, yz, zx)]
e.g. strainData1s [2][:,2] -> gives the y strain data from data set 1 for the 3rd loadstep 
'''

strainData1s = np.zeros((5,int(np.shape(exampleDatas)[0]/2),7))
strainData2s = np.zeros((5,int(np.shape(exampleDatas)[0]/2),7))

for i in dataFileNames:
    importedDatas = load_file("Data/FEM/shell_"+i+".out")
    importedDatas = importedDatas.to_numpy()
    processFEMStrainData (importedDatas)
    print(importedDatas)

#print (data2)