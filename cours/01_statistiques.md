# Module 1 — Statistiques descriptives

## Objectif

Calculer à la main les métriques de base (count, mean, std, min, quartiles, max) pour chaque **feature numérique** du dataset. C'est ce que fait `describe.py`.

## Concepts clés

### Count

Le nombre de valeurs **non manquantes** (non-NaN) dans une colonne. Attention : le dataset contient des trous, il faut les ignorer.

### Mean (moyenne)

La somme de toutes les valeurs divisée par le nombre de valeurs.

```
mean = somme des valeurs / count
```

Analogie : si 3 personnes ont 10€, 20€ et 30€, la moyenne c'est 60/3 = 20€.

### Std (écart-type / standard deviation)

Mesure à quel point les valeurs sont dispersées autour de la moyenne. Un std élevé = données très étalées. Un std faible = données regroupées.

Étapes :
1. Calculer la moyenne
2. Pour chaque valeur : `(valeur - moyenne)²`
3. Faire la moyenne de ces carrés → c'est la **variance**
4. Prendre la racine carrée → c'est le **std**

**Attention** : pour un échantillon (sample), on divise par `n - 1` et non `n`. C'est la correction de Bessel. Pandas utilise `n - 1` par défaut.

### Min / Max

La plus petite et la plus grande valeur. Rien de compliqué, mais il faut ignorer les NaN.

### Percentiles (25%, 50%, 75%)

Le percentile P signifie : "P% des valeurs sont en dessous de cette valeur".

- **25%** (Q1) : premier quartile
- **50%** (Q2) : médiane — la valeur du milieu
- **75%** (Q3) : troisième quartile

Algorithme pour calculer un percentile :
1. Trier les valeurs
2. Calculer la position : `pos = percentile/100 * (n - 1)`
3. Si `pos` est entier → la valeur à cet index
4. Si `pos` est décimal → interpoler entre les deux valeurs encadrantes :
   `valeur = lower + (upper - lower) * partie_décimale`

Exemple : données triées `[2, 4, 6, 8, 10]`, percentile 25% :
- `pos = 0.25 * 4 = 1.0` → index 1 → valeur = **4**

Même données, percentile 30% :
- `pos = 0.30 * 4 = 1.2` → entre index 1 (valeur 4) et index 2 (valeur 6)
- `résultat = 4 + (6 - 4) * 0.2 = 4.4`

## Formules résumées

| Métrique | Formule |
|----------|---------|
| count | nombre de valeurs non-NaN |
| mean | `Σxᵢ / n` |
| variance | `Σ(xᵢ - mean)² / (n - 1)` |
| std | `√variance` |
| min | `min(valeurs)` |
| percentile P | trier → position `P/100 * (n-1)` → interpoler |
| max | `max(valeurs)` |

## Pièges courants

1. **Oublier les NaN** — le dataset a des valeurs manquantes. Si tu additionnes sans filtrer, tout pète. Filtre d'abord.
2. **`n` vs `n - 1`** pour le std — pandas utilise `n - 1` (sample std). Si tu divises par `n`, tes résultats ne matcheront pas.
3. **Colonnes non numériques** — le dataset a des colonnes texte (noms, maisons…). Il faut les détecter et les ignorer.
4. **Interpolation des percentiles** — il existe plusieurs méthodes. Pandas utilise l'interpolation linéaire par défaut. Utilise la même pour que tes résultats collent.
5. **Précision flottante** — compare tes résultats avec 6 décimales, pas plus. Les flottants ont des erreurs d'arrondi.

## Ressources

- [Standard Deviation Formulas — MathIsFun](https://www.mathsisfun.com/data/standard-deviation-formulas.html) — explication visuelle et interactive
- [How to Calculate Standard Deviation — Scribbr](https://www.scribbr.com/statistics/standard-deviation/) — guide pas à pas avec exemples
- [Quartiles and Percentiles — W3Schools](https://www.w3schools.com/statistics/statistics_quartiles_and_percentiles.php) — simple et direct
- [Step-by-Step Standard Deviation — PrepScholar](https://blog.prepscholar.com/standard-deviation-formula) — 6 étapes claires
