# 4. Data Flow

1.  **Initial Setup**: The historical data from the CSV is loaded into the SQLite database.
2.  **Data Collection**: Airflow triggers the scraper to fetch new betting odds, which are then stored in the database.
3.  **Model Training**: Airflow triggers the model training script, which reads the combined data from the database and saves the trained model as a file (e.g., a `.pkl` file).
4.  **Prediction and Display**:
    -   The Streamlit app starts.
    -   It calls the prediction service to get predictions for the upcoming matches.
    -   It queries the database directly to get team statistics.
    -   It displays all this information to the user.
