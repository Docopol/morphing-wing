import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file = pd.read_csv("Data/ModelData/target_shape.csv")

x_skin = file["x[mm]"][:]
y_skin = file["y[mm]"][:]

x_skin, y_skin = x_skin.to_numpy(), y_skin.to_numpy()
x_skin, y_skin = x_skin - np.min(x_skin), y_skin


coordinates_skin = np.array([x_skin, y_skin])