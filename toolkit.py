import csv
from dataclasses import dataclass
import math

@dataclass
class Dataset:
    header: list[str]
    rows: list[list[str]]

@dataclass
class Column:
    name: str
    values: list[float]
    
    def count(self) -> int:
        return len(self.values)
    
    def mean(self) -> float:
        total = 0
        for value in self.values:
            total += value
        return total / self.count()
    
    def std(self) -> float:
        mean = self.mean()
        count = self.count()
        sse = 0         # Sum of Squared Errors
        for value in self.values:
            error = value - mean
            squared_error = error * error
            sse += squared_error
        variance = sse / (count - 1)
        return math.sqrt(variance)
    
    def min(self) -> float:
        current = self.values[0]
        for value in self.values:
            if value < current:
                current = value
        return current
    
    def max(self) -> float:
        current = self.values[0]
        for value in self.values:
            if value > current:
               current = value
        return current
    
    def percentile(self, p: float) -> float:
        if p not in (0.25, 0.5, 0.75):
            raise ValueError("p must be 0.25, 0.5 or 0.75")
        sorted_values = sorted(self.values)
        count = self.count() - 1
        percent = count * p
        lower_index = math.floor(percent)
        upper_index = math.ceil(percent)
        fraction = percent - lower_index
        lower = sorted_values[lower_index]
        upper = sorted_values[upper_index]
        return lower + (upper - lower) * fraction

def read_csv(filepath: str) -> Dataset:
    if not filepath.endswith(".csv"):
        raise ValueError("File must be .csv")
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        rows = [row for row in reader]
    return Dataset(header, rows)

def extract_numeric_columns(dataset: Dataset, skip: list[str] = []) -> list[Column]:
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
             