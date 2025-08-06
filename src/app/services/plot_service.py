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
            xaxis_title='Teams',
            yaxis_title='Average Goals',
            updatemenus=[
                dict(
                    type='dropdown',
                    direction='down',
                    buttons=[
                        dict(
                            label='Home Teams',
                            method='update',
                            args=[
                                {'visible': [True, False]},
                                {'xaxis': {'title': 'Home Teams'}, 'yaxis': {'title': 'Average Home Goals'}}
                            ]
                        ),
                        dict(
                            label='Away Teams',
                            method='update',
                            args=[
                                {'visible': [False, True]},
                                {'xaxis': {'title': 'Away Teams'}, 'yaxis': {'title': 'Average Away Goals'}}
                            ]
                        ),
                    ],
                    showactive=True,
                    x=0.88,
                    xanchor="left",
                    y=1.003,
                    yanchor="bottom"
                ),
            ],
            margin=dict(t=80, l=50, r=50, b=50)
        )

        fig.update_layout(height=500)

        return fig

    def getWinLossDrawChart(self):
        # Calculate win/loss/draw statistics for all teams
        team_stats = []
        
        # Get all unique teams
        all_teams = set(self.df['HomeTeam'].unique()) | set(self.df['AwayTeam'].unique())
        
        for team in all_teams:
            # Home matches
            home_matches = self.df[self.df['HomeTeam'] == team]
            home_wins = len(home_matches[home_matches['FTR'] == 'H'])
            home_draws = len(home_matches[home_matches['FTR'] == 'D'])
            home_losses = len(home_matches[home_matches['FTR'] == 'A'])
            
            # Away matches
            away_matches = self.df[self.df['AwayTeam'] == team]
            away_wins = len(away_matches[away_matches['FTR'] == 'A'])
            away_draws = len(away_matches[away_matches['FTR'] == 'D'])
            away_losses = len(away_matches[away_matches['FTR'] == 'H'])
            
            # Total stats
            total_wins = home_wins + away_wins
            total_draws = home_draws + away_draws
            total_losses = home_losses + away_losses
            total_matches = total_wins + total_draws + total_losses
            
            if total_matches > 0:
                # Calculate percentages
                win_pct = (total_wins / total_matches * 100)
                draw_pct = (total_draws / total_matches * 100)
                loss_pct = (total_losses / total_matches * 100)
                
                team_stats.append({
                    'Team': team,
                    'Wins': total_wins,
                    'Draws': total_draws,
                    'Losses': total_losses,
                    'Win_Pct': win_pct,
                    'Draw_Pct': draw_pct,
                    'Loss_Pct': loss_pct,
                    'Total': total_matches
                })
        
        # Convert to DataFrame and sort by win percentage
        stats_df = pd.DataFrame(team_stats)
        stats_df = stats_df.sort_values('Win_Pct', ascending=True)
        
        # Create the figure with initial data (absolute numbers)
        fig = go.Figure()
        
        # Add absolute numbers traces
        fig.add_trace(go.Bar(
            name='Wins',
            x=stats_df['Wins'],
            y=stats_df['Team'],
            orientation='h',
            marker_color='#2E8B57',  # Sea Green
            visible=True
        ))
        
        fig.add_trace(go.Bar(
            name='Draws',
            x=stats_df['Draws'],
            y=stats_df['Team'],
            orientation='h',
            marker_color='#FFD700',  # Gold
            visible=True
        ))
        
        fig.add_trace(go.Bar(
            name='Losses',
            x=stats_df['Losses'],
            y=stats_df['Team'],
            orientation='h',
            marker_color='#DC143C',  # Crimson
            visible=True
        ))
        
        # Add percentage traces (initially hidden)
        fig.add_trace(go.Bar(
            name='Win %',
            x=stats_df['Win_Pct'],
            y=stats_df['Team'],
            orientation='h',
            marker_color='#2E8B57',  # Sea Green
            visible=False
        ))
        
        fig.add_trace(go.Bar(
            name='Draw %',
            x=stats_df['Draw_Pct'],
            y=stats_df['Team'],
            orientation='h',
            marker_color='#FFD700',  # Gold
            visible=False
        ))
        
        fig.add_trace(go.Bar(
            name='Loss %',
            x=stats_df['Loss_Pct'],
            y=stats_df['Team'],
            orientation='h',
            marker_color='#DC143C',  # Crimson
            visible=False
        ))
        
        # Update layout with dropdown
        fig.update_layout(
            title='Win/Draw/Loss Statistics by Team',
            xaxis_title='Number of Matches',
            yaxis_title='Teams',
            barmode='stack',
            height=600,
            updatemenus=[
                dict(
                    type='dropdown',
                    direction='down',
                    buttons=[
                        dict(
                            label='Absolute Numbers',
                            method='update',
                            args=[
                                {'visible': [True, True, True, False, False, False]},
                                {'xaxis': {'title': 'Number of Matches'}}
                            ]
                        ),
                        dict(
                            label='Percentages',
                            method='update',
                            args=[
                                {'visible': [False, False, False, True, True, True]},
                                {'xaxis': {'title': 'Percentage (%)', 'range': [0, 100]}}
                            ]
                        ),
                    ],
                    showactive=True,
                    x=0.84,
                    xanchor="left",
                    y=1.07,
                    yanchor="top"
                ),
            ],
            margin=dict(t=100, l=50, r=50, b=50)
        )
        
        return fig

    def getShotsVsGoalsCharts(self):
        # Create a scatter plot showing relationship between shots and goals with sized markers
        # First, count occurrences of each (HS, FTHG) combination
        df_counts = self.df.groupby(['HS', 'FTHG', 'FTR']).size().reset_index(name='count')

        fig_shots_goals = px.scatter(
            df_counts, 
            x='HS', 
            y='FTHG',
            color='FTR',
            size='count',  # Size dots based on count of overlapping points
            title='Home Team: Shots vs Goals Scored (Dot size = frequency)',
            labels={
                'HS': 'Home Shots',
                'FTHG': 'Home Goals',
                'FTR': 'Match Result',
                'count': 'Number of matches'
            },
            color_discrete_map={
                'H': '#2E8B57',  # Green for home wins
                'D': '#FFD700',  # Gold for draws
                'A': '#DC143C'   # Red for home losses
            },
            size_max=20,  # Maximum dot size
            hover_data=['count']
        )

        fig_shots_goals.update_layout(
            height=500,
            showlegend=True
        )

        return fig_shots_goals

    def getDisciplineChart(self):
        # Create a comprehensive cards vs wins analysis
        team_cards_wins = []

        for team in self.df['HomeTeam'].unique():
            # Home matches
            home_matches = self.df[self.df['HomeTeam'] == team]
            home_wins = len(home_matches[home_matches['FTR'] == 'H'])
            home_yellow = home_matches['HY'].sum()
            home_red = home_matches['HR'].sum()
            home_total = len(home_matches)
            
            # Away matches  
            away_matches = self.df[self.df['AwayTeam'] == team]
            away_wins = len(away_matches[away_matches['FTR'] == 'A'])
            away_yellow = away_matches['AY'].sum()
            away_red = away_matches['AR'].sum()
            away_total = len(away_matches)
            
            # Combined stats
            total_wins = home_wins + away_wins
            total_matches = home_total + away_total
            total_yellow = home_yellow + away_yellow
            total_red = home_red + away_red
            total_cards = total_yellow + (total_red * 2)  # Weight red cards more heavily
            
            if total_matches > 20:  # Only include teams with sufficient matches
                team_cards_wins.append({
                    'Team': team,
                    'Win_Rate': (total_wins / total_matches) * 100,
                    'Cards_Per_Match': total_cards / total_matches,
                    'Yellow_Per_Match': total_yellow / total_matches,
                    'Red_Per_Match': total_red / total_matches,
                    'Total_Matches': total_matches,
                    'Discipline_Score': (total_yellow * 1 + total_red * 5) / total_matches  # Discipline penalty score
                })

        cards_df = pd.DataFrame(team_cards_wins)

        # Create the main bubble chart
        fig_cards = px.scatter(
            cards_df,
            x='Cards_Per_Match',
            y='Win_Rate',
            size='Total_Matches',
            color='Discipline_Score',
            hover_name='Team',
            title='The Card Penalty Effect: How Discipline Affects Team Success',
            labels={
                'Cards_Per_Match': 'Total Cards per Match (Yellow + 2×Red)',
                'Win_Rate': 'Win Rate (%)',
                'Discipline_Score': 'Discipline Penalty Score',
                'Total_Matches': 'Total Matches'
            },
            color_continuous_scale='Reds',
            size_max=25
        )

        # Customize the layout
        fig_cards.update_layout(
            height=600,
            showlegend=True,
            plot_bgcolor='rgba(240,240,240,0.8)',
            font=dict(size=12),
            title_font_size=16,
            annotations=[
                dict(
                    x=0.02, y=0.98,
                    xref='paper', yref='paper',
                    text='🫧 Bubble size = Total matches played<br>🔴 Color intensity = Disciplinary issues',
                    showarrow=False,
                    font=dict(size=10),
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='gray',
                    borderwidth=1
                )
            ]
        )

        # Add quadrant lines for better interpretation
        mean_cards = cards_df['Cards_Per_Match'].mean()
        mean_wins = cards_df['Win_Rate'].mean()

        fig_cards.add_hline(y=mean_wins, line_dash="dot", line_color="gray", 
                        annotation_text=f"Avg Win Rate: {mean_wins:.1f}%")
        fig_cards.add_vline(x=mean_cards, line_dash="dot", line_color="gray",
                        annotation_text=f"Avg Cards: {mean_cards:.1f}")

        # Update hover template for better information
        fig_cards.update_traces(
            hovertemplate='<b>%{hovertext}</b><br>' +
                        'Win Rate: %{y:.1f}%<br>' +
                        'Cards per Match: %{x:.2f}<br>' +
                        'Total Matches: %{marker.size}<br>' +
                        'Discipline Score: %{marker.color:.2f}<br>' +
                        '<extra></extra>',
            selector=dict(mode='markers')
        )

        return fig_cards
    
    def getTeamPlayingStyleChart(self):
        # Classify teams by playing style
        team_styles = []

        for team in self.df['HomeTeam'].unique():
            # Home matches
            home_matches = self.df[self.df['HomeTeam'] == team]
            home_goals_scored = home_matches['FTHG'].sum()
            home_goals_conceded = home_matches['FTAG'].sum()
            home_matches_count = len(home_matches)
            
            # Away matches
            away_matches = self.df[self.df['AwayTeam'] == team]
            away_goals_scored = away_matches['FTAG'].sum()
            away_goals_conceded = away_matches['FTHG'].sum()
            away_matches_count = len(away_matches)
            
            total_matches = home_matches_count + away_matches_count
            
            if total_matches >= 30:  # Minimum matches for reliable analysis
                # Calculate averages
                goals_scored_per_game = (home_goals_scored + away_goals_scored) / total_matches
                goals_conceded_per_game = (home_goals_conceded + away_goals_conceded) / total_matches
                
                # Calculate style metrics
                attacking_power = goals_scored_per_game
                defensive_power = 3.0 - goals_conceded_per_game  # Higher is better defense
                
                # Calculate win rate for bubble size
                home_wins = len(home_matches[home_matches['FTR'] == 'H'])
                away_wins = len(away_matches[away_matches['FTR'] == 'A'])
                win_rate = (home_wins + away_wins) / total_matches * 100
                
                # Classify style
                if attacking_power > 1.3 and defensive_power > 1.7:
                    style = "Balanced Strong"
                elif attacking_power > 1.4:
                    style = "Attacking"
                elif defensive_power > 2.0:
                    style = "Defensive"
                elif attacking_power < 1.0 and defensive_power < 1.5:
                    style = "Struggling"
                else:
                    style = "Balanced"
                
                team_styles.append({
                    'Team': team,
                    'Goals_Scored_Per_Game': goals_scored_per_game,
                    'Goals_Conceded_Per_Game': goals_conceded_per_game,
                    'Attacking_Power': attacking_power,
                    'Defensive_Power': defensive_power,
                    'Win_Rate': win_rate,
                    'Total_Matches': total_matches,
                    'Style': style
                })

        style_df = pd.DataFrame(team_styles)

        # Create team style scatter plot
        fig_style = px.scatter(
            style_df,
            x='Attacking_Power',
            y='Defensive_Power',
            color='Style',
            size='Win_Rate',
            hover_name='Team',
            title='Team Playing Styles',
            labels={
                'Attacking_Power': 'Attacking Power (Goals/Game)',
                'Defensive_Power': 'Defensive Power (3 - Goals Conceded/Game)',
                'Win_Rate': 'Win Rate (%)'
            },
            color_discrete_map={
                'Attacking': '#FF4444',
                'Defensive': '#4444FF', 
                'Balanced': '#44FF44',
                'Balanced Strong': '#FFD700',
                'Struggling': '#888888'
            },
            size_max=30
        )

        # Add quadrant lines
        fig_style.add_hline(y=style_df['Defensive_Power'].mean(), line_dash="dot", 
                        line_color="gray", annotation_text="Avg Defense")
        fig_style.add_vline(x=style_df['Attacking_Power'].mean(), line_dash="dot", 
                        line_color="gray", annotation_text="Avg Attack")

        # Add style zone annotations
        fig_style.add_annotation(x=0.7, y=2.3, text="🛡️ Defensive<br>Teams", 
                                showarrow=False, bgcolor="rgba(68,68,255,0.1)")
        fig_style.add_annotation(x=1.8, y=1.2, text="⚔️ Attacking<br>Teams", 
                                showarrow=False, bgcolor="rgba(255,68,68,0.1)")
        fig_style.add_annotation(x=1.6, y=2.2, text="👑 Elite<br>Teams", 
                                showarrow=False, bgcolor="rgba(255,215,0,0.1)")

        fig_style.update_layout(
            height=600,
            showlegend=True,
            legend=dict(title="Playing Style")
        )

        return fig_style