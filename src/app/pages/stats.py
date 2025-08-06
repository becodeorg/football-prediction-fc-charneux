import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from services.plot_service import PlotService

dash.register_page(__name__, path="/stats")

ps = PlotService()

layout = html.Div([
    html.H2("Football Statistics"),
    dcc.Graph(figure=ps.getTopTeamsBarChart()),
    dcc.Graph(figure=ps.getWinLossDrawChart()),
    dcc.Graph(figure=ps.getShotsVsGoalsCharts()),
    html.Div([
        dcc.Graph(figure=ps.getDisciplineChart()),
        dcc.Graph(figure=ps.getTeamPlayingStyleChart()),
    ], className='graph-row'),
])