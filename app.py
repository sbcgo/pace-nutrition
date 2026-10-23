
import streamlit as st

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide"
)

# -----------------------------------------
# Titel
# -----------------------------------------
st.title("🥗 PACE Nutrition")
st.subheader("Dein Ernährungsplan für Kraft und Ausdauer")
st.write(
    "Plane deine Ernährung passend zu deinem Training "
    "und unterstütze deine Leistung und Muskelentwicklung."
)

st.divider()

# -----------------------------------------
# Profil
# -----------------------------------------
st.header("👤 Dein Profil")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input(
        "Alter",
        min_value=16,
        max_value=100,
        value=30
    )

with col2:
    weight = st.number_input(
        "Gewicht (kg)",
        min_value=35.0,
        max_value=200.0,
        value=62.0,
        step=0.5
    )

with col3:
    height = st.number_input(
        "Grösse (cm)",
        min_value=130,
        max_value=230,
        value=165
    )

sex = st.selectbox(
    "Geschlecht",
    ["Männlich", "Weiblich"]
)

goal = st.selectbox(
    "Dein Hauptziel",
    [
        "Muskeln aufbauen",
        "Leistung verbessern",
        "Gewicht halten"
    ]
)

activity = st.selectbox(
    "Allgemeine Alltagsaktivität",
    [
        "Wenig Bewegung",
        "Leicht aktiv",
        "Moderat aktiv",
        "Sehr aktiv"
    ],
    index=2
)

st.divider()

# -----------------------------------------
# Training
# -----------------------------------------
st.header("🏋️ Deine heutige Trainingseinheit")

training_type = st.selectbox(
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

col4, col5 = st.columns(2)

with col4:
    duration = st.slider(
        "Trainingsdauer (Minuten)",
        min_value=0,
        max_value=240,
        value=60,
        step=15
    )

with col5:
    intensity = st.select_slider(
        "Trainingsintensität",
        options=["Leicht", "Moderat", "Intensiv"],
        value="Moderat"
    )

st.caption(
    "Die Berechnung ist eine grobe Orientierung und ersetzt "
    "keine individuelle Ernährungsberatung."
)

st.divider()

# -----------------------------------------
# Berechnung starten und Status speichern
# -----------------------------------------
if "calculated" not in st.session_state:
    st.session_state.calculated = False

if st.button(
    "Ernährungsplan berechnen",
    type="primary"
):
    st.session_state.calculated = True

# -----------------------------------------
# Ergebnisse anzeigen
# -----------------------------------------
if st.session_state.calculated:

    # Grundumsatz nach Mifflin-St Jeor
    if sex == "Männlich":
        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            + 5
        )
    else:
        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            - 161
        )

    # Alltagsaktivität
    activity_factors = {
        "Wenig Bewegung": 1.2,
        "Leicht aktiv": 1.375,
        "Moderat aktiv": 1.55,
        "Sehr aktiv": 1.725
    }

    daily_energy = bmr * activity_factors[activity]

    # Grobe Schätzung des zusätzlichen Trainingsverbrauchs
    met_values = {
        "Ruhetag": 0,
        "Krafttraining": 5,
        "Laufen": 9,
        "Radfahren": 7,
        "Schwimmen": 7,
        "Koppeltraining": 8
    }

    intensity_factors = {
        "Leicht": 0.75,
        "Moderat": 1.0,
        "Intensiv": 1.2
    }

    met = met_values[training_type]
    training_calories = max(
        0,
        (met * 3.5 * weight / 200) * duration
        * intensity_factors[intensity]
    )

    total_calories = daily_energy + training_calories

    # Zielanpassung
    if goal == "Muskeln aufbauen":
        calorie_target = total_calories * 1.08
    elif goal == "Leistung verbessern":
        calorie_target = total_calories
    else:
        calorie_target = total_calories

    # Makros
    protein_target = weight * 1.8
    fat_target = weight * 0.9

    carb_target = max(
        0,
        (calorie_target - protein_target * 4 - fat_target * 9) / 4
    )

    st.header("📊 Dein Tagesziel")

    col6, col7, col8, col9 = st.columns(4)

    with col6:
        st.metric(
            "Kalorien",
            f"{round(calorie_target):,} kcal".replace(",", "'")
        )

    with col7:
        st.metric(
            "Protein",
            f"{round(protein_target)} g"
        )

    with col8:
        st.metric(
            "Kohlenhydrate",
            f"{round(carb_target)} g"
        )

    with col9:
        st.metric(
            "Fett",
            f"{round(fat_target)} g"
        )

    st.caption(
        "Schätzwerte: Der tatsächliche Energiebedarf hängt unter anderem "
        "von Trainingsbelastung, Erholung und individuellem Stoffwechsel ab."
    )

    st.divider()

    # -----------------------------------------
    # Beispiel-Menü
    # -----------------------------------------
    st.header("🍽️ Dein Beispiel-Menü")

    meals = [
        {
            "meal": "🥣 Frühstück: Porridge mit Beeren und Protein",
            "calories": 500,
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
            "meal": "🍚 Mittagessen: Reis mit Poulet und Gemüse",
            "calories": 650,
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
            "meal": "🍌 Snack: Banane mit Skyr",
            "calories": 250,
            "protein": 20,
            "carbs": 35,
            "fat": 2,
            "ingredients": [
                "Banane",
                "Skyr"
            ]
        },
        {
            "meal": "🐟 Abendessen: Lachs mit Kartoffeln und Gemüse",
            "calories": 600,
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

    total_meal_calories = sum(
        meal["calories"] for meal in meals
    )
    total_meal_protein = sum(
        meal["protein"] for meal in meals
    )
    total_meal_carbs = sum(
        meal["carbs"] for meal in meals
    )
    total_meal_fat = sum(
        meal["fat"] for meal in meals
    )

    for meal in meals:
        with st.container(border=True):
            st.subheader(meal["meal"])

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Kalorien", f'{meal["calories"]} kcal')
            c2.metric("Protein", f'{meal["protein"]} g')
            c3.metric("Kohlenhydrate", f'{meal["carbs"]} g')
            c4.metric("Fett", f'{meal["fat"]} g')

    st.divider()

    # -----------------------------------------
    # Menübilanz
    # -----------------------------------------
    st.header("🎯 Vergleich mit deinem Tagesziel")

    st.write(
        f"**Menü insgesamt:** {total_meal_calories} kcal | "
        f"Protein: {total_meal_protein} g | "
        f"Kohlenhydrate: {total_meal_carbs} g | "
        f"Fett: {total_meal_fat} g"
    )

    remaining_calories = round(
        calorie_target - total_meal_calories
    )
    remaining_protein = round(
        protein_target - total_meal_protein
    )
    remaining_carbs = round(
        carb_target - total_meal_carbs
    )
    remaining_fat = round(
        fat_target - total_meal_fat
    )

    if remaining_calories > 0:
        st.info(
            f"Zum geschätzten Tagesziel fehlen noch ungefähr "
            f"{remaining_calories} kcal."
        )
    else:
        st.info(
            f"Das Beispiel-Menü liegt ungefähr "
            f"{abs(remaining_calories)} kcal über deinem Tagesziel."
        )

    st.write(
        f"**Makro-Differenz:** Protein {remaining_protein} g · "
        f"Kohlenhydrate {remaining_carbs} g · "
        f"Fett {remaining_fat} g"
    )

    st.caption(
        "Das Beispiel-Menü ist noch nicht automatisch auf deine "
        "Zielwerte skaliert. Die angegebenen Nährwerte sind Richtwerte."
    )

    st.divider()

    # -----------------------------------------
    # Einkaufsliste
    # -----------------------------------------
    st.header("🛒 Deine Einkaufsliste")

    ingredients = []

    for meal in meals:
        ingredients.extend(meal["ingredients"])

    # Doppelte Einträge entfernen, Reihenfolge beibehalten
    ingredients = list(dict.fromkeys(ingredients))

    st.write(
        "Kreuze die Zutaten an, die du bereits eingekauft hast. "
        "Dein Ernährungsplan bleibt dabei sichtbar."
    )

    # Schlüssel in session_state verhindert, dass der Status
    # der Checkboxen bei jedem Streamlit-Rerun verloren geht.
    if "shopping_checked" not in st.session_state:
        st.session_state.shopping_checked = {}

    for ingredient in ingredients:
        checkbox_key = f"shopping_{ingredient}"

        if checkbox_key not in st.session_state:
            st.session_state[checkbox_key] = False

        st.checkbox(
            ingredient,
            key=checkbox_key
        )

    checked_count = sum(
        bool(st.session_state.get(f"shopping_{item}", False))
        for item in ingredients
    )

    st.progress(
        checked_count / len(ingredients) if ingredients else 0
    )

    st.caption(
        f"{checked_count} von {len(ingredients)} Zutaten erledigt."
    )

    if st.button("Einkaufsliste zurücksetzen"):
        for ingredient in ingredients:
            st.session_state[f"shopping_{ingredient}"] = False
        st.rerun()

else:
    st.info(
        "Gib deine Angaben ein und klicke auf "
        "«Ernährungsplan berechnen», um deinen Plan zu sehen."
    )
