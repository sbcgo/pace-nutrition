
import streamlit as st
from collections import defaultdict

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide",
)

st.title("🥗 PACE Nutrition")
st.subheader("Deine Ernährung passend zu deinem Training")
st.write(
    "Automatische Portionsberechnung, individuelle Makroziele "
    "und eine Einkaufsliste, die sich an dein Menü anpasst."
)

st.info(
    "Die Berechnung verwendet hinterlegte Durchschnittswerte. "
    "Die tatsächlichen Nährwerte hängen von Produkt, Marke und Zubereitung ab."
)

# =====================================================
# REZEPTE
# Nährwerte und Zutatenmengen jeweils pro Basisportion
# =====================================================

RECIPES = {
    "Porridge mit Beeren und Skyr": {
        "category": "Frühstück",
        "kcal": 520, "protein": 34, "carbs": 72, "fat": 10,
        "ingredients": {
            "Haferflocken": (80, "g"),
            "Skyr nature": (200, "g"),
            "Beeren (frisch oder TK)": (100, "g"),
            "Banane": (100, "g"),
        },
    },
    "Overnight Oats mit Apfel und Quark": {
        "category": "Frühstück",
        "kcal": 500, "protein": 32, "carbs": 70, "fat": 9,
        "ingredients": {
            "Haferflocken": (70, "g"),
            "Magerquark": (200, "g"),
            "Apfel": (150, "g"),
            "Milch": (100, "ml"),
        },
    },
    "Eierbrot mit Hüttenkäse": {
        "category": "Frühstück",
        "kcal": 490, "protein": 31, "carbs": 48, "fat": 17,
        "ingredients": {
            "Vollkornbrot": (120, "g"),
            "Eier": (2, "Stk."),
            "Hüttenkäse": (100, "g"),
            "Tomaten": (100, "g"),
        },
    },
    "Poulet mit Reis und Gemüse": {
        "category": "Mittagessen",
        "kcal": 650, "protein": 46, "carbs": 82, "fat": 12,
        "ingredients": {
            "Pouletbrust": (160, "g"),
            "Reis (trocken)": (100, "g"),
            "Gemüsemix": (200, "g"),
            "Olivenöl": (5, "ml"),
        },
    },
    "Linsen-Bolognese mit Pasta": {
        "category": "Mittagessen",
        "kcal": 630, "protein": 28, "carbs": 95, "fat": 12,
        "ingredients": {
            "Vollkornpasta (trocken)": (100, "g"),
            "Linsen (gekocht)": (150, "g"),
            "Passata": (150, "g"),
            "Zwiebeln": (50, "g"),
            "Olivenöl": (5, "ml"),
        },
    },
    "Tofu-Reis-Pfanne": {
        "category": "Mittagessen",
        "kcal": 620, "protein": 27, "carbs": 78, "fat": 19,
        "ingredients": {
            "Tofu": (180, "g"),
            "Reis (trocken)": (90, "g"),
            "Gemüsemix": (200, "g"),
            "Sojasauce": (15, "ml"),
        },
    },
    "Skyr mit Banane und Haferflocken": {
        "category": "Snack",
        "kcal": 330, "protein": 27, "carbs": 48, "fat": 4,
        "ingredients": {
            "Skyr nature": (200, "g"),
            "Banane": (120, "g"),
            "Haferflocken": (30, "g"),
        },
    },
    "Brot mit Hüttenkäse": {
        "category": "Snack",
        "kcal": 300, "protein": 21, "carbs": 38, "fat": 6,
        "ingredients": {
            "Vollkornbrot": (100, "g"),
            "Hüttenkäse": (100, "g"),
            "Gurke": (80, "g"),
        },
    },
    "Lachs mit Kartoffeln und Gemüse": {
        "category": "Abendessen",
        "kcal": 650, "protein": 38, "carbs": 62, "fat": 26,
        "ingredients": {
            "Lachs": (150, "g"),
            "Kartoffeln": (300, "g"),
            "Gemüsemix": (200, "g"),
            "Olivenöl": (5, "ml"),
        },
    },
    "Poulet-Kartoffel-Blech": {
        "category": "Abendessen",
        "kcal": 590, "protein": 45, "carbs": 58, "fat": 15,
        "ingredients": {
            "Pouletbrust": (150, "g"),
            "Kartoffeln": (300, "g"),
            "Gemüsemix": (200, "g"),
            "Olivenöl": (5, "ml"),
        },
    },
    "Kichererbsen-Curry mit Reis": {
        "category": "Abendessen",
        "kcal": 620, "protein": 22, "carbs": 94, "fat": 16,
        "ingredients": {
            "Kichererbsen (gekocht)": (180, "g"),
            "Reis (trocken)": (80, "g"),
            "Passata": (150, "g"),
            "Kokosmilch": (50, "ml"),
            "Zwiebeln": (50, "g"),
        },
    },
}

SLOTS = [
    ("Frühstück", "breakfast"),
    ("Mittagessen", "lunch"),
    ("Snack", "snack"),
    ("Abendessen", "dinner"),
]

DEFAULT_MEALS = {
    "breakfast": "Porridge mit Beeren und Skyr",
    "lunch": "Poulet mit Reis und Gemüse",
    "snack": "Skyr mit Banane und Haferflocken",
    "dinner": "Poulet-Kartoffel-Blech",
}

def fmt(value):
    return f"{round(value):,}".replace(",", "'")

def recipe_options(category):
    return [
        name for name, recipe in RECIPES.items()
        if recipe["category"] == category
    ]

def calculate_totals(names, portions):
    totals = {
        "kcal": 0.0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0,
    }

    for name, portion in zip(names, portions):
        for key in totals:
            totals[key] += RECIPES[name][key] * portion

    return totals

def optimize_portions(names, calorie_target, protein_target,
                      carbs_target, fat_target):
    """
    Optimiert die Portionsfaktoren anhand von Kalorien und Makros.
    Die Kalorien haben das höchste Gewicht. Die Portionsfaktoren
    bleiben in einem praktikablen Bereich von 0.35 bis 2.5.
    """
    portions = [1.0 for _ in names]

    # Kalorien werden am stärksten gewichtet.
    targets = {
        "kcal": max(calorie_target, 1),
        "protein": max(protein_target, 1),
        "carbs": max(carbs_target, 1),
        "fat": max(fat_target, 1),
    }

    weights = {
        "kcal": 8.0,
        "protein": 2.0,
        "carbs": 1.5,
        "fat": 1.0,
    }

    def loss(candidate_portions):
        totals = calculate_totals(names, candidate_portions)
        result = 0.0

        for key in targets:
            relative_error = (
                (totals[key] - targets[key]) / targets[key]
            )
            result += weights[key] * relative_error ** 2

        # Extreme Portionsgrössen leicht bestrafen.
        for portion in candidate_portions:
            result += 0.025 * (portion - 1.0) ** 2

        return result

    # Einfache coordinate-search-Optimierung ohne Zusatzbibliotheken.
    steps = [0.25, 0.12, 0.06, 0.03, 0.01]

    for step in steps:
        improved = True
        while improved:
            improved = False
            current_loss = loss(portions)

            for i in range(len(portions)):
                best_value = portions[i]
                best_loss = current_loss

                for change in (-step, step):
                    candidate = portions.copy()
                    candidate[i] = min(
                        2.5, max(0.35, candidate[i] + change)
                    )
                    candidate_loss = loss(candidate)

                    if candidate_loss < best_loss:
                        best_loss = candidate_loss
                        best_value = candidate[i]

                if best_value != portions[i]:
                    portions[i] = best_value
                    current_loss = best_loss
                    improved = True

    # Letzte proportionale Korrektur: Kalorienziel exakt auf
    # Basis der hinterlegten Rezeptwerte treffen, sofern möglich.
    totals = calculate_totals(names, portions)

    if totals["kcal"] > 0:
        scale = calorie_target / totals["kcal"]
        portions = [
            min(2.5, max(0.35, portion * scale))
            for portion in portions
        ]

    return portions

# =====================================================
# PROFIL
# =====================================================

st.header("👤 Dein Profil")

c1, c2, c3 = st.columns(3)

with c1:
    age = st.number_input(
        "Alter", min_value=16, max_value=100, value=30
    )

with c2:
    weight = st.number_input(
        "Gewicht (kg)", min_value=35.0, max_value=200.0,
        value=62.0, step=0.5
    )

with c3:
    height = st.number_input(
        "Grösse (cm)", min_value=130, max_value=230, value=165
    )

sex = st.selectbox("Geschlecht", ["Männlich", "Weiblich"])

goal = st.selectbox(
    "Dein Hauptziel",
    ["Muskeln aufbauen", "Leistung verbessern", "Gewicht halten"]
)

activity = st.selectbox(
    "Alltagsaktivität",
    ["Wenig Bewegung", "Leicht aktiv", "Moderat aktiv", "Sehr aktiv"],
    index=2
)

st.divider()

# =====================================================
# TRAINING
# =====================================================

st.header("🏃 Deine heutige Trainingseinheit")

c4, c5 = st.columns(2)

with c4:
    training_type = st.selectbox(
        "Trainingsart",
        ["Ruhetag", "Krafttraining", "Laufen", "Radfahren",
         "Schwimmen", "Koppeltraining"]
    )

with c5:
    intensity = st.selectbox(
        "Trainingsintensität",
        ["Leicht", "Moderat", "Intensiv"],
        index=1
    )

duration = st.slider(
    "Trainingsdauer (Minuten)",
    min_value=0, max_value=240, value=60, step=15
)

# =====================================================
# TAGESZIELE
# =====================================================

if sex == "Männlich":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

activity_factors = {
    "Wenig Bewegung": 1.2,
    "Leicht aktiv": 1.375,
    "Moderat aktiv": 1.55,
    "Sehr aktiv": 1.725,
}

base_energy = bmr * activity_factors[activity]

met_values = {
    "Ruhetag": 0,
    "Krafttraining": 5,
    "Laufen": 9,
    "Radfahren": 7,
    "Schwimmen": 7,
    "Koppeltraining": 8,
}

intensity_factors = {
    "Leicht": 0.75,
    "Moderat": 1.0,
    "Intensiv": 1.2,
}

training_calories = (
    met_values[training_type]
    * 3.5 * weight / 200
    * duration
    * intensity_factors[intensity]
)

estimated_energy = base_energy + training_calories

if goal == "Muskeln aufbauen":
    calorie_target = estimated_energy * 1.08
else:
    calorie_target = estimated_energy

protein_target = weight * 1.8
fat_target = weight * 0.9
carb_target = max(
    0,
    (calorie_target - protein_target * 4 - fat_target * 9) / 4
)

st.divider()
st.header("🎯 Deine geschätzten Tagesziele")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Kalorien", f"{fmt(calorie_target)} kcal")
m2.metric("Protein", f"{round(protein_target)} g")
m3.metric("Kohlenhydrate", f"{round(carb_target)} g")
m4.metric("Fett", f"{round(fat_target)} g")

# =====================================================
# MENÜPLAN UND MAHLZEITENAUSTAUSCH
# =====================================================

st.divider()
st.header("🍽️ Dein automatisch angepasster Menüplan")

st.write(
    "Wähle deine bevorzugten Gerichte. PACE passt die Portionsgrössen "
    "an dein Tagesziel an und berechnet die Einkaufsliste neu."
)

# Speichert die Auswahl über Streamlit-Neuberechnungen hinweg.
for slot_key, default_recipe in DEFAULT_MEALS.items():
    state_key = f"meal_{slot_key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = default_recipe

selected_names = []

for category, slot_key in SLOTS:
    state_key = f"meal_{slot_key}"
    options = recipe_options(category)

    if st.session_state[state_key] not in options:
        st.session_state[state_key] = options[0]

    selected = st.selectbox(
        f"{category}: Gericht auswählen",
        options,
        key=state_key
    )
    selected_names.append(selected)

# Optimiert Portionen bei jeder Änderung von Profil,
# Training oder Mahlzeitenauswahl.
portions = optimize_portions(
    selected_names,
    calorie_target,
    protein_target,
    carb_target,
    fat_target,
)

# Menü ausgeben
for name, portion in zip(selected_names, portions):
    recipe = RECIPES[name]

    with st.container(border=True):
        st.subheader(name)
        st.write(f"**Portion:** {portion:.2f} Basisportion(en)")

        a, b, c, d = st.columns(4)
        a.metric("Kalorien", f'{round(recipe["kcal"] * portion)} kcal')
        b.metric("Protein", f'{round(recipe["protein"] * portion)} g')
        c.metric("Kohlenhydrate", f'{round(recipe["carbs"] * portion)} g')
        d.metric("Fett", f'{round(recipe["fat"] * portion)} g')

totals = calculate_totals(selected_names, portions)

st.divider()
st.header("📊 Dein Menü im Vergleich zum Tagesziel")

a, b, c, d = st.columns(4)
a.metric(
    "Menü-Kalorien",
    f'{fmt(totals["kcal"])} kcal',
    delta=f'{round(totals["kcal"] - calorie_target):+} kcal'
)
b.metric(
    "Protein",
    f'{round(totals["protein"])} g',
    delta=f'{round(totals["protein"] - protein_target):+} g'
)
c.metric(
    "Kohlenhydrate",
    f'{round(totals["carbs"])} g',
    delta=f'{round(totals["carbs"] - carb_target):+} g'
)
d.metric(
    "Fett",
    f'{round(totals["fat"])} g',
    delta=f'{round(totals["fat"] - fat_target):+} g'
)

st.caption(
    "Der Optimierer priorisiert Kalorien und versucht gleichzeitig, "
    "Protein, Kohlenhydrate und Fett möglichst gut zu treffen. "
    "Durch begrenzte Portionsgrössen und unterschiedliche Rezept-Makros "
    "können Abweichungen bestehen bleiben."
)

st.warning(
    "Wichtig: Die Kalorienziele selbst sind Schätzungen. Exakte "
    "Übereinstimmung in der App bedeutet nicht automatisch, dass der "
    "geschätzte Bedarf physiologisch exakt ist."
)

# =====================================================
# EINKAUFSLISTE MIT SKALIERTEN ZUTATENMENGEN
# =====================================================

st.divider()
st.header("🛒 Einkaufsliste")

st.write(
    "Die Mengen werden anhand der angepassten Portionsgrössen berechnet. "
    "Checkboxen bleiben beim Anklicken erhalten."
)

shopping = defaultdict(lambda: {"amount": 0.0, "unit": ""})

for name, portion in zip(selected_names, portions):
    for ingredient, (amount, unit) in RECIPES[name]["ingredients"].items():
        shopping[ingredient]["amount"] += amount * portion
        shopping[ingredient]["unit"] = unit

ingredients_sorted = sorted(shopping.keys())

checked_count = 0

for ingredient in ingredients_sorted:
    amount = shopping[ingredient]["amount"]
    unit = shopping[ingredient]["unit"]

    if unit == "Stk.":
        quantity = f"{amount:.1f} {unit}"
    else:
        quantity = f"{round(amount)} {unit}"

    key = f"shopping_{ingredient}"

    if key not in st.session_state:
        st.session_state[key] = False

    if st.checkbox(
        f"{ingredient} — {quantity}",
        key=key
    ):
        checked_count += 1

total_items = len(ingredients_sorted)
progress = checked_count / total_items if total_items else 0

st.progress(progress)
st.caption(f"{checked_count} von {total_items} Zutaten erledigt.")

if st.button("Einkaufsliste zurücksetzen"):
    for ingredient in ingredients_sorted:
        st.session_state[f"shopping_{ingredient}"] = False
    st.rerun()

st.divider()
st.caption(
    "PACE Nutrition ist ein Prototyp. Die Nährwerte sind Näherungswerte "
    "und können je nach Produkt und Zubereitung abweichen."
)
