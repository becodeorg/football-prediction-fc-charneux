# Project Brief: Football Match Prediction Project

## Executive Summary

**Product Concept:** A system designed to predict Belgian Jupiler Pro League football match outcomes by combining historical data with real-time scraped information (odds, recent matches) and presenting these predictions via a Streamlit dashboard.

**Primary Problem Being Solved:** The challenge of accurately predicting football match outcomes, providing users with data-driven insights and a visual representation of predictions and team statistics.

**Target Market Identification:** Football enthusiasts, bettors, and data science students interested in applying machine learning and data engineering to sports analytics.

**Key Value Proposition:** Provides an end-to-end solution for football match prediction, from data ingestion and model training to interactive visualization, enabling users to make informed decisions or simply enjoy data-driven insights into football matches.

## Problem Statement

Predicting football match outcomes is a complex task due to numerous variables and inherent unpredictability. Existing solutions often lack real-time data integration, comprehensive team statistics, or an intuitive visualization interface. This project aims to address these pain points by providing a robust, automated system that combines historical trends with live data to offer more accurate and timely predictions, thereby enhancing the user's understanding and engagement with football analytics.

## Proposed Solution

The proposed solution is an end-to-end football prediction system for the Belgian Jupiler Pro League. It will leverage web scraping to gather real-time data (odds, recent matches) and integrate it with a provided historical dataset. A machine learning model will be trained on this combined data to predict match outcomes. The predictions, along with team statistics and odds, will be displayed on an interactive Streamlit dashboard. The entire data pipeline, including scraping and model retraining, will be automated using Airflow, ensuring the system remains up-to-date and accurate.

## Target Users

### Primary User Segment: Football Enthusiasts/Bettors
- **Demographic/Firmographic Profile:** Individuals interested in Belgian Jupiler Pro League football, potentially engaging in sports betting.
- **Current Behaviors and Workflows:** Currently rely on various sources for match information, statistics, and odds; may manually track team performance.
- **Specific Needs and Pain Points:** Desire accurate predictions, easy access to team statistics, and a consolidated view of upcoming matches and odds.
- **Goals they're trying to achieve:** Make informed betting decisions, gain deeper insights into team performance, and enjoy a more data-driven approach to following football.

### Secondary User Segment: Data Science Students/Learners
- **Demographic/Firmographic Profile:** Students or individuals learning about data science, machine learning, and data engineering.
- **Current Behaviors and Workflows:** Seeking practical projects to apply their skills, understand end-to-end data pipelines, and explore real-world data challenges.
- **Specific Needs and Pain Points:** Need a clear project structure, access to relevant datasets, and a tangible outcome to demonstrate their learning.
- **Goals they're trying to achieve:** Apply theoretical knowledge, build a portfolio project, and understand the integration of various data tools and techniques.

## Goals & Success Metrics

### Business Objectives
- Achieve a predictive accuracy rate of X% for match outcomes (to be defined during model training and evaluation).
- Ensure the Streamlit dashboard is accessible and functional for users.
- Successfully automate data scraping and model retraining processes with Airflow.

### User Success Metrics
- User engagement with the Streamlit dashboard (e.g., number of unique visitors, session duration).
- Positive feedback on the clarity and usefulness of predictions and statistics.

### Key Performance Indicators (KPIs)
- **Prediction Accuracy:** Percentage of correctly predicted match outcomes.
- **Data Freshness:** Frequency and success rate of data updates via Airflow.
- **Dashboard Uptime:** Availability of the Streamlit application.

## MVP Scope

### Core Features (Must Have)
- **Streamlit Dashboard:** Display upcoming 3 matches, predicted outcomes, outcome odds, and team stats for the last 5 matches.
- **Web Scraping and Database:** Store historical match data in a database (SQLite or free hosting service). Build a scraper for recent match data and betting odds. Automate scraping with Airflow.
- **Model Training and Scheduling Retraining:** Train an ML model on historical data to predict future matches. Periodically retrain the model with recent data.

### Out of Scope for MVP
- Automated Betting Simulation
- Advanced Model Exploration (e.g., possession stats, player absences)

### MVP Success Criteria
- The Streamlit dashboard successfully displays predictions and stats for upcoming matches.
- The data pipeline (scraping, database storage, Airflow automation) is fully functional.
- The machine learning model is trained and provides predictions.

## Post-MVP Vision

### Phase 2 Features
- Implement automated betting simulation to track virtual betting performance.
- Integrate additional features into the model (e.g., possession stats, player absences) for improved accuracy.

### Long-term Vision
- Expand prediction capabilities to other football leagues.
- Develop more sophisticated machine learning models and ensemble techniques.
- Explore real-time prediction updates during live matches.

### Expansion Opportunities
- Offer personalized predictions or betting strategies.
- Integrate with other sports data APIs.
- Develop a mobile application for predictions.

## Technical Considerations

### Platform Requirements
- **Target Platforms:** Web (Streamlit app)
- **Browser/OS Support:** Standard web browsers on various operating systems.
- **Performance Requirements:** Dashboard should load quickly; data updates and model retraining should be efficient.

### Technology Preferences
- **Frontend:** Streamlit (Python)
- **Backend:** Python for data processing, ML model, and scraping logic.
- **Database:** SQLite (local development) or free hosting services like Heroku Postgres, ElephantSQL.
- **Data Scraping**: Playwright (for dynamic content), BeautifulSoup, Requests (for static content)
- **Hosting/Infrastructure:** Airflow for orchestration.

### Architecture Considerations
- **Repository Structure:** A single GitHub repository (`football-prediction`) containing all code, README, and documentation.
- **Service Architecture:** Separation of concerns between data engineering (scraping, database, Airflow) and data analysis (ML model, Streamlit app).
- **Integration Requirements:** Seamless data flow from scraped sources to database, to ML model, and finally to the Streamlit dashboard.
- **Security/Compliance:** Basic data security for the database; no sensitive user data involved.

## Constraints & Assumptions

### Constraints
- **Budget:** Free hosting services preferred for the database.
- **Timeline:** 8 days duration, deadline 13/09/2024 5PM.
- **Resources:** Team of 4 learners.
- **Technical:** Reliance on provided historical dataset and specified scraping sources.

### Key Assumptions
- The provided historical dataset is clean and sufficient for initial model training.
- Publicly available betting odds and recent match data can be reliably scraped.
- Streamlit is a suitable framework for the dashboard requirements.

## Risks & Open Questions

### Key Risks
- **Scraping Reliability:** Websites may change their structure, breaking scrapers.
- **Model Accuracy:** Achieving satisfactory prediction accuracy within the given timeframe.
- **Data Volume:** Managing and processing large volumes of historical and real-time data efficiently.

### Open Questions
- What specific machine learning algorithms will be most effective for prediction?
- How will model performance be rigorously evaluated and tracked?
- What is the strategy for handling missing or inconsistent data from scraped sources?

### Areas Needing Further Research
- Best practices for robust web scraping to handle website changes.
- Advanced machine learning techniques for sports prediction.
- Optimal strategies for periodic model retraining and deployment.

## Appendices

### A. Research Summary

Key findings from the project description:
- Historical match data available via CSV from football-data.co.uk.
- Bookmaker odds can be scraped from WhoScored, SportsGambler, OddsChecker, BetFirst.
- SQLite, Heroku Postgres, ElephantSQL are suggested database hosting options.

### C. References
- [football-data.co.uk](https://www.football-data.co.uk/)
- [football-data.co.uk/notes.txt](https://www.football-data.co.uk/notes.txt) (column definitions)
- [Heroku Postgres](https://www.heroku.com/postgres)
- [ElephantSQL](https://www.elephantsql.com/)
- [SummaryOfOptions](https://gist.github.com/bmaupin/0ce79806467804fdbbf8761970511b8c)
- [WhoScored](https://www.whoscored.com/)
- [SportsGambler](https://www.sportsgambler.com/)
- [OddsChecker](https://www.oddschecker.com/)
- [BetFirst](https://betfirst.dhnet.be/)

## Next Steps

### Immediate Actions
1. Set up the GitHub repository (`football-prediction`).
2. Study project requirements in detail.
3. Split work between Data Engineering and Data Analysis teams.

### PM Handoff
This Project Brief provides the full context for Football Match Prediction Project. Please start in 'PRD Generation Mode', review the brief thoroughly to work with the user to create the PRD section by section as the template indicates, asking for any necessary clarification or suggesting improvements.