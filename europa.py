import streamlit as st import math

---------- FUNCTIONS ----------

def implied_prob(odds): return 1 / odds if odds > 0 else 0

def normalize(probs): total = sum(probs.values()) return {k: v / total for k, v in probs.items()} if total > 0 else probs

def factorial(n): if n <= 1: return 1 return n * factorial(n - 1)

def poisson_over(lmbda, threshold): cumulative = 0 for k in range(threshold + 1): cumulative += (lmbda ** k * math.exp(-lmbda)) / factorial(k) return 1 - cumulative

---------- UI ----------

st.set_page_config(page_title="Europa League Predictor", layout="centered")

st.title("Europa League Predictor ⚽")

home_team = st.text_input("Home Team") away_team = st.text_input("Away Team")

home_strength = st.number_input("Home Strength", value=1.0, step=0.1) away_strength = st.number_input("Away Strength", value=1.0, step=0.1)

avg_goals = st.number_input("Expected Average Goals", value=2.5, step=0.1)

st.subheader("Bookmaker Odds (Optional)") odds_1 = st.number_input("Odds 1", value=0.0, step=0.01) odds_x = st.number_input("Odds X", value=0.0, step=0.01) odds_2 = st.number_input("Odds 2", value=0.0, step=0.01)

---------- CALCULATE ----------

if st.button("Calculate Probabilities"): if home_strength + away_strength == 0: st.error("Strength values cannot both be zero.") else: raw = { "1": home_strength / (home_strength + away_strength), "2": away_strength / (home_strength + away_strength), } raw["X"] = 1 - (raw["1"] + raw["2"])

prob_1x2 = normalize(raw)

    goal_markets = {
        "Over 1.5": poisson_over(avg_goals, 1),
        "Over 2.5": poisson_over(avg_goals, 2),
        "Over 3.5": poisson_over(avg_goals, 3),
    }

    double_chance = {
        "1X": prob_1x2["1"] + prob_1x2["X"],
        "12": prob_1x2["1"] + prob_1x2["2"],
        "X2": prob_1x2["X"] + prob_1x2["2"],
    }

    st.subheader(f"Results: {home_team} vs {away_team}")

    st.write("### 1X2 Probabilities")
    for k, v in prob_1x2.items():
        st.write(f"{k}: {v*100:.2f}%")

    st.write("### Goal Markets")
    for k, v in goal_markets.items():
        st.write(f"{k}: {v*100:.2f}%")

    st.write("### Double Chance")
    for k, v in double_chance.items():
        st.write(f"{k}: {v*100:.2f}%")

    if odds_1 > 0 and odds_x > 0 and odds_2 > 0:
        odds_probs = normalize({
            "1": implied_prob(odds_1),
            "X": implied_prob(odds_x),
            "2": implied_prob(odds_2),
        })

        st.write("### Bookmaker Implied Probabilities")
        for k, v in odds_probs.items():
            st.write(f"{k}: {v*100:.2f}%")
