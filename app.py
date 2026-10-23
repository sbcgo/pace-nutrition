
import streamlit as st
from collections import defaultdict

st.set_page_config(
    page_title="PACE Nutrition",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 PACE Nutrition")
st.subheader("Deine Ernährung. Dein Training. Dein Fortschritt.")
st.write(
    "Dein Ernährungsplaner für Hybrid-Athleten: "
    "günstige Mahlzeiten, passende Makros und eine praktische Einkaufsliste."
)

st.info(
    "Die Angaben sind Schätzwerte und dienen der Orientierung. "
    "Der Prototyp ersetzt keine individuelle Ernährungsberatung."
)

# =====================================================
# REZEPTDATENBANK
# Nährwerte pro Portion; Mengen sind Richtwerte.
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
        "description": "Kohlenhydratreiches Frühstück für aktive Tage."
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
        "description": "Günstig, proteinreich und gut vorzubereiten."
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
        "description": "Herzhaftes Frühstück mit Protein."
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
        "description": "Günstiger Meal-Prep-Klassiker."
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
        "description": "Preiswerte pflanzliche Mahlzeit mit vielen Kohlenhydraten."
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
        "description": "Pflanzliche Alternative mit Reis und Gemüse."
    },
    "Skyr mit Banane und Haferflocken": {
        "category": "Snack",
        "kcal": 330, "protein": 27, "carbs": 48, "fat": 4,
        "ingredients": {
            "Skyr nature": (200, "g"),
            "Banane": (120, "g"),
            "Haferflocken": (30, "g"),
        },
        "description": "Praktischer Snack vor oder nach dem Training."
    },
    "Brot mit Hüttenkäse": {
        "category": "Snack",
        "kcal": 300, "protein": 21, "carbs": 38, "fat": 6,
        "ingredients": {
            "Vollkornbrot": (100, "g"),
            "Hüttenkäse": (100, "g"),
            "Gurke": (80, "g"),
        },
        "description": "Einfacher Snack aus wenigen Zutaten."
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
        "description": "Proteinreiches Abendessen mit Kohlenhydraten."
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
        "description": "Preiswerte, sättigende Mahlzeit."
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
        "description": "Günstiges pflanzliches Gericht mit vielen Kohlenhydraten."
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

def fmt(number):
    return f"{round(number):,}".replace(",", "'")

def recipe_options(category):
    return [
        name for name, recipe in RECIPES.items()
        if recipe["category"] == category
    ]

def sum_recipes(names):
    totals = {
        "kcal": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
    }
    for name in names:
        for key in totals:
            totals[key] += RECIPES[name][key]
    return totals

# =====================================================
# PROFIL
# =====================================================

st.header("👤 Dein Profil")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input(
        "Alter", min_value=16, max_value=100, value=30
    )

with col2:
    weight = st.number_input(
        "Gewicht (kg)", min_value=35.0, max_value=200.0,
        value=62.0, step=0.5
    )

with col3:
    height = st.number_input(
        "Grösse (cm)", min_value=130, max_value=230,
        value=165
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

col4, col5 = st.columns(2)

with col4:
    training_type = st.selectbox(
        "Trainingsart",
        ["Ruhetag", "Krafttraining", "Laufen", "Radfahren",
         "Schwimmen", "Koppeltraining"]
    )

with col5:
    intensity = st.selectbox(
        "Trainingsintensität",
        ["Leicht", "Moderat", "Intensiv"],
        index=1
    )

duration = st.slider(
    "Trainingsdauer (Minuten)",
    min_value=0,
    max_value=240,
    value=60,
    step=15
)

# =====================================================
# KALORIEN UND MAKROS
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
    * 3.5
    * weight / 200
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

c1, c2, c3, c4 = st.columns(4)
c1.metric("Kalorien", f"{fmt(calorie_target)} kcal")
c2.metric("Protein", f"{round(protein_target)} g")
c3.metric("Kohlenhydrate", f"{round(carb_target)} g")
c4.metric("Fett", f"{round(fat_target)} g")

st.caption(
    "Diese Werte sind Schätzungen. Der tatsächliche Bedarf hängt unter "
    "anderem von Trainingsbelastung, Erholung und individuellem Stoffwechsel ab."
)

# =====================================================
# MENÜPLAN MIT AUSTAUSCHBAREN MAHLZEITEN
# =====================================================

st.divider()
st.header("🍽️ Dein Menüplan")
st.write(
    "Wähle für jede Mahlzeit ein Gericht. "
    "Der Menüvergleich und die Einkaufsliste werden automatisch aktualisiert."
)

# Auswahlwerte werden in der Session gespeichert und bleiben
# auch beim Anklicken der Checkboxen erhalten.
for slot_key, default_recipe in DEFAULT_MEALS.items():
    state_key = f"meal_{slot_key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = default_recipe

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

    recipe = RECIPES[selected]

    with st.container(border=True):
        st.subheader(selected)
        st.write(recipe["description"])

        a, b, c, d = st.columns(4)
        a.metric("Kalorien", f'{recipe["kcal"]} kcal')
        b.metric("Protein", f'{recipe["protein"]} g')
        c.metric("Kohlenhydrate", f'{recipe["carbs"]} g')
        d.metric("Fett", f'{recipe["fat"]} g')

selected_names = [
    st.session_state[f"meal_{slot_key}"]
    for _, slot_key in SLOTS
]

totals = sum_recipes(selected_names)

st.divider()
st.header("📊 Dein Menü im Vergleich zum Tagesziel")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Menü-Kalorien",
    f'{fmt(totals["kcal"])} kcal',
    delta=f'{round(totals["kcal"] - calorie_target):+} kcal zum Ziel'
)

m2.metric(
    "Protein",
    f'{totals["protein"]} g',
    delta=f'{round(totals["protein"] - protein_target):+} g'
)

m3.metric(
    "Kohlenhydrate",
    f'{totals["carbs"]} g',
    delta=f'{round(totals["carbs"] - carb_target):+} g'
)

m4.metric(
    "Fett",
    f'{totals["fat"]} g',
    delta=f'{round(totals["fat"] - fat_target):+} g'
)

if totals["kcal"] < calorie_target * 0.85:
    st.warning(
        "Dein Menü liegt deutlich unter dem geschätzten Tagesziel. "
        "Ergänze bei Bedarf weitere Portionen oder Snacks."
    )
elif totals["kcal"] > calorie_target * 1.15:
    st.info(
        "Dein Menü liegt über dem geschätzten Tagesziel. "
        "Du kannst Gerichte austauschen oder Portionen anpassen."
    )
else:
    st.success(
        "Die Kalorien deines Menüs liegen ungefähr in der Nähe "
        "des geschätzten Tagesziels."
    )

st.caption(
    "Die Nährwerte pro Rezept sind hinterlegt und werden beim Austausch "
    "aktualisiert. Portionsgrössen werden noch nicht automatisch angepasst."
)

# =====================================================
# EINKAUFSLISTE
# Zutaten aus den aktuell ausgewählten Gerichten zusammenfassen
# =====================================================

st.divider()
st.header("🛒 Deine Einkaufsliste")

st.write(
    "Die Einkaufsliste passt sich deinen ausgewählten Gerichten an. "
    "Hake ab, was du bereits eingekauft hast."
)

shopping = defaultdict(lambda: {"amount": 0.0, "unit": ""})

for recipe_name in selected_names:
    for ingredient, (amount, unit) in RECIPES[recipe_name]["ingredients"].items():
        shopping[ingredient]["amount"] += amount
        shopping[ingredient]["unit"] = unit

ingredients_sorted = sorted(shopping.keys())

if "shopping_checked" not in st.session_state:
    st.session_state.shopping_checked = {}

checked_count = 0

for ingredient in ingredients_sorted:
    amount = shopping[ingredient]["amount"]
    unit = shopping[ingredient]["unit"]

    if unit == "Stk.":
        quantity = f"{round(amount)} {unit}"
    else:
        quantity = f"{round(amount)} {unit}"

    checkbox_key = f"shopping_{ingredient}"

    if checkbox_key not in st.session_state:
        st.session_state[checkbox_key] = False

    if st.checkbox(
        f"{ingredient} — {quantity}",
        key=checkbox_key
    ):
        checked_count += 1

total_ingredients = len(ingredients_sorted)
progress = checked_count / total_ingredients if total_ingredients else 0

st.progress(progress)
st.caption(
    f"{checked_count} von {total_ingredients} Zutaten erledigt."
)

if st.button("Einkaufsliste zurücksetzen"):
    for ingredient in ingredients_sorted:
        st.session_state[f"shopping_{ingredient}"] = False
    st.rerun()

st.divider()
st.caption(
    "PACE Nutrition ist ein Prototyp und keine medizinische Beratung. "
    "Nährwerte und Energiebedarf sind Näherungswerte und können je nach "
    "Lebensmittel, Marke und Zubereitung abweichen."
)
