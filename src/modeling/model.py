import sqlite3
import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model():
    db_path = 'football.db'
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM matches", conn)
    conn.close()

    # Basic cleaning and target definition
    df = df.dropna(subset=['HomeTeam', 'AwayTeam', 'FTR'])
    X = df[['HomeTeam', 'AwayTeam', 'HS', 'AS']]
    y = df['FTR']

    # Define preprocessing pipeline
    categorical_features = ['HomeTeam', 'AwayTeam']
    numerical_features = ['HS', 'AS']

    numeric_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer([
        ('num', numeric_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features)
    ])

    # Full pipeline: preprocessing + model
    model_pipeline = Pipeline([
        ('preprocess', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Training
    model_pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred = model_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Persistence
    os.makedirs('models', exist_ok=True)
    model_path = 'models/prediction_model.pkl'
    joblib.dump(model_pipeline, model_path)
    print(f"Model saved to {model_path}")

def predict_outcome(match_data):
    model_path = 'models/prediction_model.pkl'
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found. Please train the model first.")
        return None
    
    model = joblib.load(model_path)
    # Assuming match_data is a pandas DataFrame with the same columns as X_train
    prediction = model.predict(match_data)
    return prediction[0]

if __name__ == "__main__":
    train_model()