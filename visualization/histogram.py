import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from lib.toolkit import Dataset, Column
from lib.utils import HOUSE_COLORS
import matplotlib.pyplot as plt


def main(argc: int, argv: list[str]):
    if argc != 2:
        print("Usage: python3 histogram.py <dataset.csv>", file=sys.stderr)
        exit(1)

    try:
        dataset = Dataset.from_csv(argv[1])
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

    col_names = dataset.numeric_column_names(skip=["Index"])
    fig, axes = plt.subplots(4, 4, figsize=(16, 12))
    axes = axes.flatten()

    best_score = float('inf')
    best_name = ""
    for i, name in enumerate(col_names):
        means = []
        for group in dataset.extract_numeric_column_by_group(name, "Hogwarts House"):
            color = HOUSE_COLORS.get(group.name, "gray")
            axes[i].hist(group.values, alpha=0.6, density=True, label=group.name, color=color)
            means.append(group.mean())
        mean_col = Column("tmp", means)
        score = mean_col.std()
        course_col = dataset.extract_numeric_column(name)
        score /= course_col.std()
        if score < best_score:
            best_score = score
            best_name = name
        axes[i].set_title(name)
        axes[i].xaxis.set_visible(False)
        axes[i].yaxis.set_visible(False)

    for i in range(len(col_names), len(axes)):
        axes[i].axis('off')

    last_ax = axes[len(axes) - 1]
    last_ax.text(0.5, 0.5, f"Most homogeneous course:\n{best_name}",
                 ha='center', va='center', fontsize=14, fontweight='bold',
                 transform=last_ax.transAxes)

    axes[0].legend()
    plt.tight_layout(h_pad=3)
    plt.show()


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
