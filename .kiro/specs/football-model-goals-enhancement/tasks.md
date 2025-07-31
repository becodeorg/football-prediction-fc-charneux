# Implementation Plan

- [x] 1. Modifier la requête SQL pour inclure les données de buts



  - Étendre la CTE team_games pour ajouter les colonnes goals_scored et goals_conceded basées sur FTHG et FTAG
  - Ajouter la logique de mapping correct selon que l'équipe joue à domicile ou à l'extérieur
  - _Requirements: 1.1, 1.2, 1.3_


- [ ] 2. Ajouter les colonnes LAG pour les buts dans la CTE lagged
  - Créer les colonnes LAG goals_scored_1 à goals_scored_6 pour chaque équipe
  - Créer les colonnes LAG goals_conceded_1 à goals_conceded_6 pour chaque équipe
  - Utiliser la même logique de fenêtrage que les autres caractéristiques existantes
  - _Requirements: 1.4_


- [ ] 3. Étendre la clause SELECT finale pour inclure les nouvelles colonnes LAG
  - Ajouter les colonnes goals_scored_X pour l'équipe à domicile (h.)
  - Ajouter les colonnes goals_scored_X pour l'équipe à l'extérieur avec préfixe a_
  - Ajouter les colonnes goals_conceded_X pour l'équipe à domicile (h.)
  - Ajouter les colonnes goals_conceded_X pour l'équipe à l'extérieur avec préfixe a_

  - _Requirements: 1.4_

- [ ] 4. Implémenter le calcul des moyennes de buts en Python
  - Ajouter le calcul de HomeTeam_AvgGoalsScored basé sur les 6 colonnes LAG
  - Ajouter le calcul de AwayTeam_AvgGoalsScored basé sur les 6 colonnes LAG avec préfixe a_
  - Ajouter le calcul de HomeTeam_AvgGoalsConceded basé sur les 6 colonnes LAG

  - Ajouter le calcul de AwayTeam_AvgGoalsConceded basé sur les 6 colonnes LAG avec préfixe a_
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 5. Mettre à jour la liste des caractéristiques numériques
  - Ajouter HomeTeam_AvgGoalsScored à la liste numerical_features
  - Ajouter AwayTeam_AvgGoalsScored à la liste numerical_features


  - Ajouter HomeTeam_AvgGoalsConceded à la liste numerical_features
  - Ajouter AwayTeam_AvgGoalsConceded à la liste numerical_features
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 6. Ajouter la gestion des valeurs manquantes pour les nouvelles caractéristiques
  - Implémenter une stratégie de gestion des NaN pour les équipes avec moins de 6 matchs
  - Ajouter une validation que les nouvelles colonnes sont correctement créées
  - Tester que les moyennes sont dans des plages réalistes (0-7 buts)
  - _Requirements: 2.5, 4.4_

- [ ] 7. Valider l'absence de fuite de données
  - Vérifier que la requête SQL utilise uniquement les données des matchs précédents
  - Tester avec quelques exemples manuels que les calculs LAG sont corrects chronologiquement
  - Valider que les nouvelles caractéristiques peuvent être reproduites avec des données disponibles avant le match
  - _Requirements: 4.1, 4.2, 4.3_

- [ ] 8. Tester et valider l'amélioration du modèle
  - Exécuter le notebook complet avec les nouvelles caractéristiques
  - Comparer les métriques de performance du modèle avant/après l'ajout des caractéristiques de buts
  - Vérifier que le modèle s'entraîne correctement avec les nouvelles caractéristiques
  - Sauvegarder le modèle amélioré avec les nouvelles caractéristiques
  - _Requirements: 3.5_