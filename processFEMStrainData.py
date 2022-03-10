import numpy as np
import pandas as pd

def load_file(file: str, skip_rows: int = None): #to be deleted once the code works
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows, header=None) #header= None part needed to read file properly 
    return data_file

data1 = load_file("Data/FEM/shell_loadstep4_str.out") #call function to insert data
data2 = data1.to_numpy() #convert into numpy arraw with 1 column

for i in data2[0]:
    print (np.shape(data2))


def processFEMStrainData (data2:np.ndarray): #convert into numpy array with several columns
    data3 = np.zeros((np.shape(data1)[0],7))
    for i in range(np.shape(data1)[0]):
        #node number
        data3 [i][0] = data2[i][0][3:8]
        
        #x strain
        data3 [i][1] = data2[i][0][9:21]
        # if data2[i][0][9] == '-':
        #     print('True', data2[i][0][3:8], data2[i][0][10:21]) #wtf it doesn't print the corresponding numberst o eachother
        #     data3 [i][1] = data2[i][0][10:21]

    return data3#:numpy.ndarray
'''

11904 -0.11220E-02-0.20635E-03 0.31551E-04-0.35103E-02 0.44769E-07-0.14782E-06'
'''
print (processFEMStrainData(data2))
#print (data2)