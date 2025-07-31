from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta
import joblib
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

DATABASE_URL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "football.db")
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models", "best_xgboost_model.pkl")

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row # This allows accessing columns by name
        logger.info("Database connection successful.")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

def load_model():
    """Load trained model"""
    try:
        model = joblib.load(MODEL_PATH)
        logger.info("Model loaded successfully.")
        return model
    except FileNotFoundError:
        logger.error(f"Error: Model file not found at {MODEL_PATH}")
        return None

def get_historical_data(conn, teams):
    """Get historical data for relevant teams"""
    placeholders = ', '.join(['?'] * len(teams))
    query = f"""
    SELECT * FROM matches 
    WHERE HomeTeam IN ({placeholders}) OR AwayTeam IN ({placeholders})
    ORDER BY Date DESC
    LIMIT 100
    """
    df = pd.read_sql_query(query, conn, params=teams*2)
    logger.info(f"Retrieved {len(df)} rows of historical data for teams: {teams}")
    return df

def calculate_features(team, df, side):
    """Calculate features for given team"""
    team_df = df[(df['HomeTeam'] == team) | (df['AwayTeam'] == team)]
    
    # Calculate averages for last 6 matches
    features = {}
    for stat in ['FTHG', 'FTAG', 'HS', 'AS', 'HC', 'AC', 'HF', 'AF']:
        vals = team_df.head(6)[stat].tolist()
        for i in range(1, 7):
            features[f'{stat}_{i}'] = vals[i-1] if i <= len(vals) else 0
    
    # Calculate form scores
    points = []
    for _, row in team_df.head(6).iterrows():
        if row['HomeTeam'] == team:
            points.append(3 if row['FTR'] == 'H' else (1 if row['FTR'] == 'D' else 0))
        else:
            points.append(3 if row['FTR'] == 'A' else (1 if row['FTR'] == 'D' else 0))
    
    weights = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1]
    form_score = sum(p * w for p, w in zip(points[:6], weights)) / 9.3 * 10
    
    return {
        f'{side}_FormScore': form_score,
        f'{side}_AvgGoalsScored': sum(features[f'FTHG_{i}'] for i in range(1,7)) / 6,
        f'{side}_AvgGoalsConceded': sum(features[f'FTAG_{i}'] for i in range(1,7)) / 6,
        f'{side}_AvgShots': sum(features[f'HS_{i}'] for i in range(1,7)) / 6,
        f'{side}_AvgCorners': sum(features[f'HC_{i}'] for i in range(1,7)) / 6,
        f'{side}_AvgFouls': sum(features[f'HF_{i}'] for i in range(1,7)) / 6
    }

def prepare_features(upcoming_matches, historical_data):
    """Prepare features for prediction"""
    features_list = []
    
    for _, row in upcoming_matches.iterrows():
        home_features = calculate_features(row['HomeTeam'], historical_data, 'HomeTeam')
        away_features = calculate_features(row['AwayTeam'], historical_data, 'AwayTeam')
        features = {**home_features, **away_features}
        features_list.append(features)
    
    logger.info(f"Prepared features for {len(features_list)} matches.")
    return pd.DataFrame(features_list)

@app.get("/matches/upcoming")
async def get_upcoming_matches():
    logger.info("Received request for /matches/upcoming")
    try:
        conn = get_db_connection()
        
        # Calculate next weekend dates (Friday to Sunday)
        today = datetime.now()
        next_friday = (today + timedelta(days=(4 - today.weekday()) % 7)).strftime('%Y-%m-%d')
        next_saturday = (today + timedelta(days=(5 - today.weekday()) % 7)).strftime('%Y-%m-%d')
        next_sunday = (today + timedelta(days=(6 - today.weekday()) % 7)).strftime('%Y-%m-%d')
        
        query = f"""
        SELECT Date, HomeTeam, AwayTeam FROM calendar
        WHERE Date IN ('{next_friday}', '{next_saturday}', '{next_sunday}')
        ORDER BY Date ASC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        logger.info(f"Found {len(df)} upcoming matches.")
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error in /matches/upcoming: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
async def predict_match_outcome(match_data: dict):
    logger.info(f"Received request for /predict with data: {match_data}")
    model = load_model()
    if model is None:
        raise HTTPException(status_code=500, detail="ML model not loaded. Check server logs.")

    try:
        # Convert input match_data to DataFrame for feature preparation
        # Assuming match_data contains 'HomeTeam' and 'AwayTeam'
        # and other necessary fields for calculate_features if not directly provided
        upcoming_match_df = pd.DataFrame([match_data])

        conn = get_db_connection()
        teams = [match_data['HomeTeam'], match_data['AwayTeam']]
        historical_data = get_historical_data(conn, teams)
        conn.close()

        if historical_data.empty:
            logger.warning("Not enough historical data for prediction.")
            raise HTTPException(status_code=400, detail="Not enough historical data for prediction.")

        features_df = prepare_features(upcoming_match_df, historical_data)
        
        # Make prediction
        probabilities = model.predict_proba(features_df)
        prediction = model.classes_[np.argmax(probabilities)]
        
        result = {"prediction": prediction, "probabilities": probabilities.tolist()[0]}
        logger.info(f"Prediction successful: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in /predict: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# To run the FastAPI application, use the following command in your terminal:
# uvicorn src.api.main:app --reload
# This will start the server at http://127.0.0.1:8000
