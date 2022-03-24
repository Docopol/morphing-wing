import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate

def f3(x):
    y = (1.75 - 0.3) / (2500 - 0) * x + 0.3


def f5(x):
    y = (3.9 - 0.4) / (1800 - 0) * x + 0.4


def f6(x):
    y = (3.55 - 0.4) / (1500 - 0) * x + 0.4


def f9(x):
    y = (1.85 - 0.4) / (1200 - 0) * x + 0.4


def f12(x):
    y = (1.8 - 0.3) / (850 - 0) * x + 0.3


def readFile(data_file: str):
    data_file = pd.read_csv(data_file, sep=",")
    return data_file


data_real = [readFile("Data/DispAndForce/Dis1.csv"), readFile("Data/DispAndForce/Dis2.csv"),
             readFile("Data/DispAndForce/Dis3.csv"), readFile("Data/DispAndForce/Dis4.csv")]

calibration_data = [readFile("Data/DispAndForce/CurrentSensorCalibration3.csv"),
                    readFile("Data/DispAndForce/CurentVoltageReading3.csv")]

# ____Calculate the displacement of the actuator
actuator_disp = []
for index_dis in range(len(data_real[:])):
    actuator_disp.append(data_real[index_dis]["Voltage power source [V]"][:] / 2)

# ____Calculate the current with the real power source voltages and the calibrationVoltageReadings3
current_real = []

current_real_interpolation = scipy.interpolate.interp1d(calibration_data[1]["Voltage power source [V]"][:],
                                                        calibration_data[1]["Current power source [A]"][:],
                                                        fill_value='extrapolate')
for h in range(len(data_real[:])):
    current_x = np.zeros((len(data_real[h]["Voltage power source [V]"][:]), 2))
    for i in range(len(data_real[h]["Voltage power source [V]"][:])):
        current_x[i, 0] = data_real[h]["Time [s]"][i]
        current_x[i, 1] = current_real_interpolation(data_real[h]["Voltage power source [V]"][i])
    current_real.append(current_x)  # current_real is a 4xix2 matrix with time and current on the axis

print(current_real)


# ____Calculate the real force






# ____put plots below____
# plt.plot(data_real[2]["Time [s]"][:], actuator_disp[2])
# plt.show()

# plt.plot(calibration_data[1]["Current power source [A]"][:], calibration_data[1]["Voltage power source [V]"][:])
# plt.show()
