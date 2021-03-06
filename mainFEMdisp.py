import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from math import atan

def readFile(data_file: str):
    data_file = pd.read_csv(data_file, sep="\t")
    return data_file


def reformatFile(data_file: pd.DataFrame) -> np.ndarray:
    data_file = data_file.to_numpy()
    nr_rows = len(data_file[:, 0])
    data_file_reformat = np.zeros((nr_rows, 7))
    # data_s = str(data_file[50, 0])
    # print((data_s[61:73]))
    for data_file_row in range(nr_rows):
        data_s = str(data_file[data_file_row, 0])
        data_file_reformat[data_file_row, 0] = int(float(data_s[9:17]))
        data_file_reformat[data_file_row, 1] = float(data_s[20:33])
        data_file_reformat[data_file_row, 2] = float(data_s[33:46])
        data_file_reformat[data_file_row, 3] = float(data_s[48:60])
        data_file_reformat[data_file_row, 4] = float(data_s[60:73])
        data_file_reformat[data_file_row, 5] = float(data_s[74:86])
        data_file_reformat[data_file_row, 6] = float(data_s[90:102])

    return data_file_reformat


def nodeDistanceAndOrientation(data_file: np.ndarray):
    nr_rows = len(data_file[:, 0])

    node_distance = np.zeros((nr_rows, 1))
    node_orientation = np.zeros(nr_rows)
    for data_file_row in range(0, nr_rows - 1):
        dx = (data_file[data_file_row + 1, 1] + data_file[data_file_row + 1, 4]) - (
                data_file[data_file_row, 1] + data_file[data_file_row, 4])
        dy = (data_file[data_file_row + 1, 2] + data_file[data_file_row + 1, 5]) - (
                data_file[data_file_row, 2] + data_file[data_file_row, 5])
        node_distance[data_file_row, 0] = np.sqrt(dx ** 2 + dy ** 2)
        node_orientation[data_file_row] = np.arctan(dy/dx)


    return node_distance, node_orientation


def nodeLocation(node_distances: np.ndarray) -> np.ndarray:
    node_location = np.zeros(len(node_distances[:, 0]))
    for index in range(1, len(node_distances)):
        node_location[index] = node_location[index - 1] + node_distances[index]
    return node_location


loadstep1_disp = reformatFile(readFile("Data/FEM/shell_loadstep1_disp.out"))[2:, :] # first two nodes are deleted for weird placement
loadstep2_disp = reformatFile(readFile("Data/FEM/shell_loadstep2_disp.out"))[2:, :]
loadstep3_disp = reformatFile(readFile("Data/FEM/shell_loadstep3_disp.out"))[2:, :]
loadstep4_disp = reformatFile(readFile("Data/FEM/shell_loadstep4_disp.out"))[2:, :]
loadstep5_disp = reformatFile(readFile("Data/FEM/shell_loadstep5_disp.out"))[2:, :]

loadstep1_disp_nodes, loadstep1_node_orientation = nodeDistanceAndOrientation(loadstep1_disp)
loadstep2_disp_nodes, loadstep2_node_orientation = nodeDistanceAndOrientation(loadstep2_disp)
loadstep3_disp_nodes, loadstep3_node_orientation = nodeDistanceAndOrientation(loadstep3_disp)
loadstep4_disp_nodes, loadstep4_node_orientation = nodeDistanceAndOrientation(loadstep4_disp)
loadstep5_disp_nodes, loadstep5_node_orientation = nodeDistanceAndOrientation(loadstep5_disp)

loadstep1_disp_loc = nodeLocation(loadstep1_disp_nodes)
loadstep2_disp_loc = nodeLocation(loadstep2_disp_nodes)
loadstep3_disp_loc = nodeLocation(loadstep3_disp_nodes)
loadstep4_disp_loc = nodeLocation(loadstep4_disp_nodes)
loadstep5_disp_loc = nodeLocation(loadstep5_disp_nodes)

# print(sum(loadstep1_disp_nodes))
# print(sum(loadstep2_disp_nodes))
# print(sum(loadstep3_disp_nodes))
# print(sum(loadstep4_disp_nodes))
#print(sum(loadstep5_disp_nodes))


'''Below plots the leading edge shapes for 5 loadsteps for mm'''

#plt.plot(loadstep1_disp[:, 1] + loadstep1_disp[:, 4], loadstep1_disp[:, 2] + loadstep1_disp[:, 5],
#            label="Loadstep 1")
#plt.plot(loadstep2_disp[:, 1] + loadstep2_disp[:, 4], loadstep2_disp[:, 2] + loadstep2_disp[:, 5],
#            label="Loadstep 2")
#plt.plot(loadstep3_disp[:, 1] + loadstep3_disp[:, 4], loadstep3_disp[:, 2] + loadstep3_disp[:, 5],
#            label="Loadstep 3")
#plt.plot(loadstep4_disp[:, 1] + loadstep4_disp[:, 4], loadstep4_disp[:, 2] + loadstep4_disp[:, 5],
#            label="Loadstep 4")
#plt.plot(loadstep5_disp[:, 1] + loadstep5_disp[:, 4], loadstep5_disp[:, 2] + loadstep5_disp[:, 5],
#            label="Loadstep 5")

#plt.legend()
#plt.show()

loadstep1_coord_x = (loadstep1_disp[:, 1] + loadstep1_disp[:, 4])*1000 #output converted to mm
loadstep1_coord_y = (loadstep1_disp[:, 2] + loadstep1_disp[:, 5])*1000 + 134.28528#shifted up so that leading edge lower side starts at y=0
loadstep2_coord_x = (loadstep2_disp[:, 1] + loadstep2_disp[:, 4])*1000
loadstep2_coord_y = (loadstep2_disp[:, 2] + loadstep2_disp[:, 5])*1000+ 134.28528
loadstep3_coord_x = (loadstep3_disp[:, 1] + loadstep3_disp[:, 4])*1000
loadstep3_coord_y = (loadstep3_disp[:, 2] + loadstep3_disp[:, 5])*1000+ 134.28528
loadstep4_coord_x = (loadstep4_disp[:, 1] + loadstep4_disp[:, 4])*1000
loadstep4_coord_y = (loadstep4_disp[:, 2] + loadstep4_disp[:, 5])*1000+ 134.28528
loadstep5_coord_x = (loadstep5_disp[:, 1] + loadstep5_disp[:, 4])*1000
loadstep5_coord_y = (loadstep5_disp[:, 2] + loadstep5_disp[:, 5])*1000+ 134.28528

plt.xlabel("Position in X direction")
plt.ylabel("Position in Y direction")
#plt.plot(loadstep2_disp[:, 1] + loadstep2_disp[:, 4], loadstep2_disp[:, 2] + loadstep2_disp[:, 5],
#            label="Loadstep 2")
#plt.plot(loadstep3_disp[:, 1] + loadstep3_disp[:, 4], loadstep3_disp[:, 2] + loadstep3_disp[:, 5],
#            label="Loadstep 3")
#plt.plot(loadstep4_disp[:, 1] + loadstep4_disp[:, 4], loadstep4_disp[:, 2] + loadstep4_disp[:, 5],
#            label="Loadstep 4")
#plt.plot(loadstep5_disp[:, 1] + loadstep5_disp[:, 4], loadstep5_disp[:, 2] + loadstep5_disp[:, 5],
#            label="Loadstep 5")

###         COMMENT THIS OUT OR PUT IN MAIN TO AVOID GRAPHS OF DEFLECTIONS SHOWING EVERY TIME.      ###

'''plt.plot(loadstep1_coord_x,loadstep1_coord_y,
            label="Loadstep 1")
plt.plot(loadstep2_coord_x,loadstep2_coord_y,
            label="Loadstep 2")
plt.plot(loadstep3_coord_x,loadstep3_coord_y,
            label="Loadstep 3")
plt.plot(loadstep4_coord_x,loadstep4_coord_y,
            label="Loadstep 4")
plt.plot(loadstep5_coord_x,loadstep5_coord_y,
            label="Loadstep 5")
plt.plot()
plt.plot()
plt.legend()
plt.show()
'''