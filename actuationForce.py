import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate


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
# len_h = len(data_real[:])
# len_i = len(data_real[1]["Voltage power source [V]"][:])
# len_j = len(calibration_data[1]["Voltage power source [V]"][:])
# print(len_h)
# print(len_i)
# print(len_j)
# delta_list = [0.06, 0.05, 0.05, 0.05]
# for h in range(len_h):
#     current_x = np.zeros(len(data_real[h]["Voltage power source [V]"][:]))
#     for i in range(len(data_real[h]["Voltage power source [V]"][:])):
#         for j in range(len_j):
#             vps_real = data_real[h]["Voltage power source [V]"][i]
#             vps_cal = calibration_data[1]["Voltage power source [V]"][j]
#             delta_vps = abs(vps_real - vps_cal)
#
#             if delta_vps < delta_list[h]:
#                 current_x[i] = calibration_data[1]["Current power source [A]"][j]
#
#     current_real.append(current_x)



current_real_interpolation = scipy.interpolate.interp1d(calibration_data[1]["Voltage power source [V]"][:],
                                      calibration_data[1]["Current power source [A]"][:], fill_value='extrapolate')
print(current_real_interpolation(0.0142))


for h in range(len(data_real[:])):
    current_x = np.zeros((len(data_real[h]["Voltage power source [V]"][:]), 2))
    for i in range(len(data_real[h]["Voltage power source [V]"][:])):
        current_x[i, 0] = data_real[h]["Time [s]"][i]
        current_x[i, 1] = current_real_interpolation(data_real[h]["Voltage power source [V]"][i])
    current_real.append(current_x)      # current_real is a 4xix2 matrix

print(current_real)


# ____put plots below____
# plt.plot(data_real[2]["Time [s]"][:], actuator_disp[2])
# plt.show()

# plt.plot(calibration_data[1]["Current power source [A]"][:], calibration_data[1]["Voltage power source [V]"][:])
# plt.show()
