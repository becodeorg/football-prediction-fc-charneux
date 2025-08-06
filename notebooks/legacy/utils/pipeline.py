from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import RidgeClassifier

def pipeline_LDA():
    pipeline_LDA = Pipeline([
        ('ColumnTransform', ColumnTransformer([
            ('num', Pipeline([('imputer', SimpleImputer(strategy='mean')), ('scaler', StandardScaler())]), ['B365H', 'B365D', 'B365A', 'HomeTeam_FormScore', 'AwayTeam_FormScore', 'HomeTeam_AvgRedCards', 'AwayTeam_AvgRedCards', 'HomeTeam_AvgGoalsScored', 'AwayTeam_AvgGoalsScored']),
            ('cat', Pipeline([('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('ordinal', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))]), ['HomeTeam', 'AwayTeam'])
        ])),
        ('classifier', LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto'))
    ])
    return pipeline_LDA

def pipeline_RC():
    pipeline_RC = Pipeline([
        ('ColumnTransform', ColumnTransformer([
            ('num', Pipeline([('imputer', SimpleImputer(strategy='mean')), ('scaler', StandardScaler())]), ['HomeTeam_FormScore', 'AwayTeam_FormScore', 'HomeTeam_AvgShots', 'AwayTeam_AvgShots', 'HomeTeam_AvgFouls', 'AwayTeam_AvgFouls', 'HomeTeam_AvgRedCards', 'AwayTeam_AvgRedCards']),
            ('cat', Pipeline([('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), ['HomeTeam', 'AwayTeam'])
        ])),
        ('classifier', RidgeClassifier(max_iter=1000))
    ])
    return pipeline_RC