import streamlit as st

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide"
)

st.title("PACE Nutrition")
st.subheader("Nutrition that adapts to your training")

st.write(
    "Dein persönlicher Ernährungsplan für Kraft, "
    "Ausdauer und Hybrid-Training."
)

st.divider()

st.header("Dein Profil")

col1, col2, col3 = st.columns(3)

with col1:
    weight = st.number_input(
        "Körpergewicht (kg)",
        min_value=30.0,
        max_value=250.0,
        value=62.0,
        step=0.5
    )

with col2:
    height = st.number_input(
        "Körpergrösse (cm)",
        min_value=100,
        max_value=230,
        value=165
    )

with col3:
    goal = st.selectbox(
        "Dein Ziel",
        [
            "Muskeln aufbauen",
            "Leistung verbessern",
            "Gewicht halten"
        ]
    )

st.header("Dein heutiges Training")

training = st.selectbox(
    "Welche Einheit steht heute an?",
    [
        "Ruhetag",
        "Krafttraining",
        "Laufen",
        "Radfahren",
        "Schwimmen",
        "Koppeltraining"
    ]
)

duration = st.slider(
    "Trainingsdauer (Minuten)",
    min_value=0,
    max_value=240,
    value=60,
    step=15
)

if st.button("Mein Profil anzeigen"):
    st.success("Dein Profil wurde berechnet!")

    st.write(f"**Gewicht:** {weight} kg")
    st.write(f"**Grösse:** {height} cm")
    st.write(f"**Ziel:** {goal}")
    st.write(f"**Training:** {training}")
    st.write(f"**Dauer:** {duration} Minuten")

st.caption("PACE Nutrition · Your training. Your fuel.")
