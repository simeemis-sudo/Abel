import streamlit as st
from scipy.stats import poisson
import pandas as pd
import numpy as np

st.set_page_config(page_title="Simple Poisson Predictor", layout="centered")

st.title("⚽ Simple Football Poisson Predictor")

st.markdown("Enter team averages and bookmaker odds to calculate probabilities and expected value.")

# ─── Inputs ──────────────────────────────

st.header("League Averages")
avg_home_goals = st.number_input("Avg Home Goals (League)", 0.5, 3.5, 1.50)
avg_away_goals = st.number_input("Avg Away Goals (League)", 0.5, 3.5, 1.20)

st.header("Home Team")
home_scored = st.number_input("Home Goals Scored (Home)", 0.0, 5.0, 2.00)
home_conceded = st.number_input("Home Goals Conceded (Home)", 0.0, 5.0, 1.00)

st.header("Away Team")
away_scored = st.number_input("Away Goals Scored (Away)", 0.0, 5.0, 1.30)
away_conceded = st.number_input("Away Goals Conceded (Away)", 0.0, 5.0, 1.70)

st.header("Bookmaker Odds")
odds_home = st.number_input("Home Win Odds", 1.01, 10.0, 1.90)
odds_draw = st.number_input("Draw Odds", 1.01, 10.0, 3.50)
odds_away = st.number_input("Away Win Odds", 1.01, 10.0, 4.00)

# ─── Calculate Expected Goals ────────────

home_attack = home_scored / avg_home_goals
away_defense = away_conceded / avg_away_goals
away_attack = away_scored / avg_away_goals
home_defense = home_conceded / avg_home_goals

lambda_home = home_attack * away_defense * avg_home_goals
lambda_away = away_attack * home_defense * avg_away_goals

# ─── Calculate Probabilities ─────────────

max_goals = 10
home_win = draw = away_win = over_25 = 0

for h in range(max_goals + 1):
    for a in range(max_goals + 1):
        p = poisson.pmf(h, lambda_home) * poisson.pmf(a, lambda_away)

        if h > a:
            home_win += p
        elif h == a:
            draw += p
        else:
            away_win += p

        if h + a > 2:
            over_25 += p

under_25 = 1 - over_25

# ─── Display Results ─────────────────────

st.header("Expected Goals")
st.write(f"Home λ: **{lambda_home:.2f}**")
st.write(f"Away λ: **{lambda_away:.2f}**")

st.header("Match Probabilities (%)")
st.write(f"Home Win: **{home_win*100:.1f}%**")
st.write(f"Draw: **{draw*100:.1f}%**")
st.write(f"Away Win: **{away_win*100:.1f}%**")
st.write(f"Over 2.5: **{over_25*100:.1f}%**")
st.write(f"Under 2.5: **{under_25*100:.1f}%**")

# ─── Expected Value Calculation ──────────

st.header("Expected Value (%)")

def ev(model_p, odds):
    return (model_p * odds - 1) * 100

st.write(f"Home EV: **{ev(home_win, odds_home):+.2f}%**")
st.write(f"Draw EV: **{ev(draw, odds_draw):+.2f}%**")
st.write(f"Away EV: **{ev(away_win, odds_away):+.2f}%**")

st.markdown("---")
st.caption("Simple Poisson model. For learning and analysis purposes.")
