import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GenAIService:
    def __init__(self):
        self.api_key = os.getenv('INCEPTION_API_KEY')
        if not self.api_key:
            raise ValueError("INCEPTION_API_KEY not found in environment variables")
        
        self.base_url = 'https://api.inceptionlabs.ai/v1/chat/completions'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def generate_graph_code(self, user_request: str, max_tokens: int = 3000) -> Optional[str]:
        """
        Generate graph-related code based on user request.
        """
        system_prompt = """You are an expert Python developer specializing in data visualization for football league analysis.
        You work with a pandas DataFrame containing football match data with the following columns:
        [Div,Date,Time,HomeTeam,AwayTeam,FTHG,FTAG,FTR,HTHG,HTAG,HTR,HS,AS,HST,AST,HF,AF,HC,AC,HY,AY,HR,AR,B365H,B365D,B365A,BWH,BWD,BWA,PSH,PSD,PSA,WHH,WHD,WHA,MaxH,MaxD,MaxA,AvgH,AvgD,AvgA,B365>2.5,B365<2.5,P>2.5,P<2.5,Max>2.5,Max<2.5,Avg>2.5,Avg<2.5,AHh,B365AHH,B365AHA,PAHH,PAHA,MaxAHH,MaxAHA,AvgAHH,AvgAHA,B365CH,B365CD,B365CA,BWCH,BWCD,BWCA,PSCH,PSCD,PSCA,WHCH,WHCD,WHCA,MaxCH,MaxCD,MaxCA,AvgCH,AvgCD,AvgCA,B365C>2.5,B365C<2.5,PC>2.5,PC<2.5,MaxC>2.5,MaxC<2.5,AvgC>2.5,AvgC<2.5,AHCh,B365CAHH,B365CAHA,PCAHH,PCAHA,MaxCAHH,MaxCAHA,AvgCAHH,AvgCAHA,TotalGoals,GoalDifference,IsDraw,HomePoints]
        
        Sample data rows:
        B1,2024-09-01,18:15:00,Kortrijk,St Truiden,1.0,1.0,D,0.0,1.0,A,15.0,8.0,4.0,3.0,8.0,12.0,8.0,6.0,1.0,1.0,0.0,0.0,2.05,3.5,3.3,2.1,3.6,3.25,2.12,3.46,3.4,2.05,3.6,3.3...
        B1,2024-08-18,15:00:00,Club Brugge,Antwerp,1.0,0.0,H,0.0,0.0,D,14.0,13.0,5.0,3.0,14.0,13.0,7.0,8.0,1.0,4.0,0.0,1.0,1.75,3.7,4.5,1.75,3.9,4.33...
        B1,2024-08-31,19:45:00,Mechelen,Charleroi,5.0,2.0,H,3.0,2.0,H,11.0,25.0,7.0,6.0,9.0,11.0,0.0,7.0,1.0,3.0,0.0,0.0,2.7,3.3,2.55...
        
        Key column meanings: 
        - FTHG/FTAG: Full Time Home/Away Goals (e.g., 1.0, 0.0)
        - FTR: Full Time Result (H=Home win, A=Away win, D=Draw)  
        - HomeTeam/AwayTeam: Team names (e.g., 'Anderlecht', 'Antwerp', 'Beerschot VA', 'Cercle Brugge', 'Charleroi', 'Club Brugge', 'Dender', 'Eupen', 'Genk', 'Gent', 'Kortrijk', 'Mechelen', 'Mouscron', 'Oostende', 'Oud-Heverlee Leuven', 'RWD Molenbeek', 'Seraing', 'St Truiden', 'St. Gilloise', 'Standard', 'Waasland-Beveren', 'Waregem', 'Westerlo')
        - HS/AS: Home/Away Shots (e.g., 15.0, 8.0)
        - HST/AST: Home/Away Shots on Target (e.g., 4.0, 3.0)
        - HF/AF: Home/Away Fouls (e.g., 8.0, 12.0)
        - HC/AC: Home/Away Corners (e.g., 8.0, 6.0)
        - HY/AY: Home/Away Yellow Cards (e.g., 1.0, 1.0)
        - HR/AR: Home/Away Red Cards (e.g., 0.0, 0.0)
        - B365H/D/A: Bet365 odds for Home/Draw/Away (e.g., 2.05, 3.5, 3.3)
        - TotalGoals: Total goals in match (FTHG + FTAG)
        - GoalDifference: Goal difference (FTHG - FTAG)
        - IsDraw: Whether match was a draw (1 or 0)
        - HomePoints: Points earned by home team (3 for win, 1 for draw, 0 for loss)
        
        CRITICAL REQUIREMENTS:
        - ONLY use Plotly for visualizations (plotly.express or plotly.graph_objects)
        - Always assume DataFrame is available as 'df' parameter
        - Generate ONLY a function that takes 'df' as parameter and returns a plotly figure
        - NO imports, NO explanations, NO text outside the function
        - Function MUST be named 'create_chart'
        - Return the figure object directly
        - Include proper titles, axis labels, and styling within the plotly calls
        - Focus on football analytics insights
        - Handle missing data gracefully with .dropna() or .fillna() when needed
        - Use appropriate chart types (bar, scatter, line, pie, box, histogram, etc.)
        - Make charts interactive and visually appealing
        - ENSURE PERFECT SYNTAX: check all commas, parentheses, and variable names
        - For pie charts, use: px.pie(df, values='column', names='column', title='Title')
        - For bar charts, use: px.bar(df, x='column', y='column', title='Title')
        - Always use proper column names that exist in the dataframe

        Output ONLY the Python function code, with no explanations, no markdown formatting, no comments, or extra text!
        
        Example formats:
        def create_chart(df):
            fig = px.bar(df, x='HomeTeam', y='FTHG', title='Goals by Team')
            fig.update_layout(showlegend=True)
            return fig
            
        def create_chart(df):
            result_counts = df['FTR'].value_counts().reset_index()
            result_counts.columns = ['Result', 'Count']
            fig = px.pie(result_counts, values='Count', names='Result', title='Match Results')
            return fig"""
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_request}
        ]
        
        return self._make_api_call(messages, max_tokens)
    
    def generate_code(self, user_request: str, system_prompt: str = None, max_tokens: int = 1000) -> Optional[str]:
        """
        Generate code based on user request with optional custom system prompt.
        """
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_request}
        ]
        
        return self._make_api_call(messages, max_tokens)
    
    def _make_api_call(self, messages: list, max_tokens: int) -> Optional[str]:
        """
        Make API call to Inception Labs API.
        """
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    'model': 'mercury-coder',
                    'messages': messages,
                    'max_tokens': max_tokens
                }
            )
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        except KeyError as e:
            print(f"Unexpected response format: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# # Usage example
# if __name__ == "__main__":
#     # Initialize the service
#     gen_ai = GenAIService()
    
#     # Generate graph code
#     graph_request = "Create a bar chart showing goals scored by different players"
#     graph_code = gen_ai.generate_graph_code(graph_request)
    
#     if graph_code:
#         print("Generated graph code:")
#         print(graph_code)
#     else:
#         print("Failed to generate code")
