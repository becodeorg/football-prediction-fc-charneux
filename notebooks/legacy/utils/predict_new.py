import sqlite3
import joblib
import pandas as pd
import numpy as np
from scipy.special import softmax
from notebooks.legacy.utils.prepare_X import prepare_X

def show_preds(Date: str, HomeTeam: str, AwayTeam: str, using_odds: bool, B365H=None, B365D=None, B365A=None):
    # Load df_X from db
    db_path = "C:/Users/yinmi/Becode_projects/football-prediction-fc-charneux/football.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM matches", conn)
    df_X = df.drop(columns=['FTR'])

    # Prepare X
    # Inject X into df_X to get rolling performance
    X_raw = pd.DataFrame([{col: np.nan for col in df.columns}])
    X_raw['Date'] = Date
    X_raw['HomeTeam'] = HomeTeam
    X_raw['AwayTeam'] = AwayTeam
    if using_odds == True: # then fill in odds
        X_raw['B365H'] = B365H
        X_raw['B365D'] = B365D
        X_raw['B365A'] = B365A
    print(X_raw)
    df_full = pd.concat([X_raw, df_X], ignore_index=True)
    print(df_full.head())
    if using_odds == True: # then use LDA model
        df_prep = prepare_X(df_full, rolling_window=10, for_model='LDA')
    else: # use RC model
        df_prep = prepare_X(df_full, rolling_window=10, for_model='RC')
    print(df_prep)
    # Retrive X
    X = df_prep[(df_prep['HomeTeam'] == HomeTeam) & (df_prep['AwayTeam'] == AwayTeam)].tail(1)
    print(X)

    # Predict
    if using_odds == True:
        model = joblib.load('C:/Users/yinmi/Becode_projects/football-prediction-fc-charneux/notebooks/models/model_LDA.pkl')
        probs = model.predict_proba(X)
        y_pred = model.predict(X)
        print(y_pred)
    else:
        model = joblib.load('C:/Users/yinmi/Becode_projects/football-prediction-fc-charneux/notebooks/models/model_RC.pkl')
        raw_scores = model.decision_function(X)
        probs = softmax(raw_scores, axis=1)
        y_pred = model.predict(X)
        print(y_pred)
    label_to_index = {label: idx for idx, label in enumerate(model.classes_)}
    prob_H = probs[0][label_to_index['H']]
    prob_D = probs[0][label_to_index['D']]
    prob_A = probs[0][label_to_index['A']]

    return prob_H, prob_D, prob_A

# Test one match without odds (model: LDA)
prob_H, prob_D, prob_A = show_preds(Date='2025-08-01', HomeTeam='Mechelen', AwayTeam='Club Brugge', using_odds=False, B365H=None, B365D=None, B365A=None)
print(f"H: {prob_H}, D: {prob_D}, A: {prob_A}")
# Test one match with odds (model: RC)
prob_H, prob_D, prob_A = show_preds(Date='2025-08-01', HomeTeam='Mechelen', AwayTeam='Club Brugge', using_odds=True, B365H=4.5, B365D=4, B365A=1)
print(f"H: {prob_H}, D: {prob_D}, A: {prob_A}")