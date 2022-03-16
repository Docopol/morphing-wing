import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


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


def nodeDistance(data_file: np.ndarray) -> np.ndarray:
    nr_rows = len(data_file[:, 0])

    node_distance = np.zeros((nr_rows, 1))
    for data_file_row in range(0, nr_rows - 1):
        dx = (data_file[data_file_row + 1, 1] + data_file[data_file_row + 1, 4]) - (
                data_file[data_file_row, 1] + data_file[data_file_row, 4])
        dy = (data_file[data_file_row + 1, 2] + data_file[data_file_row + 1, 5]) - (
                data_file[data_file_row, 2] + data_file[data_file_row, 5])
        node_distance[data_file_row, 0] = np.sqrt(dx ** 2 + dy ** 2)

    return node_distance


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

loadstep1_disp_nodes = nodeDistance(loadstep1_disp)
loadstep2_disp_nodes = nodeDistance(loadstep2_disp)
loadstep3_disp_nodes = nodeDistance(loadstep3_disp)
loadstep4_disp_nodes = nodeDistance(loadstep4_disp)
loadstep5_disp_nodes = nodeDistance(loadstep5_disp)

loadstep1_disp_loc = nodeLocation(loadstep1_disp_nodes)
loadstep2_disp_loc = nodeLocation(loadstep2_disp_nodes)
loadstep3_disp_loc = nodeLocation(loadstep3_disp_nodes)
loadstep4_disp_loc = nodeLocation(loadstep4_disp_nodes)
loadstep5_disp_loc = nodeLocation(loadstep5_disp_nodes)

# print(sum(loadstep1_disp_nodes[2:, 0]))
# print(sum(loadstep2_disp_nodes))
# print(sum(loadstep3_disp_nodes))
# print(sum(loadstep4_disp_nodes))
# print(sum(loadstep5_disp_nodes))

plt.scatter(loadstep1_disp[:, 1] + loadstep1_disp[:, 4], loadstep1_disp[:, 2] + loadstep1_disp[:, 5],
            label="Loadstep 1")
plt.scatter(loadstep2_disp[:, 1] + loadstep2_disp[:, 4], loadstep2_disp[:, 2] + loadstep2_disp[:, 5],
            label="Loadstep 2")
plt.scatter(loadstep3_disp[:, 1] + loadstep3_disp[:, 4], loadstep3_disp[:, 2] + loadstep3_disp[:, 5],
            label="Loadstep 3")
plt.scatter(loadstep4_disp[:, 1] + loadstep4_disp[:, 4], loadstep4_disp[:, 2] + loadstep4_disp[:, 5],
            label="Loadstep 4")
plt.scatter(loadstep5_disp[:, 1] + loadstep5_disp[:, 4], loadstep5_disp[:, 2] + loadstep5_disp[:, 5],
            label="Loadstep 5")

plt.legend()
plt.show()
