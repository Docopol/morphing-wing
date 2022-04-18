import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate


def f3(x: np.ndarray):
    y = (x - 0.3) / ((1.75 - 0.3) / (2500 - 0))
    return y


# def f5(x):
#     y = (x - 0.4) / ((3.9 - 0.4) / (1800 - 0))
#     return y
# def f6(x):
#     y = (x - 0.4) / ((3.55 - 0.4) / (1500 - 0))
#     return y
# def f9(x):
#     y = (x - 0.4) / ((1.85 - 0.4) / (1200 - 0))
#     return y
# def f12(x):
#     y = (x - 0.3) / ((1.8 - 0.3) / (850 - 0))
#     return y


def readFile(data_file: str):
    data_file = pd.read_csv(data_file, sep=",")
    return data_file


data_real = [readFile("Data/DispAndForce/Dis1.csv"), readFile("Data/DispAndForce/Dis2.csv"),
             readFile("Data/DispAndForce/Dis3.csv"), readFile("Data/DispAndForce/Dis4.csv")]

calibration_data = [readFile("Data/DispAndForce/CurrentSensorCalibration3.csv"),
                    readFile("Data/DispAndForce/CurentVoltageReading3.csv"),
                    readFile("Data/DispAndForce/femForceDisplacement.csv")]

# ____Calculate the displacement of the actuator in mm
actuator_disp = []
for index_dis in range(len(data_real[:])):
    actuator_disp.append(10 * data_real[index_dis]["Voltage power source [V]"][:] / 2)

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

# order data
all_data = []
for index_dis_csv in range(len(data_real[:])):

    all_data_i = np.zeros((len(data_real[index_dis_csv]["Time [s]"][:]), 7))
    for index_total in range(len(data_real[index_dis_csv]["Time [s]"][:])):
        all_data_i[index_total, 0] = data_real[index_dis_csv]["Time [s]"][index_total] - \
                                     data_real[index_dis_csv]["Time [s]"][0]
        all_data_i[index_total, 1] = actuator_disp[index_dis_csv][index_total]
        all_data_i[index_total, 2] = f3(current_real[index_dis_csv][index_total, 1])
        all_data_i[index_total, 3] = current_real[index_dis_csv][index_total, 1]
        all_data_i[index_total, 4] = data_real[index_dis_csv]["Voltage power source [V]"][index_total]
        all_data_i[index_total, 5] = data_real[index_dis_csv]["Voltage current sensor [V]"][index_total]
        # all_data_i[index_total, 3] = f5(current_real[index_dis_csv][index_total, 1])
        # all_data_i[index_total, 4] = f6(current_real[index_dis_csv][index_total, 1])
        # all_data_i[index_total, 5] = f9(current_real[index_dis_csv][index_total, 1])
        # all_data_i[index_total, 6] = f12(current_real[index_dis_csv][index_total, 1])
    all_data.append(all_data_i)



# find relation between current sensor voltage and current

# interpolate so that power source voltage = f(current sensor voltage)
interp_list_voltages_real = []
for disp_index in range(4):
    psv_real_interp = scipy.interpolate.interp1d(all_data[disp_index][:, 5], all_data[disp_index][:, 4],
                                                 fill_value='extrapolate')
    interp_list_voltages_real.append(psv_real_interp)

# interpolate so that power source voltage = f(current sensor voltage) but now for SensorCalibration3
interp_list_voltages_cal = []
for disp_index in range(4):
    psv_real_interp_cal = scipy.interpolate.interp1d(calibration_data[:, 2], calibration_data[:, 1],
                                                 fill_value='extrapolate')
    interp_list_voltages_cal.append(psv_real_interp_cal)



# print(max(all_data[2][:, 2]))
# print(all_data[2][:, 1])

# ____put plots below____

# for index3 in range(4):
#     plt.xlabel("Time [s]")
#     plt.ylabel("Displacement [mm]")
#     label = ["Target: 10 mm", "Target: 20 mm", "Target: 30 mm", "Target: 39.2 mm"]
#     plt.plot(all_data[index3][:, 0], all_data[index3][:, 1], label = label[index3])
#     plt.legend()
#
# plt.show()


# plt.xlabel("Time [s]")
# plt.ylabel("Voltage power source [V]")
# plt.plot(calibration_data[0]["Time [s]"][:], calibration_data[0]["Voltage power source [V]"][:])
# plt.show()


# for index4 in range(4):
#     plt.xlabel("Time [s]")
#     plt.ylabel("Current [mm]")
#     label = ["Target: 10 mm", "Target: 20 mm", "Target: 30 mm", "Target: 39.2 mm"]
#     plt.plot(all_data[index4][:, 0], all_data[index4][:, 3], label = label[index4])
#     plt.legend()
#
# plt.show()


# plt.xlabel("Time [s]")
# plt.ylabel("Force [N]")

# for index5 in range(4):
#     plt.plot(all_data[index5][:, 0], all_data[index5][:, 2])
#
# plt.scatter([3.6, 6.0, 8.3, 10.4], calibration_data[2]["Actuation force [N]"][:], label="FEM data")
# plt.legend()
# plt.show()

for index3 in range(4):
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage current sensor [V]")
    label = ["Target: 10 mm", "Target: 20 mm", "Target: 30 mm", "Target: 39.2 mm"]
    plt.plot(all_data[index3][:, 0], all_data[index3][:, 5], label=label[index3])
    plt.legend()

plt.show()
