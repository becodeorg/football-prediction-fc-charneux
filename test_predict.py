import requests

match_data = {
    "HomeTeam": "KV Malines",
    "AwayTeam": "FC Bruges"
}

try:
    response = requests.post('http://127.0.0.1:8000/predict', json=match_data)
    response.raise_for_status()  # Lève une exception pour les erreurs HTTP (4xx ou 5xx)
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
