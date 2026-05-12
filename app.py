import streamlit as st

st.title("⚽ Football AI Predictor")

team1 = st.slider("Team 1 Strength", 50, 100, 80)
team2 = st.slider("Team 2 Strength", 50, 100, 75)

if st.button("Predict Match"):

    if team1 > team2:
        st.success("🏆 Team 1 Win")
        st.write("Predicted Score: 2-1")

    elif team2 > team1:
        st.success("🏆 Team 2 Win")
        st.write("Predicted Score: 1-2")

    else:
        st.warning("🤝 Draw")
