import dash
from dash import html

dash.register_page(__name__, path="/prediction")

layout = html.Div([
    html.H2("Match Outcome Prediction"),
    html.P("Coming soon: Input team names and get probability predictions."),
    # Add model input fields and outputs later here
])
