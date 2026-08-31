# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projet

Projet 42 "DSLR" (Data Science × Logistic Regression). Objectif : implémenter un classifieur multi-classe (Choixpeau magique) qui répartit les élèves de Poudlard dans les 4 maisons (Gryffindor, Slytherin, Ravenclaw, Hufflepuff) à partir de leurs notes.

Le sujet complet est dans `en.subject.pdf`.

## Données

- `datasets/dataset_train.csv` — 1600 élèves, 13 features numériques (cours) + métadonnées (nom, anniversaire, main dominante)
- `datasets/dataset_test.csv` — 400 élèves, même format mais sans la colonne `Hogwarts House`
- Colonne cible : `Hogwarts House`

## Programmes à livrer

| Programme | Rôle |
|---|---|
| `describe.py` | Affiche count, mean, std, min, 25%, 50%, 75%, max pour chaque feature numérique |
| `histogram.py` | Histogramme : quel cours a une distribution homogène entre les 4 maisons |
| `scatter_plot.py` | Scatter plot : quelles deux features sont similaires |
| `pair_plot.py` | Pair plot / scatter plot matrix pour choisir les features de la régression |
| `logreg_train.py` | Entraîne la régression logistique (gradient descent, one-vs-all) sur dataset_train.csv, sauvegarde les poids |
| `logreg_predict.py` | Prédit les maisons à partir de dataset_test.csv + poids, génère `houses.csv` |

## Contraintes critiques

- **Pas de fonctions toutes faites** pour `describe.py` : interdit d'utiliser toute fonction statistique (count, mean, std, min, max, percentile…), quelle que soit la bibliothèque. Tout doit être calculé manuellement.
- **Bibliothèque réutilisable** — construire un toolkit ML au fil du projet. Les fonctions utilitaires (stats, parsing CSV, normalisation…) vont dans un module partagé réutilisable par tous les programmes.
- **Gradient descent obligatoire** pour l'entraînement (pas de solver clé en main type `sklearn`).
- **One-vs-all** (one-vs-rest) pour la classification multi-classe.
- **Accuracy cible ≥ 98%** évaluée via `sklearn.metrics.accuracy_score` sur dataset_test.csv.
- Format de sortie de `logreg_predict.py` : fichier `houses.csv` avec colonnes `Index,Hogwarts House`.

## Commandes

```bash
# Exécuter un programme
python describe.py datasets/dataset_train.csv
python histogram.py datasets/dataset_train.csv
python scatter_plot.py datasets/dataset_train.csv
python pair_plot.py datasets/dataset_train.csv
python logreg_train.py datasets/dataset_train.csv
python logreg_predict.py datasets/dataset_test.csv weights.csv
```

## Formules mathématiques (annexe du sujet)

- Fonction sigmoïde : `g(z) = 1 / (1 + e^(-z))`
- Hypothèse : `h_θ(x) = g(θᵀx)`
- Coût (binary cross-entropy) : `J(θ) = -(1/m) Σ [yⁱ log(h_θ(xⁱ)) + (1-yⁱ) log(1 - h_θ(xⁱ))]`
- Gradient : `∂J/∂θⱼ = (1/m) Σ (h_θ(xⁱ) - yⁱ) xⱼⁱ`
