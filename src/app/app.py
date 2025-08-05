import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for deployment

app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="FC Charneux - CheatGPT",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dcc.Link("Home", href="/", className="nav-link")),
            dbc.NavItem(dcc.Link("Prediction", href="/prediction", className="nav-link")),
            dbc.NavItem(dcc.Link("Stats", href="/stats", className="nav-link")),
        ]
    ),
    dash.page_container
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)
