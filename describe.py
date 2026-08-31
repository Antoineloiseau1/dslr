import sys
from toolkit import read_csv, extract_numeric_columns

def main(argc: int, argv: list[str]) -> int:
    if argc != 2:
        print("Error: Wrong number of arguments", file=sys.stderr)   
        print("Usage: python describe.py <dataset.csv>", file=sys.stderr)
        exit(1)
    try:
        dataset = read_csv(argv[1])
        columns = extract_numeric_columns(dataset, skip=["Index"])
        for col in columns:
            print(f"{col.name}: {col.values[:3]}...")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    main(argc, argv)

