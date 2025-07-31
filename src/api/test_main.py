import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.api.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_db_connection():
    with patch('src.api.main.get_db_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        yield mock_conn

@pytest.fixture
def mock_load_model():
    with patch('src.api.main.load_model') as mock_load:
        mock_model = MagicMock()
        # Configure the mock model as needed for your tests
        mock_model.classes_ = ['H', 'D', 'A']
        mock_load.return_value = mock_model
        yield mock_model

def test_get_upcoming_matches_success(client, mock_db_connection):
    # Mock the database return value for this test
    mock_db_connection.cursor.return_value.fetchall.return_value = [
        ('2025-08-01', 'Team A', 'Team B'),
        ('2025-08-02', 'Team C', 'Team D')
    ]
    response = client.get("/matches/upcoming")
    assert response.status_code == 200
    assert len(response.json()) > 0 # Check if we get some matches back

def test_get_upcoming_matches_db_error(client, mock_db_connection):
    # Simulate a database error
    mock_db_connection.side_effect = Exception("Database error")
    response = client.get("/matches/upcoming")
    assert response.status_code == 500


def test_predict_success(client, mock_db_connection, mock_load_model):
    # Mock the historical data query
    with patch('pandas.read_sql_query') as mock_read_sql:
        # Create a mock DataFrame
        mock_df = MagicMock()
        mock_df.empty = False
        mock_read_sql.return_value = mock_df

        # Mock the prediction result
        mock_load_model.predict_proba.return_value = [[0.1, 0.2, 0.7]]

        response = client.post("/predict", json={"HomeTeam": "Team A", "AwayTeam": "Team B"})
        assert response.status_code == 200
        data = response.json()
        assert data["prediction"] == "A"

def test_predict_no_model(client, mock_load_model):
    mock_load_model.return_value = None
    response = client.post("/predict", json={"HomeTeam": "Team A", "AwayTeam": "Team B"})
    assert response.status_code == 500
    assert "ML model not loaded" in response.json()["detail"]

def test_predict_no_historical_data(client, mock_db_connection, mock_load_model):
    # Mock the historical data query to return an empty DataFrame
    with patch('pandas.read_sql_query') as mock_read_sql:
        mock_df = MagicMock()
        mock_df.empty = True
        mock_read_sql.return_value = mock_df

        response = client.post("/predict", json={"HomeTeam": "Team A", "AwayTeam": "Team B"})
        assert response.status_code == 400
        assert "Not enough historical data" in response.json()["detail"]
