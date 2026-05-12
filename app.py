import streamlit as st
import joblib
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Football AI Pro",
    page_icon="⚽",
    layout="wide"
)

# =========================
# STYLE (MODERN DARK UI)
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

.title {
    font-size: 40px;
    font-weight: bold;
    color: #00ff99;
    text-align: center;
}

.card {
    background: #1f2937;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 0px 15px rgba(0,255,153,0.2);
}

.result-win {
    color: #00ff99;
    font-size: 28px;
    font-weight: bold;
}

.result-lose {
    color: #ff4d4d;
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("football_model.pkl")

# =========================
# TITLE
# =========================
st.markdown("<div class='title'>⚽ Football AI Predictor Pro</div>", unsafe_allow_html=True)

st.write("")

# =========================
# INPUT UI
# =========================
col1, col2 = st.columns(2)

with col1:
    home = st.slider("🏠 Home Strength", 0, 100, 80)

with col2:
    away = st.slider("✈️ Away Strength", 0, 100, 70)

st.write("")

# =========================
# PREDICT
# =========================
if st.button("🚀 Predict Match"):

    X = np.array([[home, away]])

    pred = model.predict(X)
    prob = model.predict_proba(X)[0]

    home_prob = round(prob[1] * 100, 2)
    away_prob = round(prob[0] * 100, 2)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📊 Prediction Result")

    if pred[0] == 1:
        st.markdown("<div class='result-win'>🏆 Home Team Wins</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='result-lose'>🏆 Away Team Wins</div>", unsafe_allow_html=True)

    st.write(f"Home Win Probability: {home_prob}%")
    st.write(f"Away Win Probability: {away_prob}%")

    st.progress(int(home_prob))

    st.markdown("</div>", unsafe_allow_html=True)
