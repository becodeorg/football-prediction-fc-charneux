# 7. Epic 2: Prediction Model & Core Dashboard

**Expanded Goal:** This epic focuses on implementing the core machine learning prediction capabilities and integrating them with the Streamlit dashboard. It will involve training a model on the ingested data, creating a service to provide predictions, and building the user interface to display these predictions along with relevant team statistics.

## 7.1. Story 2.1: ML Model Training and Persistence

As a **Data Analyst**,
I want to **train a machine learning model on historical match data and save it**,
so that **the system can predict future match outcomes.**

### Acceptance Criteria

1.  **1**: The `model.py` script includes a function `train_model()` that connects to `football.db` and reads the `matches` table.
2.  **2**: The `train_model()` function preprocesses the data (e.g., feature selection, handling categorical variables if necessary) suitable for model training.
3.  **3**: The `train_model()` function trains a machine learning model (e.g., RandomForestClassifier) to predict the `FTR` (Full Time Result).
4.  **4**: The trained model is saved to a file (e.g., `prediction_model.pkl`) in the project root or a designated `models/` directory.
5.  **5**: The `train_model()` function prints the model's accuracy on a test set.
6.  **6**: A `.gitignore` entry is added to exclude `prediction_model.pkl` (or the `models/` directory) from version control.

## 7.2. Story 2.2: Prediction Service Implementation

As a **Data Analyst**,
I want to **implement a function to load the trained model and make predictions**,
so that **the Streamlit app can easily get match outcome predictions.**

### Acceptance Criteria

1.  **1**: The `model.py` script includes a function `predict_outcome(match_data)` that loads the `prediction_model.pkl`.
2.  **2**: The `predict_outcome()` function takes new match data (e.g., features of an upcoming match) as input.
3.  **3**: The `predict_outcome()` function returns the predicted outcome (H, D, or A) for the given match data.
4.  **4**: The `predict_outcome()` function handles cases where the model file is not found, providing an informative error.

## 7.3. Story 2.3: Streamlit Dashboard - Upcoming Matches & Predictions

As a **Data Analyst**,
I want to **display upcoming matches and their predicted outcomes on the Streamlit dashboard**,
so that **users can quickly see the system's predictions.**

### Acceptance Criteria

1.  **1**: The `app.py` Streamlit application displays a clear header for "Upcoming Matches".
2.  **2**: The `app.py` connects to `football.db` and retrieves the next 3 upcoming matches (based on date).
3.  **3**: For each upcoming match, the `app.py` calls the `predict_outcome()` function from `model.py` to get the prediction.
4.  **4**: The dashboard clearly displays the home team, away team, and the predicted outcome for each of the 3 upcoming matches.
5.  **5**: The dashboard gracefully handles cases where no upcoming matches are found in the database.

## 7.4. Story 2.4: Streamlit Dashboard - Team Statistics & Odds Display

As a **Data Analyst**,
I want to **display team statistics and betting odds for upcoming matches on the Streamlit dashboard**,
so that **users have comprehensive information for analysis.**

### Acceptance Criteria

1.  **1**: For each upcoming match, the `app.py` retrieves and displays relevant statistics for both the home and away teams (e.g., goals scored/conceded, shots, etc.) for their last 5 matches.
2.  **2**: The team statistics are presented in a clear and readable format (e.g., a small table or summary).
3.  **3**: The `app.py` retrieves and displays the scraped betting odds for each upcoming match.
4.  **4**: The odds are clearly associated with their respective match and outcome (Home Win, Draw, Away Win).
5.  **5**: The dashboard gracefully handles cases where team statistics or odds are not available.
