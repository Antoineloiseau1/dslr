import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from lib.toolkit import Dataset, Column, covariance, correlation, find_most_correlated_pair
import matplotlib.pyplot as plt


def main(argc: int, argv: list[str]):
    if argc != 2:
        print("Usage: python3 scatter_plot.py <dataset.csv>", file=sys.stderr)
        exit(1)

    try:
        dataset = Dataset.from_csv(argv[1])
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

    feature_names = dataset.numeric_column_names(skip=["Index"])
    best_pair, best_correlation, best_columns = find_most_correlated_pair(dataset, feature_names)
    feature_a, feature_b = best_pair
    col_a, col_b = best_columns

    print(f"Most similar features: {feature_a} and {feature_b} (r = {best_correlation:.4f})")

    plt.scatter(col_a.values, col_b.values, alpha=0.6, color="hotpink")
    plt.xlabel(feature_a)
    plt.ylabel(feature_b)
    plt.title(f"{feature_a} vs {feature_b} (r = {best_correlation:.4f})")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)