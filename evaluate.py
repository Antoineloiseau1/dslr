import random
import matplotlib.pyplot as plt
from lib.toolkit import Dataset, Column, gradient_descent, cost, columns_to_rows, hypothesis

MAX_EPOCHS = 1000
LEARNING_RATE = 0.1
SPLIT_RATIO = 0.8
SEED = 42

def main():
    dataset = Dataset.from_csv("datasets/dataset_train.csv")

    skip = ["Index", "First Name", "Last Name", "Birthday", "Best Hand",
        "Hogwarts House", "Arithmancy", "Care of Magical Creatures"]

    feature_names = [name for name in dataset.header if name not in skip]
    houses = ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"]

    columns = [dataset.extract_nullable_column(name) for name in feature_names]
    columns = [col.impute_mean() for col in columns]

    means = {col.name: col.mean() for col in columns}
    stds = {col.name: col.std() for col in columns}

    columns = [col.standardize() for col in columns]
    labels = dataset.extract_column("Hogwarts House").values

    bias = Column("bias", [1.0] * len(columns[0].values))
    columns.insert(0, bias)
    rows = columns_to_rows(columns)

    # Shuffle
    indices = list(range(len(rows)))
    random.seed(SEED)
    random.shuffle(indices)
    rows = [rows[i] for i in indices]
    labels = [labels[i] for i in indices]

    # Split
    split = int(len(rows) * SPLIT_RATIO)
    train_rows, val_rows = rows[:split], rows[split:]
    train_labels, val_labels = labels[:split], labels[split:]

    # Train (one-vs-all) + cost history
    thetas = {}
    cost_history = {house: [] for house in houses}
    for house in houses:
        tmp_thetas = [0.0] * len(train_rows[0])
        targets = [label == house for label in train_labels]
        for epoch in range(MAX_EPOCHS):
            if epoch % 10 == 0:
                cost_history[house].append(cost(tmp_thetas, train_rows, targets))
            gradients = gradient_descent(train_rows, tmp_thetas, targets)
            for i in range(len(tmp_thetas)):
                tmp_thetas[i] -= LEARNING_RATE * gradients[i]
        thetas[house] = tmp_thetas

    # Predict on validation set
    predictions = []
    correct = 0
    for i in range(len(val_rows)):
        best_house = None
        best_prob = -1
        for house in houses:
            h = hypothesis(thetas[house], val_rows[i])
            if h > best_prob:
                best_prob = h
                best_house = house
        predictions.append(best_house)
        if best_house == val_labels[i]:
            correct += 1

    accuracy = correct / len(val_labels) * 100
    print(f"Validation: {correct}/{len(val_labels)}")
    print(f"Accuracy: {accuracy:.2f}%")

    # --- Confusion Matrix ---
    matrix = {true: {pred: 0 for pred in houses} for true in houses}
    for true, pred in zip(val_labels, predictions):
        matrix[true][pred] += 1

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    ax = axes[0]
    data = [[matrix[true][pred] for pred in houses] for true in houses]
    im = ax.imshow(data, cmap="Blues")
    ax.set_xticks(range(len(houses)))
    ax.set_yticks(range(len(houses)))
    ax.set_xticklabels(houses, rotation=45, ha="right")
    ax.set_yticklabels(houses)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion Matrix (accuracy: {accuracy:.2f}%)")
    for i in range(len(houses)):
        for j in range(len(houses)):
            color = "white" if data[i][j] > max(max(row) for row in data) / 2 else "black"
            ax.text(j, i, str(data[i][j]), ha="center", va="center", color=color, fontweight="bold")
    fig.colorbar(im, ax=ax)

    # --- Cost Curve ---
    ax = axes[1]
    colors = {"Gryffindor": "#740001", "Slytherin": "#1a472a",
              "Hufflepuff": "#ecb939", "Ravenclaw": "#0e1a40"}
    epochs = list(range(0, MAX_EPOCHS, 10))
    for house in houses:
        ax.plot(epochs, cost_history[house], label=house, color=colors[house], linewidth=2)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Cost (binary cross-entropy)")
    ax.set_title("Training Cost per House")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
