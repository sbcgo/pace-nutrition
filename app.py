
import itertools
import math
import streamlit as st

st.set_page_config(page_title="PACE Nutrition", page_icon="🥗", layout="wide")

st.title("🥗 PACE Nutrition")
st.caption("Deine Ernährung. Dein Training. Dein Plan.")
st.write(
    "Plane deine Mahlzeiten passend zu deinem Trainingspensum. "
    "PACE berechnet Nährwerte anhand der Zutaten und hilft dir, "
    "deine Tagesziele zu erreichen."
)

# --------------------------------------------------
# 1. ZUTATEN: ungefähre Nährwerte pro 100 g / 100 ml
# --------------------------------------------------

INGREDIENTS = {
    "Haferflocken": {"kcal": 372, "protein": 13.5, "carbs": 58.7, "fat": 7.0},
    "Skyr": {"kcal": 63, "protein": 11, "carbs": 4, "fat": 0.2},
    "Beeren": {"kcal": 50, "protein": 1, "carbs": 8, "fat": 0.5},
    "Honig": {"kcal": 304, "protein": 0.3, "carbs": 82, "fat": 0},
    "Magerquark": {"kcal": 67, "protein": 12, "carbs": 4, "fat": 0.2},
    "Apfel": {"kcal": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
    "Milch": {"kcal": 47, "protein": 3.4, "carbs": 4.8, "fat": 1.5},
    "Ei": {"kcal": 143, "protein": 12.6, "carbs": 0.7, "fat": 9.5},
    "Vollkornbrot": {"kcal": 240, "protein": 9, "carbs": 41, "fat": 3.5},
    "Hüttenkäse": {"kcal": 98, "protein": 12.5, "carbs": 3, "fat": 4.3},
    "Pouletbrust": {"kcal": 120, "protein": 23, "carbs": 0, "fat": 2.5},
    "Reis trocken": {"kcal": 360, "protein": 7, "carbs": 80, "fat": 0.8},
    "Gemüse": {"kcal": 35, "protein": 2, "carbs": 5, "fat": 0.5},
    "Olivenöl": {"kcal": 884, "protein": 0, "carbs": 0, "fat": 100},
    "Vollkornpasta trocken": {"kcal": 350, "protein": 13, "carbs": 65, "fat": 2.5},
    "Linsen gekocht": {"kcal": 116, "protein": 9, "carbs": 20, "fat": 0.4},
    "Passata": {"kcal": 30, "protein": 1.5, "carbs": 4.5, "fat": 0.2},
    "Parmesan": {"kcal": 402, "protein": 32, "carbs": 0, "fat": 30},
    "Tofu": {"kcal": 145, "protein": 16, "carbs": 2, "fat": 9},
    "Sojasauce": {"kcal": 53, "protein": 8, "carbs": 5, "fat": 0.1},
    "Banane": {"kcal": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3},
    "Lachs": {"kcal": 208, "protein": 20, "carbs": 0, "fat": 13},
    "Kartoffeln": {"kcal": 77, "protein": 2, "carbs": 17, "fat": 0.1},
    "Kichererbsen gekocht": {"kcal": 164, "protein": 8.9, "carbs": 27.4, "fat": 2.6},
    "Kokosmilch light": {"kcal": 75, "protein": 1, "carbs": 3, "fat": 6.5},
}

# --------------------------------------------------
# 2. REZEPTE
# Zutatenmengen pro Portion; Reis und Pasta trocken
# --------------------------------------------------

RECIPES = {
    "Porridge mit Beeren und Skyr": {
        "category": "Frühstück",
        "ingredients": {
            "Haferflocken": 70, "Skyr": 200, "Beeren": 100, "Honig": 10
        },
    },
    "Overnight Oats mit Apfel": {
        "category": "Frühstück",
        "ingredients": {
            "Haferflocken": 65, "Magerquark": 150, "Apfel": 120, "Milch": 100
        },
    },
    "Eierbrot mit Hüttenkäse": {
        "category": "Frühstück",
        "ingredients": {
            "Ei": 100, "Vollkornbrot": 100, "Hüttenkäse": 100
        },
    },
    "Poulet mit Reis und Gemüse": {
        "category": "Mittagessen",
        "ingredients": {
            "Pouletbrust": 160, "Reis trocken": 90, "Gemüse": 200, "Olivenöl": 5
        },
    },
    "Linsen-Bolognese mit Vollkornpasta": {
        "category": "Mittagessen",
        "ingredients": {
            "Vollkornpasta trocken": 100, "Linsen gekocht": 150,
            "Passata": 150, "Parmesan": 10
        },
    },
    "Tofu mit Reis und Gemüse": {
        "category": "Mittagessen",
        "ingredients": {
            "Tofu": 150, "Reis trocken": 80, "Gemüse": 200, "Sojasauce": 15
        },
    },
    "Skyr mit Banane und Haferflocken": {
        "category": "Snack",
        "ingredients": {"Skyr": 200, "Banane": 120, "Haferflocken": 25},
    },
    "Vollkornbrot mit Hüttenkäse": {
        "category": "Snack",
        "ingredients": {"Vollkornbrot": 80, "Hüttenkäse": 120},
    },
    "Lachs mit Kartoffeln und Gemüse": {
        "category": "Abendessen",
        "ingredients": {
            "Lachs": 150, "Kartoffeln": 250, "Gemüse": 200, "Olivenöl": 5
        },
    },
    "Poulet-Kartoffel-Blech": {
        "category": "Abendessen",
        "ingredients": {
            "Pouletbrust": 160, "Kartoffeln": 300, "Gemüse": 200, "Olivenöl": 5
        },
    },
    "Kichererbsen-Curry mit Reis": {
        "category": "Abendessen",
        "ingredients": {
            "Kichererbsen gekocht": 160, "Reis trocken": 75,
            "Kokosmilch light": 100, "Gemüse": 150
        },
    },
}

CATEGORIES = ["Frühstück", "Mittagessen", "Snack", "Abendessen"]
MACROS = ["kcal", "protein", "carbs", "fat"]
MACRO_LABELS = {
    "kcal": "Kalorien",
    "protein": "Protein",
    "carbs": "Kohlenhydrate",
    "fat": "Fett",
}


# --------------------------------------------------
# 3. NÄHRWERTE UND PORTIONSBERECHNUNG
# --------------------------------------------------

def recipe_nutrition(recipe_name, portion=1.0):
    totals = {macro: 0.0 for macro in MACROS}

    for ingredient, grams in RECIPES[recipe_name]["ingredients"].items():
        values = INGREDIENTS[ingredient]
        factor = grams * portion / 100

        for macro in MACROS:
            totals[macro] += values[macro] * factor

    return totals


def plan_totals(names, portions):
    totals = {macro: 0.0 for macro in MACROS}

    for name, portion in zip(names, portions):
        nutrition = recipe_nutrition(name, portion)
        for macro in MACROS:
            totals[macro] += nutrition[macro]

    return totals


def score_plan(totals, targets, portions):
    # Kalorien werden stärker gewichtet, Protein ebenfalls berücksichtigt.
    weights = {"kcal": 5.0, "protein": 3.0, "carbs": 1.2, "fat": 1.0}
    score = 0.0

    for macro in MACROS:
        target = max(float(targets[macro]), 1.0)
        deviation = (totals[macro] - target) / target
        score += weights[macro] * deviation**2

    # Verhindert unnötig extreme Portionsgrössen.
    score += sum(0.12 * (portion - 1.0) ** 2 for portion in portions)
    return score


def optimize_portions(names, targets):
    # Koordinatensuche: verändert jeweils eine Mahlzeit und prüft,
    # ob die Tageswerte dadurch näher an die Ziele kommen.
    portions = [1.0] * len(names)
    candidates = [0.5, 0.65, 0.8, 0.9, 1.0, 1.1, 1.2, 1.35, 1.5, 1.7, 2.0, 2.3]

    for _ in range(3):
        for i in range(len(names)):
            best_portion = portions[i]
            best_score = score_plan(plan_totals(names, portions), targets, portions)

            for candidate in candidates:
                trial = portions.copy()
                trial[i] = candidate
                trial_score = score_plan(plan_totals(names, trial), targets, trial)

                if trial_score < best_score:
                    best_score = trial_score
                    best_portion = candidate

            portions[i] = best_portion

    return portions


def find_best_combination(targets):
    choices_by_category = {
        category: [
            name for name, recipe in RECIPES.items()
            if recipe["category"] == category
        ]
        for category in CATEGORIES
    }

    best_names = None
    best_portions = None
    best_score = float("inf")

    combinations = itertools.product(
        *(choices_by_category[category] for category in CATEGORIES)
    )

    for combination in combinations:
        names = list(combination)
        portions = optimize_portions(names, targets)
        totals = plan_totals(names, portions)
        score = score_plan(totals, targets, portions)

        if score < best_score:
            best_score = score
            best_names = names
            best_portions = portions

    return best_names, best_portions


def shopping_list(names, portions):
    quantities = {}

    for name, portion in zip(names, portions):
        for ingredient, grams in RECIPES[name]["ingredients"].items():
            quantities[ingredient] = quantities.get(ingredient, 0) + grams * portion

    return quantities


# --------------------------------------------------
# 4. PROFIL
# --------------------------------------------------

st.header("1. Dein Profil")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Alter", min_value=16, max_value=100, value=30)
    weight = st.number_input("Gewicht (kg)", min_value=35.0, max_value=250.0, value=62.0, step=0.5)

with col2:
    height = st.number_input("Grösse (cm)", min_value=130, max_value=230, value=165)
    sex = st.selectbox("Berechnungsgrundlage", ["Männlich", "Weiblich", "Andere"])

with col3:
    goal = st.selectbox(
        "Dein Ziel",
        ["Leistung erhalten", "Muskelaufbau", "Fettverlust"],
    )
    activity = st.selectbox(
        "Alltag ausserhalb des Trainings",
        ["Sitzend", "Leicht aktiv", "Aktiv"],
    )

activity_factors = {"Sitzend": 1.2, "Leicht aktiv": 1.3, "Aktiv": 1.4}

# Mifflin-St Jeor; bei "Andere" wird der Mittelwert der beiden
# geschlechtsspezifischen Formeln als Näherung verwendet.
base_bmr = 10 * weight + 6.25 * height - 5 * age
if sex == "Männlich":
    bmr = base_bmr + 5
elif sex == "Weiblich":
    bmr = base_bmr - 161
else:
    bmr = base_bmr - 78

daily_base = bmr * activity_factors[activity]


# --------------------------------------------------
# 5. TRAINING
# --------------------------------------------------

st.header("2. Dein Training")

if "training_sessions" not in st.session_state:
    st.session_state.training_sessions = []

with st.form("training_form", clear_on_submit=True):
    tcol1, tcol2, tcol3 = st.columns(3)

    with tcol1:
        sport = st.selectbox(
            "Sportart",
            ["Laufen", "Krafttraining", "Radfahren", "Schwimmen", "Tennis", "Gehen", "Andere"],
        )
    with tcol2:
        duration = st.number_input(
            "Dauer in Minuten", min_value=5, max_value=600, value=45, step=5
        )
    with tcol3:
        intensity = st.selectbox("Intensität", ["Locker", "Mittel", "Intensiv"])

    add_training = st.form_submit_button("Training hinzufügen")

if add_training:
    st.session_state.training_sessions.append(
        {"sport": sport, "duration": duration, "intensity": intensity}
    )

met_values = {
    "Laufen": 8.5,
    "Krafttraining": 4.5,
    "Radfahren": 7.0,
    "Schwimmen": 6.0,
    "Tennis": 7.0,
    "Gehen": 3.5,
    "Andere": 5.0,
}
intensity_factors = {"Locker": 0.8, "Mittel": 1.0, "Intensiv": 1.2}

training_kcal = 0.0

if st.session_state.training_sessions:
    st.write("**Heutige Trainingseinheiten**")

    for i, session in enumerate(st.session_state.training_sessions):
        st.write(
            f"{i + 1}. {session['sport']} – {session['duration']} Min. – "
            f"{session['intensity']}"
        )
        # Grobe Netto-Schätzung oberhalb des Ruheverbrauchs.
        met = met_values[session["sport"]]
        factor = intensity_factors[session["intensity"]]
        training_kcal += max(0, (met * factor - 1) * 3.5 * weight / 200) * session["duration"]

    if st.button("Alle Trainingseinheiten entfernen"):
        st.session_state.training_sessions = []
        st.rerun()
else:
    st.info("Füge deine heutigen Trainingseinheiten hinzu oder fahre ohne Training fort.")

goal_factors = {
    "Leistung erhalten": 1.0,
    "Muskelaufbau": 1.08,
    "Fettverlust": 0.90,
}

calorie_target = max(1200, (daily_base + training_kcal) * goal_factors[goal])

protein_target = weight * 1.8
fat_target = weight * 0.9
carb_target = max(0, (calorie_target - protein_target * 4 - fat_target * 9) / 4)

targets = {
    "kcal": calorie_target,
    "protein": protein_target,
    "carbs": carb_target,
    "fat": fat_target,
}

st.subheader("Deine geschätzten Tagesziele")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Kalorien", f"{calorie_target:.0f} kcal")
m2.metric("Protein", f"{protein_target:.0f} g")
m3.metric("Kohlenhydrate", f"{carb_target:.0f} g")
m4.metric("Fett", f"{fat_target:.0f} g")

st.caption(
    "Alle Ziele sind Schätzungen und keine medizinische Ernährungsberatung. "
    "Der Trainingsverbrauch kann deutlich abweichen."
)


# --------------------------------------------------
# 6. MAHLZEITEN: AUTOMATISCH ODER MANUELL
# --------------------------------------------------

st.header("3. Dein Tagesplan")

st.write(
    "Lass PACE eine Kombination suchen, die zu deinen Tageszielen passt, "
    "oder wähle jede Mahlzeit selbst aus."
)

# Wichtig: Die automatische Auswahl erfolgt vor dem Aufbau der Auswahlfelder.
if st.button("✨ Mahlzeiten automatisch planen", type="primary"):
    with st.spinner("PACE vergleicht Mahlzeiten und Portionsgrössen …"):
        recommended_names, recommended_portions = find_best_combination(targets)

    for category, name in zip(CATEGORIES, recommended_names):
        st.session_state[f"meal_{category}"] = name

    st.session_state["recommended_portions"] = {
        name: portion for name, portion in zip(recommended_names, recommended_portions)
    }
    st.session_state["auto_plan_ready"] = True
    st.rerun()

if "recommended_portions" not in st.session_state:
    st.session_state["recommended_portions"] = {}

selected_names = []

for category in CATEGORIES:
    options = [
        name for name, recipe in RECIPES.items()
        if recipe["category"] == category
    ]
    default_name = options[0]
    current_name = st.session_state.get(f"meal_{category}", default_name)

    if current_name not in options:
        current_name = default_name

    selected_name = st.selectbox(
        category,
        options,
        index=options.index(current_name),
        key=f"meal_{category}",
    )
    selected_names.append(selected_name)

if st.button("Tagesplan berechnen", type="secondary"):
    portions = optimize_portions(selected_names, targets)
    st.session_state["calculated_names"] = selected_names.copy()
    st.session_state["calculated_portions"] = portions

# Nur den gespeicherten Plan anzeigen, bis neu berechnet wird.
if "calculated_names" not in st.session_state:
    st.session_state["calculated_names"] = selected_names.copy()
    st.session_state["calculated_portions"] = [1.0] * len(selected_names)

# Änderungen an den Mahlzeiten sollen beim Berechnen übernommen werden.
if st.session_state["calculated_names"] != selected_names:
    st.info("Du hast Mahlzeiten geändert. Klicke auf «Tagesplan berechnen», um die Mengen neu anzupassen.")

plan_names = st.session_state["calculated_names"]
plan_portions = st.session_state["calculated_portions"]

st.subheader("Deine Mahlzeiten")

for category, name, portion in zip(CATEGORIES, plan_names, plan_portions):
    nutrition = recipe_nutrition(name, portion)
    st.markdown(f"**{category}: {name}**")
    st.write(
        f"Portion: {portion:.2f}× · "
        f"{nutrition['kcal']:.0f} kcal · "
        f"Protein {nutrition['protein']:.1f} g · "
        f"Kohlenhydrate {nutrition['carbs']:.1f} g · "
        f"Fett {nutrition['fat']:.1f} g"
    )

    ingredients_text = ", ".join(
        f"{ingredient}: {grams * portion:.0f} g"
        for ingredient, grams in RECIPES[name]["ingredients"].items()
    )
    st.caption(ingredients_text)

totals = plan_totals(plan_names, plan_portions)

st.subheader("Deine Tagesbilanz")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Kalorien", f"{totals['kcal']:.0f} kcal", f"{totals['kcal'] - targets['kcal']:+.0f} kcal")
c2.metric("Protein", f"{totals['protein']:.0f} g", f"{totals['protein'] - targets['protein']:+.0f} g")
c3.metric("Kohlenhydrate", f"{totals['carbs']:.0f} g", f"{totals['carbs'] - targets['carbs']:+.0f} g")
c4.metric("Fett", f"{totals['fat']:.0f} g", f"{totals['fat'] - targets['fat']:+.0f} g")

st.write("**Fortschritt zu deinen Tageszielen**")
for macro in MACROS:
    target = max(targets[macro], 1)
    progress = min(totals[macro] / target, 1.0)
    st.write(f"{MACRO_LABELS[macro]}: {totals[macro]:.0f} / {target:.0f}")
    st.progress(progress)

if totals["kcal"] < targets["kcal"] * 0.85:
    st.warning("Dein Plan liegt deutlich unter deinem Kalorienziel. Prüfe, ob du ausreichend isst.")
elif totals["kcal"] > targets["kcal"] * 1.15:
    st.info("Dein Plan liegt deutlich über deinem Kalorienziel. Du kannst Mahlzeiten oder Portionsgrössen anpassen.")
else:
    st.success("Dein Kalorienplan liegt ungefähr im Zielbereich. Die Nährwerte bleiben Schätzungen.")


# --------------------------------------------------
# 7. EINKAUFSLISTE
# --------------------------------------------------

st.header("4. Einkaufsliste")

quantities = shopping_list(plan_names, plan_portions)

for ingredient, amount in sorted(quantities.items()):
    unit = "ml" if ingredient in ["Milch", "Kokosmilch light"] else "g"
    st.write(f"- {ingredient}: {amount:.0f} {unit}")

shopping_text = "\n".join(
    f"- {ingredient}: {amount:.0f} "
    f"{'ml' if ingredient in ['Milch', 'Kokosmilch light'] else 'g'}"
    for ingredient, amount in sorted(quantities.items())
)

plan_text = "PACE Nutrition – Tagesplan\n\n"
for category, name, portion in zip(CATEGORIES, plan_names, plan_portions):
    nutrition = recipe_nutrition(name, portion)
    plan_text += (
        f"{category}: {name} ({portion:.2f} Portionen) – "
        f"{nutrition['kcal']:.0f} kcal, "
        f"Protein {nutrition['protein']:.1f} g, "
        f"Kohlenhydrate {nutrition['carbs']:.1f} g, "
        f"Fett {nutrition['fat']:.1f} g\n"
    )

plan_text += (
    f"\nTagessumme: {totals['kcal']:.0f} kcal, "
    f"Protein {totals['protein']:.1f} g, "
    f"Kohlenhydrate {totals['carbs']:.1f} g, Fett {totals['fat']:.1f} g\n\n"
    f"Einkaufsliste:\n{shopping_text}\n"
)

st.download_button(
    "📥 Tagesplan und Einkaufsliste herunterladen",
    data=plan_text,
    file_name="pace_nutrition_tagesplan.txt",
    mime="text/plain",
)

st.caption(
    "Hinweis: Nährwerte variieren je nach Marke und Zubereitung. "
    "Reis und Pasta sind als Trockengewicht angegeben; Linsen und Kichererbsen "
    "als gekochtes Gewicht. Bitte Zutatenetiketten für genauere Werte prüfen."
)
