import csv
import sys
from lib.toolkit import Dataset, Column, gradient_descent, columns_to_rows

MAX_EPOCHS = 1000
LEARNING_RATE = 0.1

def main(argc: int, argv: list[str]):
    if argc != 2:
        print("Usage: python3 logreg_train.py <dataset.csv>", file=sys.stderr)
        exit(1)

    try:
        dataset = Dataset.from_csv(argv[1])
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

    skip = ["Index", "First Name", "Last Name", "Birthday", "Best Hand",
        "Hogwarts House", "Arithmancy", "Care of Magical Creatures"]

    feature_names = [name for name in dataset.header if name not in skip]
    houses = ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"]

    # Data Preparation
    columns = [dataset.extract_nullable_column(name) for name in feature_names]
    columns = [col.impute_mean() for col in columns]

    means = {col.name: col.mean() for col in columns}
    stds = {col.name: col.std() for col in columns}

    columns = [col.standardize() for col in columns]
    labels = dataset.extract_column("Hogwarts House").values

    bias = Column("bias", [1.0] * len(columns[0].values))
    columns.insert(0, bias)
    rows = columns_to_rows(columns)

    # Training (one-vs-all)
    thetas = {}
    for house in houses:
        tmp_thetas = [0.0] * len(rows[0])
        targets = [label == house for label in labels]
        for _ in range(MAX_EPOCHS):
            gradients = gradient_descent(rows, tmp_thetas, targets)
            for i in range(len(tmp_thetas)):
                tmp_thetas[i] -= LEARNING_RATE * gradients[i]
        thetas[house] = tmp_thetas

    # De-Normalisation
    for house in houses:
        bias_correction = 0
        for i in range(len(feature_names)):
            name = feature_names[i]
            bias_correction += thetas[house][i + 1] * means[name] / stds[name]
            thetas[house][i + 1] /= stds[name]
        thetas[house][0] -= bias_correction


    # Save weights
    with open("weights.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["house", "bias"] + feature_names)
        for house in houses:
            writer.writerow([house] + thetas[house])
        writer.writerow(["_mean", 0.0] + [means[name] for name in feature_names])

    print("Weights saved to weights.csv")

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
