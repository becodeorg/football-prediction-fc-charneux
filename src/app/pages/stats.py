import dash
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from services.plot_service import PlotService
from services.gen_ai_service import GenAIService
import plotly.graph_objects as go
import sys
from io import StringIO

dash.register_page(__name__, path="/stats")

ps = PlotService()
gen_ai = GenAIService()

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
    
    # AI Graph Generation Section
    html.Hr(style={'margin': '50px 0', 'borderColor': '#ddd', 'borderWidth': '2px'}),
    html.H3("🤖 AI Graph Generator", style={'textAlign': 'center', 'marginBottom': '30px'}),
    html.P("Describe the graph you want to create and our AI will generate it for you!", 
           style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#666'}),
    
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.Textarea(
                    id="graph-request-input",
                    placeholder="e.g., 'Create a scatter plot showing the relationship between shots and goals for each team' or 'Show a pie chart of home wins vs away wins vs draws'",
                    style={'minHeight': '100px', 'resize': 'vertical'},
                    className="mb-2"
                ),
            ], className="mb-3"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-magic me-2"), "Generate Graph"],
                        id="generate-graph-btn",
                        color="primary",
                        size="lg",
                        className="w-100"
                    ),
                ], width=6),
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-trash me-2"), "Clear All Graphs"],
                        id="clear-graphs-btn",
                        color="outline-secondary",
                        size="lg",
                        className="w-100"
                    ),
                ], width=6)
            ], className="mb-4"),
            
            # Loading spinner
            dbc.Spinner(
                html.Div(id="loading-placeholder"),
                color="primary",
                size="lg",
                spinner_style={"width": "3rem", "height": "3rem"}
            ),
            
            # Container for generated graphs
            html.Div(id="generated-graphs-container", children=[], className="mt-4"),
            
        ], width=12)
    ], className="px-3"),
    
], className='stats-container')

@callback(
    [Output("generated-graphs-container", "children"),
     Output("graph-request-input", "value"),
     Output("loading-placeholder", "children")],
    [Input("generate-graph-btn", "n_clicks"),
     Input("clear-graphs-btn", "n_clicks")],
    [State("graph-request-input", "value"),
     State("generated-graphs-container", "children")],
    prevent_initial_call=True
)
def handle_graph_generation(generate_clicks, clear_clicks, user_request, current_graphs):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return no_update, no_update, no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Clear all graphs
    if button_id == "clear-graphs-btn" and clear_clicks:
        return [], "", ""
    
    # Generate new graph
    if button_id == "generate-graph-btn" and generate_clicks and user_request:
        try:
            # Show loading state
            loading_msg = dbc.Alert(
                [html.I(className="fas fa-spinner fa-spin me-2"), "Generating your graph..."],
                color="info",
                className="mb-3"
            )
            
            # Generate code using AI service
            generated_code = gen_ai.generate_graph_code(user_request)
            
            if not generated_code:
                error_alert = dbc.Alert(
                    [html.I(className="fas fa-exclamation-triangle me-2"), 
                     "Failed to generate graph. Please try again with a different description."],
                    color="danger",
                    dismissable=True,
                    className="mb-3"
                )
                return [error_alert] + current_graphs, user_request, ""
            
            # Execute the generated code safely
            fig = execute_graph_code(generated_code, ps.df)
            
            if fig is None:
                error_alert = dbc.Alert(
                    [html.I(className="fas fa-code me-2"), 
                     "Generated code had errors. Please try rephrasing your request."],
                    color="warning",
                    dismissable=True,
                    className="mb-3"
                )
                return [error_alert] + current_graphs, user_request, ""
            
            # Create unique index based on current timestamp or use a counter
            # This ensures each graph has a truly unique index
            import time
            unique_index = int(time.time() * 1000)  # Use timestamp for unique ID
            
            # Calculate graph number - count actual graph components, excluding alerts
            current_graph_count = len([item for item in current_graphs 
                                     if isinstance(item, dict) and 
                                     item.get('type') == 'Div' and 
                                     'mb-4' in item.get('props', {}).get('className', '')])
            graph_number = current_graph_count + 1
            
            new_graph = html.Div([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.H5([
                                html.I(className="fas fa-chart-line me-2"),
                                f"Generated Graph #{graph_number}"
                            ], className="mb-2"),
                            html.P(user_request, className="text-muted mb-2", style={'fontStyle': 'italic'}),
                        ], width=8),
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-code me-2"),
                                "View Code"
                            ],
                                id={'type': 'code-toggle', 'index': unique_index},
                                color="outline-info",
                                size="sm",
                                className="float-end"
                            ),
                        ], width=4, className="d-flex align-items-center justify-content-end")
                    ], className="mb-3"),
                    
                    # Collapsible code section
                    dbc.Collapse([
                        dbc.Card([
                            dbc.CardHeader([
                                html.I(className="fas fa-terminal me-2"),
                                "Generated Python Code"
                            ]),
                            dbc.CardBody([
                                html.Pre([
                                    html.Code(generated_code, style={
                                        'fontSize': '12px',
                                        'lineHeight': '1.4',
                                        'color': '#2d3748'
                                    })
                                ], style={
                                    'backgroundColor': '#f7fafc',
                                    'border': '1px solid #e2e8f0',
                                    'borderRadius': '6px',
                                    'padding': '12px',
                                    'margin': '0',
                                    'overflow': 'auto',
                                    'maxHeight': '300px'
                                }),
                                html.Small([
                                    html.I(className="fas fa-info-circle me-1"),
                                    "This code was automatically generated by AI based on your request."
                                ], className="text-muted mt-2 d-block")
                            ])
                        ], className="mb-3")
                    ],
                        id={'type': 'code-collapse', 'index': unique_index},
                        is_open=False
                    ),
                ]),
                dcc.Graph(figure=fig, className='graph-padding-x'),
                html.Hr(style={'margin': '20px 0'})
            ], className="mb-4", style={
                'border': '2px solid #e9ecef',
                'borderRadius': '10px',
                'padding': '20px',
                'backgroundColor': '#f8f9fa'
            })
            
            success_alert = dbc.Alert(
                [html.I(className="fas fa-check-circle me-2"), 
                 "Graph generated successfully!"],
                color="success",
                dismissable=True,
                duration=3000,
                className="mb-3"
            )
            
            return [success_alert, new_graph] + current_graphs, "", ""
            
        except Exception as e:
            error_alert = dbc.Alert(
                [html.I(className="fas fa-bug me-2"), 
                 f"An error occurred: {str(e)}"],
                color="danger",
                dismissable=True,
                className="mb-3"
            )
            return [error_alert] + current_graphs, user_request, ""
    
    return no_update, no_update, ""

@callback(
    Output({'type': 'code-collapse', 'index': dash.dependencies.MATCH}, 'is_open'),
    Input({'type': 'code-toggle', 'index': dash.dependencies.MATCH}, 'n_clicks'),
    State({'type': 'code-collapse', 'index': dash.dependencies.MATCH}, 'is_open'),
    prevent_initial_call=True
)
def toggle_code_collapse(n_clicks, is_open):
    """Toggle the visibility of the code collapse for individual graphs."""
    if n_clicks:
        return not is_open
    return is_open

def execute_graph_code(code: str, df: pd.DataFrame):
    """
    Safely execute the generated graph code and return the figure.
    """
    try:
        # Import necessary modules
        import numpy as np
        import re
        
        # Clean up common syntax errors in generated code
        cleaned_code = clean_generated_code(code)
        
        # Create a restricted execution environment with all necessary imports
        safe_globals = {
            "__builtins__": {
                # Allow only safe built-in functions
                "len": len,
                "range": range,
                "enumerate": enumerate,
                "zip": zip,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "min": min,
                "max": max,
                "sum": sum,
                "round": round,
                "abs": abs,
                "sorted": sorted,
                "reversed": reversed,
            },
            # Add necessary modules to globals
            'pd': pd,
            'px': px,
            'go': go,
            'np': np
        }
        
        local_vars = {
            'df': df,
        }
        
        print(f"Executing cleaned code: {cleaned_code}")
        
        # Execute the cleaned code
        exec(cleaned_code, safe_globals, local_vars)
        
        # Get the created figure
        if 'create_chart' in local_vars:
            fig = local_vars['create_chart'](df)
            return fig
        else:
            print("No 'create_chart' function found in generated code")
            return None
            
    except Exception as e:
        print(f"Error executing graph code: {e}")
        # print(f"Generated code was: {code}")
        return None

def clean_generated_code(code: str) -> str:
    """
    Clean up common syntax errors in AI-generated code.
    """
    import re
    
    # Remove extra commas (like "names=result,, values=")
    code = re.sub(r'=\s*\w+,\s*,', '=', code)
    
    # Fix common plotly syntax errors
    # Fix "names=result," -> "names=result_counts.index,"
    if 'result_counts' in code and 'names=result,' in code:
        code = code.replace('names=result,', 'names=result_counts.index,')
    
    # Fix other common patterns
    code = re.sub(r',\s*,', ',', code)  # Remove double commas
    code = re.sub(r'=\s*,', '=', code)  # Remove assignments to comma
    
    # Remove any trailing commas before closing parentheses
    code = re.sub(r',\s*\)', ')', code)
    
    return code