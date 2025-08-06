import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from services.plot_service import PlotService

dash.register_page(__name__, path="/stats")

ps = PlotService()

layout = html.Div([
    html.Br(),
    html.H2("Football Statistics"),
    html.Br(),
    dcc.Graph(figure=ps.getTopTeamsBarChart(), className='graph-padding-x'),
    dcc.Graph(figure=ps.getWinLossDrawChart(), className='graph-padding-x'),
    dcc.Graph(figure=ps.getShotsVsGoalsCharts(), className='graph-padding-x'),
    html.Div([
        dcc.Graph(figure=ps.getDisciplineChart()),
        dcc.Graph(figure=ps.getTeamPlayingStyleChart()),
    ], className='graph-row'),
])