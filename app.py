
import streamlit as st
from collections import defaultdict
import math

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 PACE Nutrition")
st.subheader("Deine Ernährung passend zu Training, Zielen und Budget")
st.caption(
    "Version 4 – individuelle Portionsgrössen und automatische Einkaufsliste"
)

# --------------------------------------------------
# 1. REZEPTDATEN
# Alle Angaben pro Basisportion.
# Nährwerte sind Schätzungen.
# Zutatenmengen beziehen sich auf Rohgewicht,
# sofern nicht anders angegeben.
# --------------------------------------------------

RECIPES = {
    "Porridge mit Beeren und Skyr": {
        "category": "Frühstück",
        "kcal": 520, "protein": 35, "carbs": 72, "fat": 9,
        "ingredients": {
            "Haferflocken (g)": 70,
            "Skyr (g)": 200,
            "Beeren (g)": 100,
            "Banane (g)": 80
        }
    },
    "Overnight Oats mit Apfel": {
        "category": "Frühstück",
        "kcal": 490, "protein": 31, "carbs": 70, "fat": 10,
        "ingredients": {
            "Haferflocken (g)": 65,
            "Magerquark (g)": 150,
            "Apfel (g)": 150,
            "Milch (ml)": 100
        }
    },
    "Eier mit Brot und Hüttenkäse": {
        "category": "Frühstück",
        "kcal": 510, "protein": 34, "carbs": 45, "fat": 19,
        "ingredients": {
            "Eier (Stück)": 2,
            "Vollkornbrot (g)": 100,
            "Hüttenkäse (g)": 100,
            "Tomaten (g)": 100
        }
    },
    "Poulet mit Reis und Gemüse": {
        "category": "Mittagessen",
        "kcal": 650, "protein": 48, "carbs": 85, "fat": 10,
        "ingredients": {
            "Pouletbrust (g)": 160,
            "Reis trocken (g)": 100,
            "Gemüse (g)": 200,
            "Olivenöl (g)": 5
        }
    },
    "Linsen-Bolognese mit Pasta": {
        "category": "Mittagessen",
        "kcal": 620, "protein": 28, "carbs": 95, "fat": 12,
        "ingredients": {
            "Vollkornpasta trocken (g)": 100,
            "Linsen gekocht (g)": 150,
            "Passata (g)": 150,
            "Zwiebel (g)": 50,
            "Olivenöl (g)": 5
        }
    },
    "Tofu mit Reis und Gemüse": {
        "category": "Mittagessen",
        "kcal": 630, "protein": 30, "carbs": 78, "fat": 20,
        "ingredients": {
            "Tofu (g)": 150,
            "Reis trocken (g)": 90,
            "Gemüse (g)": 200,
            "Sojasauce (ml)": 15
        }
    },
    "Skyr-Bananen-Snack": {
        "category": "Snack",
        "kcal": 300, "protein": 25, "carbs": 43, "fat": 3,
        "ingredients": {
            "Skyr (g)": 200,
            "Banane (g)": 120,
            "Haferflocken (g)": 20
        }
    },
    "Brot mit Hüttenkäse": {
        "category": "Snack",
        "kcal": 310, "protein": 22, "carbs": 40, "fat": 6,
        "ingredients": {
            "Vollkornbrot (g)": 80,
            "Hüttenkäse (g)": 150,
            "Gurke (g)": 100
        }
    },
    "Lachs mit Kartoffeln und Gemüse": {
        "category": "Abendessen",
        "kcal": 650, "protein": 40, "carbs": 65, "fat": 24,
        "ingredients": {
            "Lachs (g)": 150,
            "Kartoffeln (g)": 250,
            "Gemüse (g)": 200,
            "Olivenöl (g)": 5
        }
    },
    "Poulet mit Ofenkartoffeln": {
        "category": "Abendessen",
        "kcal": 620, "protein": 48, "carbs": 65, "fat": 12,
        "ingredients": {
            "Pouletbrust (g)": 160,
            "Kartoffeln (g)": 300,
            "Gemüse (g)": 150,
            "Olivenöl (g)": 5
        }
    },
    "Kichererbsen-Curry mit Reis": {
        "category": "Abendessen",
        "kcal": 640, "protein": 22, "carbs": 95, "fat": 18,
        "ingredients": {
            "Kichererbsen gekocht (g)": 180,
            "Reis trocken (g)": 80,
            "Kokosmilch light (ml)": 100,
            "Passata (g)": 100
        }
    }
}

MEAL_CATEGORIES = [
    "Frühstück",
    "Mittagessen",
    "Snack",
    "Abendessen"
]

# --------------------------------------------------
# 2. HILFSFUNKTIONEN
# --------------------------------------------------

def calculate_nutrition(names, portions):
    result = {
        "kcal": 0.0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0
    }

    for name, factor in zip(names, portions):
        recipe = RECIPES[name]
        for key in result:
            result[key] += recipe[key] * factor

    return result


def calculate_targets(
    age, weight, height, sex, activity, goal,
    training_minutes, training_intensity, training_type
):
    # Mifflin-St-Jeor: Grundumsatz
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

    maintenance = bmr * activity_factors[activity]

    # Grobe Schätzung des zusätzlichen Trainingsverbrauchs.
    # Der MET-Wert ist bewusst nur eine Näherung.
    met_values = {
        "Krafttraining": 4.5,
        "Laufen": 8.0,
        "Radfahren": 7.0,
        "Schwimmen": 7.0,
        "Ruhetag / Spaziergang": 2.0,
        "Andere": 5.0
    }

    met = met_values[training_type]

    intensity_factors = {
        "Locker": 0.8,
        "Moderat": 1.0,
        "Intensiv": 1.2
    }

    # Nettoverbrauch über Ruheumsatz hinaus, grob geschätzt
    training_kcal = max(
        0,
        (met - 1) * 3.5 * weight / 200
        * training_minutes
        * intensity_factors[training_intensity]
    )

    # Training ist in Aktivitätsfaktoren oft bereits teilweise enthalten.
    # Deshalb wird nur ein Anteil des geschätzten Verbrauchs ergänzt.
    calories = maintenance + training_kcal * 0.6

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
        "fat": round(fat)
    }


def optimize_portions(names, targets):
    """
    Optimiert die Portionen innerhalb sinnvoller Grenzen.
    Kalorien werden stark gewichtet; Makros werden ebenfalls
    berücksichtigt. Es wird kein exaktes Ergebnis versprochen.
    """
    if not names:
        return []

    # Start mit Basisportionen.
    portions = [1.0 for _ in names]

    # Gewichtung der Abweichungen.
    weights = {
        "kcal": 8.0,
        "protein": 2.0,
        "carbs": 1.5,
        "fat": 1.0
    }

    def loss(candidate):
        totals = calculate_nutrition(names, candidate)
        score = 0.0

        for key, weight in weights.items():
            target = targets[key]
            if target > 0:
                relative_error = (
                    (totals[key] - target) / target
                )
                score += weight * relative_error ** 2

        # Verhindert unnötig extreme Portionsgrössen.
        score += sum(
            0.08 * (factor - 1.0) ** 2
            for factor in candidate
        )

        return score

    # Coordinate Search: Jede Mahlzeit einzeln anpassen.
    # Mehrere Durchläufe verbessern die Näherung.
    step_sizes = [0.25, 0.10, 0.04, 0.015]

    for step in step_sizes:
        for _ in range(3):
            for i in range(len(portions)):
                current = portions[i]
                best_factor = current
                best_score = loss(portions)

                for direction in (-1, 1):
                    candidate_factor = max(
                        0.4,
                        min(2.2, current + direction * step)
                    )

                    candidate = portions.copy()
                    candidate[i] = candidate_factor
                    candidate_score = loss(candidate)

                    if candidate_score < best_score:
                        best_score = candidate_score
                        best_factor = candidate_factor

                portions[i] = best_factor

    return portions


def ingredient_amount(amount, factor, unit):
    value = amount * factor

    if unit == "Stück":
        return f"{value:.1f} Stück"

    if unit == "ml":
        return f"{value:.0f} ml"

    return f"{value:.0f} g"


def ingredient_unit(ingredient):
    if ingredient.endswith("(Stück)"):
        return "Stück"
    if ingredient.endswith("(ml)"):
        return "ml"
    return "g"


# --------------------------------------------------
# 3. PROFIL UND TAGESZIEL
# --------------------------------------------------

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
        min_value=130,
        max_value=230,
        value=165
    )
    sex = st.selectbox(
        "Geschlecht für die Grundumsatzformel",
        ["Männlich", "Weiblich"]
    )

with col3:
    goal = st.selectbox(
        "Ernährungsziel",
        ["Leistung erhalten", "Muskelaufbau", "Fettabbau"]
    )
    activity = st.selectbox(
        "Allgemeine Aktivität",
        [
            "Wenig aktiv",
            "Leicht aktiv",
            "Moderat aktiv",
            "Sehr aktiv"
        ],
        index=2
    )

st.header("2. Dein heutiges Training")

col1, col2, col3 = st.columns(3)

with col1:
    training_type = st.selectbox(
        "Trainingsart",
        [
            "Ruhetag / Spaziergang",
            "Krafttraining",
            "Laufen",
            "Radfahren",
            "Schwimmen",
            "Andere"
        ]
    )

with col2:
    training_minutes = st.number_input(
        "Trainingsdauer (Minuten)",
        min_value=0,
        max_value=600,
        value=60,
        step=15
    )

with col3:
    training_intensity = st.selectbox(
        "Trainingsintensität",
        ["Locker", "Moderat", "Intensiv"],
        index=1
    )

targets = calculate_targets(
    age,
    weight,
    height,
    sex,
    activity,
    goal,
    training_minutes,
    training_intensity,
    training_type
)

st.header("3. Dein berechnetes Tagesziel")

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric("Kalorien", f'{targets["kcal"]} kcal')
metric2.metric("Protein", f'{targets["protein"]} g')
metric3.metric("Kohlenhydrate", f'{targets["carbs"]} g')
metric4.metric("Fett", f'{targets["fat"]} g')

st.caption(
    "Schätzwerte: Der tatsächliche Bedarf hängt unter anderem von "
    "Alltagsbewegung, Trainingsbelastung und individueller Physiologie ab."
)

# --------------------------------------------------
# 4. MENÜ ZUSAMMENSTELLEN
# --------------------------------------------------

st.header("4. Stelle dein Menü zusammen")
st.write(
    "Wähle für jede Mahlzeit ein Gericht. "
    "PACE passt danach die Portionen an dein Tagesziel an."
)

selected = {}

for category in MEAL_CATEGORIES:
    options = [
        name for name, recipe in RECIPES.items()
        if recipe["category"] == category
    ]

    selected[category] = st.selectbox(
        category,
        options,
        key=f"meal_{category}"
    )

if st.button("Portionen optimieren", type="primary"):
    names = [selected[category] for category in MEAL_CATEGORIES]
    portions = optimize_portions(names, targets)

    st.session_state["optimized_names"] = names
    st.session_state["optimized_portions"] = portions

# Wenn sich das Menü ändert, die vorherige Optimierung nicht
# stillschweigend auf die neue Auswahl anwenden.
current_names = [selected[category] for category in MEAL_CATEGORIES]

if (
    "optimized_names" not in st.session_state
    or st.session_state["optimized_names"] != current_names
):
    st.info(
        "Wähle deine Gerichte und klicke auf «Portionen optimieren», "
        "um die Mengen für dein Tagesziel zu berechnen."
    )
else:
    names = st.session_state["optimized_names"]
    portions = st.session_state["optimized_portions"]
    totals = calculate_nutrition(names, portions)

    st.header("5. Dein optimierter Tagesplan")

    for category, name, factor in zip(
        MEAL_CATEGORIES, names, portions
    ):
        recipe = RECIPES[name]

        st.markdown(f"**{category}: {name}**")
        st.write(f"Portionsfaktor: {factor:.2f} × Basisportion")

        ingredients_text = []
        for ingredient, amount in recipe["ingredients"].items():
            unit = ingredient_unit(ingredient)
            ingredients_text.append(
                f"{ingredient.split(' (')[0]}: "
                f"{ingredient_amount(amount, factor, unit)}"
            )

        st.write(" · ".join(ingredients_text))
        st.caption(
            f"Ca. {recipe['kcal'] * factor:.0f} kcal | "
            f"Protein {recipe['protein'] * factor:.0f} g | "
            f"Kohlenhydrate {recipe['carbs'] * factor:.0f} g | "
            f"Fett {recipe['fat'] * factor:.0f} g"
        )
        st.divider()

    st.header("6. Tagesbilanz")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Kalorien",
        f'{totals["kcal"]:.0f} kcal',
        f'{totals["kcal"] - targets["kcal"]:+.0f} kcal'
    )
    c2.metric(
        "Protein",
        f'{totals["protein"]:.0f} g',
        f'{totals["protein"] - targets["protein"]:+.0f} g'
    )
    c3.metric(
        "Kohlenhydrate",
        f'{totals["carbs"]:.0f} g',
        f'{totals["carbs"] - targets["carbs"]:+.0f} g'
    )
    c4.metric(
        "Fett",
        f'{totals["fat"]:.0f} g',
        f'{totals["fat"] - targets["fat"]:+.0f} g'
    )

    calorie_difference = totals["kcal"] - targets["kcal"]
    calorie_percent = (
        abs(calorie_difference) / targets["kcal"] * 100
        if targets["kcal"] else 0
    )

    if calorie_percent <= 3:
        st.success(
            "Das Menü liegt sehr nahe am berechneten Kalorienziel."
        )
    elif calorie_percent <= 8:
        st.warning(
            "Das Menü liegt relativ nahe am Ziel. "
            "Die Makros und die Alltagstauglichkeit der Portionen "
            "sollten ebenfalls geprüft werden."
        )
    else:
        st.warning(
            "Das Menü weicht noch merklich vom Tagesziel ab. "
            "Probiere andere Gerichte oder Mahlzeitenkombinationen."
        )

    st.caption(
        "Die Optimierung sucht eine möglichst passende Kombination. "
        "Sie kann wegen der begrenzten Portionsgrössen und der "
        "unterschiedlichen Makroverteilung nicht jedes Ziel exakt treffen."
    )

    # --------------------------------------------------
    # 7. AUTOMATISCHE EINKAUFSLISTE
    # --------------------------------------------------

    st.header("7. Deine Einkaufsliste")

    shopping_list = defaultdict(float)

    for name, factor in zip(names, portions):
        for ingredient, amount in RECIPES[name]["ingredients"].items():
            shopping_list[ingredient] += amount * factor

    for ingredient in sorted(shopping_list):
        unit = ingredient_unit(ingredient)
        amount = shopping_list[ingredient]

        if unit == "Stück":
            amount_text = f"{amount:.1f} Stück"
        elif unit == "ml":
            amount_text = f"{amount:.0f} ml"
        else:
            amount_text = f"{amount:.0f} g"

        st.checkbox(
            f"{ingredient.split(' (')[0]} – {amount_text}",
            key=f"shopping_{ingredient}"
        )

    shopping_text = "\n".join(
        f"- {ingredient.split(' (')[0]}: "
        f"{ingredient_amount(amount, 1, ingredient_unit(ingredient))}"
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
    "PACE Nutrition ist ein Planungsprototyp und ersetzt keine "
    "individuelle Ernährungsberatung. Nährwerte, Energiebedarf und "
    "Trainingsverbrauch sind Näherungen."
)
