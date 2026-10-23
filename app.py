
import streamlit as st

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide"
)

st.title("PACE Nutrition")
st.subheader("Nutrition that adapts to your training")
st.write(
    "Deine Ernährung abgestimmt auf Kraft, Ausdauer "
    "und Muskelaufbau."
)

st.divider()

st.header("1. Dein Profil")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input(
        "Alter", min_value=18, max_value=100, value=30
    )
    weight = st.number_input(
        "Gewicht (kg)", min_value=35.0,
        max_value=250.0, value=62.0, step=0.5
    )

with col2:
    height = st.number_input(
        "Grösse (cm)", min_value=120,
        max_value=230, value=165
    )
    sex = st.selectbox(
        "Berechnungsgrundlage",
        ["Männlich", "Weiblich"]
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
    activity = st.selectbox(
        "Alltagsaktivität ohne Sport",
        [
            "Überwiegend sitzend",
            "Gemischt",
            "Sehr aktiv"
        ]
    )

st.divider()
st.header("2. Dein heutiges Training")

col1, col2, col3 = st.columns(3)

with col1:
    training = st.selectbox(
        "Trainingsart",
        [
            "Ruhetag",
            "Krafttraining",
            "Laufen",
            "Radfahren",
            "Schwimmen",
            "Koppeltraining"
        ]
    )

with col2:
    duration = st.slider(
        "Dauer (Minuten)",
        min_value=0,
        max_value=240,
        value=60,
        step=15
    )

with col3:
    intensity = st.select_slider(
        "Intensität",
        options=["Leicht", "Mittel", "Intensiv"],
        value="Mittel"
    )

if st.button("Mein Ernährungsziel berechnen", type="primary"):

    # Grundumsatz nach Mifflin-St Jeor
    sex_adjustment = 5 if sex == "Männlich" else -161

    bmr = (
        10 * weight
        + 6.25 * height
        - 5 * age
        + sex_adjustment
    )

    # Grobe Alltagsaktivität ohne geplantes Training
    activity_factor = {
        "Überwiegend sitzend": 1.35,
        "Gemischt": 1.50,
        "Sehr aktiv": 1.65
    }[activity]

    daily_base = bmr * activity_factor

    # Grobe MET-Schätzwerte für den Prototyp
    met_values = {
        "Ruhetag": 1.0,
        "Krafttraining": 4.5,
        "Laufen": 8.0,
        "Radfahren": 6.5,
        "Schwimmen": 6.0,
        "Koppeltraining": 7.0
    }

    intensity_factor = {
        "Leicht": 0.75,
        "Mittel": 1.0,
        "Intensiv": 1.20
    }[intensity]

    # Nur zusätzliche Energie über Ruheverbrauch
    training_kcal = max(
        0,
        (met_values[training] * 3.5 * weight / 200 - 1)
        * duration
        * intensity_factor
    )

    # Geschätzter Tagesbedarf
    maintenance = daily_base + training_kcal

    goal_factor = {
        "Muskeln aufbauen": 1.08,
        "Leistung verbessern": 1.00,
        "Gewicht halten": 1.00
    }[goal]

    target_kcal = maintenance * goal_factor

    # Makros: Protein und Fett zuerst, Rest Kohlenhydrate
    protein = weight * 1.8
    fat = weight * 0.9
    carbs = max(
        0,
        (target_kcal - protein * 4 - fat * 9) / 4
    )

    st.divider()
    st.header("3. Deine Ergebnisse")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Tagesziel", f"{target_kcal:.0f} kcal")
    c2.metric("Protein", f"{protein:.0f} g")
    c3.metric("Kohlenhydrate", f"{carbs:.0f} g")
    c4.metric("Fett", f"{fat:.0f} g")

    st.subheader("So setzt sich dein Bedarf zusammen")

    st.write(f"**Geschätzter Grundumsatz:** {bmr:.0f} kcal")
    st.write(f"**Alltagsbedarf inkl. Grundumsatz:** {daily_base:.0f} kcal")
    st.write(f"**Geschätzter Trainingsverbrauch:** {training_kcal:.0f} kcal")

    if goal == "Muskeln aufbauen":
        st.info(
            "Für den Muskelaufbau wird hier ein kleiner "
            "Energieüberschuss von 8 % angesetzt. Beobachte "
            "Gewicht, Leistung und Erholung und passe das "
            "Ziel bei Bedarf an."
        )
    else:
        st.info(
            "Das Ergebnis ist ein Startwert. Passe die "
            "Kalorien anhand deiner Entwicklung, deines "
            "Hungers und deiner Trainingsleistung an."
        )

    st.caption(
        "Prototyp: Alle Werte sind Schätzungen. "
        "Der Trainingsverbrauch hängt stark von Tempo, "
        "Technik und tatsächlicher Intensität ab."
    )

st.divider()
st.caption("PACE Nutrition | Your training. Your fuel.")
