import main
import pandas as pd

def load_file(file: str, skip_rows: int = None):
    data_file = pd.read_csv(file, sep="\t", skiprows=skip_rows)
    return data_file

