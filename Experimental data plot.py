import pandas as pd
import matplotlib.pyplot as plt

data_load_step1 = pd.read_csv("Data/FEM/shell_loadstep1_disp.out", sep="\t")
print(data_load_step1)