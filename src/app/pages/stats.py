import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from services.plot_service import PlotService

dash.register_page(__name__, path="/stats")

ps = PlotService()

layout = html.Div([
    html.H2("Football Statistics"),
    dcc.Graph(figure=ps.getTopTeamsBarChart())
])
