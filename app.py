
import streamlit as st

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide"
)

# ----------------------------
# Seitenkopf
# ----------------------------

st.title("PACE Nutrition")
st.subheader("Nutrition that adapts to your training")
st.write(
    "Dein persönlicher Ernährungsplan für Kraft, "
    "Ausdauer und Hybrid-Training."
)

st.divider()

# ----------------------------
# 1. Profil
# ----------------------------

st.header("1. Dein Profil")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input(
        "Alter",
        min_value=18,
        max_value=100,
        value=30
    )
    weight = st.number_input(
        "Gewicht (kg)",
        min_value=35.0,
        max_value=250.0,
        value=62.0,
        step=0.5
    )

with col2:
    height = st.number_input(
        "Grösse (cm)",
        min_value=120,
        max_value=230,
        value=165
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

# ----------------------------
# 2. Training
# ----------------------------

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
        "Trainingsdauer (Minuten)",
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

calculate = st.button(
    "Ernährungsplan berechnen",
    type="primary"
)

if calculate:

    # ----------------------------
    # 3. Kalorienbedarf
    # ----------------------------

    # Mifflin-St Jeor: geschätzter Grundumsatz
    sex_adjustment = 5 if sex == "Männlich" else -161

    bmr = (
        10 * weight
        + 6.25 * height
        - 5 * age
        + sex_adjustment
    )

    activity_factors = {
        "Überwiegend sitzend": 1.35,
        "Gemischt": 1.50,
        "Sehr aktiv": 1.65
    }

    base_calories = bmr * activity_factors[activity]

    # Grobe MET-basierte Schätzung des Trainingsverbrauchs
    met_values = {
        "Ruhetag": 1.0,
        "Krafttraining": 4.5,
        "Laufen": 8.0,
        "Radfahren": 6.5,
        "Schwimmen": 6.0,
        "Koppeltraining": 7.0
    }

    intensity_factors = {
        "Leicht": 0.75,
        "Mittel": 1.0,
        "Intensiv": 1.20
    }

    training_calories = max(
        0,
        (
            met_values[training] * 3.5 * weight / 200 - 1
        )
        * duration
        * intensity_factors[intensity]
    )

    maintenance_calories = base_calories + training_calories

    goal_factors = {
        "Muskeln aufbauen": 1.08,
        "Leistung verbessern": 1.00,
        "Gewicht halten": 1.00
    }

    target_calories = maintenance_calories * goal_factors[goal]

    # ----------------------------
    # 4. Makronährstoffe
    # ----------------------------

    protein = weight * 1.8
    fat = weight * 0.9

    carbs = max(
        0,
        (
            target_calories
            - protein * 4
            - fat * 9
        ) / 4
    )

    st.divider()
    st.header("3. Dein Ernährungsziel")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Kalorien", f"{target_calories:.0f} kcal")
    c2.metric("Protein", f"{protein:.0f} g")
    c3.metric("Kohlenhydrate", f"{carbs:.0f} g")
    c4.metric("Fett", f"{fat:.0f} g")

    with st.expander("Wie wird dein Bedarf berechnet?"):
        st.write(f"Geschätzter Grundumsatz: {bmr:.0f} kcal")
        st.write(
            "Alltagsbedarf inklusive Grundumsatz: "
            f"{base_calories:.0f} kcal"
        )
        st.write(
            f"Zusätzlicher Trainingsverbrauch: "
            f"{training_calories:.0f} kcal"
        )
        st.write(
            "Die Werte sind Schätzungen. Der tatsächliche "
            "Bedarf kann davon abweichen."
        )

    if goal == "Muskeln aufbauen":
        st.info(
            "Für den Muskelaufbau wird ein kleiner "
            "Energieüberschuss von 8 % angesetzt."
        )
    else:
        st.info(
            "Nutze den Wert als Ausgangspunkt und beobachte "
            "deine Energie, Erholung und Gewichtsveränderung."
        )

    # ----------------------------
    # 5. Beispielmenü
    # ----------------------------

    st.divider()
    st.header("4. Dein Tagesmenü")

    st.write(
        "Die folgenden Mahlzeiten sind ein Beispiel. "
        "Ihre Portionen werden noch nicht automatisch "
        "an dein Kalorienziel angepasst."
    )

    meals = [
        {
            "meal": "Frühstück",
            "name": "Porridge mit Beeren und Protein",
            "kcal": 500,
            "protein": 35,
            "carbs": 65,
            "fat": 12,
            "ingredients": [
                "Haferflocken",
                "Beeren",
                "Proteinpulver",
                "Milch oder Pflanzendrink"
            ]
        },
        {
            "meal": "Mittagessen",
            "name": "Reis mit Poulet und Gemüse",
            "kcal": 650,
            "protein": 45,
            "carbs": 80,
            "fat": 14,
            "ingredients": [
                "Reis",
                "Poulet",
                "Gemüse",
                "Olivenöl"
            ]
        },
        {
            "meal": "Snack",
            "name": "Banane mit Skyr",
            "kcal": 250,
            "protein": 20,
            "carbs": 35,
            "fat": 2,
            "ingredients": [
                "Banane",
                "Skyr"
            ]
        },
        {
            "meal": "Abendessen",
            "name": "Lachs mit Kartoffeln und Gemüse",
            "kcal": 600,
            "protein": 40,
            "carbs": 55,
            "fat": 22,
            "ingredients": [
                "Lachs",
                "Kartoffeln",
                "Gemüse",
                "Olivenöl"
            ]
        }
    ]

    for meal in meals:
        with st.expander(
            f"{meal['meal']}: {meal['name']}",
            expanded=True
        ):
            st.write(
                f"**{meal['kcal']} kcal** · "
                f"Protein {meal['protein']} g · "
                f"Kohlenhydrate {meal['carbs']} g · "
                f"Fett {meal['fat']} g"
            )
            st.write("Zutaten: " + ", ".join(meal["ingredients"]))

    total_kcal = sum(meal["kcal"] for meal in meals)
    total_protein = sum(meal["protein"] for meal in meals)
    total_carbs = sum(meal["carbs"] for meal in meals)
    total_fat = sum(meal["fat"] for meal in meals)

    st.subheader("Tagesübersicht")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Menü-Kalorien",
        f"{total_kcal} kcal",
        delta=f"{total_kcal - target_calories:.0f} kcal zum Ziel"
    )
    c2.metric("Protein gesamt", f"{total_protein} g")
    c3.metric("Kohlenhydrate gesamt", f"{total_carbs} g")
    c4.metric("Fett gesamt", f"{total_fat} g")

    if total_kcal < target_calories:
        st.info(
            f"Zum geschätzten Tagesziel fehlen noch "
            f"{target_calories - total_kcal:.0f} kcal."
        )
    elif total_kcal > target_calories:
        st.info(
            f"Der Beispielmenüplan liegt "
            f"{total_kcal - target_calories:.0f} kcal über deinem Ziel."
        )
    else:
        st.success("Der Beispielmenüplan entspricht deinem Tagesziel.")

    # ----------------------------
    # 6. Einkaufsliste
    # ----------------------------

    st.divider()
    st.header("5. Deine Einkaufsliste")

    ingredients = sorted({
        ingredient
        for meal in meals
        for ingredient in meal["ingredients"]
    })

    st.write("Wähle die Zutaten aus, die du einkaufen möchtest.")

    for ingredient in ingredients:
        st.checkbox(ingredient, key=f"shopping_{ingredient}")

st.divider()

st.caption(
    "PACE Nutrition · Your training. Your fuel. "
    "Alle Nährwerte und Energiebedarfe sind Schätzungen."
)
