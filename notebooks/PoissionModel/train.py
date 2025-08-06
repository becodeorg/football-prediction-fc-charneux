import pandas as pd
import sqlite3
from poisson_features import create_poisson_features, prepare_poisson_features
from poisson_model import PoissonFootballPredictor
from evaluation import calculate_brier_score

def train_and_evaluate(db_path, model_output_path="poisson_model.pkl"):
    """
    Train and evaluate the Poisson model, save to pickle
    """
    # Load data
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM matches", conn)
    
    # Create features
    print("Creating Poisson features...")
    df_featured, league_avg_goals = create_poisson_features(df)
    
    # Split data
    split_point = int(0.85 * len(df_featured))
    df_train = df_featured[:split_point]
    df_test = df_featured[split_point:]
    
    print(f"Training samples: {len(df_train)}")
    print(f"Test samples: {len(df_test)}")
    
    # Prepare features
    X_train_ph, X_train_pa, feature_names = prepare_poisson_features(df_train, league_avg_goals)
    X_test_ph, X_test_pa, _ = prepare_poisson_features(df_test, league_avg_goals, feature_names=feature_names)
    
    print(f"Feature dimensions: Poisson Home={X_train_ph.shape[1]}, Poisson Away={X_train_pa.shape[1]}")
    
    # Get target variables
    y_train_home = df_train['FTHG'].values
    y_train_away = df_train['FTAG'].values
    y_test_result = df_test['FTR'].values
    
    # Train model
    predictor = PoissonFootballPredictor()
    predictor.league_avg_goals = league_avg_goals
    predictor.train(X_train_ph, X_train_pa, y_train_home, y_train_away)
    
    # Evaluate on test set
    print("\nEvaluating Poisson model...")
    probabilities = predictor.predict_probabilities(X_test_ph, X_test_pa)
    brier_score, brier_scores = calculate_brier_score(y_test_result, probabilities)
    
    # Save model
    predictor.save_model(model_output_path)
    
    return brier_score, probabilities

if __name__ == "__main__":
    db_path = "C:/Users/yinmi/Becode_projects/football-prediction-fc-charneux/football.db"
    brier_score, predictions = train_and_evaluate(db_path=db_path)