import pandas as pd
import glob


def load_file(file: str, separator="\t", skip_last: bool = None, skip_rows: int = None):
    data_file = pd.read_csv(file, sep=separator, skiprows=skip_rows)
    headers = list(data_file.columns.values)

    if skip_last:
        data_file.drop(data_file.columns[len(data_file.columns) - 1], axis=1, inplace=True)

    for index, header in enumerate(headers):
        if "-----" in header:
            data_file.rename(columns={header: 'Timestamp[t]'}, errors='raise', inplace=True)
    return data_file


def files_in_directory(folder: str, file_extension: str) -> list:
    return glob.glob(f"Data/{folder}/*.{file_extension}")