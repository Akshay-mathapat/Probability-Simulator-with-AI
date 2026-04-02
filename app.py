import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
import requests

# Page Config
st.set_page_config(page_title="Probability Simulator", page_icon="🎲", layout="wide")

# Load Lottie Animation
def load_lottie(url):
    r = requests.get(url)
    return r.json()

lottie = load_lottie("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")

# UI Header
col1, col2 = st.columns([2,1])

with col1:
    st.title("🎲 Probability Simulator")
    st.write("Interactive simulation of probability experiments with real-time insights.")

with col2:
    st_lottie(lottie, height=150)

# Sidebar
st.sidebar.header("⚙️ Simulation Controls")
experiment = st.sidebar.selectbox("Experiment", ["Coin Toss", "Dice Roll"])
trials = st.sidebar.slider("Trials", 10, 10000, 500)
run = st.sidebar.button("🚀 Run Simulation")

# Tabs
tab1, tab2 = st.tabs(["📊 Simulation", "📘 Theory"])

if run:
    if experiment == "Coin Toss":
        outcomes = np.random.choice(["Heads", "Tails"], size=trials)
        df = pd.Series(outcomes).value_counts()
        theoretical = {"Heads": 0.5, "Tails": 0.5}
    else:
        outcomes = np.random.randint(1, 7, size=trials)
        df = pd.Series(outcomes).value_counts().sort_index()
        theoretical = {i: 1/6 for i in range(1, 7)}

    exp_prob = df / trials

    result_df = pd.DataFrame({
        "Frequency": df,
        "Experimental Probability": exp_prob,
        "Theoretical Probability": pd.Series(theoretical)
    })

    with tab1:
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("📋 Results")
            st.dataframe(result_df)

        with c2:
            st.subheader("📈 Visualization")
            fig, ax = plt.subplots()
            result_df["Experimental Probability"].plot(kind='bar', ax=ax)
            st.pyplot(fig)

        st.download_button("⬇ Download CSV", result_df.to_csv(), "results.csv")

    with tab2:
        st.subheader("📘 Theoretical Explanation")
        if experiment == "Coin Toss":
            st.write("Probability of Heads = 0.5, Tails = 0.5")
        else:
            st.write("Each outcome (1–6) has probability = 1/6")

else:
    st.info("👈 Select options and run simulation")