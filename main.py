import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob


def load_file(file: str, skip_rows: int = None):
    return pd.read_csv(file, sep="\t", skiprows=skip_rows)


def files_in_directory(folder: str, file_extension: str) -> list:
    return glob.glob(f"Data/{folder}/*.{file_extension}")


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

    print(f"{files_dap=}")
    print(f"{files_es=}")
    print(f"{files_fem=}")
    print(f"{files_md=}")

    print(f"{data=}")
    print(f"{data1=}")


if __name__ == "__main__":
    main()
