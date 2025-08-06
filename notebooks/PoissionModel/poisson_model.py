import numpy as np
from sklearn.linear_model import PoissonRegressor
from sklearn.preprocessing import RobustScaler
from scipy.stats import poisson
import pickle

class PoissonFootballPredictor:
    def __init__(self):
        self.poisson_home = None
        self.poisson_away = None
        self.poisson_home_scaler = None
        self.poisson_away_scaler = None
        self.league_avg_goals = None
        self.feature_names = {'home': [], 'away': []}
    
    def train(self, X_poisson_home, X_poisson_away, y_home, y_away):
        """
        Train Poisson models for home and away goals
        """
        print("Training Poisson models...")
        self.poisson_home_scaler = RobustScaler()
        self.poisson_away_scaler = RobustScaler()
        
        X_ph_scaled = self.poisson_home_scaler.fit_transform(X_poisson_home)
        X_pa_scaled = self.poisson_away_scaler.fit_transform(X_poisson_away)
        
        self.poisson_home = PoissonRegressor(alpha=0.05, max_iter=1000)
        self.poisson_away = PoissonRegressor(alpha=0.05, max_iter=1000)
        
        self.poisson_home.fit(X_ph_scaled, y_home)
        self.poisson_away.fit(X_pa_scaled, y_away)
        
        # Store feature names
        self.feature_names['home'] = list(X_poisson_home.columns)
        self.feature_names['away'] = list(X_poisson_away.columns)
        
        print("Poisson models trained!")
    
    def predict_probabilities(self, X_home, X_away, max_goals=7):
        """
        Predict match outcome probabilities using Poisson models
        """
        # Ensure feature names match those used during training
        if list(X_home.columns) != self.feature_names['home']:
            missing = [f for f in self.feature_names['home'] if f not in X_home.columns]
            extra = [f for f in X_home.columns if f not in self.feature_names['home']]
            raise ValueError(f"Feature mismatch: missing {missing}, extra {extra}")
        if list(X_away.columns) != self.feature_names['away']:
            missing = [f for f in self.feature_names['away'] if f not in X_away.columns]
            extra = [f for f in X_away.columns if f not in self.feature_names['away']]
            raise ValueError(f"Feature mismatch: missing {missing}, extra {extra}")
        
        X_h_scaled = self.poisson_home_scaler.transform(X_home)
        X_a_scaled = self.poisson_away_scaler.transform(X_away)
        
        home_goals_expected = self.poisson_home.predict(X_h_scaled)
        away_goals_expected = self.poisson_away.predict(X_a_scaled)
        
        home_goals_expected = np.clip(home_goals_expected, 0.3, 4.5)
        away_goals_expected = np.clip(away_goals_expected, 0.3, 4.5)
        
        n_matches = len(home_goals_expected)
        probabilities = np.zeros((n_matches, 3))
        
        for i in range(n_matches):
            home_lambda = home_goals_expected[i]
            away_lambda = away_goals_expected[i]
            
            correlation_adj = -0.02 * (home_lambda + away_lambda - 3.0)
            home_lambda = max(home_lambda + correlation_adj, 0.3)
            away_lambda = max(away_lambda + correlation_adj, 0.3)
            
            prob_home = prob_draw = prob_away = 0.0
            for home_goals in range(max_goals + 1):
                for away_goals in range(max_goals + 1):
                    prob_score = (poisson.pmf(home_goals, home_lambda) * 
                                poisson.pmf(away_goals, away_lambda))
                    if home_goals > away_goals:
                        prob_home += prob_score
                    elif home_goals == away_goals:
                        prob_draw += prob_score
                    else:
                        prob_away += prob_score
            
            probabilities[i] = [prob_home, prob_draw, prob_away]
        
        probabilities = probabilities / probabilities.sum(axis=1, keepdims=True)
        return probabilities
    
    def save_model(self, filename):
        """
        Save the model, scalers, and feature names to a pickle file
        """
        with open(filename, 'wb') as f:
            pickle.dump({
                'poisson_home': self.poisson_home,
                'poisson_away': self.poisson_away,
                'poisson_home_scaler': self.poisson_home_scaler,
                'poisson_away_scaler': self.poisson_away_scaler,
                'league_avg_goals': self.league_avg_goals,
                'feature_names': self.feature_names
            }, f)
        print(f"Model saved to {filename}")
    
    def load_model(self, filename):
        """
        Load the model, scalers, and feature names from a pickle file
        """
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.poisson_home = data['poisson_home']
            self.poisson_away = data['poisson_away']
            self.poisson_home_scaler = data['poisson_home_scaler']
            self.poisson_away_scaler = data['poisson_away_scaler']
            self.league_avg_goals = data['league_avg_goals']
            self.feature_names = data.get('feature_names', {'home': [], 'away': []})
        print(f"Model loaded from {filename}")