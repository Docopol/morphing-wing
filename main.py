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


if __name__ == "__main__":
    version = platform.python_version_tuple()
    if int(version[0]) < 3:
        raise Exception(f"Must be using Python +3.7. Current version Python {version[0]}.{version[1]}.{version[2]}")
    if int(version[1]) < 7:
        raise Exception(f"Must be using Python +3.7. Current version Python {version[0]}.{version[1]}.{version[2]}")
    main()
