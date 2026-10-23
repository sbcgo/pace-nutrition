
import streamlit as st

st.set_page_config(page_title="PACE Nutrition", page_icon="🥗", layout="wide")
st.title("🥗 PACE Nutrition")
st.caption("Ernährung, die zu deinen Lieblingslebensmitteln und deinem Training passt.")

# Nährwerte pro 100 g bzw. 100 ml:
# kcal, Protein, Kohlenhydrate, Fett, Kategorie
FOODS = {
    "Haferflocken": (372, 13.5, 58.7, 7, "carb"),
    "Müsli": (370, 10, 64, 7, "carb"),
    "Reis, trocken": (360, 7, 80, 0.8, "carb"),
    "Vollkornpasta, trocken": (350, 13, 65, 2.5, "carb"),
    "Couscous, trocken": (376, 12.8, 77, 0.6, "carb"),
    "Quinoa, trocken": (368, 14, 64, 6, "carb"),
    "Kartoffeln": (77, 2, 17, 0.1, "carb"),
    "Süsskartoffeln": (86, 1.6, 20, 0.1, "carb"),
    "Vollkornbrot": (240, 9, 41, 3.5, "carb"),
    "Wraps": (310, 9, 52, 8, "carb"),
    "Reiswaffeln": (387, 8, 81, 3, "carb"),

    "Pouletbrust": (120, 23, 0, 2.5, "protein"),
    "Truthahn": (114, 24, 0, 1.5, "protein"),
    "Rindfleisch, mager": (150, 21, 0, 7, "protein"),
    "Hackfleisch, mager": (170, 21, 0, 9, "protein"),
    "Lachs": (208, 20, 0, 13, "protein"),
    "Thunfisch, abgetropft": (116, 26, 0, 1, "protein"),
    "Eier": (143, 12.6, 0.7, 9.5, "protein"),
    "Tofu": (145, 16, 2, 9, "protein"),
    "Tempeh": (193, 20, 8, 11, "protein"),
    "Linsen, gekocht": (116, 9, 20, 0.4, "protein"),
    "Kichererbsen, gekocht": (164, 8.9, 27.4, 2.6, "protein"),
    "Kidneybohnen, gekocht": (127, 8.7, 22.8, 0.5, "protein"),

    "Skyr": (63, 11, 4, 0.2, "dairy"),
    "Magerquark": (67, 12, 4, 0.2, "dairy"),
    "Hüttenkäse": (98, 12.5, 3, 4.3, "dairy"),
    "Griechischer Joghurt": (120, 6, 4, 10, "dairy"),
    "Naturjoghurt": (63, 3.5, 4.7, 3.3, "dairy"),
    "Milch": (47, 3.4, 4.8, 1.5, "dairy"),
    "Käse": (350, 25, 1, 27, "dairy"),
    "Parmesan": (402, 32, 0, 30, "dairy"),
    "Whey-Protein": (390, 78, 7, 6, "dairy"),

    "Banane": (89, 1.1, 22.8, 0.3, "fruit"),
    "Apfel": (52, 0.3, 14, 0.2, "fruit"),
    "Beeren": (50, 1, 8, 0.5, "fruit"),
    "Orange": (47, 0.9, 12, 0.1, "fruit"),
    "Birne": (57, 0.4, 15, 0.1, "fruit"),
    "Kiwi": (61, 1.1, 15, 0.5, "fruit"),
    "Mango": (60, 0.8, 15, 0.4, "fruit"),

    "Brokkoli": (34, 2.8, 7, 0.4, "veg"),
    "Spinat": (23, 2.9, 3.6, 0.4, "veg"),
    "Zucchetti": (17, 1.2, 3.1, 0.3, "veg"),
    "Tomaten": (18, 0.9, 3.9, 0.2, "veg"),
    "Peperoni": (31, 1, 6, 0.3, "veg"),
    "Karotten": (41, 0.9, 10, 0.2, "veg"),
    "Gurken": (15, 0.7, 3.6, 0.1, "veg"),
    "Champignons": (22, 3.1, 3.3, 0.3, "veg"),
    "Gemüsemix": (35, 2, 5, 0.5, "veg"),
    "Salat": (15, 1.4, 2.9, 0.2, "veg"),

    "Avocado": (160, 2, 8.5, 14.7, "fat"),
    "Olivenöl": (884, 0, 0, 100, "fat"),
    "Nüsse": (607, 20, 21, 54, "fat"),
    "Erdnussbutter": (588, 25, 20, 50, "fat"),
    "Chiasamen": (486, 17, 42, 31, "fat"),
}

FOOD_GROUPS = {
    "Kohlenhydrate": [f for f, v in FOODS.items() if v[4] == "carb"],
    "Proteinreiche Lebensmittel": [f for f, v in FOODS.items() if v[4] == "protein"],
    "Milchprodukte und Proteinpulver": [f for f, v in FOODS.items() if v[4] == "dairy"],
    "Früchte": [f for f, v in FOODS.items() if v[4] == "fruit"],
    "Gemüse": [f for f, v in FOODS.items() if v[4] == "veg"],
    "Fette und Extras": [f for f, v in FOODS.items() if v[4] == "fat"],
}

SPORTS = {
    "Laufen": 8.5,
    "Krafttraining": 4.5,
    "Radfahren": 7.0,
    "Schwimmen": 6.0,
    "Tennis": 7.0,
    "Gehen/Wandern": 3.5,
    "Andere": 5.0,
}
INTENSITY = {"Locker": 0.8, "Mittel": 1.0, "Intensiv": 1.2}


def calculate_nutrition(ingredients):
    result = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for food, grams in ingredients.items():
        kcal, protein, carbs, fat, _ = FOODS[food]
        for key, value in zip(result, (kcal, protein, carbs, fat)):
            result[key] += value * grams / 100
    return result


def generate_recipes(favorites):
    """Erstellt einfache, regelbasierte Gerichte aus ausgewählten Favoriten."""
    groups = {
        group: [f for f in favorites if FOODS[f][4] == group]
        for group in ["carb", "protein", "dairy", "fruit", "veg", "fat"]
    }
    recipes = {"Frühstück": [], "Mittagessen": [], "Snack": [], "Abendessen": []}

    def add(category, name, ingredients):
        if ingredients and all(f in favorites for f in ingredients):
            recipes[category].append({"name": name, "ingredients": ingredients})

    # Frühstück und Snacks
    for carb in groups["carb"]:
        if carb in ["Haferflocken", "Müsli"]:
            for dairy in groups["dairy"]:
                for fruit in groups["fruit"] or [None]:
                    ingredients = {carb: 60, dairy: 200}
                    if fruit:
                        ingredients[fruit] = 100
                    add("Frühstück", f"{carb} mit {dairy}" + (f" und {fruit}" if fruit else ""), ingredients)

        if carb in ["Vollkornbrot", "Wraps"]:
            for protein in groups["protein"]:
                if protein in ["Eier", "Thunfisch, abgetropft", "Tofu"]:
                    add("Frühstück", f"{carb} mit {protein}", {carb: 90, protein: 100})

    for dairy in groups["dairy"]:
        for fruit in groups["fruit"]:
            add("Snack", f"{dairy} mit {fruit}", {dairy: 200, fruit: 120})
        for extra in groups["fat"]:
            if extra in ["Nüsse", "Chiasamen", "Erdnussbutter"]:
                add("Snack", f"{dairy} mit {extra}", {dairy: 200, extra: 15})

    for fruit in groups["fruit"]:
        if "Nüsse" in favorites:
            add("Snack", f"{fruit} mit Nüssen", {fruit: 150, "Nüsse": 15})

    if "Vollkornbrot" in favorites and "Hüttenkäse" in favorites:
        add("Snack", "Vollkornbrot mit Hüttenkäse", {"Vollkornbrot": 80, "Hüttenkäse": 120})

    # Mittag- und Abendessen: Kohlenhydratquelle + Proteinquelle + Gemüse
    for carb in groups["carb"]:
        carb_amount = 80 if "trocken" in carb else 250
        for protein in groups["protein"]:
            for veg in groups["veg"]:
                ingredients = {carb: carb_amount, protein: 150, veg: 200}
                if "Olivenöl" in favorites and protein != "Lachs":
                    ingredients["Olivenöl"] = 5
                name = f"{protein} mit {carb} und {veg}"
                add("Mittagessen", name, ingredients)
                add("Abendessen", name, ingredients)

    # Einfache Varianten für Mahlzeiten ohne Gemüseauswahl
    for carb in groups["carb"]:
        for protein in groups["protein"]:
            ingredients = {carb: 80 if "trocken" in carb else 250, protein: 150}
            name = f"{protein} mit {carb}"
            add("Mittagessen", name, ingredients)
            add("Abendessen", name, ingredients)

    # Duplikate vermeiden
    for category in recipes:
        unique = {}
        for recipe in recipes[category]:
            signature = (recipe["name"], tuple(sorted(recipe["ingredients"].items())))
            unique[signature] = recipe
        recipes[category] = list(unique.values())

    return recipes


st.header("1. Dein Profil")
c1, c2, c3 = st.columns(3)
with c1:
    age = st.number_input("Alter", 16, 100, 30)
    weight = st.number_input("Gewicht (kg)", 35.0, 250.0, 62.0, step=0.5)
with c2:
    height = st.number_input("Grösse (cm)", 130, 230, 165)
    sex = st.selectbox("Berechnungsgrundlage", ["Männlich", "Weiblich", "Andere"])
with c3:
    goal = st.selectbox("Ziel", ["Leistung erhalten", "Muskelaufbau", "Fettverlust"])
    activity = st.selectbox("Alltag", ["Sitzend", "Leicht aktiv", "Aktiv"])

bmr_base = 10 * weight + 6.25 * height - 5 * age
bmr = bmr_base + (5 if sex == "Männlich" else -161 if sex == "Weiblich" else -78)
activity_factor = {"Sitzend": 1.2, "Leicht aktiv": 1.3, "Aktiv": 1.4}[activity]
base_calories = bmr * activity_factor

st.header("2. Dein Training")
st.write("Du kannst beliebig viele Einheiten hinzufügen. Alle Einheiten werden zusammengerechnet.")

if "sessions" not in st.session_state:
    st.session_state.sessions = []

with st.form("add_session", clear_on_submit=True):
    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        sport = st.selectbox("Sportart", list(SPORTS.keys()))
    with tc2:
        duration = st.number_input("Dauer (Minuten)", min_value=5, max_value=600, value=45, step=5)
    with tc3:
        intensity = st.selectbox("Intensität", list(INTENSITY.keys()))
    add_session = st.form_submit_button("➕ Trainingseinheit hinzufügen")

if add_session:
    st.session_state.sessions.append({
        "sport": sport, "duration": duration, "intensity": intensity
    })

if st.session_state.sessions:
    for i, session in enumerate(st.session_state.sessions):
        col_text, col_remove = st.columns([5, 1])
        with col_text:
            st.write(
                f"**Einheit {i + 1}:** {session['sport']} · "
                f"{session['duration']} Min. · {session['intensity']}"
            )
        with col_remove:
            if st.button("Entfernen", key=f"remove_{i}"):
                st.session_state.sessions.pop(i)
                st.rerun()
else:
    st.info("Noch keine Trainingseinheiten hinzugefügt.")

training_calories = 0.0
for session in st.session_state.sessions:
    met = SPORTS[session["sport"]] * INTENSITY[session["intensity"]]
    training_calories += max(0, (met - 1) * 3.5 * weight / 200) * session["duration"]

goal_factor = {"Leistung erhalten": 1.0, "Muskelaufbau": 1.08, "Fettverlust": 0.90}[goal]
target_calories = max(1200, (base_calories + training_calories) * goal_factor)
target_protein = weight * 1.8
target_fat = weight * 0.9
target_carbs = max(0, (target_calories - target_protein * 4 - target_fat * 9) / 4)

st.subheader("Geschätzte Tagesziele")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Kalorien", f"{target_calories:.0f} kcal")
m2.metric("Protein", f"{target_protein:.0f} g")
m3.metric("Kohlenhydrate", f"{target_carbs:.0f} g")
m4.metric("Fett", f"{target_fat:.0f} g")
st.caption("Trainingsverbrauch und Tagesbedarf sind Schätzungen, keine exakten Messwerte.")

st.header("3. Deine Lieblingslebensmittel")
st.write("Wähle mehrere Zutaten aus. PACE verwendet diese Auswahl zur Menügenerierung.")

favorites = []
food_columns = st.columns(2)
for i, (group, foods) in enumerate(FOOD_GROUPS.items()):
    with food_columns[i % 2]:
        defaults = {
            "Kohlenhydrate": ["Haferflocken", "Reis, trocken", "Kartoffeln"],
            "Proteinreiche Lebensmittel": ["Pouletbrust", "Eier", "Lachs"],
            "Milchprodukte und Proteinpulver": ["Skyr", "Magerquark"],
            "Früchte": ["Banane", "Beeren"],
            "Gemüse": ["Brokkoli", "Gemüsemix"],
            "Fette und Extras": ["Olivenöl", "Nüsse"],
        }
        selected = st.multiselect(
            group,
            foods,
            default=[f for f in defaults[group] if f in foods],
            key=f"food_{group}",
        )
        favorites.extend(selected)

if st.button("✨ Menüs aus meinen Lebensmitteln generieren", type="primary"):
    if not favorites:
        st.warning("Bitte wähle zuerst Lebensmittel aus.")
    else:
        st.session_state.generated_recipes = generate_recipes(favorites)
        st.session_state.generated_favorites = favorites.copy()
        st.session_state.chosen_recipe = {}
        st.rerun()

if "generated_recipes" in st.session_state:
    if st.session_state.generated_favorites != favorites:
        st.info("Du hast deine Favoriten verändert. Generiere die Menüs erneut, um die Änderungen zu übernehmen.")

    recipes = st.session_state.generated_recipes
    st.header("4. Deine persönlichen Menüs")

    meal_shares = {
        "Frühstück": 0.25,
        "Mittagessen": 0.30,
        "Snack": 0.15,
        "Abendessen": 0.30,
    }
    total = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    shopping = {}

    for category, share in meal_shares.items():
        options = recipes[category]
        st.subheader(category)

        if not options:
            st.warning(f"Keine passenden Vorschläge für {category}. Wähle weitere Lebensmittel aus und generiere die Menüs erneut.")
            continue

        labels = [
            f"{r['name']} – {calculate_nutrition(r['ingredients'])['kcal']:.0f} kcal pro Grundportion"
            for r in options
        ]
        previous = st.session_state.chosen_recipe.get(category, 0)
        previous = min(previous, len(options) - 1)

        chosen_index = st.selectbox(
            f"Menü für {category}",
            options=list(range(len(options))),
            index=previous,
            format_func=lambda i, labels=labels: labels[i],
            key=f"meal_{category}",
        )
        st.session_state.chosen_recipe[category] = chosen_index

        recipe = options[chosen_index]
        base = calculate_nutrition(recipe["ingredients"])
        portion = max(0.5, min(2.5, target_calories * share / max(base["kcal"], 1)))
        scaled = {food: grams * portion for food, grams in recipe["ingredients"].items()}
        macros = calculate_nutrition(scaled)

        st.write(f"**Portion:** {portion:.2f} × Grundportion")
        st.write(
            f"{macros['kcal']:.0f} kcal · Protein {macros['protein']:.1f} g · "
            f"Kohlenhydrate {macros['carbs']:.1f} g · Fett {macros['fat']:.1f} g"
        )
        st.caption("Zutaten: " + ", ".join(f"{f} {g:.0f} g" for f, g in scaled.items()))

        for macro in total:
            total[macro] += macros[macro]
        for food, grams in scaled.items():
            shopping[food] = shopping.get(food, 0) + grams

    st.header("5. Tagesbilanz")
    a, b, c, d = st.columns(4)
    a.metric("Kalorien", f"{total['kcal']:.0f} kcal", f"{total['kcal'] - target_calories:+.0f}")
    b.metric("Protein", f"{total['protein']:.0f} g", f"{total['protein'] - target_protein:+.0f}")
    c.metric("Kohlenhydrate", f"{total['carbs']:.0f} g", f"{total['carbs'] - target_carbs:+.0f}")
    d.metric("Fett", f"{total['fat']:.0f} g", f"{total['fat'] - target_fat:+.0f}")

    st.header("6. Einkaufsliste")
    for food, grams in sorted(shopping.items()):
        st.write(f"- {food}: {grams:.0f} g")

    shopping_text = "PACE Nutrition – Einkaufsliste\n\n" + "\n".join(
        f"- {food}: {grams:.0f} g" for food, grams in sorted(shopping.items())
    )
    st.download_button(
        "📥 Einkaufsliste herunterladen",
        data=shopping_text,
        file_name="pace_einkaufsliste.txt",
        mime="text/plain",
    )

st.divider()
st.caption(
    "Die Lebensmittelwerte sind Richtwerte. Die Menügenerierung verwendet einfache "
    "Kombinationsregeln; Portionsgrössen werden hier primär nach Kalorienanteilen geschätzt."
)
