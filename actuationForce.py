import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def readFile(data_file: str):
    data_file = pd.read_csv(data_file, sep=",")
    return data_file


cur_vol_res = [readFile("Data/DispAndForce/Dis1.csv"), readFile("Data/DispAndForce/Dis2.csv"),
               readFile("Data/DispAndForce/Dis3.csv"), readFile("Data/DispAndForce/Dis4.csv")]

calibration_data = [readFile("Data/DispAndForce/CurrentSensorCalibration3.csv"),
                    readFile("Data/DispAndForce/CurentVoltageReading3.csv")]




actuator_disp = []
print(len(cur_vol_res[:]))
for index_dis in range(len(cur_vol_res[:])):
    actuator_disp.append(cur_vol_res[index_dis]["Voltage power source [V]"][:]/2)


print(actuator_disp)
plt.plot(cur_vol_res[2]["Time [s]"][:], actuator_disp[2])
plt.show()
# print(actuator_disp)


# plt.plot(calibration_data[1]["Current power source [A]"][:], calibration_data[1]["Voltage power source [V]"][:])
# plt.show()