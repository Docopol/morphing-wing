import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import platform
import glob
import time


def load_file(file: str, skip_rows: int = None):
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows)
    headers = list(data_file.columns.values)
    for index, header in enumerate(headers):
        if "-----" in header:
            data_file.rename(columns={header: 'Timestamp[t]'}, errors='raise', inplace=True)
    return data_file


def files_in_directory(folder: str, file_extension: str) -> list:
    return glob.glob(f"Data/{folder}/*.{file_extension}")


def perftimer(func):
    """
    A timer decorator to time to runtime of a function
    add @perftimer above a function to make use of it.
    output is string in seconds
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        outcome = func(*args, **kwargs)
        stop = time.time() - start
        print(f"--- Process {func.__name__} ran in: {stop}s ---")
        return outcome
    return wrapper


class Plotter:

    def __init__(self, x, y, x_label, y_label, legend_labels=None) -> None:
        if any(isinstance(i, list) for i in x):
            self.x = x
            self.y = y
        if any(isinstance(i, pd.DataFrame) for i in x):
            self.x = x
            self.y = y
        if any(isinstance(i, pd.Series) for i in x):
            self.x = x
            self.y = y
        else:
            self.x = [x]
            self.y = [y]
        self.x_label = str(x_label)
        self.y_label = str(y_label)
        if legend_labels:
            self.legend = legend_labels
        else:
            self.legend = [None] * 2

    def plotgraphs(self):
        for i, j, k in zip(self.x, self.y, self.legend):
            print("loop")
            if len(i) != len(j):
                raise Exception(f"Can't create graph, with irregular points ({len(i)}x{len(j)})")
            if k:
                plt.plot(i, j, label=self.legend)
            else:
                plt.plot(i, j)
        plt.ylabel(self.y_label)
        plt.xlabel(self.x_label)
        if None not in self.legend:
            plt.legend()
        plt.show()

    @classmethod
    def commaformat(cls,):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass


@perftimer
def main():
    """
    Main
    """
    files_dap = files_in_directory("DispAndForce", "txt")
    files_es = files_in_directory("Experimental strains", "txt")
    files_fem = files_in_directory("FEM", "out")
    files_md = files_in_directory("ModelData", "txt")

    data = load_file("Data/DispAndForce/CurentVoltageReading3.txt")
    data1 = load_file("Data/Experimental strains/Measurements2014_05_22.txt", 4)

    print(f"{files_dap}")
    print(f"{files_es}")
    print(f"{files_fem}")
    print(f"{files_md}")

    print(f"{data}")
    print(f"{data1}")

    file = pd.read_csv("Data/ModelData/target_shape.csv")
    file2 = pd.read_csv("Data/ModelData/target_shape.csv")
    a = [file["x[mm]"], file2["y[mm]"]]
    b = [file["y[mm]"], file2["x[mm]"]]
    a = [1,2,3]
    b = [1,2,3]

    plot = Plotter(a,b,"x","y")
    plot.plotgraphs()
    print(plot.__dict__)
    # print(plot.x[0])
    # print("----")
    # print(plot.x[1])


if __name__ == "__main__":
    version = platform.python_version_tuple()
    if int(version[0]) < 3:
        raise Exception(f"Must be using Python +3.7. Current version Python {version[0]}.{version[1]}.{version[2]}")
    if int(version[1]) < 7:
        raise Exception(f"Must be using Python +3.7. Current version Python {version[0]}.{version[1]}.{version[2]}")
    main()
