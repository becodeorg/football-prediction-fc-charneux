import dash
from dash import html, dcc, Input, Output, State, callback, no_update, clientside_callback, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from services.plot_service import PlotService
from services.gen_ai_service import GenAIService
from services.persistence_service import PersistenceService
import plotly.graph_objects as go
import sys
from io import StringIO
import json

dash.register_page(__name__, path="/stats")

ps = PlotService()
gen_ai = GenAIService()
persistence_service = PersistenceService()

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
           style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#414141'}),
    
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
                        style={'backgroundColor': 'transparent', 'borderColor': '#414141'},
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
            
            # Hidden components for localStorage integration
            dcc.Store(id="stored-graphs-data", data=[]),
            html.Div(id="localStorage-trigger", style={'display': 'none'}),
            html.Div(id="clear-storage-trigger", style={'display': 'none'}),
            
        ], width=12)
    ], className="px-3"),
    
], className='stats-container')

# Clientside callback to load graphs from localStorage on page load
clientside_callback(
    """
    function(n_intervals) {
        try {
            var storedData = localStorage.getItem('football_ai_graphs');
            if (storedData) {
                return JSON.parse(storedData);
            }
        } catch (e) {
            console.error('Error loading from localStorage:', e);
        }
        return [];
    }
    """,
    Output("stored-graphs-data", "data"),
    Input("generated-graphs-container", "id"),  # Trigger on page load
    prevent_initial_call=False
)

# Clientside callback to save graphs to localStorage
clientside_callback(
    """
    function(graphs_data) {
        if (graphs_data && graphs_data.length > 0) {
            try {
                localStorage.setItem('football_ai_graphs', JSON.stringify(graphs_data));
            } catch (e) {
                console.error('Error saving to localStorage:', e);
            }
        }
        return "";
    }
    """,
    Output("localStorage-trigger", "children"),
    Input("stored-graphs-data", "data"),
    prevent_initial_call=True
)

# Clientside callback to clear localStorage
clientside_callback(
    """
    function(data) {
        if (data && data.length === 0) {
            try {
                localStorage.removeItem('football_ai_graphs');
                console.log('localStorage cleared');
            } catch (e) {
                console.error('Error clearing localStorage:', e);
            }
        }
        return "";
    }
    """,
    Output("clear-storage-trigger", "children"),
    Input("stored-graphs-data", "data"),
    prevent_initial_call=True
)

# Load stored graphs on page initialization
@callback(
    Output("generated-graphs-container", "children"),
    Input("stored-graphs-data", "data"),
    prevent_initial_call=False
)
def load_stored_graphs(stored_graphs_data):
    """Load and display stored graphs from localStorage on page load."""
    if not stored_graphs_data:
        return []
    
    try:
        graphs_components = []
        for graph_data in reversed(stored_graphs_data):  # Reverse to show newest first
            graph_component = persistence_service.create_graph_component(graph_data)
            graphs_components.append(graph_component)
        
        if graphs_components:
            # Add info message about loaded graphs
            info_alert = dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                f"Loaded {len(graphs_components)} saved graph(s) from your previous session."
            ], color="info", dismissable=True, duration=5000, className="mb-3")
            return [info_alert] + graphs_components
        
        return graphs_components
    except Exception as e:
        error_alert = dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"Error loading saved graphs: {str(e)}"
        ], color="warning", dismissable=True, className="mb-3")
        return [error_alert]

@callback(
    [Output("generated-graphs-container", "children", allow_duplicate=True),
     Output("graph-request-input", "value"),
     Output("loading-placeholder", "children"),
     Output("stored-graphs-data", "data", allow_duplicate=True)],
    [Input("generate-graph-btn", "n_clicks"),
     Input("clear-graphs-btn", "n_clicks")],
    [State("graph-request-input", "value"),
     State("generated-graphs-container", "children"),
     State("stored-graphs-data", "data")],
    prevent_initial_call=True
)
def handle_graph_generation(generate_clicks, clear_clicks, user_request, current_graphs, stored_graphs_data):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Clear all graphs
    if button_id == "clear-graphs-btn" and clear_clicks:
        # Clear localStorage by triggering the clientside callback
        return [], "", "", []
    
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
                return [error_alert] + current_graphs, user_request, "", stored_graphs_data
            
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
                return [error_alert] + current_graphs, user_request, "", stored_graphs_data
            
            # Calculate graph number
            current_graph_count = len([item for item in current_graphs 
                                     if isinstance(item, dict) and 
                                     item.get('type') == 'Div' and 
                                     'mb-4' in item.get('props', {}).get('className', '')])
            graph_number = current_graph_count + 1
            
            # Create graph data for persistence
            graph_data = persistence_service.create_graph_data(
                user_request=user_request,
                generated_code=generated_code,
                graph_number=graph_number
            )
            
            # Create the graph component
            new_graph = persistence_service.create_graph_component(graph_data)
            
            # Update stored data
            updated_stored_data = (stored_graphs_data or []) + [graph_data]
            
            success_alert = dbc.Alert(
                [html.I(className="fas fa-check-circle me-2"), 
                 "Graph generated successfully and saved!"],
                color="success",
                dismissable=True,
                duration=3000,
                className="mb-3"
            )
            
            return [success_alert, new_graph] + current_graphs, "", "", updated_stored_data
            
        except Exception as e:
            error_alert = dbc.Alert(
                [html.I(className="fas fa-bug me-2"), 
                 f"An error occurred: {str(e)}"],
                color="danger",
                dismissable=True,
                className="mb-3"
            )
            return [error_alert] + current_graphs, user_request, "", stored_graphs_data
    
    return no_update, no_update, no_update, no_update

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