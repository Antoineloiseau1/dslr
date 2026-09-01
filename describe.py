import sys
from toolkit import read_csv, extract_numeric_columns, Column

def format_stats_table(columns: list[Column]) -> str:
    stats = [
        ("Count", lambda col: col.count()),
        ("Mean", lambda col: col.mean()),
        ("Std", lambda col: col.std()),
        ("Min", lambda col: col.min()),
        ("25%", lambda col: col.percentile(0.25)),
        ("50%", lambda col: col.percentile(0.5)),
        ("75%", lambda col: col.percentile(0.75)),
        ("Max", lambda col: col.max()),
    ]
    lines = []
    # Largeur fixe pour chaque colonne
    col_width = 12
    # En-tête
    header = [""] + [col.name[:col_width] for col in columns]
    lines.append("".join(f"{value:>{col_width}}" for value in header))
    # Statistiques
    for stat_name, stat_function in stats:
        values = [stat_function(col) for col in columns]
        formatted_values = [
            f"{value:>{col_width}.6f}" for value in values
        ]
        lines.append(
            f"{stat_name:<{col_width}}" + "".join(formatted_values)
        )
    return "\n".join(lines)


def main(argc: int, argv: list[str]) -> int:
    if argc != 2:
        print("Error: Wrong number of arguments", file=sys.stderr)   
        print("Usage: python describe.py <dataset.csv>", file=sys.stderr)
        exit(1)
    try:
        dataset = read_csv(argv[1])
        columns = extract_numeric_columns(dataset, skip=["Index"])
    except Exception as e:
        print(e)
        exit(1)
    print(format_stats_table(columns))

if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    main(argc, argv)

