import matplotlib.pyplot as plt
import pandas as pd

file = pd.read_csv("Data/ModelData/target_shape.csv")

print(file["x[mm]"][:])
x_skin = file["x[mm]"][::-1]
y_skin = file["y[mm]"][:]

plt.plot(x_skin, y_skin)
plt.show()