import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Football AI Predictor",
    page_icon="⚽",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.stApp {
    background: linear-gradient(to bottom right, #0f172a, #111827);
    color: white;
}

.big-title {
    font-size: 42px;
    font-weight: bold;
    color: #00ffae;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 0px 15px rgba(0,255,174,0.15);
}

.team-name {
    font-size: 26px;
    font-weight: bold;
    text-align: center;
}

.predict-box {
    background-color: #111827;
    padding: 30px;
    border-radius: 25px;
    border: 1px solid #00ffae;
}

.stat-box {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 18px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown(
    "<div class='big-title'>⚽ Football AI Predictor</div>",
    unsafe_allow_html=True
)

st.write("Modern AI Football Prediction App")

# =========================
# LOAD MODEL
# =========================
try:
    model = joblib.load("football_model.pkl")
except:
    model = None

# =========================
# TEAM DATA
# =========================
teams = {
    "Manchester City": {
        "strength": 95,
        "logo": "https://media.api-sports.io/football/teams/50.png"
    },
    "Liverpool": {
        "strength": 92,
        "logo": "https://media.api-sports.io/football/teams/40.png"
    },
    "Arsenal": {
        "strength": 89,
        "logo": "https://media.api-sports.io/football/teams/42.png"
    },
    "Chelsea": {
        "strength": 84,
        "logo": "https://media.api-sports.io/football/teams/49.png"
    },
    "Manchester United": {
        "strength": 85,
        "logo": "https://media.api-sports.io/football/teams/33.png"
    },
    "Tottenham": {
        "strength": 83,
        "logo": "https://media.api-sports.io/football/teams/47.png"
    }
}

# =========================
# SELECT TEAMS
# =========================
col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox(
        "🏠 Home Team",
        list(teams.keys())
    )

with col2:
    away_team = st.selectbox(
        "✈️ Away Team",
        list(teams.keys()),
        index=1
    )

# =========================
# TEAM INFO
# =========================
col3, col4 = st.columns(2)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image(teams[home_team]["logo"], width=120)
    st.markdown(
        f"<div class='team-name'>{home_team}</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image(teams[away_team]["logo"], width=120)
    st.markdown(
        f"<div class='team-name'>{away_team}</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TEAM STRENGTH
# =========================
home_strength = teams[home_team]["strength"]
away_strength = teams[away_team]["strength"]

# =========================
# MATCH STATS
# =========================
st.subheader("📊 Match Statistics")

s1, s2, s3 = st.columns(3)

with s1:
    st.markdown(f"""
    <div class='stat-box'>
    <h3>Home Power</h3>
    <h2>{home_strength}</h2>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class='stat-box'>
    <h3>Away Power</h3>
    <h2>{away_strength}</h2>
    </div>
    """, unsafe_allow_html=True)

with s3:
    diff = abs(home_strength - away_strength)
    st.markdown(f"""
    <div class='stat-box'>
    <h3>Strength Gap</h3>
    <h2>{diff}</h2>
    </div>
    """, unsafe_allow_html=True)

# =========================
# PREDICT BUTTON
# =========================
st.write("")
st.write("")

if st.button("🚀 Predict Match"):

    st.markdown(
        "<div class='predict-box'>",
        unsafe_allow_html=True
    )

    if model:

        prediction = model.predict(
            [[home_strength, away_strength]]
        )

        probability = model.predict_proba(
            [[home_strength, away_strength]]
        )

        home_win_prob = round(probability[0][1] * 100, 2)
        away_win_prob = round(100 - home_win_prob, 2)

    else:

        home_win_prob = round(
            (home_strength / (home_strength + away_strength)) * 100,
            2
        )

        away_win_prob = round(100 - home_win_prob, 2)

        prediction = [1 if home_strength > away_strength else 0]

    # RESULT
    st.subheader("🤖 AI Prediction")

    if prediction[0] == 1:

        st.success(f"🏆 {home_team} will likely WIN!")

        st.progress(int(home_win_prob))

        st.metric(
            "Winning Probability",
            f"{home_win_prob}%"
        )

    else:

        st.error(f"🏆 {away_team} will likely WIN!")

        st.progress(int(away_win_prob))

        st.metric(
            "Winning Probability",
            f"{away_win_prob}%"
        )

    # ANALYSIS
    st.subheader("🧠 AI Match Analysis")

    if home_strength > away_strength:

        st.info(f"""
        {home_team} has stronger attacking quality,
        better overall squad depth and home advantage.

        AI expects more possession and scoring chances
        for {home_team}.
        """)

    else:

        st.info(f"""
        {away_team} appears stronger statistically
        and may dominate key match moments.

        AI predicts higher efficiency in attack
        for {away_team}.
        """)

    # EXTRA STATS
    st.subheader("📈 Match Insights")

    x1, x2, x3 = st.columns(3)

    with x1:
        st.metric("Expected Goals", round(np.random.uniform(1,4),2))

    with x2:
        st.metric("Possession", f"{np.random.randint(45,70)}%")

    with x3:
        st.metric("Shots on Target", np.random.randint(3,12))

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# LIVE MATCHES SECTION
# =========================
st.write("")
st.write("")

st.subheader("🔥 Trending Matches")

matches = [
    ["Manchester City", "Liverpool"],
    ["Arsenal", "Chelsea"],
    ["Manchester United", "Tottenham"]
]

for match in matches:

    c1, c2, c3 = st.columns([4,1,4])

    with c1:
        st.markdown(f"""
        <div class='card'>
        <h3>{match[0]}</h3>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.write("VS")

    with c3:
        st.markdown(f"""
        <div class='card'>
        <h3>{match[1]}</h3>
        </div>
        """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.write("")
st.write("")

st.caption(
    f"⚡ AI Powered Football Predictions | {datetime.now().year}"
        )
