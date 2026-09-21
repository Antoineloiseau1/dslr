# DSLR — Data Science × Logistic Regression

Classifieur multi-classe (Choixpeau magique) qui répartit les élèves de Poudlard dans les 4 maisons à partir de leurs notes, via une régression logistique one-vs-all.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

### 1. Analyse descriptive

```bash
python3 analysis/describe.py datasets/dataset_train.csv
```

### 2. Visualisation

```bash
python3 visualization/histogram.py datasets/dataset_train.csv
python3 visualization/scatter_plot.py datasets/dataset_train.csv
python3 visualization/pair_plot.py datasets/dataset_train.csv
```

### 3. Entraînement

Entraîne la régression logistique sur le dataset et sauvegarde les poids dans `weights.csv`.

```bash
python3 logreg_train.py datasets/dataset_train.csv
```

### 4. Prédiction

Prédit les maisons à partir du dataset de test et des poids, génère `houses.csv`.

```bash
python3 logreg_predict.py datasets/dataset_test.csv weights.csv
```

### 5. Évaluation

Compare les prédictions avec les vraies valeurs.

```bash
python3 evaluate.py
```
