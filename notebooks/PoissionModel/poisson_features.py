import pandas as pd
import numpy as np

def create_poisson_features(df, form_window=8, elo_k=20):
    """
    Create features for Poisson model based on past performance only
    """
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()
    
    # Initialize ELO ratings
    elo_ratings = {team: 1500.0 for team in teams}
    
    # Initialize team statistics
    team_stats = {team: {
        'games_played': 0, 'goals_scored': 0, 'goals_conceded': 0,
        'home_goals_scored': 0, 'home_goals_conceded': 0,
        'away_goals_scored': 0, 'away_goals_conceded': 0,
        'home_games': 0, 'away_games': 0,
        'recent_form': [], 'recent_goals_for': [], 'recent_goals_against': [],
        'recent_shots': [], 'comeback_wins': 0, 'lead_losses': 0,
        'attacking_actions': 0, 'defensive_actions': 0,
        'possession_avg': 50.0
    } for team in teams}
    
    # Initialize league averages
    league_avg_goals = {'home': df['FTHG'].mean() if 'FTHG' in df.columns else 1.5, 
                        'away': df['FTAG'].mean() if 'FTAG' in df.columns else 1.2}
    
    # Feature names for Poisson model (excluding match-specific shot data)
    poisson_features = [
        'home_attack_strength', 'away_defense_strength', 'home_form_attack',
        'away_form_defense', 'home_momentum', 'home_streak_value',
        'home_elo_rating', 'away_elo_rating', 'elo_difference',
        'home_shot_efficiency', 'away_defensive_solidity',
        'h2h_home_advantage', 'h2h_goal_tendency', 'match_importance',
        'season_stage', 'home_squad_strength'
    ]
    away_poisson_features = [
        'away_attack_strength', 'home_defense_strength', 'away_form_attack',
        'home_form_defense', 'away_momentum', 'away_streak_value',
        'away_elo_rating', 'home_elo_rating', 'elo_difference',
        'away_shot_efficiency', 'home_defensive_solidity',
        'travel_fatigue_away', 'match_importance', 'season_stage',
        'away_squad_strength'
    ]
    
    # Initialize features
    for feature in set(poisson_features + away_poisson_features):
        df[feature] = 0.0 if 'difference' in feature or 'momentum' in feature or 'streak' in feature else 1.0
    
    # Head-to-head data
    h2h_data = {}
    season_stage_weights = np.array([0.8, 0.9, 1.0, 1.1, 1.2])
    
    for idx in range(len(df)):
        row = df.iloc[idx]
        home_team, away_team = row['HomeTeam'], row['AwayTeam']
        match_date = row['Date']
        
        home_stats, away_stats = team_stats[home_team], team_stats[away_team]
        
        # Season stage
        season_progress = idx / len(df)
        season_stage = int(season_progress * 5)
        stage_weight = season_stage_weights[min(season_stage, 4)]
        
        # ELO ratings
        home_elo = elo_ratings[home_team]
        away_elo = elo_ratings[away_team]
        elo_diff = home_elo - away_elo
        
        # Basic strength
        min_games_strong = 8
        min_games_weak = 3
        
        if home_stats['home_games'] >= min_games_strong:
            home_attack = (home_stats['home_goals_scored'] / home_stats['home_games']) / league_avg_goals['home']
            home_defense = league_avg_goals['away'] / max(home_stats['home_goals_conceded'] / home_stats['home_games'], 0.1)
        elif home_stats['home_games'] >= min_games_weak:
            home_attack_home = (home_stats['home_goals_scored'] / home_stats['home_games']) / league_avg_goals['home']
            home_attack_overall = (home_stats['goals_scored'] / max(home_stats['games_played'], 1)) / ((league_avg_goals['home'] + league_avg_goals['away']) / 2)
            home_attack = 0.7 * home_attack_home + 0.3 * home_attack_overall
            home_defense_home = league_avg_goals['away'] / max(home_stats['home_goals_conceded'] / home_stats['home_games'], 0.1)
            home_defense_overall = ((league_avg_goals['home'] + league_avg_goals['away']) / 2) / max(home_stats['goals_conceded'] / max(home_stats['games_played'], 1), 0.1)
            home_defense = 0.7 * home_defense_home + 0.3 * home_defense_overall
        else:
            home_attack = home_defense = 1.0
        
        if away_stats['away_games'] >= min_games_strong:
            away_attack = (away_stats['away_goals_scored'] / away_stats['away_games']) / league_avg_goals['away']
            away_defense = league_avg_goals['home'] / max(away_stats['away_goals_conceded'] / away_stats['away_games'], 0.1)
        elif away_stats['away_games'] >= min_games_weak:
            away_attack_away = (away_stats['away_goals_scored'] / away_stats['away_games']) / league_avg_goals['away']
            away_attack_overall = (away_stats['goals_scored'] / max(away_stats['games_played'], 1)) / ((league_avg_goals['home'] + league_avg_goals['away']) / 2)
            away_attack = 0.7 * away_attack_away + 0.3 * away_attack_overall
            home_defense_away = league_avg_goals['home'] / max(away_stats['away_goals_conceded'] / away_stats['away_games'], 0.1)
            home_defense_overall = ((league_avg_goals['home'] + league_avg_goals['away']) / 2) / max(away_stats['goals_conceded'] / max(away_stats['games_played'], 1), 0.1)
            away_defense = 0.7 * home_defense_away + 0.3 * home_defense_overall
        else:
            away_attack = away_defense = 1.0
        
        # Form-based strength
        form_decay = 0.9
        if len(home_stats['recent_goals_for']) >= 4:
            weights = np.array([form_decay**i for i in range(len(home_stats['recent_goals_for']))][::-1])
            recent_goals_for = np.array(home_stats['recent_goals_for'][-form_window:])
            recent_goals_against = np.array(home_stats['recent_goals_against'][-form_window:])
            w_subset = weights[-len(recent_goals_for):]
            home_form_attack = np.average(recent_goals_for, weights=w_subset) / league_avg_goals['home']
            home_form_defense = league_avg_goals['away'] / max(np.average(recent_goals_against, weights=w_subset), 0.1)
        else:
            home_form_attack = home_attack
            home_form_defense = home_defense
        
        if len(away_stats['recent_goals_for']) >= 4:
            weights = np.array([form_decay**i for i in range(len(away_stats['recent_goals_for']))][::-1])
            recent_goals_for = np.array(away_stats['recent_goals_for'][-form_window:])
            recent_goals_against = np.array(away_stats['recent_goals_against'][-form_window:])
            w_subset = weights[-len(recent_goals_for):]
            away_form_attack = np.average(recent_goals_for, weights=w_subset) / league_avg_goals['away']
            away_form_defense = league_avg_goals['home'] / max(np.average(recent_goals_against, weights=w_subset), 0.1)
        else:
            away_form_attack = away_attack
            away_form_defense = away_defense
        
        # Momentum and streak
        home_momentum = away_momentum = 0.0
        if len(home_stats['recent_form']) >= 3:
            weights = np.array([0.5, 0.3, 0.2][-len(home_stats['recent_form'][-3:]):])
            home_momentum = np.average(home_stats['recent_form'][-3:], weights=weights)
        
        if len(away_stats['recent_form']) >= 3:
            weights = np.array([0.5, 0.3, 0.2][-len(away_stats['recent_form'][-3:]):])
            away_momentum = np.average(away_stats['recent_form'][-3:], weights=weights)
        
        home_streak = away_streak = 0.0
        if len(home_stats['recent_form']) >= 2:
            recent_results = home_stats['recent_form'][-5:]
            if len(recent_results) >= 2:
                if all(r >= 0.5 for r in recent_results[-3:]):
                    home_streak = 0.2
                elif all(r == 1.0 for r in recent_results[-2:]):
                    home_streak = 0.3
                elif all(r == 0.0 for r in recent_results[-2:]):
                    home_streak = -0.2
        if len(away_stats['recent_form']) >= 2:
            recent_results = away_stats['recent_form'][-5:]
            if len(recent_results) >= 2:
                if all(r >= 0.5 for r in recent_results[-3:]):
                    away_streak = 0.2
                elif all(r == 1.0 for r in recent_results[-2:]):
                    away_streak = 0.3
                elif all(r == 0.0 for r in recent_results[-2:]):
                    away_streak = -0.2
        
        # Shot efficiency and defensive solidity (using goals instead of shots)
        home_shot_eff = home_stats['goals_scored'] / max(home_stats['games_played'], 1)
        away_shot_eff = away_stats['goals_scored'] / max(away_stats['games_played'], 1)
        home_def_solid = 1.0 - (home_stats['goals_conceded'] / max(home_stats['games_played'], 1))
        away_def_solid = 1.0 - (away_stats['goals_conceded'] / max(away_stats['games_played'], 1))
        
        # Head-to-head
        h2h_key = f"{home_team}_vs_{away_team}"
        h2h_home_adv = goal_tendency = 0.0
        if h2h_key in h2h_data and h2h_data[h2h_key]['games'] >= 3:
            h2h_stats = h2h_data[h2h_key]
            h2h_home_adv = (h2h_stats['home_wins'] / h2h_stats['games']) - 0.33
            goal_tendency = h2h_stats['avg_goals'] - (league_avg_goals['home'] + league_avg_goals['away'])
        
        # Squad strength (placeholder)
        home_squad = away_squad = 1.0
        
        # Assign features
        smoothing = 0.9
        df.at[idx, 'home_attack_strength'] = smoothing * home_attack + (1-smoothing)
        df.at[idx, 'home_defense_strength'] = smoothing * home_defense + (1-smoothing)
        df.at[idx, 'away_attack_strength'] = smoothing * away_attack + (1-smoothing)
        df.at[idx, 'away_defense_strength'] = smoothing * away_defense + (1-smoothing)
        df.at[idx, 'home_form_attack'] = smoothing * home_form_attack + (1-smoothing)
        df.at[idx, 'home_form_defense'] = smoothing * home_form_defense + (1-smoothing)
        df.at[idx, 'away_form_attack'] = smoothing * away_form_attack + (1-smoothing)
        df.at[idx, 'away_form_defense'] = smoothing * away_form_defense + (1-smoothing)
        df.at[idx, 'home_momentum'] = home_momentum
        df.at[idx, 'away_momentum'] = away_momentum
        df.at[idx, 'home_streak_value'] = home_streak
        df.at[idx, 'away_streak_value'] = away_streak
        df.at[idx, 'home_elo_rating'] = home_elo / 2000.0
        df.at[idx, 'away_elo_rating'] = away_elo / 2000.0
        df.at[idx, 'elo_difference'] = elo_diff / 500.0
        df.at[idx, 'home_shot_efficiency'] = np.clip(home_shot_eff, 0, 2)
        df.at[idx, 'away_shot_efficiency'] = np.clip(away_shot_eff, 0, 2)
        df.at[idx, 'home_defensive_solidity'] = np.clip(home_def_solid, 0, 1)
        df.at[idx, 'away_defensive_solidity'] = np.clip(away_def_solid, 0, 1)
        df.at[idx, 'h2h_home_advantage'] = h2h_home_adv
        df.at[idx, 'h2h_goal_tendency'] = goal_tendency
        df.at[idx, 'match_importance'] = stage_weight
        df.at[idx, 'season_stage'] = season_stage / 4.0
        df.at[idx, 'home_squad_strength'] = home_squad
        df.at[idx, 'away_squad_strength'] = away_squad
        df.at[idx, 'travel_fatigue_away'] = 1.0
        
        # Update statistics only if match has results
        if idx < len(df) - 1 and pd.notna(row.get('FTHG')) and pd.notna(row.get('FTAG')):
            home_goals, away_goals = row['FTHG'], row['FTAG']
            home_shots = home_goals * 5  # Estimate shots based on goals
            away_shots = away_goals * 5
            
            # Update ELO
            expected_home = 1 / (1 + 10**((away_elo - home_elo - 100)/400))
            actual_home = 1.0 if home_goals > away_goals else 0.5 if home_goals == away_goals else 0.0
            elo_ratings[home_team] += elo_k * (actual_home - expected_home)
            elo_ratings[away_team] += elo_k * (expected_home - actual_home)
            elo_ratings[home_team] = np.clip(elo_ratings[home_team], 800, 2200)
            elo_ratings[away_team] = np.clip(elo_ratings[away_team], 800, 2200)
            
            # Update results
            home_result = actual_home
            away_result = 1.0 - actual_home if home_goals != away_goals else 0.5
            
            # Update stats
            home_stats['games_played'] += 1
            home_stats['goals_scored'] += home_goals
            home_stats['goals_conceded'] += away_goals
            home_stats['home_goals_scored'] += home_goals
            home_stats['home_goals_conceded'] += away_goals
            home_stats['home_games'] += 1
            away_stats['games_played'] += 1
            away_stats['goals_scored'] += away_goals
            away_stats['goals_conceded'] += home_goals
            away_stats['away_goals_scored'] += away_goals
            away_stats['away_goals_conceded'] += home_goals
            home_stats['attacking_actions'] += home_shots
            home_stats['defensive_actions'] += max(away_shots - away_goals, 0)
            away_stats['attacking_actions'] += away_shots
            away_stats['defensive_actions'] += max(home_shots - home_goals, 0)
            
            # Update form
            home_stats['recent_form'].append(home_result)
            home_stats['recent_goals_for'].append(home_goals)
            home_stats['recent_goals_against'].append(away_goals)
            home_stats['recent_shots'].append(home_shots)
            away_stats['recent_form'].append(away_result)
            away_stats['recent_goals_for'].append(away_goals)
            away_stats['recent_goals_against'].append(home_goals)
            away_stats['recent_shots'].append(away_shots)
            
            # Maintain sliding windows
            max_history = form_window * 3
            for stat_type in ['recent_form', 'recent_goals_for', 'recent_goals_against', 'recent_shots']:
                if len(home_stats[stat_type]) > max_history:
                    home_stats[stat_type] = home_stats[stat_type][-max_history:]
                if len(away_stats[stat_type]) > max_history:
                    away_stats[stat_type] = away_stats[stat_type][-max_history:]
            
            # Update head-to-head
            h2h_key = f"{home_team}_vs_{away_team}"
            reverse_key = f"{away_team}_vs_{home_team}"
            for key in [h2h_key, reverse_key]:
                if key not in h2h_data:
                    h2h_data[key] = {'games': 0, 'home_wins': 0, 'recent_results': [], 'total_goals': 0, 'avg_goals': 0}
            h2h_data[h2h_key]['games'] += 1
            h2h_data[reverse_key]['games'] += 1
            h2h_data[h2h_key]['total_goals'] += (home_goals + away_goals)
            h2h_data[reverse_key]['total_goals'] += (home_goals + away_goals)
            if home_goals > away_goals:
                h2h_data[h2h_key]['home_wins'] += 1
                h2h_data[h2h_key]['recent_results'].append(1.0)
                h2h_data[reverse_key]['recent_results'].append(0.0)
            elif home_goals == away_goals:
                h2h_data[h2h_key]['recent_results'].append(0.5)
                h2h_data[reverse_key]['recent_results'].append(0.5)
            else:
                h2h_data[reverse_key]['home_wins'] += 1
                h2h_data[h2h_key]['recent_results'].append(0.0)
                h2h_data[reverse_key]['recent_results'].append(1.0)
            for key in [h2h_key, reverse_key]:
                h2h_data[key]['avg_goals'] = h2h_data[key]['total_goals'] / h2h_data[key]['games']
                if len(h2h_data[key]['recent_results']) > 6:
                    h2h_data[key]['recent_results'] = h2h_data[key]['recent_results'][-6:]
    
    print(f"Created {len(set(poisson_features + away_poisson_features))} features for Poisson model")
    return df, league_avg_goals

def prepare_poisson_features(df, league_avg_goals, feature_names=None):
    """
    Prepare feature matrices for Poisson models, using specified feature names if provided
    """
    poisson_features = [
        'home_attack_strength', 'away_defense_strength', 'home_form_attack',
        'away_form_defense', 'home_momentum', 'home_streak_value',
        'home_elo_rating', 'away_elo_rating', 'elo_difference',
        'home_shot_efficiency', 'away_defensive_solidity',
        'h2h_home_advantage', 'h2h_goal_tendency', 'match_importance',
        'season_stage', 'home_squad_strength'
    ]
    away_poisson_features = [
        'away_attack_strength', 'home_defense_strength', 'away_form_attack',
        'home_form_defense', 'away_momentum', 'away_streak_value',
        'away_elo_rating', 'home_elo_rating', 'elo_difference',
        'away_shot_efficiency', 'home_defensive_solidity',
        'travel_fatigue_away', 'match_importance', 'season_stage',
        'away_squad_strength'
    ]
    
    # Use provided feature names or default
    poisson_features = feature_names['home'] if feature_names and 'home' in feature_names else poisson_features
    away_poisson_features = feature_names['away'] if feature_names and 'away' in feature_names else away_poisson_features
    
    X_poisson_home = df[poisson_features].copy()
    X_poisson_away = df[away_poisson_features].copy()
    
    for df_temp in [X_poisson_home, X_poisson_away]:
        for col in df_temp.columns:
            if 'efficiency' in col or 'strength' in col:
                df_temp[col] = df_temp[col].fillna(1.0)
            elif 'momentum' in col or 'streak' in col or 'difference' in col:
                df_temp[col] = df_temp[col].fillna(0.0)
            else:
                df_temp[col] = df_temp[col].fillna(df_temp[col].median() if df_temp[col].notna().sum() > 0 else 0.0)
    
    return X_poisson_home, X_poisson_away, {'home': poisson_features, 'away': away_poisson_features}