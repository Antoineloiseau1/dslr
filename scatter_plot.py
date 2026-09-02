import sys
from lib.toolkit import Dataset, Column
import matplotlib.pyplot as plt


def covariance(col_a: Column, col_b: Column) -> float:
    mean_a = col_a.mean()
    mean_b = col_b.mean()
    total = 0
    for x, y in zip(col_a.values, col_b.values):
        total += (x - mean_a) * (y - mean_b)
    return total / (col_a.count() - 1)


def correlation(col_a: Column, col_b: Column) -> float:
    return covariance(col_a, col_b) / (col_a.std() * col_b.std())


def find_most_correlated_pair(dataset: Dataset, course_names: list[str]):
    best_pair = None
    best_correlation = 0
    best_columns = None

    for i in range(len(course_names)):
        for j in range(i + 1, len(course_names)):
            course_a = course_names[i]
            course_b = course_names[j]
            col_a, col_b = dataset.extract_numeric_column_pair(course_a, course_b)
            r = correlation(col_a, col_b)

            if abs(r) > abs(best_correlation):
                best_correlation = r
                best_pair = (course_a, course_b)
                best_columns = (col_a, col_b)

    return best_pair, best_correlation, best_columns


def main(argc: int, argv: list[str]):
    if argc != 2:
        print("Usage: python3 scatter_plot.py <dataset.csv>", file=sys.stderr)
        exit(1)

    try:
        dataset = Dataset.from_csv(argv[1])
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

    course_names = dataset.numeric_column_names(skip=["Index"])
    best_pair, best_correlation, best_columns = find_most_correlated_pair(dataset, course_names)
    course_a, course_b = best_pair
    col_a, col_b = best_columns

    print(f"Most similar features: {course_a} and {course_b} (r = {best_correlation:.4f})")

    plt.scatter(col_a.values, col_b.values, alpha=0.6, color="hotpink")
    plt.xlabel(course_a)
    plt.ylabel(course_b)
    plt.title(f"{course_a} vs {course_b} (r = {best_correlation:.4f})")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)