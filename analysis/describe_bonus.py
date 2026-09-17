import sys
from pathlib import Path
from lib.utils import to_float
sys.path.append(str(Path(__file__).resolve().parent.parent))
from lib.toolkit import Dataset, Column


def missing_values_count(dataset: Dataset, col_name: str) -> int:
    index = dataset.header.index(col_name)
    total_rows = len(dataset.rows)
    valid_count = 0
    for row in dataset.rows:
        if to_float(row[index]) is not None:
            valid_count += 1
    return total_rows - valid_count


STATS = [
    ("Count", lambda col: col.count()),
    ("Mean", lambda col: col.mean()),
    ("Std", lambda col: col.std()),
    ("Min", lambda col: col.min()),
    ("25%", lambda col: col.percentile(0.25)),
    ("50%", lambda col: col.percentile(0.5)),
    ("75%", lambda col: col.percentile(0.75)),
    ("Max", lambda col: col.max()),
]

MAX_NAME_WIDTH = 14
GUTTER = 2
PRECISION = 6


def build_table(columns: list[Column], stats: list) -> list[list[str]]:
    table = [[""] + [col.name[:MAX_NAME_WIDTH] for col in columns]]
    for stat_name, stat_function in stats:
        row = [stat_name]
        for col in columns:
            row.append(f"{stat_function(col):.{PRECISION}f}")
        table.append(row)
    return table


def compute_column_widths(table: list[list[str]]) -> list[int]:
    widths = []
    for index in range(len(table[0])):
        longest = 0
        for row in table:
            length = len(row[index])
            if length > longest:
                longest = length
        widths.append(longest if index == 0 else longest + GUTTER)
    return widths


def format_stats_table(columns: list[Column], stats: list) -> str:
    table = build_table(columns, stats)
    widths = compute_column_widths(table)
    lines = []
    for row in table:
        cells = [f"{row[0]:<{widths[0]}}"]
        cells += [f"{cell:>{widths[i]}}" for i, cell in enumerate(row[1:], 1)]
        lines.append("".join(cells).rstrip())
    return "\n".join(lines)


def main(argc: int, argv: list[str]) -> int:
    if argc != 2:
        print("Error: Wrong number of arguments", file=sys.stderr)
        print("Usage: python describe_bonus.py <dataset.csv>", file=sys.stderr)
        exit(1)
    try:
        dataset = Dataset.from_csv(argv[1])
        columns = dataset.extract_numeric_columns(skip=["Index"])
    except Exception as e:
        print(e)
        exit(1)
    BONUS_STATS = STATS + [
        # Compte le nombre de valeurs manquantes dans la colonne
        ("NaN Count", lambda col: missing_values_count(dataset, col.name)),
        # Ecart entre la valeur max et la valeur min de la colonne
        ("Range", lambda col: col.max() - col.min()),
        # Interquartile Range : différence entre le 3ème quartile (75%) et le 1er quartile (25%) sans valeurs aberrantes
		("IQR", lambda col: col.percentile(0.75) - col.percentile(0.25)),
    ]
    print(format_stats_table(columns, BONUS_STATS))


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    main(argc, argv)