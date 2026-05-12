import streamlit as st
import joblib
import numpy as np
import requests
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Football AI Pro Max",
    page_icon="⚽",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("football_model.pkl")

# =========================
# TITLE
# =========================
st.title("⚽ Football AI Pro Max Dashboard")

st.write("AI Prediction + Stats + Live Ready System")

# =========================
# TEAM INPUT
# =========================
col1, col2 = st.columns(2)

with col1:
    home = st.slider("🏠 Home Strength", 0, 100, 80)

with col2:
    away = st.slider("✈️ Away Strength", 0, 100, 70)

# =========================
# OPTIONAL API SECTION (READY FOR REAL DATA)
# =========================
st.subheader("🔴 Live Data (Optional API)")

api_url = st.text_input("Enter Football API URL (optional)")

live_data = None

if api_url:
    try:
        live_data = requests.get(api_url).json()
        st.success("Live data loaded!")
        st.json(live_data)
    except:
        st.warning("API failed or invalid URL")

# =========================
# PREDICTION
# =========================
if st.button("🚀 Predict Match"):

    X = np.array([[home, away]])
    pred = model.predict(X)
    prob = model.predict_proba(X)[0]

    home_prob = float(prob[1] * 100)
    away_prob = float(prob[0] * 100)

    st.subheader("📊 AI Prediction Result")

    if pred[0] == 1:
        st.success("🏆 Home Team Likely WIN")
    else:
        st.error("🏆 Away Team Likely WIN")

    st.write("Home Win %:", round(home_prob, 2))
    st.write("Away Win %:", round(away_prob, 2))

    st.progress(int(home_prob))

    # =========================
    # CHART SECTION
    # =========================
    st.subheader("📈 Probability Chart")

    fig, ax = plt.subplots()

    teams = ["Home", "Away"]
    values = [home_prob, away_prob]

    ax.bar(teams, values)

    st.pyplot(fig)

    # =========================
    # SIMPLE AI ANALYSIS
    # =========================
    st.subheader("🧠 AI Analysis")

    if home > away:
        st.info("Home team has stronger squad rating and advantage.")
    elif away > home:
        st.info("Away team shows better strength metrics.")
    else:
        st.info("Teams are evenly matched, draw possible.")

# =========================
# FOOTER
# =========================
st.write("---")
st.caption("Football AI Pro Max | Streamlit Powered")
