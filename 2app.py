
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="MBO Braintrainer", layout="wide")

@st.cache_data
def load_questions():
    return pd.read_csv("mbo_braintrainer_vragen.csv")

questions_df = load_questions()
highscore = st.session_state.get("highscore", 0)

st.title("🧠 MBO Braintrainer")
st.markdown("Test je kennis in logisch redeneren, getallen, patronen, geheugen en taal.")

set_nr = st.selectbox("Kies een set", sorted(questions_df["Set"].unique()))

vragen_set = questions_df[questions_df["Set"] == set_nr].reset_index(drop=True)

score = 0
antwoorden = []

for i, row in vragen_set.iterrows():
    st.subheader(f"Vraag {i+1}: {row['Vraag']}")
    keuze = st.radio("Maak een keuze:", row['Opties'].split(", "), key=f"vraag_{i}")
    correct = keuze == row['Antwoord']
    antwoorden.append((row['Vraag'], keuze, row['Antwoord'], correct))
    if correct:
        score += 1

if st.button("Toon score"):
    st.success(f"Je score: {score} / 10")
    if score > highscore:
        st.session_state["highscore"] = score
        st.balloons()
        st.info("🎉 Nieuwe highscore!")
    else:
        st.info(f"Highscore blijft: {highscore}")

    with st.expander("Toon resultaten"):
        for vraag, gegeven, juist, goed in antwoorden:
            kleur = "✅" if goed else "❌"
            st.markdown(f"{kleur} **{vraag}**  
Je antwoord: *{gegeven}*, Correct: *{juist}*")

st.sidebar.header("📊 Highscore")
st.sidebar.metric("Hoogste score", st.session_state.get("highscore", 0))
