import csv
import sys
from lib.toolkit import Dataset, gradient_descent, impute_mean

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
    grades, labels = dataset.extract_matrix(feature_names, "Hogwarts House")
    grades = impute_mean(grades)
    
    print(grades)

    # thetas = {}

    # for house in houses:
    #     tmp_thetas = [0.00] * (len(feature_names) + 1)
    #     targets = [label == house for label in labels]
    #     for _ in range(MAX_EPOCHS):
    #         gradients = gradient_descent(grades, tmp_thetas, targets)
    #         for i in range(len(tmp_thetas)):
    #             tmp_thetas[i] -= LEARNING_RATE * gradients[i]
    #     thetas[house] = tmp_thetas

    # print(thetas)
if __name__ == "__main__":
    main(len(sys.argv), sys.argv)