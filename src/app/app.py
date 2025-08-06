import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for deployment

app.layout = html.Div([
    dbc.Navbar([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Img(
                            src="/assets/images/jupiler-pro-league.png", 
                            style={'height': '60px', 'marginRight': '15px', 'marginLeft': '15px'}
                        ),
                        dbc.NavbarBrand([
                            html.I(className="fas fa-futbol me-2"),
                            "FC Charneux Analytics",
                            html.Span(" | Jupiler Pro League", style={
                                'fontSize': '0.8rem',
                                'fontWeight': 'normal',
                                'opacity': '0.9'
                            })
                        ])
                    ], style={'display': 'flex', 'alignItems': 'center'})
                ], width="auto"),
                dbc.Col([
                    dbc.Nav([
                        dbc.NavItem([
                            html.I(className="fas fa-home me-1"),
                            dcc.Link("Home", href="/", className="nav-link")
                        ], style={'display': 'flex', 'alignItems': 'center'}),
                        dbc.NavItem([
                            html.I(className="fas fa-chart-line me-1"),
                            dcc.Link("Prediction", href="/prediction", className="nav-link")
                        ], style={'display': 'flex', 'alignItems': 'center'}),
                        dbc.NavItem([
                            html.I(className="fas fa-chart-bar me-1"),
                            dcc.Link("Stats", href="/stats", className="nav-link")
                        ], style={'display': 'flex', 'alignItems': 'center'}),
                    ], navbar=True, className="ms-auto", style={'justifyContent': 'flex-end', 'marginRight': '15px'})
                ], width=True)
            ], className="w-100", justify="between", style={'alignItems': 'center'})
        ], fluid=True)
    ], className="navbar", fixed="top"),
    
    # Main content with top padding to account for fixed navbar
    html.Div([
        dbc.Container([
            dash.page_container
        ], fluid=True, className="main-content")
    ], style={'paddingTop': '76px'})
], style={'minHeight': '100vh'})

if __name__ == '__main__':
    app.run(debug=True)
