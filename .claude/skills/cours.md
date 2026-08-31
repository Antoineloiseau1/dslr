---
name: cours
description: Rédige ou met à jour un module de cours dans cours/ avant de commencer une nouvelle étape du projet DSLR.
---

# Skill : Rédaction de cours

Ce skill est invoqué **avant de commencer le code d'une nouvelle étape** du projet DSLR.

## Entrée

L'argument `args` contient le numéro et/ou le sujet du module (ex: "1 statistiques", "3 logistic regression").

## Processus

1. **Identifier le module** à rédiger parmi :
   - `01_statistiques.md` — Statistiques descriptives (count, mean, std, min, quartiles, max)
   - `02_visualisation.md` — Visualisation de données (matplotlib, histogram, scatter plot, pair plot)
   - `03_logistic_regression.md` — Régression logistique binaire (sigmoïde, binary cross-entropy, gradient descent)
   - `04_one_vs_all.md` — Classification multi-classe (one-vs-all / one-vs-rest)
   - `05_features.md` — Feature selection, normalisation, gestion des valeurs manquantes

2. **Rechercher** des ressources à jour (WebSearch) pour s'assurer que le contenu est correct et complet.

3. **Écrire le fichier** dans `cours/` avec cette structure :
   ```
   # Titre du module

   ## Objectif
   Une phrase : pourquoi on a besoin de ça dans le projet.

   ## Concepts clés
   Explications courtes, accessibles, avec des analogies simples si possible.
   Pas de pavés. Phrases courtes.

   ## Formules
   Les formules mathématiques essentielles, avec explication de chaque terme.

   ## Exemple concret
   Un petit exemple chiffré à la main pour illustrer.

   ## Pièges courants
   Ce qui plante souvent quand on code ça pour la première fois.

   ## Ressources
   Liens vers docs, articles, vidéos recommandés.
   ```

4. **Mettre à jour** `cours/README.md` pour cocher le module comme rédigé.

## Règles

- Langue : français, termes techniques en anglais entre parenthèses quand utile
- Niveau : débutant qui a des bases en programmation mais découvre le ML
- Court et direct, pas de remplissage
- Les formules doivent être en notation lisible (pas de LaTeX complexe)
- Si le module existe déjà, le compléter/corriger plutôt que le réécrire
