# Cours DSLR

## V.2.1 Histogram

TODO

## V.2.2 Scatter plot

**Objectif** : visualiser la relation entre deux variables numériques (un point = un élève, X = note cours A, Y = note cours B).

**Lecture** : diagonale nette = forte relation linéaire. Nuage dispersé = pas de relation claire.

**Covariance** : cov(X, Y) = moyenne des [(xi - mean(X)) × (yi - mean(Y))]

Pour chaque élève, on multiplie son écart à la moyenne dans le cours X par son écart à la moyenne dans le cours Y. Si les deux écarts ont le même signe (tous les deux au-dessus ou tous les deux en dessous de la moyenne), le produit est positif → les cours évoluent dans le même sens. Signes opposés → produit négatif → évolution inverse.

**Corrélation** : r = cov(X, Y) / (std(X) × std(Y))

version normalisée de la covariance, toujours entre -1 et 1, ce qui la rend comparable peu importe l'échelle.

r proche de +1 : relation forte et positive
r proche de -1 : relation forte mais inverse
r proche de 0 : pas de relation linéaire claire

**abs(r)** : la force de la relation, sans le sens. Le signe indique la direction, la valeur absolue indique la force. Ex : `r = -0.92` est plus fort que `r = +0.85` malgré le signe — sans `abs()`, une forte corrélation négative serait ignorée à tort au profit d'une positive plus faible.

## Modules

| # | Module | Fichier | Quand |
|---|--------|---------|-------|
| 1 | Statistiques descriptives (mean, std, percentiles…) | `01_statistiques.md` | **Rédigé** |
| 2 | Visualisation de données (matplotlib, histogrammes, scatter) | `02_visualisation.md` | Avant `histogram.py` |
| 3 | Régression logistique binaire (sigmoïde, cost function, gradient descent) | `03_logistic_regression.md` | Avant `logreg_train.py` |
| 4 | Classification multi-classe (one-vs-all) | `04_one_vs_all.md` | Avant `logreg_train.py` |
| 5 | Feature selection & normalisation | `05_features.md` | Avant `pair_plot.py` / `logreg_train.py` |

## Comment utiliser

1. Avant chaque étape, lis les ressources correspondantes
2. Écris dans le fichier du module **avec tes propres mots** ce que tu as compris
3. Inclus au moins : un résumé, les formules clés, un exemple simple
4. Tu reviendras compléter ces notes au fur et à mesure
