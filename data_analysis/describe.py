import sys
from lib.toolkit import Dataset, Column

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


def build_table(columns: list[Column]) -> list[list[str]]:
    table = [[""] + [col.name[:MAX_NAME_WIDTH] for col in columns]]
    for stat_name, stat_function in STATS:
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


def format_stats_table(columns: list[Column]) -> str:
    table = build_table(columns)
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
        print("Usage: python describe.py <dataset.csv>", file=sys.stderr)
        exit(1)
    try:
        dataset = Dataset.from_csv(argv[1])
        columns = dataset.extract_numeric_columns(skip=["Index"])
    except Exception as e:
        print(e)
        exit(1)
    print(format_stats_table(columns))

if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    main(argc, argv)

