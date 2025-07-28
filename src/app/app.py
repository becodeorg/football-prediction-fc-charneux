import streamlit as st
# Import prediction function: from src.modeling.model import predict_outcome

st.title("Football Match Predictor")

st.header("Upcoming Matches & Predictions")
# Placeholder for displaying upcoming matches and predictions
st.write("No upcoming matches to display yet.")

st.header("Team Statistics & Odds")
# Placeholder for displaying team stats and odds
st.write("No team statistics or odds to display yet.")

# Example of calling a prediction (will be integrated later)
# if st.button("Get a dummy prediction"):
#     st.write(f"Dummy prediction: {predict_outcome(None)}")