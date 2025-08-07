import json
import time
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from services.plot_service import PlotService
from services.gen_ai_service import GenAIService


class PersistenceService:
    """
    Service for persisting AI-generated graphs using browser localStorage.
    """
    
    def __init__(self):
        self.storage_key = "football_ai_graphs"
        self.ps = PlotService()
        self.gen_ai = GenAIService()
    
    def create_graph_data(self, user_request: str, generated_code: str, graph_number: int) -> Dict[str, Any]:
        """
        Create a standardized graph data structure for storage.
        """
        return {
            'id': int(time.time() * 1000),  # Unique timestamp-based ID
            'user_request': user_request,
            'generated_code': generated_code,
            'graph_number': graph_number,
            'created_at': time.time(),
            'created_at_readable': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        }
    
    def serialize_graph_data(self, graphs_data: List[Dict[str, Any]]) -> str:
        """
        Serialize graph data to JSON string for localStorage.
        """
        return json.dumps(graphs_data, indent=2)
    
    def deserialize_graph_data(self, json_str: str) -> List[Dict[str, Any]]:
        """
        Deserialize graph data from JSON string.
        """
        try:
            return json.loads(json_str) if json_str else []
        except json.JSONDecodeError:
            return []
    
    def create_graph_component(self, graph_data: Dict[str, Any]) -> html.Div:
        """
        Create a Dash component for a persisted graph.
        """
        try:
            # Execute the stored code to recreate the figure
            fig = self._execute_stored_code(graph_data['generated_code'])
            
            if fig is None:
                return self._create_error_component(graph_data, "Failed to recreate graph from stored code")
            
            unique_index = graph_data['id']
            
            return html.Div([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.H5([
                                html.I(className="fas fa-chart-line me-2"),
                                f"Generated Graph #{graph_data['graph_number']} ",
                                html.Small(f"(Saved: {graph_data['created_at_readable']})", 
                                         className="text-muted", style={'fontSize': '0.7em'})
                            ], className="mb-2"),
                            html.P(graph_data['user_request'], 
                                 className="text-muted mb-2", 
                                 style={'fontStyle': 'italic'}),
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
                                    html.Code(graph_data['generated_code'], style={
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
            
        except Exception as e:
            return self._create_error_component(graph_data, f"Error recreating graph: {str(e)}")
    
    def _create_error_component(self, graph_data: Dict[str, Any], error_message: str) -> html.Div:
        """
        Create an error component when graph recreation fails.
        """
        return html.Div([
            dbc.Alert([
                html.I(className="fas fa-exclamation-triangle me-2"),
                html.Strong("Error Loading Saved Graph: "),
                error_message,
                html.Br(),
                html.Small(f"Original request: {graph_data['user_request']}", className="text-muted")
            ], color="warning", className="mb-3")
        ])
    
    def _execute_stored_code(self, code: str):
        """
        Execute stored graph code and return the figure.
        """
        try:
            # Import necessary modules
            import re
            
            # Clean up common syntax errors in generated code
            cleaned_code = self._clean_generated_code(code)
            
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
                'df': self.ps.df,
            }
            
            # Execute the cleaned code
            exec(cleaned_code, safe_globals, local_vars)
            
            # Get the created figure
            if 'create_chart' in local_vars:
                fig = local_vars['create_chart'](self.ps.df)
                return fig
            else:
                print("No 'create_chart' function found in stored code")
                return None
                
        except Exception as e:
            print(f"Error executing stored graph code: {e}")
            return None
    
    def _clean_generated_code(self, code: str) -> str:
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
    
    def get_next_graph_number(self, existing_graphs_data: List[Dict[str, Any]]) -> int:
        """
        Calculate the next graph number based on existing graphs.
        """
        if not existing_graphs_data:
            return 1
        
        existing_numbers = [graph.get('graph_number', 0) for graph in existing_graphs_data]
        return max(existing_numbers) + 1 if existing_numbers else 1
    
    def create_storage_script(self, graphs_data: List[Dict[str, Any]]) -> html.Script:
        """
        Create a script element to store data in localStorage.
        """
        json_data = self.serialize_graph_data(graphs_data)
        # Escape single quotes in JSON data
        escaped_json = json_data.replace("'", "\\'")
        script_content = f"""
        localStorage.setItem('{self.storage_key}', '{escaped_json}');
        """
        return html.Script(script_content)
    
    def create_retrieval_script(self) -> html.Script:
        """
        Create a script element to retrieve data from localStorage.
        """
        script_content = f"""
        window.addEventListener('DOMContentLoaded', function() {{
            var storedData = localStorage.getItem('{self.storage_key}');
            if (storedData) {{
                // Trigger a custom event with the stored data
                var event = new CustomEvent('loadStoredGraphs', {{
                    detail: {{ data: storedData }}
                }});
                window.dispatchEvent(event);
            }}
        }});
        """
        return html.Script(script_content)
    
    def clear_storage_script(self) -> html.Script:
        """
        Create a script element to clear localStorage.
        """
        script_content = f"""
        localStorage.removeItem('{self.storage_key}');
        """
        return html.Script(script_content)
