
import streamlit as st
from collections import defaultdict
from copy import deepcopy

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 PACE Nutrition")
st.caption("Deine Ernährung abgestimmt auf Training, Regeneration und Muskelaufbau.")

# --------------------------------------------------
# 1. REZEPTDATEN
# Nährwerte und Zutaten sind Näherungswerte pro Portion.
# Mengen werden für die Einkaufsliste mit skaliert.
# --------------------------------------------------

RECIPES = {
    "Porridge mit Beeren und Skyr": {
        "category": "Frühstück",
        "kcal": 480, "protein": 34, "carbs": 65, "fat": 9,
        "ingredients": {
            "Haferflocken (g)": 70,
            "Skyr (g)": 200,
            "Beeren (g)": 100,
            "Honig (g)": 10,
        },
    },
    "Overnight Oats mit Apfel": {
        "category": "Frühstück",
        "kcal": 460, "protein": 28, "carbs": 66, "fat": 9,
        "ingredients": {
            "Haferflocken (g)": 65,
            "Magerquark (g)": 150,
            "Apfel (g)": 120,
            "Milch (ml)": 100,
        },
    },
    "Eier mit Brot und Hüttenkäse": {
        "category": "Frühstück",
        "kcal": 490, "protein": 35, "carbs": 43, "fat": 18,
        "ingredients": {
            "Eier (Stück)": 2,
            "Vollkornbrot (g)": 100,
            "Hüttenkäse (g)": 100,
        },
    },
    "Poulet mit Reis und Gemüse": {
        "category": "Mittagessen",
        "kcal": 620, "protein": 48, "carbs": 78, "fat": 11,
        "ingredients": {
            "Pouletbrust (g)": 160,
            "Reis, trocken (g)": 90,
            "Gemüse (g)": 200,
            "Olivenöl (g)": 5,
        },
    },
    "Linsen-Bolognese mit Pasta": {
        "category": "Mittagessen",
        "kcal": 610, "protein": 29, "carbs": 91, "fat": 12,
        "ingredients": {
            "Vollkornpasta, trocken (g)": 100,
            "Linsen, gekocht (g)": 150,
            "Passata (g)": 150,
            "Parmesan (g)": 10,
        },
    },
    "Tofu mit Reis und Gemüse": {
        "category": "Mittagessen",
        "kcal": 600, "protein": 29, "carbs": 75, "fat": 19,
        "ingredients": {
            "Tofu (g)": 150,
            "Reis, trocken (g)": 80,
            "Gemüse (g)": 200,
            "Sojasauce (ml)": 15,
        },
    },
    "Skyr-Bananen-Snack": {
        "category": "Snack",
        "kcal": 330, "protein": 28, "carbs": 48, "fat": 3,
        "ingredients": {
            "Skyr (g)": 200,
            "Banane (g)": 120,
            "Haferflocken (g)": 25,
        },
    },
    "Brot mit Hüttenkäse": {
        "category": "Snack",
        "kcal": 300, "protein": 21, "carbs": 38, "fat": 6,
        "ingredients": {
            "Vollkornbrot (g)": 80,
            "Hüttenkäse (g)": 120,
        },
    },
    "Lachs mit Kartoffeln und Gemüse": {
        "category": "Abendessen",
        "kcal": 650, "protein": 42, "carbs": 65, "fat": 23,
        "ingredients": {
            "Lachs (g)": 150,
            "Kartoffeln (g)": 250,
            "Gemüse (g)": 200,
            "Olivenöl (g)": 5,
        },
    },
    "Poulet mit Kartoffeln aus dem Ofen": {
        "category": "Abendessen",
        "kcal": 590, "protein": 48, "carbs": 62, "fat": 12,
        "ingredients": {
            "Pouletbrust (g)": 160,
            "Kartoffeln (g)": 300,
            "Gemüse (g)": 200,
            "Olivenöl (g)": 5,
        },
    },
    "Kichererbsen-Curry mit Reis": {
        "category": "Abendessen",
        "kcal": 640, "protein": 22, "carbs": 94, "fat": 18,
        "ingredients": {
            "Kichererbsen, gekocht (g)": 160,
            "Reis, trocken (g)": 75,
            "Kokosmilch light (ml)": 100,
            "Gemüse (g)": 150,
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
# 2. SESSION STATE
# --------------------------------------------------

if "training_sessions" not in st.session_state:
    st.session_state.training_sessions = [
        {
            "id": 1,
            "sport": "Laufen",
            "duration": 45,
            "intensity": "Moderat",
        }
    ]

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

if "shopping_checked" not in st.session_state:
    st.session_state.shopping_checked = {}


# --------------------------------------------------
# 3. BERECHNUNGEN
# --------------------------------------------------

def calculate_training_calories(weight):
    """Schätzt zusätzliche Trainingskalorien mit MET-Näherungen."""
    total = 0.0

    for session in st.session_state.training_sessions:
        met = SPORTS[session["sport"]]
        intensity = INTENSITY[session["intensity"]]
        hours = session["duration"] / 60

        # Ruheverbrauch während des Trainings abziehen,
        # damit die Trainingsenergie nicht doppelt gezählt wird.
        gross = met * weight * hours * intensity
        resting = 1.0 * weight * hours
        net = max(0, gross - resting)

        total += net

    return total


def calculate_targets(
    age, weight, height, sex, activity, goal
):
    """Schätzt Tagesenergie und Makroziele."""
    if sex == "Männlich":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex == "Weiblich":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        # Näherungswert bei nicht-binärer/anderer Auswahl
        bmr = 10 * weight + 6.25 * height - 5 * age - 78

    # Aktivitätsfaktor bezieht sich auf den Alltag
    # ohne die separat eingetragenen Trainingseinheiten.
    activity_factors = {
        "Überwiegend sitzend": 1.2,
        "Leicht aktiv": 1.3,
        "Aktiver Alltag": 1.4,
    }

    daily_activity = bmr * activity_factors[activity]
    training_kcal = calculate_training_calories(weight)

    calories = daily_activity + training_kcal

    if goal == "Muskelaufbau":
        calories *= 1.08
    elif goal == "Fettabbau":
        calories *= 0.90

    protein = weight * 1.8
    fat = weight * 0.9
    carbs = max(0, (calories - protein * 4 - fat * 9) / 4)

    return {
        "bmr": round(bmr),
        "training_kcal": round(training_kcal),
        "calories": round(calories),
        "protein": round(protein),
        "carbs": round(carbs),
        "fat": round(fat),
    }


def totals_for_plan(names, portions):
    totals = {
        "kcal": 0.0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0,
    }

    for name, portion in zip(names, portions):
        recipe = RECIPES[name]
        for key in totals:
            totals[key] += recipe[key] * portion

    return totals


def optimize_portions(names, targets):
    """
    Sucht Portionen, die den Tageszielen nahekommen.
    Die Grenzen verhindern extrem kleine oder grosse Portionen.
    """
    portions = [1.0 for _ in names]

    # Schrittweise Verbesserung jeder Portion
    for _ in range(8):
        for i in range(len(portions)):
            best_portion = portions[i]
            best_loss = float("inf")

            for candidate in [
                0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                1.1, 1.2, 1.3, 1.4, 1.5, 1.7,
                1.9, 2.1, 2.3, 2.5
            ]:
                trial = portions.copy()
                trial[i] = candidate
                totals = totals_for_plan(names, trial)

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
                    (p - 1.0) ** 2 for p in trial
                ) / len(trial)

                loss = (
                    8 * calorie_error ** 2
                    + 2 * protein_error ** 2
                    + 1.5 * carb_error ** 2
                    + 1 * fat_error ** 2
                    + 0.04 * portion_penalty
                )

                if loss < best_loss:
                    best_loss = loss
                    best_portion = candidate

            portions[i] = best_portion

    return portions


def build_shopping_list(names, portions):
    shopping = defaultdict(float)

    for name, portion in zip(names, portions):
        for ingredient, amount in RECIPES[name]["ingredients"].items():
            shopping[ingredient] += amount * portion

    return dict(sorted(shopping.items()))


# --------------------------------------------------
# 4. PROFIL
# --------------------------------------------------

st.header("1. Dein Profil")

c1, c2, c3 = st.columns(3)

with c1:
    age = st.number_input(
        "Alter", min_value=18, max_value=100, value=30
    )
    weight = st.number_input(
        "Gewicht (kg)", min_value=35.0, max_value=250.0,
        value=62.0, step=0.5
    )

with c2:
    height = st.number_input(
        "Grösse (cm)", min_value=130, max_value=230, value=165
    )
    sex = st.selectbox(
        "Berechnungsprofil",
        ["Männlich", "Weiblich", "Andere / keine Angabe"]
    )

with c3:
    goal = st.selectbox(
        "Dein Ziel",
        ["Leistung erhalten", "Muskelaufbau", "Fettabbau"]
    )
    activity = st.selectbox(
        "Alltagsaktivität ohne Training",
        [
            "Überwiegend sitzend",
            "Leicht aktiv",
            "Aktiver Alltag",
        ],
    )

st.caption(
    "Wähle deine normale Alltagsaktivität. Geplante Sporteinheiten "
    "werden separat berücksichtigt."
)


# --------------------------------------------------
# 5. TRAININGSEINHEITEN
# --------------------------------------------------

st.header("2. Dein Training")

st.write(
    "Füge alle geplanten Einheiten für diesen Tag hinzu. "
    "Jede Einheit wird separat nach Sportart, Dauer und Intensität geschätzt."
)

remove_id = None

for session in st.session_state.training_sessions:
    with st.container(border=True):
        st.markdown(f"**Trainingseinheit {session['id']}**")
        c1, c2, c3, c4 = st.columns([2, 1, 1.5, 0.8])

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

if st.button("＋ Trainingseinheit hinzufügen", type="secondary"):
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
# 6. TAGESZIELE
# --------------------------------------------------

targets = calculate_targets(
    age, weight, height, sex, activity, goal
)

st.header("3. Deine geschätzten Tagesziele")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Kalorien", f"{targets['calories']} kcal")
m2.metric("Protein", f"{targets['protein']} g")
m3.metric("Kohlenhydrate", f"{targets['carbs']} g")
m4.metric("Fett", f"{targets['fat']} g")

st.caption(
    f"Geschätzter Grundumsatz: {targets['bmr']} kcal · "
    f"Zusätzliche Trainingsenergie: ca. {targets['training_kcal']} kcal"
)

st.info(
    "Das sind Schätzwerte, keine Messungen. Insbesondere Trainingskalorien "
    "können deutlich abweichen. Beobachte deine Energie, Regeneration und "
    "Gewichtsentwicklung und passe die Ziele bei Bedarf an."
)


# --------------------------------------------------
# 7. MAHLZEITEN AUSWÄHLEN
# --------------------------------------------------

st.header("4. Dein Tagesmenü")

st.write(
    "Wähle deine Gerichte. Anschliessend berechnet PACE passende "
    "Portionsgrössen für den gesamten Tag."
)

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

if st.button("Tagesplan berechnen", type="primary", use_container_width=True):
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
# 8. ERGEBNIS
# --------------------------------------------------

if st.session_state.portion_results is not None:
    results = st.session_state.portion_results
    names = results["names"]
    portions = results["portions"]
    result_targets = results["targets"]

    # Wenn sich Trainingsziele seit der letzten Berechnung geändert haben,
    # soll der Nutzer den Plan erneut berechnen.
    if result_targets != targets:
        st.warning(
            "Dein Profil oder Training hat sich geändert. "
            "Berechne den Tagesplan erneut, damit die Portionen aktualisiert werden."
        )

    st.header("5. Dein angepasster Tagesplan")

    for slot, name, portion in zip(
        [s for s, _ in MEAL_SLOTS], names, portions
    ):
        recipe = RECIPES[name]
        st.markdown(f"**{slot}: {name}**")
        st.write(
            f"Portion: **{portion:.1f}×** · "
            f"{round(recipe['kcal'] * portion)} kcal · "
            f"Protein {round(recipe['protein'] * portion)} g · "
            f"Kohlenhydrate {round(recipe['carbs'] * portion)} g · "
            f"Fett {round(recipe['fat'] * portion)} g"
        )

        ingredients = []
        for ingredient, amount in recipe["ingredients"].items():
            scaled = amount * portion
            if ingredient.endswith("(Stück)"):
                quantity = f"{scaled:.1f}"
            else:
                quantity = f"{scaled:.0f}"
            ingredients.append(f"{quantity} {ingredient}")

        st.caption("Zutaten: " + ", ".join(ingredients))

    totals = totals_for_plan(names, portions)

    st.header("6. Tagesbilanz")

    rows = [
        ("Kalorien", totals["kcal"], targets["calories"], "kcal"),
        ("Protein", totals["protein"], targets["protein"], "g"),
        ("Kohlenhydrate", totals["carbs"], targets["carbs"], "g"),
        ("Fett", totals["fat"], targets["fat"], "g"),
    ]

    for label, actual, target, unit in rows:
        delta = actual - target
        st.write(
            f"**{label}:** {actual:.0f} {unit} von "
            f"{target:.0f} {unit} · Abweichung: {delta:+.0f} {unit}"
        )
        st.progress(
            min(max(actual / max(target, 1), 0.0), 1.0)
        )

    calorie_difference = totals["kcal"] - targets["calories"]

    if abs(calorie_difference) <= targets["calories"] * 0.05:
        st.success("Die Kalorien liegen innerhalb von ungefähr 5 % des Zielwerts.")
    else:
        st.info(
            "Das Menü liegt noch mehr als 5 % vom Kalorienziel entfernt. "
            "Teste andere Gerichte oder passe die Auswahl an."
        )

    st.caption(
        "Die Nährwerte der Rezepte sind Näherungswerte. "
        "Kalorien und Makros lassen sich nicht immer gleichzeitig exakt treffen."
    )

    # Einkaufsliste
    st.header("7. Einkaufsliste")

    shopping = build_shopping_list(names, portions)

    shopping_text = ["PACE Nutrition – Einkaufsliste", ""]

    for ingredient, amount in shopping.items():
        if ingredient.endswith("(Stück)"):
            quantity = f"{amount:.1f}"
        else:
            quantity = f"{amount:.0f}"

        shopping_text.append(f"- {ingredient}: {quantity}")

    for ingredient, amount in shopping.items():
        label = (
            f"{ingredient}: {amount:.1f}"
            if ingredient.endswith("(Stück)")
            else f"{ingredient}: {amount:.0f}"
        )
        st.checkbox(
            label,
            key=f"shop_{ingredient}",
        )

    st.download_button(
        "Einkaufsliste herunterladen",
        data="\n".join(shopping_text),
        file_name="pace_einkaufsliste.txt",
        mime="text/plain",
        use_container_width=True,
    )

else:
    st.info(
        "Wähle deine Mahlzeiten aus und klicke auf "
        "«Tagesplan berechnen», um die Portionsgrössen und Einkaufsliste zu erhalten."
    )

st.divider()
st.caption(
    "PACE Nutrition · Prototyp · Keine medizinische oder "
    "ernährungsmedizinische Beratung."
)
