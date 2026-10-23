
import streamlit as st
from collections import defaultdict
from copy import deepcopy

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide",
)

st.title("🥗 PACE Nutrition")
st.caption("Nutrition planning for hybrid athletes.")

# --------------------------------------------------
# 1. ZUTATEN-DATENBANK
# Nährwerte pro 100 g bzw. 100 ml.
# Werte sind gerundete Näherungswerte.
# --------------------------------------------------

INGREDIENTS = {
    "Haferflocken": {"kcal": 372, "protein": 13.5, "carbs": 58.7, "fat": 7.0},
    "Skyr": {"kcal": 63, "protein": 11.0, "carbs": 4.0, "fat": 0.2},
    "Beeren": {"kcal": 50, "protein": 1.0, "carbs": 8.0, "fat": 0.5},
    "Honig": {"kcal": 304, "protein": 0.3, "carbs": 82.0, "fat": 0.0},
    "Magerquark": {"kcal": 67, "protein": 12.0, "carbs": 4.0, "fat": 0.2},
    "Apfel": {"kcal": 52, "protein": 0.3, "carbs": 14.0, "fat": 0.2},
    "Milch": {"kcal": 47, "protein": 3.4, "carbs": 4.8, "fat": 1.5},
    "Ei": {"kcal": 143, "protein": 12.6, "carbs": 0.7, "fat": 9.5},
    "Vollkornbrot": {"kcal": 240, "protein": 9.0, "carbs": 41.0, "fat": 3.5},
    "Hüttenkäse": {"kcal": 98, "protein": 12.5, "carbs": 3.0, "fat": 4.3},
    "Pouletbrust": {"kcal": 120, "protein": 23.0, "carbs": 0.0, "fat": 2.5},
    "Reis trocken": {"kcal": 360, "protein": 7.0, "carbs": 80.0, "fat": 0.8},
    "Gemüse": {"kcal": 35, "protein": 2.0, "carbs": 5.0, "fat": 0.5},
    "Olivenöl": {"kcal": 884, "protein": 0.0, "carbs": 0.0, "fat": 100.0},
    "Vollkornpasta trocken": {"kcal": 350, "protein": 13.0, "carbs": 65.0, "fat": 2.5},
    "Linsen gekocht": {"kcal": 116, "protein": 9.0, "carbs": 20.0, "fat": 0.4},
    "Passata": {"kcal": 30, "protein": 1.5, "carbs": 4.5, "fat": 0.2},
    "Parmesan": {"kcal": 402, "protein": 32.0, "carbs": 0.0, "fat": 30.0},
    "Tofu": {"kcal": 145, "protein": 16.0, "carbs": 2.0, "fat": 9.0},
    "Sojasauce": {"kcal": 53, "protein": 8.0, "carbs": 5.0, "fat": 0.1},
    "Banane": {"kcal": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3},
    "Lachs": {"kcal": 208, "protein": 20.0, "carbs": 0.0, "fat": 13.0},
    "Kartoffeln": {"kcal": 77, "protein": 2.0, "carbs": 17.0, "fat": 0.1},
    "Kichererbsen gekocht": {"kcal": 164, "protein": 8.9, "carbs": 27.4, "fat": 2.6},
    "Kokosmilch light": {"kcal": 75, "protein": 1.0, "carbs": 3.0, "fat": 6.5},
}

# --------------------------------------------------
# 2. REZEPTE
# Alle Zutatenmengen sind pro Basisportion in Gramm.
# --------------------------------------------------

RECIPES = {
    "Porridge mit Beeren und Skyr": {
        "category": "Frühstück",
        "ingredients": {
            "Haferflocken": 70,
            "Skyr": 200,
            "Beeren": 100,
            "Honig": 10,
        },
    },
    "Overnight Oats mit Apfel": {
        "category": "Frühstück",
        "ingredients": {
            "Haferflocken": 65,
            "Magerquark": 150,
            "Apfel": 120,
            "Milch": 100,
        },
    },
    "Eier mit Brot und Hüttenkäse": {
        "category": "Frühstück",
        "ingredients": {
            "Ei": 100,
            "Vollkornbrot": 100,
            "Hüttenkäse": 100,
        },
    },
    "Poulet mit Reis und Gemüse": {
        "category": "Mittagessen",
        "ingredients": {
            "Pouletbrust": 160,
            "Reis trocken": 90,
            "Gemüse": 200,
            "Olivenöl": 5,
        },
    },
    "Linsen-Bolognese mit Pasta": {
        "category": "Mittagessen",
        "ingredients": {
            "Vollkornpasta trocken": 100,
            "Linsen gekocht": 150,
            "Passata": 150,
            "Parmesan": 10,
        },
    },
    "Tofu mit Reis und Gemüse": {
        "category": "Mittagessen",
        "ingredients": {
            "Tofu": 150,
            "Reis trocken": 80,
            "Gemüse": 200,
            "Sojasauce": 15,
        },
    },
    "Skyr-Bananen-Snack": {
        "category": "Snack",
        "ingredients": {
            "Skyr": 200,
            "Banane": 120,
            "Haferflocken": 25,
        },
    },
    "Brot mit Hüttenkäse": {
        "category": "Snack",
        "ingredients": {
            "Vollkornbrot": 80,
            "Hüttenkäse": 120,
        },
    },
    "Lachs mit Kartoffeln und Gemüse": {
        "category": "Abendessen",
        "ingredients": {
            "Lachs": 150,
            "Kartoffeln": 250,
            "Gemüse": 200,
            "Olivenöl": 5,
        },
    },
    "Poulet mit Kartoffeln aus dem Ofen": {
        "category": "Abendessen",
        "ingredients": {
            "Pouletbrust": 160,
            "Kartoffeln": 300,
            "Gemüse": 200,
            "Olivenöl": 5,
        },
    },
    "Kichererbsen-Curry mit Reis": {
        "category": "Abendessen",
        "ingredients": {
            "Kichererbsen gekocht": 160,
            "Reis trocken": 75,
            "Kokosmilch light": 100,
            "Gemüse": 150,
        },
    },
}

SPORTS = {
    "Laufen": 8.0,
    "Krafttraining": 4.5,
    "Radfahren": 7.0,
    "Schwimmen": 7.0,
    "Tennis": 7.0,
    "Spazieren": 3.0,
    "Andere": 5.0,
}

INTENSITY = {
    "Locker": 0.8,
    "Moderat": 1.0,
    "Intensiv": 1.2,
}

MEAL_SLOTS = [
    ("Frühstück", "Frühstück"),
    ("Mittagessen", "Mittagessen"),
    ("Snack", "Snack"),
    ("Abendessen", "Abendessen"),
]


# --------------------------------------------------
# 3. APP-ZUSTAND
# --------------------------------------------------

if "training_sessions" not in st.session_state:
    st.session_state.training_sessions = [{
        "id": 1,
        "sport": "Laufen",
        "duration": 45,
        "intensity": "Moderat",
    }]

if "next_training_id" not in st.session_state:
    st.session_state.next_training_id = 2

if "meal_choices" not in st.session_state:
    st.session_state.meal_choices = {
        "Frühstück": "Porridge mit Beeren und Skyr",
        "Mittagessen": "Poulet mit Reis und Gemüse",
        "Snack": "Skyr-Bananen-Snack",
        "Abendessen": "Lachs mit Kartoffeln und Gemüse",
    }

if "portion_results" not in st.session_state:
    st.session_state.portion_results = None


# --------------------------------------------------
# 4. NÄHRWERTE AUS ZUTATEN BERECHNEN
# --------------------------------------------------

def recipe_nutrition(recipe_name, portion=1.0):
    recipe = RECIPES[recipe_name]

    result = {
        "kcal": 0.0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0,
    }

    for ingredient, amount in recipe["ingredients"].items():
        nutrition = INGREDIENTS[ingredient]
        factor = amount * portion / 100

        for key in result:
            result[key] += nutrition[key] * factor

    return result


def plan_totals(names, portions):
    total = {
        "kcal": 0.0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0,
    }

    for name, portion in zip(names, portions):
        nutrition = recipe_nutrition(name, portion)

        for key in total:
            total[key] += nutrition[key]

    return total


def shopping_list(names, portions):
    result = defaultdict(float)

    for name, portion in zip(names, portions):
        for ingredient, amount in RECIPES[name]["ingredients"].items():
            result[ingredient] += amount * portion

    return dict(sorted(result.items()))


# --------------------------------------------------
# 5. PORTIONEN OPTIMIEREN
# --------------------------------------------------

def optimize_portions(names, targets):
    # Suche über mögliche Portionen in 0.1er-Schritten.
    # Bevorzugt Kalorienziel und ausreichend Protein.
    portions = [1.0] * len(names)
    candidates = [
        round(x / 10, 1) for x in range(5, 31)
    ]

    for _ in range(5):
        for i in range(len(portions)):
            best_portion = portions[i]
            best_loss = float("inf")

            for candidate in candidates:
                trial = portions.copy()
                trial[i] = candidate
                totals = plan_totals(names, trial)

                calorie_error = (
                    (totals["kcal"] - targets["calories"])
                    / max(targets["calories"], 1)
                )
                protein_error = (
                    (totals["protein"] - targets["protein"])
                    / max(targets["protein"], 1)
                )
                carb_error = (
                    (totals["carbs"] - targets["carbs"])
                    / max(targets["carbs"], 1)
                )
                fat_error = (
                    (totals["fat"] - targets["fat"])
                    / max(targets["fat"], 1)
                )

                portion_penalty = sum(
                    (p - 1) ** 2 for p in trial
                ) / len(trial)

                loss = (
                    8 * calorie_error ** 2
                    + 2 * protein_error ** 2
                    + 1.5 * carb_error ** 2
                    + fat_error ** 2
                    + 0.04 * portion_penalty
                )

                if loss < best_loss:
                    best_loss = loss
                    best_portion = candidate

            portions[i] = best_portion

    return portions


# --------------------------------------------------
# 6. PROFIL UND KALORIENZIELE
# --------------------------------------------------

st.header("1. Dein Profil")

c1, c2, c3 = st.columns(3)

with c1:
    age = st.number_input("Alter", 18, 100, 30)
    weight = st.number_input(
        "Gewicht (kg)", 35.0, 250.0, 62.0, step=0.5
    )

with c2:
    height = st.number_input("Grösse (cm)", 130, 230, 165)
    sex = st.selectbox(
        "Berechnungsprofil",
        ["Männlich", "Weiblich", "Andere / keine Angabe"],
    )

with c3:
    goal = st.selectbox(
        "Dein Ziel",
        ["Leistung erhalten", "Muskelaufbau", "Fettabbau"],
    )
    activity = st.selectbox(
        "Alltagsaktivität ohne geplantes Training",
        [
            "Überwiegend sitzend",
            "Leicht aktiv",
            "Aktiver Alltag",
        ],
    )

bmr_adjustment = {
    "Männlich": 5,
    "Weiblich": -161,
    "Andere / keine Angabe": -78,
}

bmr = (
    10 * weight
    + 6.25 * height
    - 5 * age
    + bmr_adjustment[sex]
)

activity_factor = {
    "Überwiegend sitzend": 1.2,
    "Leicht aktiv": 1.3,
    "Aktiver Alltag": 1.4,
}[activity]


# --------------------------------------------------
# 7. MEHRERE TRAININGSEINHEITEN
# --------------------------------------------------

st.header("2. Dein Training")

st.write(
    "Trage alle Trainingseinheiten für den Tag ein. "
    "Die Berechnung bleibt eine Schätzung."
)

remove_id = None

for session in st.session_state.training_sessions:
    with st.container(border=True):
        st.markdown(f"**Trainingseinheit {session['id']}**")
        c1, c2, c3, c4 = st.columns([2, 1, 1.5, 1])

        with c1:
            session["sport"] = st.selectbox(
                "Sportart",
                list(SPORTS.keys()),
                index=list(SPORTS.keys()).index(session["sport"]),
                key=f"sport_{session['id']}",
            )

        with c2:
            session["duration"] = st.number_input(
                "Minuten",
                min_value=0,
                max_value=600,
                value=session["duration"],
                step=15,
                key=f"duration_{session['id']}",
            )

        with c3:
            session["intensity"] = st.selectbox(
                "Intensität",
                list(INTENSITY.keys()),
                index=list(INTENSITY.keys()).index(session["intensity"]),
                key=f"intensity_{session['id']}",
            )

        with c4:
            st.write("")
            if st.button(
                "Entfernen",
                key=f"remove_{session['id']}",
                disabled=len(st.session_state.training_sessions) == 1,
            ):
                remove_id = session["id"]

if remove_id is not None:
    st.session_state.training_sessions = [
        s for s in st.session_state.training_sessions
        if s["id"] != remove_id
    ]
    st.session_state.portion_results = None
    st.rerun()

if st.button("＋ Trainingseinheit hinzufügen"):
    new_id = st.session_state.next_training_id

    st.session_state.training_sessions.append({
        "id": new_id,
        "sport": "Krafttraining",
        "duration": 60,
        "intensity": "Moderat",
    })

    st.session_state.next_training_id += 1
    st.session_state.portion_results = None
    st.rerun()


# --------------------------------------------------
# 8. ZIELE BERECHNEN
# --------------------------------------------------

training_kcal = 0.0

for session in st.session_state.training_sessions:
    hours = session["duration"] / 60
    met = SPORTS[session["sport"]]
    intensity = INTENSITY[session["intensity"]]

    gross = met * weight * hours * intensity
    resting = weight * hours
    training_kcal += max(0, gross - resting)

calories = bmr * activity_factor + training_kcal

if goal == "Muskelaufbau":
    calories *= 1.08
elif goal == "Fettabbau":
    calories *= 0.90

protein_target = weight * 1.8
fat_target = weight * 0.9
carbs_target = max(
    0, (calories - protein_target * 4 - fat_target * 9) / 4
)

targets = {
    "calories": round(calories),
    "protein": round(protein_target),
    "carbs": round(carbs_target),
    "fat": round(fat_target),
}

st.header("3. Deine Tagesziele")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Kalorien", f"{targets['calories']} kcal")
m2.metric("Protein", f"{targets['protein']} g")
m3.metric("Kohlenhydrate", f"{targets['carbs']} g")
m4.metric("Fett", f"{targets['fat']} g")

st.caption(
    f"Geschätzter Grundumsatz: {bmr:.0f} kcal · "
    f"Zusätzliche Trainingsenergie: {training_kcal:.0f} kcal"
)

st.info(
    "Die Kalorienziele sind Schätzwerte. Trainingskalorien, "
    "Alltagsaktivität und tatsächlicher Energiebedarf können abweichen."
)


# --------------------------------------------------
# 9. MAHLZEITEN WÄHLEN
# --------------------------------------------------

st.header("4. Dein Tagesmenü")

for slot, category in MEAL_SLOTS:
    options = [
        name for name, recipe in RECIPES.items()
        if recipe["category"] == category
    ]

    current = st.session_state.meal_choices[slot]
    if current not in options:
        current = options[0]

    st.session_state.meal_choices[slot] = st.selectbox(
        slot,
        options,
        index=options.index(current),
        key=f"meal_{slot}",
    )

if st.button(
    "Tagesplan berechnen",
    type="primary",
    use_container_width=True,
):
    names = [
        st.session_state.meal_choices[slot]
        for slot, _ in MEAL_SLOTS
    ]

    portions = optimize_portions(names, targets)

    st.session_state.portion_results = {
        "names": names,
        "portions": portions,
        "targets": deepcopy(targets),
    }


# --------------------------------------------------
# 10. MENÜ, BILANZ UND EINKAUFSLISTE
# --------------------------------------------------

if st.session_state.portion_results is not None:
    results = st.session_state.portion_results
    names = results["names"]
    portions = results["portions"]

    st.header("5. Dein angepasster Tagesplan")

    for (slot, _), name, portion in zip(
        MEAL_SLOTS, names, portions
    ):
        nutrition = recipe_nutrition(name, portion)

        st.markdown(f"**{slot}: {name}**")
        st.write(
            f"Portion: {portion:.1f}× · "
            f"{nutrition['kcal']:.0f} kcal · "
            f"Protein {nutrition['protein']:.1f} g · "
            f"Kohlenhydrate {nutrition['carbs']:.1f} g · "
            f"Fett {nutrition['fat']:.1f} g"
        )

        ingredient_lines = []

        for ingredient, amount in RECIPES[name]["ingredients"].items():
            scaled_amount = amount * portion
            ingredient_lines.append(
                f"{ingredient}: {scaled_amount:.0f} g"
            )

        st.caption("Zutaten: " + " · ".join(ingredient_lines))

    totals = plan_totals(names, portions)

    st.header("6. Tagesbilanz")

    for label, key, unit in [
        ("Kalorien", "kcal", "kcal"),
        ("Protein", "protein", "g"),
        ("Kohlenhydrate", "carbs", "g"),
        ("Fett", "fat", "g"),
    ]:
        target_key = "calories" if key == "kcal" else key
        target = targets[target_key]
        actual = totals[key]
        delta = actual - target

        st.write(
            f"**{label}:** {actual:.0f} {unit} / "
            f"{target:.0f} {unit} · Abweichung {delta:+.0f} {unit}"
        )

        st.progress(
            min(max(actual / max(target, 1), 0.0), 1.0)
        )

    if abs(totals["kcal"] - targets["calories"]) <= targets["calories"] * 0.05:
        st.success("Die Kalorien liegen innerhalb von ungefähr 5 % des Ziels.")
    else:
        st.warning(
            "Das Menü liegt noch mehr als 5 % vom Kalorienziel entfernt. "
            "Probiere andere Gerichte oder ergänze später weitere Rezepte."
        )

    st.caption(
        "Die Portionsoptimierung sucht eine möglichst passende Kombination. "
        "Sie garantiert keine exakte Übereinstimmung aller Makros."
    )

    st.header("7. Einkaufsliste")

    shopping = shopping_list(names, portions)
    shopping_lines = ["PACE Nutrition – Einkaufsliste", ""]

    for ingredient, amount in shopping.items():
        shopping_lines.append(f"- {ingredient}: {amount:.0f} g")

        st.checkbox(
            f"{ingredient}: {amount:.0f} g",
            key=f"shopping_{ingredient}",
        )

    st.download_button(
        "Einkaufsliste herunterladen",
        data="\n".join(shopping_lines),
        file_name="pace_einkaufsliste.txt",
        mime="text/plain",
        use_container_width=True,
    )

else:
    st.info(
        "Wähle deine Mahlzeiten aus und klicke auf "
        "«Tagesplan berechnen»."
    )

st.divider()
st.caption(
    "PACE Nutrition · Prototyp · Keine medizinische Ernährungsberatung."
)
