import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate


def f3(x: np.ndarray):
    y = (x - 0.3) / ((1.75 - 0.3) / (2500 - 0))
    return y


def f5(x):
    y = (x - 0.4) / ((3.9 - 0.4) / (1800 - 0))
    return y


def f6(x):
    y = (x - 0.4) / ((3.55 - 0.4) / (1500 - 0))
    return y


def f9(x):
    y = (x - 0.4) / ((1.85 - 0.4) / (1200 - 0))
    return y


def f12(x):
    y = (x - 0.3) / ((1.8 - 0.3) / (850 - 0))
    return y


def readFile(data_file: str):
    data_file = pd.read_csv(data_file, sep=",")
    return data_file


data_real = [readFile("Data/DispAndForce/Dis1.csv"), readFile("Data/DispAndForce/Dis2.csv"),
             readFile("Data/DispAndForce/Dis3.csv"), readFile("Data/DispAndForce/Dis4.csv")]

calibration_data = [readFile("Data/DispAndForce/CurrentSensorCalibration3.csv"),
                    readFile("Data/DispAndForce/CurentVoltageReading3.csv")]

# ____Calculate the displacement of the actuator in mm
actuator_disp = []
for index_dis in range(len(data_real[:])):
    actuator_disp.append(10*data_real[index_dis]["Voltage power source [V]"][:] / 2)


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

# ____Calculate the real force
# force_real = [[f3(current_real[0][:, 1]), f5(current_real[0][:, 1]), f6(current_real[0][:, 1]),
#                     f9(current_real[0][:, 1]), f12(current_real[0][:, 1])],
#
#                    [f3(current_real[1][:, 1]), f5(current_real[1][:, 1]),
#                     f6(current_real[1][:, 1]),
#                     f9(current_real[1][:, 1]),
#                     f12(current_real[1][:, 1])],
#
#                    [f3(current_real[2][:, 1]), f5(current_real[2][:, 1]),
#                     f6(current_real[2][:, 1]), f9(current_real[2][:, 1]),
#                     f12(current_real[2][:, 1])],
#
#                    [f3(current_real[3][:, 1]), f5(current_real[3][:, 1]),
#                     f6(current_real[3][:, 1]), f9(current_real[3][:, 1]),
#                     f12(current_real[3][:, 1])]]

# The forc_real_dis gives the forces for each disX.csv for each pitch function fi(). It is an array with arrays with
# arrays; if you want the force for the displacements of Dis1 for pitch functin f5 you say force_real[0][1][:]

# interpolate the given fem force-displacement
fem_force_csv = readFile("Data/DispAndForce/femForceDisplacement.csv")
fem_force_interpolation = scipy.interpolate.interp1d(fem_force_csv["Displacement [mm]"][:],
                                                        fem_force_csv["Actuation force [N]"][:],
                                                        fill_value='extrapolate')

# fem_force = [fem_force_interpolation(actuator_disp[0]), fem_force_interpolation(actuator_disp[1]),
#                           fem_force_interpolation(actuator_disp[2]), fem_force_interpolation(actuator_disp[3])]


# order data
all_data = []
for index_dis_csv in range(len(data_real[:])):

    all_data_i = np.zeros((len(data_real[index_dis_csv]["Time [s]"][:]), 8))
    for index_total in range(len(data_real[index_dis_csv]["Time [s]"][:])):
        all_data_i[index_total, 0] = data_real[index_dis_csv]["Time [s]"][index_total]-data_real[index_dis_csv]["Time [s]"][0]
        all_data_i[index_total, 1] = actuator_disp[index_dis_csv][index_total]
        all_data_i[index_total, 2] = f3(current_real[index_dis_csv][index_total, 1])
        # all_data_i[index_total, 3] = f5(current_real[index_dis_csv][index_total, 1])
        # all_data_i[index_total, 4] = f6(current_real[index_dis_csv][index_total, 1])
        # all_data_i[index_total, 5] = f9(current_real[index_dis_csv][index_total, 1])
        # all_data_i[index_total, 6] = f12(current_real[index_dis_csv][index_total, 1])
        # all_data_i[index_total, 7] = fem_force_interpolation(actuator_disp[index_dis_csv][index_total])
    all_data.append(all_data_i)


# ____put plots below____
# plt.plot(data_real[2]["Time [s]"][:], actuator_disp[2])
# plt.show()

# plt.plot(calibration_data[1]["Current power source [A]"][:], calibration_data[1]["Voltage power source [V]"][:])
# plt.show()


# for index1 in range(4):
#
#     for index2 in range(1):
#         f = plt.figure()
#         plt.scatter(fem_force_csv["Displacement [mm]"][:], fem_force_csv["Actuation force [N]"][:], label = "FEM")
#         plt.plot(all_data[index1][:, 1], all_data[index1][:, index2+2], label = "Experimental")
#         plt.xlabel("Displacement [mm]")
#         plt.ylabel("Force [N]")
#         plt.legend()
#         plt.title("Dis"+str(index1+1) + "-" + "Pitch " + str(index2+1))
#         # filename = "Data/DispAndForce/FEM_Experimental_forces/" + "Dis" +str(index1+1) + "-" + "Pitch " + str(index2+1)+ ".png"
#         # f.savefig(filename, bbox_inches='tight')
#         plt.show()

for index3 in range(4):
    plt.plot(all_data[index3][:, 0], all_data[index3][:, 1], label = "Experimental")

# plt.scatter()
plt.show()

for index4 in range(4):
    plt.plot(all_data[index4][:, 0], all_data[index4][:, 2])

plt.show()