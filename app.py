
import streamlit as st
from collections import defaultdict

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 PACE Nutrition")
st.subheader("Deine Ernährung passend zu Training, Zielen und Budget")
st.caption("Version 5 – mehrere Trainingseinheiten pro Tag")

# --------------------------------------------------
# 1. REZEPTE: NÄHRWERTE PRO BASISPORTION
# --------------------------------------------------

RECIPES = {
    "Porridge mit Beeren und Skyr": {
        "category": "Frühstück",
        "kcal": 520, "protein": 35, "carbs": 72, "fat": 9,
        "ingredients": {
            "Haferflocken (g)": 70, "Skyr (g)": 200,
            "Beeren (g)": 100, "Banane (g)": 80
        }
    },
    "Overnight Oats mit Apfel": {
        "category": "Frühstück",
        "kcal": 490, "protein": 31, "carbs": 70, "fat": 10,
        "ingredients": {
            "Haferflocken (g)": 65, "Magerquark (g)": 150,
            "Apfel (g)": 150, "Milch (ml)": 100
        }
    },
    "Eier mit Brot und Hüttenkäse": {
        "category": "Frühstück",
        "kcal": 510, "protein": 34, "carbs": 45, "fat": 19,
        "ingredients": {
            "Eier (Stück)": 2, "Vollkornbrot (g)": 100,
            "Hüttenkäse (g)": 100, "Tomaten (g)": 100
        }
    },
    "Poulet mit Reis und Gemüse": {
        "category": "Mittagessen",
        "kcal": 650, "protein": 48, "carbs": 85, "fat": 10,
        "ingredients": {
            "Pouletbrust (g)": 160, "Reis trocken (g)": 100,
            "Gemüse (g)": 200, "Olivenöl (g)": 5
        }
    },
    "Linsen-Bolognese mit Pasta": {
        "category": "Mittagessen",
        "kcal": 620, "protein": 28, "carbs": 95, "fat": 12,
        "ingredients": {
            "Vollkornpasta trocken (g)": 100,
            "Linsen gekocht (g)": 150, "Passata (g)": 150,
            "Zwiebel (g)": 50, "Olivenöl (g)": 5
        }
    },
    "Tofu mit Reis und Gemüse": {
        "category": "Mittagessen",
        "kcal": 630, "protein": 30, "carbs": 78, "fat": 20,
        "ingredients": {
            "Tofu (g)": 150, "Reis trocken (g)": 90,
            "Gemüse (g)": 200, "Sojasauce (ml)": 15
        }
    },
    "Skyr-Bananen-Snack": {
        "category": "Snack",
        "kcal": 300, "protein": 25, "carbs": 43, "fat": 3,
        "ingredients": {
            "Skyr (g)": 200, "Banane (g)": 120,
            "Haferflocken (g)": 20
        }
    },
    "Brot mit Hüttenkäse": {
        "category": "Snack",
        "kcal": 310, "protein": 22, "carbs": 40, "fat": 6,
        "ingredients": {
            "Vollkornbrot (g)": 80, "Hüttenkäse (g)": 150,
            "Gurke (g)": 100
        }
    },
    "Lachs mit Kartoffeln und Gemüse": {
        "category": "Abendessen",
        "kcal": 650, "protein": 40, "carbs": 65, "fat": 24,
        "ingredients": {
            "Lachs (g)": 150, "Kartoffeln (g)": 250,
            "Gemüse (g)": 200, "Olivenöl (g)": 5
        }
    },
    "Poulet mit Ofenkartoffeln": {
        "category": "Abendessen",
        "kcal": 620, "protein": 48, "carbs": 65, "fat": 12,
        "ingredients": {
            "Pouletbrust (g)": 160, "Kartoffeln (g)": 300,
            "Gemüse (g)": 150, "Olivenöl (g)": 5
        }
    },
    "Kichererbsen-Curry mit Reis": {
        "category": "Abendessen",
        "kcal": 640, "protein": 22, "carbs": 95, "fat": 18,
        "ingredients": {
            "Kichererbsen gekocht (g)": 180,
            "Reis trocken (g)": 80,
            "Kokosmilch light (ml)": 100, "Passata (g)": 100
        }
    }
}

MEAL_CATEGORIES = ["Frühstück", "Mittagessen", "Snack", "Abendessen"]

# --------------------------------------------------
# 2. TRAININGSLOGIK
# --------------------------------------------------

SPORTS = {
    "Laufen": 8.0,
    "Krafttraining": 4.5,
    "Radfahren": 7.0,
    "Schwimmen": 7.0,
    "Tennis": 7.0,
    "Spazieren": 3.0,
    "Andere": 5.0
}

INTENSITY_FACTORS = {
    "Locker": 0.8,
    "Moderat": 1.0,
    "Intensiv": 1.2
}

if "training_sessions" not in st.session_state:
    st.session_state.training_sessions = [
        {"id": 1, "sport": "Laufen", "minutes": 45, "intensity": "Moderat"}
    ]

if "next_training_id" not in st.session_state:
    st.session_state.next_training_id = 2


def add_training():
    new_id = st.session_state.next_training_id
    st.session_state.training_sessions.append({
        "id": new_id,
        "sport": "Krafttraining",
        "minutes": 60,
        "intensity": "Moderat"
    })
    st.session_state.next_training_id += 1


def remove_training(training_id):
    st.session_state.training_sessions = [
        session
        for session in st.session_state.training_sessions
        if session["id"] != training_id
    ]


# --------------------------------------------------
# 3. KALORIEN- UND MAKROZIELE
# --------------------------------------------------

def calculate_targets(
    age, weight, height, sex, activity, goal, sessions
):
    if sex == "Männlich":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factors = {
        "Wenig aktiv": 1.2,
        "Leicht aktiv": 1.375,
        "Moderat aktiv": 1.55,
        "Sehr aktiv": 1.725
    }

    # Aktivitätsniveau beschreibt den Alltag ohne geplantes Training.
    baseline = bmr * activity_factors[activity]

    total_training_kcal = 0

    for session in sessions:
        met = SPORTS[session["sport"]]
        intensity = INTENSITY_FACTORS[session["intensity"]]
        minutes = session["minutes"]

        # Nettoverbrauch über den Ruheverbrauch hinaus.
        session_kcal = (
            max(0, met - 1) * 3.5 * weight / 200
            * minutes * intensity
        )
        total_training_kcal += session_kcal

    # Nur ein Anteil wird addiert, da der Basiswert bereits
    # Alltagsbewegung enthält und Schätzungen ungenau sind.
    calories = baseline + total_training_kcal * 0.75

    if goal == "Muskelaufbau":
        calories *= 1.08
    elif goal == "Fettabbau":
        calories *= 0.90

    protein = weight * 1.8
    fat = weight * 0.9
    carbs = max(0, (calories - protein * 4 - fat * 9) / 4)

    return {
        "kcal": round(calories),
        "protein": round(protein),
        "carbs": round(carbs),
        "fat": round(fat),
        "training_kcal": round(total_training_kcal)
    }


# --------------------------------------------------
# 4. MENÜOPTIMIERUNG
# --------------------------------------------------

def calculate_nutrition(names, portions):
    result = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}

    for name, factor in zip(names, portions):
        for key in result:
            result[key] += RECIPES[name][key] * factor

    return result


def optimize_portions(names, targets):
    portions = [1.0 for _ in names]

    weights = {"kcal": 8.0, "protein": 2.0, "carbs": 1.5, "fat": 1.0}

    def loss(candidate):
        totals = calculate_nutrition(names, candidate)
        score = 0.0

        for key, weight in weights.items():
            target = targets[key]
            if target > 0:
                score += weight * ((totals[key] - target) / target) ** 2

        score += sum(0.08 * (factor - 1.0) ** 2 for factor in candidate)
        return score

    for step in [0.25, 0.10, 0.04, 0.015]:
        for _ in range(3):
            for i in range(len(portions)):
                current = portions[i]
                best_factor = current
                best_score = loss(portions)

                for direction in (-1, 1):
                    test_factor = max(0.4, min(2.2, current + direction * step))
                    candidate = portions.copy()
                    candidate[i] = test_factor
                    score = loss(candidate)

                    if score < best_score:
                        best_score = score
                        best_factor = test_factor

                portions[i] = best_factor

    return portions


def unit_for(ingredient):
    if ingredient.endswith("(Stück)"):
        return "Stück"
    if ingredient.endswith("(ml)"):
        return "ml"
    return "g"


def format_amount(amount, unit):
    if unit == "Stück":
        return f"{amount:.1f} Stück"
    return f"{amount:.0f} {unit}"


# --------------------------------------------------
# 5. PROFIL
# --------------------------------------------------

st.header("1. Dein Profil")

c1, c2, c3 = st.columns(3)

with c1:
    age = st.number_input("Alter", 18, 100, 30)
    weight = st.number_input("Gewicht (kg)", 35.0, 250.0, 62.0, step=0.5)

with c2:
    height = st.number_input("Grösse (cm)", 130, 230, 165)
    sex = st.selectbox("Geschlecht für Grundumsatzformel", ["Männlich", "Weiblich"])

with c3:
    goal = st.selectbox(
        "Ernährungsziel",
        ["Leistung erhalten", "Muskelaufbau", "Fettabbau"]
    )
    activity = st.selectbox(
        "Alltagsaktivität (ohne geplantes Training)",
        ["Wenig aktiv", "Leicht aktiv", "Moderat aktiv", "Sehr aktiv"],
        index=1
    )

# --------------------------------------------------
# 6. BELIEBIG VIELE TRAININGSEINHEITEN
# --------------------------------------------------

st.header("2. Dein Training heute")
st.write(
    "Füge jede geplante Einheit separat hinzu. "
    "Sportart, Dauer und Intensität werden pro Einheit erfasst."
)

st.button(
    "＋ Trainingseinheit hinzufügen",
    on_click=add_training,
    use_container_width=False
)

remove_id = None

for index, session in enumerate(st.session_state.training_sessions):
    with st.container(border=True):
        st.markdown(f"**Trainingseinheit {index + 1}**")

        c1, c2, c3, c4 = st.columns([2, 1, 1.5, 0.8])

        with c1:
            session["sport"] = st.selectbox(
                "Sportart",
                list(SPORTS.keys()),
                index=list(SPORTS.keys()).index(session["sport"]),
                key=f"sport_{session['id']}"
            )

        with c2:
            session["minutes"] = st.number_input(
                "Dauer (Min.)",
                min_value=0,
                max_value=600,
                value=session["minutes"],
                step=5,
                key=f"minutes_{session['id']}"
            )

        with c3:
            session["intensity"] = st.selectbox(
                "Intensität",
                ["Locker", "Moderat", "Intensiv"],
                index=["Locker", "Moderat", "Intensiv"].index(session["intensity"]),
                key=f"intensity_{session['id']}"
            )

        with c4:
            st.write("")
            st.write("")
            if st.button("Entfernen", key=f"remove_{session['id']}"):
                remove_id = session["id"]

if remove_id is not None:
    remove_training(remove_id)
    st.rerun()

targets = calculate_targets(
    age, weight, height, sex, activity, goal,
    st.session_state.training_sessions
)

st.header("3. Dein berechnetes Tagesziel")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Kalorien", f'{targets["kcal"]} kcal')
m2.metric("Protein", f'{targets["protein"]} g')
m3.metric("Kohlenhydrate", f'{targets["carbs"]} g')
m4.metric("Fett", f'{targets["fat"]} g')

st.caption(
    f"Erfasste Einheiten: {len(st.session_state.training_sessions)} · "
    f"Gesamte Trainingsdauer: "
    f"{sum(s['minutes'] for s in st.session_state.training_sessions)} Minuten · "
    f"Geschätzter Brutto-Trainingsverbrauch: "
    f"{targets['training_kcal']} kcal"
)

st.info(
    "Der Trainingsverbrauch ist eine grobe Schätzung. "
    "Wähle bei der Alltagsaktivität möglichst eine Stufe, die dein "
    "normales Leben ohne die oben erfassten Trainingseinheiten beschreibt."
)

# --------------------------------------------------
# 7. MENÜ AUSWÄHLEN
# --------------------------------------------------

st.header("4. Dein Menü")

selected = {}

for category in MEAL_CATEGORIES:
    options = [
        name for name, recipe in RECIPES.items()
        if recipe["category"] == category
    ]
    selected[category] = st.selectbox(category, options, key=f"meal_{category}")

if st.button("Portionen optimieren", type="primary"):
    names = [selected[category] for category in MEAL_CATEGORIES]
    portions = optimize_portions(names, targets)

    st.session_state["optimized_names"] = names
    st.session_state["optimized_portions"] = portions

current_names = [selected[category] for category in MEAL_CATEGORIES]

if (
    "optimized_names" not in st.session_state
    or st.session_state["optimized_names"] != current_names
):
    st.info("Wähle deine Gerichte und klicke auf «Portionen optimieren».")
else:
    names = st.session_state["optimized_names"]
    portions = st.session_state["optimized_portions"]
    totals = calculate_nutrition(names, portions)

    st.header("5. Dein optimierter Tagesplan")

    for category, name, factor in zip(MEAL_CATEGORIES, names, portions):
        recipe = RECIPES[name]
        st.markdown(f"**{category}: {name}**")
        st.write(f"Portionsfaktor: {factor:.2f} × Basisportion")

        ingredients = [
            f"{ingredient.split(' (')[0]}: "
            f"{format_amount(amount * factor, unit_for(ingredient))}"
            for ingredient, amount in recipe["ingredients"].items()
        ]
        st.write(" · ".join(ingredients))
        st.caption(
            f"Ca. {recipe['kcal'] * factor:.0f} kcal | "
            f"Protein {recipe['protein'] * factor:.0f} g | "
            f"Kohlenhydrate {recipe['carbs'] * factor:.0f} g | "
            f"Fett {recipe['fat'] * factor:.0f} g"
        )
        st.divider()

    st.header("6. Tagesbilanz")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Kalorien", f'{totals["kcal"]:.0f} kcal',
              f'{totals["kcal"] - targets["kcal"]:+.0f} kcal')
    c2.metric("Protein", f'{totals["protein"]:.0f} g',
              f'{totals["protein"] - targets["protein"]:+.0f} g')
    c3.metric("Kohlenhydrate", f'{totals["carbs"]:.0f} g',
              f'{totals["carbs"] - targets["carbs"]:+.0f} g')
    c4.metric("Fett", f'{totals["fat"]:.0f} g',
              f'{totals["fat"] - targets["fat"]:+.0f} g')

    calorie_diff_pct = (
        abs(totals["kcal"] - targets["kcal"]) / targets["kcal"] * 100
        if targets["kcal"] else 0
    )

    if calorie_diff_pct <= 3:
        st.success("Das Menü liegt sehr nahe am berechneten Kalorienziel.")
    elif calorie_diff_pct <= 8:
        st.warning("Das Menü liegt relativ nahe am Ziel, weicht aber noch etwas ab.")
    else:
        st.warning("Das Menü weicht merklich vom Tagesziel ab. Probiere andere Gerichte.")

    st.caption(
        "Die Optimierung ist eine Näherung. Begrenzte Portionen und "
        "unterschiedliche Makroverteilungen können Abweichungen verursachen."
    )

    # --------------------------------------------------
    # 8. EINKAUFSLISTE
    # --------------------------------------------------

    st.header("7. Deine Einkaufsliste")

    shopping_list = defaultdict(float)

    for name, factor in zip(names, portions):
        for ingredient, amount in RECIPES[name]["ingredients"].items():
            shopping_list[ingredient] += amount * factor

    for ingredient in sorted(shopping_list):
        unit = unit_for(ingredient)
        amount_text = format_amount(shopping_list[ingredient], unit)
        st.checkbox(
            f"{ingredient.split(' (')[0]} – {amount_text}",
            key=f"shopping_{ingredient}"
        )

    shopping_text = "\n".join(
        f"- {ingredient.split(' (')[0]}: "
        f"{format_amount(amount, unit_for(ingredient))}"
        for ingredient, amount in sorted(shopping_list.items())
    )

    st.download_button(
        "Einkaufsliste als TXT herunterladen",
        data=shopping_text,
        file_name="pace_einkaufsliste.txt",
        mime="text/plain"
    )

st.divider()
st.caption(
    "PACE Nutrition ist ein Planungsprototyp. Kalorienbedarf, "
    "Trainingsverbrauch und Rezeptnährwerte sind Schätzungen."
)
