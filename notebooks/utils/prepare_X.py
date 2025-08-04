import pandas as pd
import numpy as np

def prepare_X(df_X, rolling_window: int, using_odds: bool):

    # Copy and sort dataset chronologically
    df_raw = df_X.copy()
    df_raw = df_raw.sort_values('Date').reset_index(drop=True)
    df_raw['rowid'] = df_raw.index  # Unique ID to merge later

    # Home team features
    home_df = df_raw[['rowid', 'Date', 'HomeTeam', 'HS', 'HST', 'HC', 'HF', 'HY', 'HR', 'FTHG', 'FTAG']].copy()
    home_df['team'] = home_df['HomeTeam']
    home_df['side'] = 'home'
    home_df['points'] = (home_df['FTHG'] > home_df['FTAG']).astype(int)*3 + (home_df['FTHG'] == home_df['FTAG']).astype(int)*1
    home_df = home_df.rename(columns={
        'HS': 'shots', 'HST': 'shots_on_target',
        'HC': 'corners', 'HF': 'fouls',
        'HY': 'yellow_cards', 'HR': 'red_cards',
        'FTHG': 'goals_scored', 'FTAG': 'goals_conceded'
    })

    # Away team features
    away_df = df_raw[['rowid', 'Date', 'AwayTeam', 'AS', 'AST', 'AC', 'AF', 'AY', 'AR', 'FTAG', 'FTHG']].copy()
    away_df['team'] = away_df['AwayTeam']
    away_df['side'] = 'away'
    away_df['points'] = (away_df['FTAG'] > away_df['FTHG']).astype(int)*3 + (away_df['FTAG'] == away_df['FTHG']).astype(int)*1
    away_df = away_df.rename(columns={
        'AS': 'shots', 'AST': 'shots_on_target',
        'AC': 'corners', 'AF': 'fouls',
        'AY': 'yellow_cards', 'AR': 'red_cards',
        'FTAG': 'goals_scored', 'FTHG': 'goals_conceded'
    })

    # Combine and sort
    team_games = pd.concat([
        home_df[['rowid', 'Date', 'team', 'side', 'points', 'shots', 'shots_on_target',
                    'corners', 'fouls', 'yellow_cards', 'red_cards', 'goals_scored', 'goals_conceded']],
        away_df[['rowid', 'Date', 'team', 'side', 'points', 'shots', 'shots_on_target',
                    'corners', 'fouls', 'yellow_cards', 'red_cards', 'goals_scored', 'goals_conceded']]
    ])
    team_games = team_games.sort_values(by=['team', 'Date'])

    # Weight setup
    weights = np.arange(1, rolling_window + 1)
    weights = weights / weights.sum()

    def weighted_avg(series, weights_array):
        w = weights_array[-len(series):]
        return np.dot(series, w)

    # Form Score (weighted Averages)
    team_games['form_score'] = (
        team_games.groupby('team')['points']
        .apply(lambda x: x.shift(1).rolling(window=rolling_window, min_periods=rolling_window)
                .apply(lambda y: weighted_avg(y, weights), raw=True))
        .reset_index(level=0, drop=True)
    )

    # Other stats (weighted Averages)
    for col in ['shots', 'shots_on_target', 'corners', 'fouls',
                'yellow_cards', 'red_cards', 'goals_scored', 'goals_conceded']:
        team_games[f'avg_{col}'] = (
            team_games.groupby('team')[col]
            .apply(lambda x: x.shift(1).rolling(window=rolling_window, min_periods=rolling_window)
                    .apply(lambda y: weighted_avg(y, weights), raw=True))
            .reset_index(level=0, drop=True)
        )

    # Split home/away features
    home_features = team_games[team_games['side'] == 'home'].copy()
    away_features = team_games[team_games['side'] == 'away'].copy()

    # Merge back to original data
    df_enriched = df_raw.merge(home_features[[
        'rowid', 'form_score', 'avg_shots', 'avg_shots_on_target', 'avg_corners',
        'avg_fouls', 'avg_yellow_cards', 'avg_red_cards',
        'avg_goals_scored', 'avg_goals_conceded'
    ]], on='rowid', how='left').rename(columns={
        'form_score': 'HomeTeam_FormScore',
        'avg_shots': 'HomeTeam_AvgShots',
        'avg_shots_on_target': 'HomeTeam_AvgShotsOnTarget',
        'avg_corners': 'HomeTeam_AvgCorners',
        'avg_fouls': 'HomeTeam_AvgFouls',
        'avg_yellow_cards': 'HomeTeam_AvgYellowCards',
        'avg_red_cards': 'HomeTeam_AvgRedCards',
        'avg_goals_scored': 'HomeTeam_AvgGoalsScored',
        'avg_goals_conceded': 'HomeTeam_AvgGoalsConceded'
    })

    df_enriched = df_enriched.merge(away_features[[
        'rowid', 'form_score', 'avg_shots', 'avg_shots_on_target', 'avg_corners',
        'avg_fouls', 'avg_yellow_cards', 'avg_red_cards',
        'avg_goals_scored', 'avg_goals_conceded'
    ]], on='rowid', how='left').rename(columns={
        'form_score': 'AwayTeam_FormScore',
        'avg_shots': 'AwayTeam_AvgShots',
        'avg_shots_on_target': 'AwayTeam_AvgShotsOnTarget',
        'avg_corners': 'AwayTeam_AvgCorners',
        'avg_fouls': 'AwayTeam_AvgFouls',
        'avg_yellow_cards': 'AwayTeam_AvgYellowCards',
        'avg_red_cards': 'AwayTeam_AvgRedCards',
        'avg_goals_scored': 'AwayTeam_AvgGoalsScored',
        'avg_goals_conceded': 'AwayTeam_AvgGoalsConceded'
    })

    if using_odds == True:
        LDA_features = ['HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'HomeTeam_FormScore', 'AwayTeam_FormScore', 'HomeTeam_AvgRedCards', 'AwayTeam_AvgRedCards', 'HomeTeam_AvgGoalsScored', 'AwayTeam_AvgGoalsScored']
        df_X_prepared = df_enriched[LDA_features]
    else:
        RC_features = ['HomeTeam', 'AwayTeam', 'HomeTeam_FormScore', 'AwayTeam_FormScore', 'HomeTeam_AvgShots', 'AwayTeam_AvgShots', 'HomeTeam_AvgFouls', 'AwayTeam_AvgFouls', 'HomeTeam_AvgRedCards', 'AwayTeam_AvgRedCards']
        df_X_prepared = df_enriched[RC_features]

    return df_X_prepared