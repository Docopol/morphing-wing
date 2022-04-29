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

error_data = readFile("Data/DispAndForce/error.csv")

avg_error_data = np.array([[np.average(error_data["Voltage power source [V]"][0:7]),
                            np.average(error_data["Voltage current sensor [V]"][0:7])],
                           [np.average(error_data["Voltage power source [V]"][7:14]),
                            np.average(error_data["Voltage current sensor [V]"][7:14])],
                           [np.average(error_data["Voltage power source [V]"][14:25]),
                            np.average(error_data["Voltage current sensor [V]"][14:25])],
                           [np.average(error_data["Voltage power source [V]"][25:33]),
                            np.average(error_data["Voltage current sensor [V]"][25:33])],
                           [np.average(error_data["Voltage power source [V]"][33:44]),
                            np.average(error_data["Voltage current sensor [V]"][33:44])],
                           ])
print(avg_error_data)

index_start_data = [7, 7, 10, 8, 10]  # dis1, dis2, dis3, dis4, csc3

# ____Calculate the displacement of the actuator in mm
actuator_disp = []
for index_dis in range(len(data_real[:])):
    actuator_disp.append(10 * (data_real[index_dis]["Voltage power source [V]"][:] ) / 2)

# ____Calculate the current with the real power source voltages and the calibrationVoltageReadings3


current_real = []

# interpolate so that you get a function Current Power source = f(Voltage Power Source)
current_real_interpolation = scipy.interpolate.interp1d(calibration_data[1]["Voltage power source [V]"][:],
                                                        calibration_data[1]["Current power source [A]"][:],
                                                        fill_value='extrapolate')
for h in range(len(data_real[:])):
    current_x = np.zeros((len(data_real[h]["Voltage power source [V]"][:]), 2))
    for i in range(len(data_real[h]["Voltage power source [V]"][:])):
        current_x[i, 0] = data_real[h]["Time [s]"][i]
        current_x[i, 1] = current_real_interpolation(data_real[h]["Voltage power source [V]"][i] )
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


# interpolate so that real power source voltage = f(current sensor voltage)

psv_real_interp10 = scipy.interpolate.interp1d(all_data[0][:, 5], all_data[0][:, 4],
                                               fill_value='extrapolate')
psv_real_interp20 = scipy.interpolate.interp1d(all_data[1][:, 5], all_data[1][:, 4],
                                               fill_value='extrapolate')
psv_real_interp30 = scipy.interpolate.interp1d(all_data[2][:, 5], all_data[2][:, 4],
                                               fill_value='extrapolate')
psv_real_interp392 = scipy.interpolate.interp1d(all_data[3][:, 5], all_data[3][:, 4],
                                                fill_value='extrapolate')

# interpolate so that calibration voltage current sensor = f(Time) but now for SensorCalibration3
vcs_vs_time_interp_cal = scipy.interpolate.interp1d(calibration_data[0]["Time [s]"][:],
                                                    calibration_data[0]["Voltage current sensor [V]"][:],
                                                    fill_value='extrapolate')

# interpolate so that calibration voltage current sensor = f(Time) but now for SensorCalibration3
psv_vs_time_interp_cal = scipy.interpolate.interp1d(calibration_data[0]["Time [s]"][:],
                                                    calibration_data[0]["Voltage power source [V]"][:],
                                                    fill_value='extrapolate')

# interpolate so that calibration power source voltage = f(current sensor voltage) but now for SensorCalibration3
psv_interp_cal = scipy.interpolate.interp1d(calibration_data[0]["Voltage current sensor [V]"][:],
                                            calibration_data[0]["Voltage power source [V]"][:],
                                            fill_value='extrapolate')

# Get the values of the csc3 voltages for time of Disp files
time_vs_current_disp = []
for disp_index in range(4):
    time_vs_current = np.zeros((len(data_real[disp_index]["Time [s]"]), 2))
    for time_index in range(len(data_real[disp_index]["Time [s]"])):
        time_vs_current[time_index, 0] = data_real[disp_index]["Time [s]"][time_index] - \
                                         data_real[disp_index]["Time [s]"][0]  # time column

        time_vs_current[time_index, 1] = current_real_interpolation(psv_interp_cal(data_real[disp_index]
                                                                                   ["Voltage current sensor [V]"][
                                                                                       time_index]))  # current column

    time_vs_current_disp.append(time_vs_current)

# ____put plots below____

# DELIVERABLE 1: displacement vs time plot FINISHED!!!!!!!!!!
lineshape = ['dashed', 'dotted', 'dashdot', 'solid']
colors_rgb = ['blue', 'orange', 'red', 'green']
markers = ['o', '+', 's', '*']

for index3 in range(4):
    plt.xlabel("Time [s]")
    plt.ylabel("Displacement [mm]")
    label = ["Target: 10 mm", "Target: 20 mm", "Target: 30 mm", "Target: 39.2 mm"]
    plt.plot(all_data[index3][:, 0], all_data[index3][:, 1], linestyle=lineshape[index3], label=label[index3],
             color=colors_rgb[index3])
    plt.legend()

plt.show()

# DELIVERABLE 2: force time plot FINISHED!!!!!!!!!!!!
plt.xlabel("Time [s]")
plt.ylabel("Force [N]")
plt.scatter([2.915, 5.4, 7.75, 10], calibration_data[2]["Actuation force [N]"][:], label="FEM data")

print(min(f3(time_vs_current_disp[3][:, 1])))

for index3 in range(4):
    label = ["Target: 10 mm", "Target: 20 mm", "Target: 30 mm", "Target: 39.2 mm"]
    plt.plot(time_vs_current_disp[index3][:, 0],
             f3(time_vs_current_disp[index3][:, 1]) - min(f3(time_vs_current_disp[index3][:, 1])),
             linestyle=lineshape[index3], label=label[index3], color=colors_rgb[index3])

plt.legend()
plt.show()
