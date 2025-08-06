import pandas as pd
import numpy as np
import sqlite3
from poisson_features import create_poisson_features, prepare_poisson_features
from poisson_model import PoissonFootballPredictor

def predict_new_matches(historical_db_path, new_matches_path, model_path="poisson_model.pkl"):
    """
    Predict probabilities for new matches using historical data for feature calculation.
    
    Parameters:
    - historical_data_path: Path to db with historical match data (includes FTHG, FTAG, etc.)
    - new_matches_path: Path to csv with new matches (Date, HomeTeam, AwayTeam only)
    - model_path: Path to saved Poisson model
    """
    # Load historical data
    conn = sqlite3.connect(historical_db_path)
    historical_df = pd.read_sql_query("SELECT * FROM matches", conn)

    # Load new matches
    new_matches_df = pd.read_csv(new_matches_path)
    
    # Validate new matches columns
    required_columns = ['Date', 'HomeTeam', 'AwayTeam']
    if not all(col in new_matches_df.columns for col in required_columns):
        raise ValueError("New matches CSV must contain 'Date', 'HomeTeam', and 'AwayTeam' columns")
    
    # Ensure Date is in datetime format
    new_matches_df['Date'] = pd.to_datetime(new_matches_df['Date'])
    historical_df['Date'] = pd.to_datetime(historical_df['Date'])
    
    # Filter historical data to include only matches before the earliest new match date
    min_new_date = new_matches_df['Date'].min()
    historical_df = historical_df[historical_df['Date'] < min_new_date].copy()
    
    if historical_df.empty:
        raise ValueError("No historical data available before the earliest new match date")
    
    # Create features for historical data to update team statistics
    print("Creating features from historical data...")
    historical_df_featured, league_avg_goals = create_poisson_features(historical_df)
    
    # Append new matches to historical data for feature calculation
    # Add placeholder columns for new matches (FTHG, FTAG, FTR will be NaN)
    for col in ['FTHG', 'FTAG', 'FTR']:
        if col not in new_matches_df.columns:
            new_matches_df[col] = np.nan
    
    # Combine datasets
    combined_df = pd.concat([historical_df, new_matches_df], ignore_index=True)
    combined_df = combined_df.sort_values('Date').reset_index(drop=True)
    
    # Load model to get feature names
    print("Loading Poisson model...")
    predictor = PoissonFootballPredictor()
    predictor.load_model(model_path)
    
    # Recalculate features for the combined dataset using training feature names
    print("Creating features for new matches...")
    combined_df_featured, _ = create_poisson_features(combined_df)
    
    # Extract features for new matches only
    new_matches_featured = combined_df_featured[combined_df_featured['Date'].isin(new_matches_df['Date'])]
    
    # Prepare features using the same feature names as training
    X_ph, X_pa, _ = prepare_poisson_features(new_matches_featured, league_avg_goals, feature_names=predictor.feature_names)
    
    # Predict probabilities
    print("\nPredicting probabilities...")
    probabilities = predictor.predict_probabilities(X_ph, X_pa)
    
    # Format results
    results = pd.DataFrame({
        'Date': new_matches_df['Date'],
        'HomeTeam': new_matches_df['HomeTeam'],
        'AwayTeam': new_matches_df['AwayTeam'],
        'HomeWinProb': probabilities[:, 0],
        'DrawProb': probabilities[:, 1],
        'AwayWinProb': probabilities[:, 2]
    })
    
    print("\nPrediction Results:")
    print(results.to_string(index=False))
    
    # Save predictions to CSV
    output_path = new_matches_path.replace('.csv', '_predictions.csv')
    results.to_csv(output_path, index=False)
    print(f"\nPredictions saved to {output_path}")
    
    return results

if __name__ == "__main__":
    historical_db_path = "C:/Users/yinmi/Becode_projects/football-prediction-fc-charneux/football.db"
    new_matches_path = "C:/Users/yinmi/Becode_projects/football-prediction-fc-charneux/notebooks/PoissionModel/new_matches.csv"
    predict_new_matches(historical_db_path, new_matches_path)