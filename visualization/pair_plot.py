import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from lib.toolkit import Dataset
from lib.utils import to_float, HOUSE_COLORS
import matplotlib.pyplot as plt


def main(argc: int, argv: list[str]):
    if argc != 2:
        print("Usage: python3 pair_plot.py <dataset.csv>", file=sys.stderr)
        exit(1)

    try:
        dataset = Dataset.from_csv(argv[1])
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

    course_names = dataset.numeric_column_names(skip=["Index"])
    house_idx = dataset.header.index("Hogwarts House")
    n = len(course_names)

    fig, axes = plt.subplots(n, n, figsize=(n * 2, n * 2))

    for i in range(n):
        for j in range(n):
            ax = axes[i][j]
            idx_i = dataset.header.index(course_names[i])
            idx_j = dataset.header.index(course_names[j])

            if i == j:
                groups: dict[str, list] = {}
                for row in dataset.rows:
                    house = row[house_idx]
                    val = to_float(row[idx_i])
                    if val is not None and house:
                        groups.setdefault(house, []).append(val)
                for house, vals in groups.items():
                    color = HOUSE_COLORS.get(house, "gray")
                    ax.hist(vals, alpha=0.5, bins=20, color=color, label=house)
            else:
                groups_xy: dict[str, tuple[list, list]] = {}
                for row in dataset.rows:
                    house = row[house_idx]
                    val_x = to_float(row[idx_j])
                    val_y = to_float(row[idx_i])
                    if val_x is not None and val_y is not None and house:
                        groups_xy.setdefault(house, ([], []))
                        groups_xy[house][0].append(val_x)
                        groups_xy[house][1].append(val_y)
                for house, (xs, ys) in groups_xy.items():
                    color = HOUSE_COLORS.get(house, "gray")
                    ax.scatter(xs, ys, alpha=0.3, s=3, color=color)

            if i == 0:
                ax.set_title(course_names[j], fontsize=5, rotation=45, ha='left')
            if j == 0:
                ax.set_ylabel(course_names[i], fontsize=5)
            ax.tick_params(labelbottom=False, labelleft=False, length=0)

    handles = [plt.Line2D([0], [0], marker='o', color='w',
               markerfacecolor=c, markersize=6, label=h)
               for h, c in HOUSE_COLORS.items()]
    fig.legend(handles=handles, loc='lower right', fontsize=8)
    plt.suptitle("Pair Plot", fontsize=14)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
