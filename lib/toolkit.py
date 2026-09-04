import csv
from dataclasses import dataclass
import math
from lib.utils import to_float

def mean(values: list[float]) -> float:
    total = 0
    for value in values:
        total += value
    return total / len(values)

def std(values: list[float]) -> float:
    m = mean(values)
    sse = 0
    for value in values:
        error = value - m
        sse += error * error
    variance = sse / (len(values) - 1)
    return math.sqrt(variance)


@dataclass
class Column:
    name: str
    values: list[float]

    def count(self) -> int:
        return len(self.values)

    def mean(self) -> float:
        return mean(self.values)

    def std(self) -> float:
        return std(self.values)

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

    def impute_mean(self) -> 'Column':
        total = 0
        count = 0
        for v in self.values:
            if v is not None:
                total += v
                count += 1
        m = total / count
        return Column(self.name, [v if v is not None else m for v in self.values])

    def standardize(self) -> 'Column':
        m = self.mean()
        s = self.std()
        return Column(self.name, [(v - m) / s for v in self.values])


def columns_to_rows(columns: list[Column]) -> list[list[float]]:
    return [list(row) for row in zip(*(col.values for col in columns))]


@dataclass
class Dataset:
    header: list[str]
    rows: list[list[str]]

    @staticmethod
    def from_csv(filepath: str) -> 'Dataset':
        if not filepath.endswith(".csv"):
            raise ValueError("File must be .csv")
        with open(filepath) as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            rows = [row for row in reader]
        return Dataset(header, rows)

    def extract_column(self, name: str) -> Column:
        if name not in self.header:
            raise ValueError(f"{name} not found in dataset")
        index = self.header.index(name)
        values = [row[index] for row in self.rows]
        return Column(name, values)

    def numeric_column_names(self, skip: list[str] = []) -> list[str]:
        return [col.name for col in self.extract_numeric_columns(skip)]

    def extract_numeric_column(self, name: str) -> Column:
        if name not in self.header:
            raise ValueError(f"{name} not found in dataset")
        index = self.header.index(name)
        values: list[float] = []
        for row in self.rows:
            converted = to_float(row[index])
            if converted is not None:
                values.append(converted)
        return Column(name, values)

    def extract_numeric_columns(self, skip: list[str] = []) -> list[Column]:
        columns: list[Column] = []
        for index, name in enumerate(self.header):
            if name in skip:
                continue
            values: list[float] = []
            for row in self.rows:
                converted = to_float(row[index])
                if converted is not None:
                    values.append(converted)
            if values:
                columns.append(Column(name, values))
        return columns

    def extract_numeric_column_by_group(self, col_name: str, group_name: str) -> list[Column]:
        col = self.extract_column(col_name)
        group = self.extract_column(group_name)
        groups = {}
        for key, value in zip(group.values, col.values):
            converted = to_float(value)
            if converted is not None:
                groups.setdefault(key, []).append(converted)
        return [Column(name, values) for name, values in groups.items()]

    def extract_numeric_column_pair(self, feature_a: str, feature_b: str) -> tuple[Column, Column]:
        if feature_a not in self.header:
            raise ValueError(f"{feature_a} not found in dataset")
        if feature_b not in self.header:
            raise ValueError(f"{feature_b} not found in dataset")
        index_a = self.header.index(feature_a)
        index_b = self.header.index(feature_b)
        values_a: list[float] = []
        values_b: list[float] = []
        for row in self.rows:
            converted_a = to_float(row[index_a])
            converted_b = to_float(row[index_b])
            if converted_a is not None and converted_b is not None:
                values_a.append(converted_a)
                values_b.append(converted_b)
        return Column(feature_a, values_a), Column(feature_b, values_b)

    def extract_nullable_column(self, name: str) -> Column:
        if name not in self.header:
            raise ValueError(f"{name} not found in dataset")
        index = self.header.index(name)
        values = [to_float(row[index]) for row in self.rows]
        return Column(name, values)


def covariance(col_a: Column, col_b: Column) -> float:
    mean_a = col_a.mean()
    mean_b = col_b.mean()
    total = 0
    for x, y in zip(col_a.values, col_b.values):
        total += (x - mean_a) * (y - mean_b)
    return total / (col_a.count() - 1)


def correlation(col_a: Column, col_b: Column) -> float:
    return covariance(col_a, col_b) / (col_a.std() * col_b.std())


def find_most_correlated_pair(dataset: Dataset, feature_names: list[str]):
    best_pair = None
    best_correlation = 0
    best_columns = None

    for i in range(len(feature_names)):
        for j in range(i + 1, len(feature_names)):
            feature_a = feature_names[i]
            feature_b = feature_names[j]
            col_a, col_b = dataset.extract_numeric_column_pair(feature_a, feature_b)
            r = correlation(col_a, col_b)

            if abs(r) > abs(best_correlation):
                best_correlation = r
                best_pair = (feature_a, feature_b)
                best_columns = (col_a, col_b)
    return best_pair, best_correlation, best_columns


# Subject formulas:
def sigmoid(z: float) -> float:
    if z >= 0:
        return 1 / (1 + math.exp(-z))
    else:
        ez = math.exp(z)
        return ez / (1 + ez)

# scalar prouduct between thetas and features (bias included)
def hypothesis(theta: list[float], features: list[float]) -> float: 
    if(len(theta) != len(features)):
        raise ValueError("theta and features must have the same length")
    z = 0
    for i in range(len(theta)):
        z += theta[i] * features[i]
    return sigmoid(z)

def cost(theta: list[float], rows: list[list[float]], targets: list[bool]) -> float:
    m = len(rows)
    total = 0
    for i, row in enumerate(rows):
        h = hypothesis(theta, row)
        h = max(1e-15, min(1 - 1e-15, h))
        total += targets[i] * math.log(h) + (1 - targets[i]) * math.log(1 - h)
    return -total / m

def gradient_descent(rows: list[list[float]], thetas: list[float], targets: list[bool]):
    m = len(rows)
    gradients = [0.0] * len(thetas)
    for i, row in enumerate(rows):
        h = hypothesis(thetas, row)
        error =  h - targets[i]
        for j, feature in enumerate(row):
            gradients[j] += error * feature
    for j in range(len(gradients)):
        gradients[j] /= m
    return gradients

