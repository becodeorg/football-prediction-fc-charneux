import sqlite3
import joblib
import pandas as pd
from utils.pipeline import pipeline_LDA, pipeline_RC
from utils.prepare_X import prepare_X

# db should include cols: ['Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'FTR', 'HS', 'HST', 'HC', 'HF', 'HY', 'HR', 'FTHG', 'FTAG', 'AS', 'AST', 'AC', 'AF', 'AY', 'AR', 'FTAG', 'FTHG']
# Load data from db
db_path = "C:/Users/yinmi/Becode_projects/football-prediction-fc-charneux/football.db"
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM matches", conn)

# Train model LDA (using odds: B365H, B365D, B365A and rolling goal performance)
X_raw = df.drop(columns=['FTR'])
X = prepare_X(X_raw, rolling_window=10, using_odds=True)
y = df['FTR']
pipe_LDA = pipeline_LDA()
pipe_LDA.fit(X, y)

# Train model RidgeClassifier (using only rolling goal performance)
df_X = df.drop(columns=['FTR'])
X = prepare_X(df_X, rolling_window=10, using_odds=False)
y = df['FTR']
pipe_RC = pipeline_RC()
pipe_RC.fit(X, y)

# Save model to pkl
joblib.dump(pipe_LDA, 'C:/Users/yinmi/Becode_projects/football-prediction-fc-charneux/notebooks/models/model_LDA.pkl')
joblib.dump(pipe_RC, 'C:/Users/yinmi/Becode_projects/football-prediction-fc-charneux/notebooks/models/model_RC.pkl')