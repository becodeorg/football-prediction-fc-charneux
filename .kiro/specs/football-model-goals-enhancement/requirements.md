# Requirements Document

## Introduction

Cette fonctionnalité vise à améliorer le modèle de prédiction de football en intégrant des caractéristiques basées sur les moyennes de buts marqués et encaissés des équipes sur leurs matchs précédents. L'objectif est de remplacer l'utilisation des scores réels (HS, AS) qui ne sont pas disponibles avant un match, par des données historiques pertinentes qui respectent la contrainte temporelle et évitent la fuite de données.

## Requirements

### Requirement 1

**User Story:** En tant que data scientist, je veux intégrer les données de buts historiques dans la requête SQL, afin que le modèle puisse utiliser les performances offensives et défensives passées des équipes.

#### Acceptance Criteria

1. WHEN la requête SQL est exécutée THEN le système SHALL inclure les colonnes FTHG et FTAG dans la CTE team_games
2. WHEN une équipe joue à domicile THEN le système SHALL assigner FTHG comme goals_scored et FTAG comme goals_conceded
3. WHEN une équipe joue à l'extérieur THEN le système SHALL assigner FTAG comme goals_scored et FTHG comme goals_conceded
4. WHEN les données sont extraites THEN le système SHALL créer des colonnes LAG pour goals_scored et goals_conceded sur les 6 derniers matchs

### Requirement 2

**User Story:** En tant que data scientist, je veux calculer les moyennes de buts sur les matchs précédents, afin d'obtenir des indicateurs de performance offensive et défensive pour chaque équipe.

#### Acceptance Criteria

1. WHEN les données sont chargées en Python THEN le système SHALL calculer HomeTeam_AvgGoalsScored basé sur la moyenne des 6 derniers matchs
2. WHEN les données sont chargées en Python THEN le système SHALL calculer AwayTeam_AvgGoalsScored basé sur la moyenne des 6 derniers matchs
3. WHEN les données sont chargées en Python THEN le système SHALL calculer HomeTeam_AvgGoalsConceded basé sur la moyenne des 6 derniers matchs
4. WHEN les données sont chargées en Python THEN le système SHALL calculer AwayTeam_AvgGoalsConceded basé sur la moyenne des 6 derniers matchs
5. WHEN les moyennes sont calculées THEN le système SHALL gérer les valeurs manquantes pour les équipes avec moins de 6 matchs historiques

### Requirement 3

**User Story:** En tant que data scientist, je veux inclure les nouvelles caractéristiques de buts dans le modèle d'entraînement, afin d'améliorer la précision des prédictions sans introduire de fuite de données.

#### Acceptance Criteria

1. WHEN les caractéristiques sont définies THEN le système SHALL ajouter HomeTeam_AvgGoalsScored à la liste numerical_features
2. WHEN les caractéristiques sont définies THEN le système SHALL ajouter AwayTeam_AvgGoalsScored à la liste numerical_features
3. WHEN les caractéristiques sont définies THEN le système SHALL ajouter HomeTeam_AvgGoalsConceded à la liste numerical_features
4. WHEN les caractéristiques sont définies THEN le système SHALL ajouter AwayTeam_AvgGoalsConceded à la liste numerical_features
5. WHEN le modèle est entraîné THEN le système SHALL utiliser ces nouvelles caractéristiques sans accéder aux scores du match actuel

### Requirement 4

**User Story:** En tant que data scientist, je veux valider que les modifications n'introduisent pas de fuite de données, afin de garantir que le modèle reste réaliste pour des prédictions en temps réel.

#### Acceptance Criteria

1. WHEN les données sont préparées THEN le système SHALL s'assurer qu'aucune information du match actuel n'est utilisée
2. WHEN les caractéristiques LAG sont créées THEN le système SHALL utiliser uniquement les matchs précédents dans l'ordre chronologique
3. WHEN le modèle fait des prédictions THEN le système SHALL pouvoir reproduire les mêmes caractéristiques avec des données disponibles avant le match
4. IF une équipe a moins de 6 matchs historiques THEN le système SHALL calculer la moyenne sur les matchs disponibles ou utiliser une valeur par défaut appropriée