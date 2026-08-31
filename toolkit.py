import csv
from dataclasses import dataclass
from typing import Generic, TypeVar
import math

T = TypeVar("T")

@dataclass
class Dataset:
    header: list[str]
    rows: list[list[str]]

@dataclass
class Column(Generic[T]):
    name: str
    values: list[T]

def read_csv(filepath: str) -> Dataset:
    if not filepath.endswith(".csv"):
        raise ValueError("File must be .csv")
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        rows = [row for row in reader]
    return Dataset(header, rows)

def extract_numeric_columns(dataset: Dataset, skip: list[str] = []) -> list[Column[float]]:
    columns: list[Column[float]] = []
    for index, name in enumerate(dataset.header):
        if name in skip:
            continue
        values: list[float] = []
        for row in dataset.rows:
            value = row[index]
            if value:
                try:
                    converted = float(value)
                    if not math.isnan(converted):
                        values.append(converted)
                except ValueError:
                    pass
        if values:
            columns.append(Column(name, values))
    return columns
             