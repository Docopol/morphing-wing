import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file = pd.read_csv("Data/ModelData/target_shape.csv")

x_skin = (file["x[mm]"][:] * -1) + 496.0
y_skin = file["y[mm]"][:] + 146.0

x_skin, y_skin = x_skin.to_numpy(), y_skin.to_numpy()

coordinates_skin = np.array([x_skin, y_skin])