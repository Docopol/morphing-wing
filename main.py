import platform

import utils


def main():
    """
    Main
    """
    files_dap = utils.filereader.files_in_directory("DispAndForce", "txt")
    files_es = utils.filereader.files_in_directory("Experimental strains", "txt")
    files_fem = utils.filereader.files_in_directory("FEM", "out")
    files_md = utils.filereader.files_in_directory("ModelData", "txt")
    files_img_bmp = utils.filereader.files_in_directory("Images (BMP) - FOR IMAGE CALIBRATION ONLY", "bmp")

    data = utils.filereader.load_file("Data/DispAndForce/CurentVoltageReading3.txt")
    data1 = utils.filereader.load_file("Data/Experimental strains/Measurements2014_05_22.txt", 4)

    print(f"{files_dap}")
    print(f"{files_es}")
    print(f"{files_fem}")
    print(f"{files_md}")
    print(f"{files_img_bmp}")

    print(f"{data}")
    print(f"{data1}")
    

if __name__ == "__main__":
    version = platform.python_version_tuple()
    if int(version[0]) < 3:
        raise Exception(f"Must be using Python +3.7. Current version Python {version[0]}.{version[1]}.{version[2]}")
    if int(version[1]) < 7:
        raise Exception(f"Must be using Python +3.7. Current version Python {version[0]}.{version[1]}.{version[2]}")
    main()
