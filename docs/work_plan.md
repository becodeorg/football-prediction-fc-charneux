### **Detailed Work Plan with Checklists**

**Objective:** To track the progress of each task for the "must-have" Epics of the `football-prediction` project.

**Legend:**
*   `[ ]` : To-do task
*   `[x]` : Completed task
*   **(DE: Raphael/Quentin)** : Data Engineer Responsible
*   **(DA: Miao)** : Data Analyst Responsible

---

#### **Epic 1: Foundation & Data Ingestion**

**Story 1.1: Database Setup and Historical Data Ingestion**
*   **Responsible(s):** Raphael (DE Lead)
*   **Tasks / Subtasks:**
    *   [x] Create the `db_setup.py` file at the project root.
    *   [x] Implement logic in `db_setup.py` to create the `football.db` database.
    *   [x] Implement logic in `db_setup.py` to create the `matches` table with the appropriate schema (Date, Time, HomeTeam, AwayTeam, FTHG, FTAG, FTR, and other relevant CSV columns).
    *   [x] Implement logic in `db_setup.py` to load `dataset.csv` into the `matches` table.
    *   [x] Ensure `db_setup.py` is idempotent.
    *   [x] Add/verify the `football.db` entry in `.gitignore`.
    *   [x] Execute `db_setup.py` for initial database setup.

**Story 1.2: Basic Betting Odds Scraper**
*   **Responsible(s):** Quentin (DE)
*   **Tasks / Subtasks:**
    *   [x] Create the `src/data_collection/scraper.py` file.
    *   [ ] Implement basic logic for making HTTP requests to specified betting odds websites.
    *   [ ] Implement logic to extract relevant betting odds (Home Win, Draw, Away Win) for upcoming matches.
    *   [ ] Implement logic to structure the extracted data.
    *   [ ] Implement logic to store the extracted data in `football.db` (new table or updating existing records).
    *   [ ] Add basic error handling for network issues or website structure changes.
    *   [ ] Ensure `scraper.py` is executable independently for testing.

---

#### **Epic 2: Prediction Model & Core Dashboard**

**Story 2.1: ML Model Training and Persistence**
*   **Responsible(s):** Miao (DA)
*   **Tasks / Subtasks:**
    *   [x] Create the `src/modeling/model.py` file.
    *   [x] Create `notebooks/ml_model_training.ipynb` for prototyping and experimentation.
    *   [x] Implement the `train_model()` function in `model.py`.
    *   [x] In `train_model()`, connect to `football.db` and read the `matches` table.
    *   [x] In `train_model()`, implement data preprocessing (feature selection, categorical variable handling). (Completed in `ml_model_training.ipynb` for prototyping)
    *   [x] In `train_model()`, train a machine learning model to predict `FTR` (Full Time Result).
    *   [x] In `train_model()`, save the trained model to `models/prediction_model.pkl`.
    *   [x] In `train_model()`, print the model's accuracy on a test set.
    *   [ ] Add/verify the `prediction_model.pkl` (or `models/`) entry in `.gitignore`.

**Story 2.2: Prediction Service Implementation**
*   **Responsible(s):** Miao (DA)
*   **Tasks / Subtasks:**
    *   [x] Implement the `predict_outcome(match_data)` function in `src/modeling/model.py`.
    *   [x] In `predict_outcome()`, load the model from `prediction_model.pkl`.
    *   [x] In `predict_outcome()`, take new match data as input.
    *   [x] In `predict_outcome()`, return the predicted outcome (H, D, or A).
    *   [x] In `predict_outcome()`, handle cases where the model file is not found.

**Story 2.3: Streamlit Dashboard - Upcoming Matches & Predictions**
*   **Responsible(s):** Miao (DA)
*   **Tasks / Subtasks:**
    *   [x] Create the `src/app/app.py` file. (DE: Raphael)
    *   [ ] In `app.py`, display a clear header for "Upcoming Matches".
    *   [ ] In `app.py`, connect to `football.db` and retrieve the next 3 upcoming matches.
    *   [ ] For each upcoming match, call `predict_outcome()` from `model.py`.
    *   [ ] Clearly display the home team, away team, and the predicted outcome.
    *   [ ] Handle cases where no upcoming matches are found.

**Story 2.4: Streamlit Dashboard - Team Statistics & Odds Display**
*   **Responsible(s):** Miao (DA)
*   **Tasks / Subtasks:**
    *   [ ] In `src/app/app.py`, retrieve and display relevant statistics for both the home and away teams for their last 5 matches.
    *   [ ] Present team statistics in a clear and readable format.
    *   [ ] Retrieve and display the scraped betting odds for each upcoming match.
    *   [ ] Clearly associate the odds with their respective match and outcome.
    *   [ ] Handle cases where team statistics or odds are not available.

---

#### **Epic 3: Automated Data Pipeline**

**Story 3.1: Airflow DAG for Data Scraping**
*   **Responsible(s):** Quentin (DE)
*   **Tasks / Subtasks:**
    *   [x] Create the `dags/scraping_dag.py` file.
    *   [ ] Define an Airflow DAG that schedules the execution of `src/data_collection/scraper.py`.
    *   [ ] Configure the DAG's execution frequency (to be determined by the team, e.g., `@daily`).
    *   [ ] Include appropriate error handling and logging for the scraping task.
    *   [ ] Ensure the DAG successfully triggers the `scraper.py` script and that data is inserted/updated in `football.db`.

**Story 3.2: Airflow DAG for Model Retraining**
*   **Responsible(s)::** Miao (DA)
*   **Tasks / Subtasks:**
    *   [x] Create the `dags/training_dag.py` file.
    *   [ ] Define an Airflow DAG that schedules the execution of the `train_model()` function from `src/modeling/model.py`.
    *   [ ] Configure the DAG's execution frequency (to be determined by the team, e.g., `@weekly`).
    *   [ ] Include appropriate error handling and logging for the model training task.
    *   [ ] Ensure the DAG successfully triggers the `train_model()` function and that `prediction_model.pkl` is updated.

---

**Next Steps for the Team:**

1.  **Raphael** starts with Phase 1 (Fundamental Infrastructure).
2.  As soon as the directory structure is in place and `db_setup.py` is functional, **Quentin** can start Phase 2 (Entry Points and Scrapers) and **Miao** can start Phase 3 (ML Model Scaffolding).
3.  **Communication:** Maintain constant communication. If a team member is blocked or needs assistance, they should report it immediately. Data Engineers (Raphael and Quentin) should collaborate closely on database schema and data ingestion, and both can assist Miao with integration or deployment aspects as needed.
4.  **Checklist Usage:** Use this document as a living checklist. Mark tasks as `[x]` when completed. This will provide a clear overview of progress for everyone.
