# Design Document

## Overview

Cette fonctionnalité améliore le modèle de prédiction de football existant en intégrant des caractéristiques basées sur les moyennes de buts marqués et encaissés des équipes sur leurs 6 derniers matchs. L'approche remplace l'utilisation problématique des scores réels du match (HS, AS) par des données historiques pertinentes qui respectent la contrainte temporelle et évitent la fuite de données.

Le design s'appuie sur l'architecture existante du notebook `football_model_training.ipynb` et étend la requête SQL actuelle ainsi que le pipeline de traitement des données Python.

## Architecture

### Architecture Actuelle
Le système actuel utilise :
- Une base de données SQLite (`football.db`) contenant les données de matchs
- Une requête SQL complexe avec des CTEs (Common Table Expressions) pour calculer les caractéristiques LAG
- Un pipeline Python pour calculer les moyennes et entraîner le modèle XGBoost

### Architecture Proposée
L'architecture reste identique mais avec des extensions :
- Extension de la CTE `team_games` pour inclure les données de buts
- Extension de la CTE `lagged` pour inclure les colonnes LAG des buts
- Extension du pipeline Python pour calculer les moyennes de buts
- Mise à jour de la liste des caractéristiques numériques

## Components and Interfaces

### 1. Composant SQL - Extension de la Requête

#### CTE team_games (Modifiée)
```sql
team_games AS (
  SELECT
    rowid, Date, HomeTeam AS team, 'home' as side,
    CASE FTR WHEN 'H' THEN 3 WHEN 'D' THEN 1 ELSE 0 END AS points,
    HS AS shots, HC AS corners, HF AS fouls,
    FTHG AS goals_scored,    -- Nouveau: buts marqués par l'équipe à domicile
    FTAG AS goals_conceded   -- Nouveau: buts encaissés par l'équipe à domicile
  FROM matches
  UNION ALL
  SELECT
    rowid, Date, AwayTeam AS team, 'away' as side,
    CASE FTR WHEN 'A' THEN 3 WHEN 'D' THEN 1 ELSE 0 END AS points,
    "AS" AS shots, AC AS corners, AF AS fouls,
    FTAG AS goals_scored,    -- Nouveau: buts marqués par l'équipe à l'extérieur
    FTHG AS goals_conceded   -- Nouveau: buts encaissés par l'équipe à l'extérieur
  FROM matches
)
```

#### CTE lagged (Étendue)
Extension avec les colonnes LAG pour les buts :
```sql
-- Ajout des colonnes LAG pour goals_scored
LAG(goals_scored, 1) OVER (PARTITION BY team ORDER BY Date) AS goals_scored_1,
LAG(goals_scored, 2) OVER (PARTITION BY team ORDER BY Date) AS goals_scored_2,
-- ... jusqu'à goals_scored_6

-- Ajout des colonnes LAG pour goals_conceded
LAG(goals_conceded, 1) OVER (PARTITION BY team ORDER BY Date) AS goals_conceded_1,
LAG(goals_conceded, 2) OVER (PARTITION BY team ORDER BY Date) AS goals_conceded_2,
-- ... jusqu'à goals_conceded_6
```

#### SELECT final (Étendu)
Inclusion des nouvelles colonnes dans la sélection finale :
```sql
-- Colonnes existantes...
h.goals_scored_1, h.goals_scored_2, ..., h.goals_scored_6,
a.goals_scored_1 AS a_goals_scored_1, ..., a.goals_scored_6 AS a_goals_scored_6,
h.goals_conceded_1, h.goals_conceded_2, ..., h.goals_conceded_6,
a.goals_conceded_1 AS a_goals_conceded_1, ..., a.goals_conceded_6 AS a_goals_conceded_6
```

### 2. Composant Python - Calcul des Moyennes

#### Interface de Calcul des Moyennes
```python
def calculate_goals_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les moyennes de buts marqués et encaissés pour les équipes à domicile et à l'extérieur
    
    Args:
        df: DataFrame contenant les colonnes LAG des buts
        
    Returns:
        DataFrame avec les nouvelles colonnes de moyennes ajoutées
    """
```

#### Implémentation
```python
# Moyennes de buts marqués
df["HomeTeam_AvgGoalsScored"] = df[["goals_scored_1", "goals_scored_2", 
                                   "goals_scored_3", "goals_scored_4", 
                                   "goals_scored_5", "goals_scored_6"]].mean(axis=1)

df["AwayTeam_AvgGoalsScored"] = df[["a_goals_scored_1", "a_goals_scored_2", 
                                   "a_goals_scored_3", "a_goals_scored_4", 
                                   "a_goals_scored_5", "a_goals_scored_6"]].mean(axis=1)

# Moyennes de buts encaissés
df["HomeTeam_AvgGoalsConceded"] = df[["goals_conceded_1", "goals_conceded_2", 
                                     "goals_conceded_3", "goals_conceded_4", 
                                     "goals_conceded_5", "goals_conceded_6"]].mean(axis=1)

df["AwayTeam_AvgGoalsConceded"] = df[["a_goals_conceded_1", "a_goals_conceded_2", 
                                     "a_goals_conceded_3", "a_goals_conceded_4", 
                                     "a_goals_conceded_5", "a_goals_conceded_6"]].mean(axis=1)
```

### 3. Composant Modèle - Mise à jour des Caractéristiques

#### Liste des Caractéristiques Numériques (Étendue)
```python
numerical_features = [
    'HomeTeam_FormScore', 'AwayTeam_FormScore',
    'HomeTeam_AvgShots', 'AwayTeam_AvgShots',
    'HomeTeam_AvgCorners', 'AwayTeam_AvgCorners',
    'HomeTeam_AvgFouls', 'AwayTeam_AvgFouls',
    'HomeTeam_AvgGoalsScored', 'AwayTeam_AvgGoalsScored',      # Nouveau
    'HomeTeam_AvgGoalsConceded', 'AwayTeam_AvgGoalsConceded'   # Nouveau
]
```

## Data Models

### Modèle de Données d'Entrée
```
matches (table SQLite existante):
- FTHG: INTEGER (Full Time Home Goals)
- FTAG: INTEGER (Full Time Away Goals)
- [autres colonnes existantes...]
```

### Modèle de Données Intermédiaires
```
team_games (CTE):
- goals_scored: INTEGER (buts marqués par l'équipe)
- goals_conceded: INTEGER (buts encaissés par l'équipe)
- [colonnes existantes...]

lagged (CTE):
- goals_scored_1 à goals_scored_6: INTEGER (LAG des buts marqués)
- goals_conceded_1 à goals_conceded_6: INTEGER (LAG des buts encaissés)
- [colonnes LAG existantes...]
```

### Modèle de Données de Sortie
```
DataFrame final:
- HomeTeam_AvgGoalsScored: FLOAT (moyenne des buts marqués par l'équipe à domicile)
- AwayTeam_AvgGoalsScored: FLOAT (moyenne des buts marqués par l'équipe à l'extérieur)
- HomeTeam_AvgGoalsConceded: FLOAT (moyenne des buts encaissés par l'équipe à domicile)
- AwayTeam_AvgGoalsConceded: FLOAT (moyenne des buts encaissés par l'équipe à l'extérieur)
- [caractéristiques existantes...]
```

## Error Handling

### Gestion des Valeurs Manquantes
1. **Équipes avec moins de 6 matchs historiques** :
   - La fonction `mean(axis=1)` de pandas gère automatiquement les valeurs NaN
   - Calcule la moyenne sur les valeurs disponibles
   - Retourne NaN si toutes les valeurs sont manquantes

2. **Validation des données** :
   - Vérification que FTHG et FTAG sont des entiers non négatifs
   - Gestion des cas où les données de buts sont manquantes dans la base

3. **Gestion des erreurs SQL** :
   - Utilisation du bloc try-except existant pour capturer les erreurs de base de données
   - Validation que les nouvelles colonnes sont correctement créées

### Stratégies de Fallback
```python
# Gestion des valeurs manquantes pour les nouvelles caractéristiques
for col in ['HomeTeam_AvgGoalsScored', 'AwayTeam_AvgGoalsScored', 
           'HomeTeam_AvgGoalsConceded', 'AwayTeam_AvgGoalsConceded']:
    if col in df.columns:
        # Remplacer les NaN par la moyenne globale ou une valeur par défaut
        df[col] = df[col].fillna(df[col].mean())
```

## Testing Strategy

### Tests Unitaires
1. **Test de la requête SQL** :
   - Vérifier que les nouvelles colonnes sont correctement créées
   - Valider la logique de mapping des buts (domicile vs extérieur)
   - Tester avec des données de test connues

2. **Test du calcul des moyennes** :
   - Vérifier les calculs de moyenne avec des données contrôlées
   - Tester la gestion des valeurs manquantes
   - Valider que les moyennes sont cohérentes

3. **Test d'intégration** :
   - Vérifier que le modèle accepte les nouvelles caractéristiques
   - Tester que les prédictions restent dans des plages raisonnables
   - Valider que les performances du modèle s'améliorent

### Tests de Validation
1. **Validation de non-fuite de données** :
   - Vérifier que seules les données des matchs précédents sont utilisées
   - Tester avec des données chronologiques pour s'assurer de l'ordre correct
   - Valider que les caractéristiques peuvent être reproduites en temps réel

2. **Tests de performance** :
   - Mesurer l'impact sur le temps d'exécution de la requête SQL
   - Évaluer l'amélioration de la précision du modèle
   - Comparer les métriques avant/après l'ajout des caractéristiques

### Métriques de Validation
- **Précision du modèle** : Accuracy, F1-score, AUC-ROC
- **Cohérence des données** : Vérification que les moyennes sont dans des plages réalistes (0-7 buts)
- **Complétude des données** : Pourcentage de valeurs non-nulles pour les nouvelles caractéristiques