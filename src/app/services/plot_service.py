
import os

import sqlite3

import pandas as pd
from pandas.io.sql import DatabaseError

import numpy as np

import plotly.express as px
import plotly.graph_objects as go

class PlotService:

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..', '..', '..')
        db_path = os.path.join(project_root, 'football.db')

        self.df = self.__load_data(db_path)
        self.df = self.__preprocess_data(self.df)
        self.df = self.__compute_extra_features(self.df)


    def __load_data(self, db_path) -> pd.DataFrame:
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database '{db_path}' not found. Run db_setup.py first.")

        conn = sqlite3.connect(db_path)

        try:
            df = pd.read_sql_query("SELECT * FROM matches", conn)
            print(f"✅ Loaded {len(df)} rows from 'matches' table")
        except DatabaseError as e:
            df = pd.DataFrame()
            print(f"❌ Error loading data: {e}")
        finally:
            conn.close()
        
        return df
    
    def __preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # Enhanced data cleaning for analysis
        df_clean = df.copy()

        # Remove rows with missing critical information (match identifiers and results)
        critical_cols = ['HomeTeam', 'AwayTeam', 'FTR', 'Date']
        df_clean = df_clean.dropna(subset=critical_cols)

        # Handle missing values in numerical columns
        numerical_cols = ['FTHG', 'FTAG', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 
                        'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']

        # Fill missing numerical values with 0 (assuming missing means no shots, fouls, cards, etc.)
        for col in numerical_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna(0)

        # Clean string columns
        string_cols = ['HomeTeam', 'AwayTeam', 'FTR', 'HTR']
        for col in string_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].str.strip()  # Remove whitespace
                # Fill any remaining missing string values with 'Unknown'
                df_clean[col] = df_clean[col].fillna('Unknown')

        # Handle any other columns that might have missing values
        remaining_missing = df_clean.isnull().sum()
        if remaining_missing.sum() > 0:
            
            # Drop columns that are mostly missing (>50% missing)
            threshold = len(df_clean) * 0.5
            cols_to_drop = remaining_missing[remaining_missing > threshold].index.tolist()
            if cols_to_drop:
                df_clean = df_clean.drop(columns=cols_to_drop)
            
            # For remaining columns, fill with appropriate defaults
            for col in df_clean.columns:
                if df_clean[col].isnull().sum() > 0:
                    if df_clean[col].dtype in ['object', 'string']:
                        df_clean[col] = df_clean[col].fillna('Unknown')
                    else:
                        df_clean[col] = df_clean[col].fillna(0)

        # Final check - ensure no missing values remain
        assert df_clean.isnull().sum().sum() == 0, "❌ Missing values still exist!"

        return df_clean

    def __compute_extra_features(self, df: pd.DataFrame) -> pd.DataFrame:
        print(df.columns)
        # Add derived columns
        df['TotalGoals'] = df['FTHG'] + df['FTAG']
        df['GoalDifference'] = df['FTHG'] - df['FTAG']
        df['IsDraw'] = df['FTR'] == 'D'

        # Points earned by Home Team
        def home_points(row):
            if row['FTR'] == 'H':
                return 3
            elif row['FTR'] == 'D':
                return 1
            else:
                return 0

        df['HomePoints'] = df.apply(home_points, axis=1)

        # Convert Date column
        df['Date'] = pd.to_datetime(df['Date'])

        return df


    
    def getTopTeamsBarChart(self):

        # Compute top 10 home teams
        home_goals = self.df.groupby('HomeTeam')['FTHG'].mean().reset_index()
        top_home = home_goals.sort_values(by='FTHG', ascending=False).head(10)

        # Compute top 10 away teams
        away_goals = self.df.groupby('AwayTeam')['FTAG'].mean().reset_index()
        top_away = away_goals.sort_values(by='FTAG', ascending=False).head(10)

        # Create the figure
        fig = go.Figure()

        # Add home team bar chart
        fig.add_trace(go.Bar(
            x=top_home['HomeTeam'],
            y=top_home['FTHG'],
            name='Home Teams',
            visible=True
        ))

        # Add away team bar chart
        fig.add_trace(go.Bar(
            x=top_away['AwayTeam'],
            y=top_away['FTAG'],
            name='Away Teams',
            visible=False
        ))

        # Add dropdown to toggle visibility
        fig.update_layout(
            title='Top 10 Teams by Average Goals',
            updatemenus=[
                dict(
                    type='dropdown',
                    direction='down',
                    buttons=[
                        dict(label='Top Home Teams',
                            method='update',
                            args=[{'visible': [True, False]},
                                {'title': 'Top 10 Home Teams by Avg Goals',
                                    'yaxis': {'title': 'Avg Home Goals'}}]),
                        dict(label='Top Away Teams',
                            method='update',
                            args=[{'visible': [False, True]},
                                {'title': 'Top 10 Away Teams by Avg Goals',
                                    'yaxis': {'title': 'Avg Away Goals'}}]),
                    ],
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.15,
                    yanchor="top"
                ),
            ]
        )

        fig.update_layout(height=500)

        return fig
