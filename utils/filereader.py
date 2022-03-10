import pandas as pd
import glob


def load_file(file: str, skip_rows: int = None):
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows)
    headers = list(data_file.columns.values)
    for index, header in enumerate(headers):
        if "-----" in header:
            data_file.rename(columns={header: 'Timestamp[t]'}, errors='raise', inplace=True)
    return data_file


def files_in_directory(folder: str, file_extension: str) -> list:
    return glob.glob(f"Data/{folder}/*.{file_extension}")