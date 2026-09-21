import sys
from lib.toolkit import Dataset, Column, columns_to_rows, hypothesis

def main(argc, argv):
    if argc != 3:
        print("Usage: python3 logreg_train.py <dataset.csv> <weights.csv>", file=sys.stderr)
        exit(1)
    try:
        dataset = Dataset.from_csv(argv[1])
        weights = Dataset.from_csv(argv[2])
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

    skip = ["Index", "First Name", "Last Name", "Birthday", "Best Hand",
        "Hogwarts House", "Arithmancy", "Care of Magical Creatures"]

    feature_names = [name for name in dataset.header if name not in skip]
    houses = ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"]

    columns = [dataset.extract_nullable_column(name) for name in feature_names]
    columns = [col.impute_mean() for col in columns]

    bias = Column("bias", [1.0] * len(columns[0].values))
    columns.insert(0, bias)
    rows = columns_to_rows(columns)

    thetas = {}
    for row in weights.rows:
        if row[0] == "_mean":
            continue
        thetas[row[0]] = [float(x) for x in row[1:]]

    predictions = []
    for i in range(len(rows)):
        best_house = None
        best_prob = -1
        for house in houses:
            h = hypothesis(thetas[house], rows[i])
            if h > best_prob:
                best_prob = h
                best_house = house
        predictions.append(best_house)

    with open("houses.csv", "w") as f:
        f.write("Index,Hogwarts House\n")
        for i, house in enumerate(predictions):
            f.write(f"{i},{house}\n")
    print("Predictions saved to houses.csv")



if __name__ == "__main__":
    main(len(sys.argv), sys.argv)