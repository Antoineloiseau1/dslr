import csv
from dataclasses import dataclass

@dataclass
class Dataset:
    header: list[str]
    rows: list[list[str]]


def read_csv(filepath: str) -> Dataset:
    if not filepath.endswith(".csv"):
        raise ValueError("File must be .csv")
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        rows = [row for row in reader]
    return Dataset(header, rows = rows)