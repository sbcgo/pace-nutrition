
import streamlit as st
from itertools import product

st.set_page_config(page_title="PACE Nutrition", page_icon="🥗", layout="wide")
st.title("🥗 PACE Nutrition")
st.caption("Deine Ernährung. Dein Training. Dein Plan.")

# Nährwerte pro 100 g bzw. 100 ml:
# kcal, Protein, Kohlenhydrate, Fett, Kategorie
FOODS = {
    "Haferflocken": (372, 13.5, 58.7, 7, "carb"),
    "Müsli": (370, 10, 64, 7, "carb"),
    "Reis, trocken": (360, 7, 80, 0.8, "carb"),
    "Vollkornpasta, trocken": (350, 13, 65, 2.5, "carb"),
    "Normale Pasta (trocken)": {"kcal": 359, "protein": 12.5, "carbs": 72, "fat": 1.5, "category": "carbs"},
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
    "Laufen": 8.5, "Krafttraining": 4.5, "Radfahren": 7.0,
    "Schwimmen": 6.0, "Tennis": 7.0, "Gehen/Wandern": 3.5,
    "Andere": 5.0,
}
INTENSITY = {"Locker": 0.8, "Mittel": 1.0, "Intensiv": 1.2}

DEFAULTS = {
    "Kohlenhydrate": ["Haferflocken", "Reis, trocken", "Kartoffeln"],
    "Proteinreiche Lebensmittel": ["Pouletbrust", "Eier", "Lachs"],
    "Milchprodukte und Proteinpulver": ["Skyr", "Magerquark"],
    "Früchte": ["Banane", "Beeren"],
    "Gemüse": ["Brokkoli", "Gemüsemix"],
    "Fette und Extras": ["Olivenöl", "Nüsse"],
}


def calculate_nutrition(ingredients):
    result = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for food, grams in ingredients.items():
        kcal, protein, carbs, fat, _ = FOODS[food]
        for key, value in zip(result, (kcal, protein, carbs, fat)):
            result[key] += value * grams / 100
    return result


def generate_recipes(favorites):
    """Erzeugt abwechslungsreiche Rezepte aus den ausgewählten Zutaten."""
    selected = set(favorites)
    recipes = {k: [] for k in ["Frühstück", "Mittagessen", "Snack", "Abendessen"]}
    seen = set()

    def add(category, name, ingredients, instructions, prep=15, tags=None):
        if not set(ingredients).issubset(selected):
            return
        if any(g <= 0 for g in ingredients.values()):
            return
        signature = (category, name, tuple(sorted(ingredients.items())))
        if signature in seen:
            return
        seen.add(signature)
        recipes[category].append({
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "prep": prep,
            "tags": tags or [],
        })

    # Frühstück: warme Porridge-Varianten und kalte Bowls
    for carb in ["Haferflocken", "Müsli"]:
        if carb not in selected:
            continue
        for dairy in ["Skyr", "Magerquark", "Naturjoghurt", "Milch",
                      "Griechischer Joghurt"]:
            if dairy not in selected:
                continue
            for fruit in ["Banane", "Beeren", "Apfel", "Mango", "Kiwi"]:
                if fruit not in selected:
                    continue
                for style in ["Bowl", "Protein-Frühstück"]:
                    ingredients = {carb: 60, dairy: 200, fruit: 100}
                    if "Whey-Protein" in selected and style == "Protein-Frühstück":
                        ingredients["Whey-Protein"] = 15
                    add(
                        "Frühstück",
                        f"{style}: {carb} mit {fruit} und {dairy}",
                        ingredients,
                        [
                            "Alle Zutaten in eine Schüssel geben.",
                            "Bei Bedarf etwas Wasser oder Milch ergänzen.",
                            "Für eine kalte Variante über Nacht im Kühlschrank ziehen lassen.",
                        ],
                        prep=5 if style == "Bowl" else 10,
                        tags=["Schnell", "Proteinreich"],
                    )

    # Herzhaftes Frühstück
    for carb in ["Vollkornbrot", "Wraps"]:
        if carb not in selected:
            continue
        for protein in ["Eier", "Thunfisch, abgetropft", "Tofu", "Hüttenkäse"]:
            if protein not in selected:
                continue
            for veg in ["Tomaten", "Spinat", "Gurken"]:
                if veg not in selected:
                    continue
                add(
                    "Frühstück",
                    f"Herzhaftes {carb} mit {protein} und {veg}",
                    {carb: 90, protein: 100, veg: 80},
                    [
                        "Gemüse waschen und klein schneiden.",
                        "Eier oder Tofu bei Bedarf in einer beschichteten Pfanne garen.",
                        "Mit dem Brot oder Wrap servieren und das Gemüse ergänzen.",
                    ],
                    prep=12,
                    tags=["Herzhaft"],
                )

    # Snacks: Kombinationen mit sinnvoller Portionsgrösse
    for dairy in ["Skyr", "Magerquark", "Hüttenkäse", "Naturjoghurt"]:
        if dairy not in selected:
            continue
        for fruit in ["Banane", "Beeren", "Apfel", "Kiwi", "Orange"]:
            if fruit not in selected:
                continue
            add(
                "Snack", f"{dairy} mit {fruit}",
                {dairy: 200, fruit: 120},
                ["Frucht waschen und schneiden.", "Mit dem Milchprodukt vermischen."],
                prep=3, tags=["Schnell", "Proteinreich"],
            )
        for extra in ["Nüsse", "Chiasamen", "Erdnussbutter"]:
            if extra not in selected:
                continue
            add(
                "Snack", f"{dairy} mit {extra}",
                {dairy: 200, extra: 15},
                ["Zutaten in einer Schüssel vermischen.", "Nach Wunsch mit Zimt würzen."],
                prep=3, tags=["Schnell"],
            )

    for fruit in ["Banane", "Apfel", "Birne", "Orange"]:
        if fruit in selected and "Nüsse" in selected:
            add(
                "Snack", f"{fruit} mit Nüssen",
                {fruit: 150, "Nüsse": 15},
                ["Frucht waschen und schneiden.", "Zusammen mit den Nüssen essen."],
                prep=2, tags=["Ohne Kochen"],
            )

    if {"Vollkornbrot", "Hüttenkäse"}.issubset(selected):
        for veg in ["Tomaten", "Gurken"]:
            ingredients = {"Vollkornbrot": 80, "Hüttenkäse": 120}
            if veg in selected:
                ingredients[veg] = 80
            add(
                "Snack", f"Vollkornbrot mit Hüttenkäse"
                + (f" und {veg}" if veg in selected else ""),
                ingredients,
                ["Hüttenkäse auf dem Brot verteilen.",
                 "Optional Gemüse schneiden und dazu servieren."],
                prep=5, tags=["Schnell", "Proteinreich"],
            )

    # Hauptgerichte: kuratierte Zutaten-Kombinationen
    carb_options = {
        "Reis, trocken": 80,
        "Vollkornpasta, trocken": 80,
        "Couscous, trocken": 80,
        "Quinoa, trocken": 80,
        "Kartoffeln": 250,
        "Süsskartoffeln": 250,
    }
    protein_options = [
        "Pouletbrust", "Truthahn", "Rindfleisch, mager",
        "Hackfleisch, mager", "Lachs", "Thunfisch, abgetropft",
        "Tofu", "Tempeh", "Linsen, gekocht",
        "Kichererbsen, gekocht", "Kidneybohnen, gekocht",
    ]
    veg_options = [
        "Brokkoli", "Spinat", "Zucchetti", "Tomaten",
        "Peperoni", "Karotten", "Champignons", "Gemüsemix",
    ]

    for carb, protein, veg in product(carb_options, protein_options, veg_options):
        ingredients = {}
        if carb not in selected or protein not in selected or veg not in selected:
            continue
        ingredients[carb] = carb_options[carb]
        ingredients[protein] = 150
        ingredients[veg] = 200
        if "Olivenöl" in selected and protein != "Lachs":
            ingredients["Olivenöl"] = 5

        # Name und Zubereitung hängen von der gewählten Basis ab.
        name = f"{protein} mit {carb.replace(', trocken', '')} und {veg}"
        instructions = [
            f"{carb.replace(', trocken', '')} gemäss Packungsanweisung kochen "
            "oder Kartoffeln in Stücke schneiden und garen.",
            f"{protein} passend zubereiten: Fleisch vollständig durchgaren, "
            "Lachs garen oder pflanzliche Proteinquelle erhitzen.",
            f"{veg} waschen, schneiden und dünsten oder in der Pfanne garen.",
            "Alles zusammen anrichten und nach Wunsch würzen.",
        ]
        add("Mittagessen", name, ingredients, instructions, prep=25,
            tags=["Hauptgericht", "Meal Prep"])
        add("Abendessen", name, ingredients, instructions, prep=25,
            tags=["Hauptgericht", "Meal Prep"])

    # Weitere Hauptgerichte ohne Gemüse, falls keine Gemüseauswahl getroffen wurde
    for carb, protein in product(carb_options, protein_options):
        if carb not in selected or protein not in selected:
            continue
        ingredients = {carb: carb_options[carb], protein: 150}
        if "Olivenöl" in selected and protein != "Lachs":
            ingredients["Olivenöl"] = 5
        name = f"{protein} mit {carb.replace(', trocken', '')}"
        instructions = [
            f"{carb.replace(', trocken', '')} gemäss Packungsanweisung zubereiten.",
            f"{protein} passend zubereiten und vollständig durchgaren, falls erforderlich.",
            "Zusammen anrichten und nach Geschmack würzen.",
        ]
        add("Mittagessen", name, ingredients, instructions, prep=20,
            tags=["Einfach"])
        add("Abendessen", name, ingredients, instructions, prep=20,
            tags=["Einfach"])

    # Linsen- und Bohnen-Bowls: Hülsenfrüchte mit Gemüse
    for legume in ["Linsen, gekocht", "Kichererbsen, gekocht", "Kidneybohnen, gekocht"]:
        if legume not in selected:
            continue
        for veg in ["Tomaten", "Spinat", "Peperoni", "Gemüsemix"]:
            if veg not in selected:
                continue
            ingredients = {legume: 180, veg: 200}
            if "Quinoa, trocken" in selected:
                ingredients["Quinoa, trocken"] = 60
            if "Olivenöl" in selected:
                ingredients["Olivenöl"] = 5
            add(
                "Mittagessen", f"{legume} mit {veg} als Bowl",
                ingredients,
                ["Gemüse schneiden und in einer Pfanne dünsten.",
                 "Hülsenfrüchte abspülen, hinzufügen und erhitzen.",
                 "Optional Quinoa kochen und zusammen servieren."],
                prep=20, tags=["Pflanzlich", "Meal Prep"],
            )
            add(
                "Abendessen", f"{legume} mit {veg} als Bowl",
                ingredients,
                ["Gemüse schneiden und in einer Pfanne dünsten.",
                 "Hülsenfrüchte abspülen, hinzufügen und erhitzen.",
                 "Optional Quinoa kochen und zusammen servieren."],
                prep=20, tags=["Pflanzlich", "Meal Prep"],
            )

    # Begrenzte, sortierte Vorschläge verhindern endlose Auswahllisten.
    for category in recipes:
        recipes[category].sort(key=lambda r: (
            0 if "Proteinreich" in r["tags"] else 1,
            r["prep"],
            r["name"],
        ))
        recipes[category] = recipes[category][:100]

    return recipes


def scale_ingredients(ingredients, factor):
    return {food: grams * factor for food, grams in ingredients.items()}


# 1. Profil
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

# 2. Training
st.header("2. Dein Training")
st.write("Füge alle Trainingseinheiten für deinen geplanten Tag hinzu.")

if "sessions" not in st.session_state:
    st.session_state.sessions = []

with st.form("add_session", clear_on_submit=True):
    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        sport = st.selectbox("Sportart", list(SPORTS.keys()))
    with tc2:
        duration = st.number_input(
            "Dauer (Minuten)", min_value=5, max_value=600, value=45, step=5
        )
    with tc3:
        intensity = st.selectbox("Intensität", list(INTENSITY.keys()))
    add_session = st.form_submit_button("➕ Trainingseinheit hinzufügen")

if add_session:
    st.session_state.sessions.append({
        "sport": sport, "duration": duration, "intensity": intensity
    })

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

if not st.session_state.sessions:
    st.info("Noch keine Trainingseinheiten hinzugefügt.")

training_calories = sum(
    max(0, (SPORTS[s["sport"]] * INTENSITY[s["intensity"]] - 1)
        * 3.5 * weight / 200) * s["duration"]
    for s in st.session_state.sessions
)

goal_factor = {
    "Leistung erhalten": 1.0, "Muskelaufbau": 1.08, "Fettverlust": 0.90
}[goal]
target_calories = max(1200, (base_calories + training_calories) * goal_factor)
target_protein = weight * 1.8
target_fat = weight * 0.9
target_carbs = max(
    0, (target_calories - target_protein * 4 - target_fat * 9) / 4
)

st.subheader("Geschätzte Tagesziele")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Kalorien", f"{target_calories:.0f} kcal")
m2.metric("Protein", f"{target_protein:.0f} g")
m3.metric("Kohlenhydrate", f"{target_carbs:.0f} g")
m4.metric("Fett", f"{target_fat:.0f} g")
st.caption(
    "Schätzwerte: tatsächlicher Bedarf hängt unter anderem von Alltag, "
    "Trainingsbelastung und individueller Physiologie ab."
)

# 3. Lebensmittel wählen
st.header("3. Deine Lieblingslebensmittel")
st.write("Je mehr passende Zutaten du auswählst, desto mehr Rezepte sind möglich.")

favorites = []
food_columns = st.columns(2)
for i, (group, foods) in enumerate(FOOD_GROUPS.items()):
    with food_columns[i % 2]:
        selected = st.multiselect(
            group,
            foods,
            default=[f for f in DEFAULTS[group] if f in foods],
            key=f"food_{group}",
        )
        favorites.extend(selected)

if st.button("✨ Neue Menüs generieren", type="primary"):
    if not favorites:
        st.warning("Bitte wähle zuerst Lebensmittel aus.")
    else:
        st.session_state.generated_recipes = generate_recipes(favorites)
        st.session_state.generated_favorites = favorites.copy()
        st.session_state.chosen_recipe = {}
        st.rerun()

# 4. Rezepte auswählen und Portionen einstellen
if "generated_recipes" in st.session_state:
    if st.session_state.generated_favorites != favorites:
        st.info(
            "Deine Favoriten haben sich geändert. Klicke auf "
            "«Neue Menüs generieren», um die Rezepte zu aktualisieren."
        )

    recipes = st.session_state.generated_recipes
    st.header("4. Deine persönlichen Menüs")
    st.write(
        "Wähle für jede Mahlzeit ein Rezept. Du kannst die Portionsgrösse "
        "direkt anpassen."
    )

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
            st.warning(
                f"Keine passenden Vorschläge für {category}. "
                "Wähle weitere Lebensmittel aus und generiere erneut."
            )
            continue

        labels = []
        for r in options:
            n = calculate_nutrition(r["ingredients"])
            labels.append(
                f"{r['name']} · {n['kcal']:.0f} kcal · "
                f"{n['protein']:.0f} g Protein"
            )

        index_key = f"meal_{category}"
        previous = st.session_state.chosen_recipe.get(category, 0)
        previous = min(previous, len(options) - 1)

        chosen_index = st.selectbox(
            f"Rezept für {category}",
            options=list(range(len(options))),
            index=previous,
            format_func=lambda i, labels=labels: labels[i],
            key=index_key,
        )
        st.session_state.chosen_recipe[category] = chosen_index

        recipe = options[chosen_index]
        base = calculate_nutrition(recipe["ingredients"])
        default_factor = max(
            0.5, min(2.5, target_calories * share / max(base["kcal"], 1))
        )
        factor = st.slider(
            f"Portionsgrösse – {category}",
            min_value=0.5,
            max_value=2.5,
            value=round(default_factor, 2),
            step=0.05,
            key=f"portion_{category}",
        )

        scaled = scale_ingredients(recipe["ingredients"], factor)
        macros = calculate_nutrition(scaled)

        with st.expander("Zubereitung und Zutaten", expanded=True):
            st.write(f"**Zubereitungszeit:** ca. {recipe['prep']} Minuten")
            if recipe["tags"]:
                st.caption(" · ".join(recipe["tags"]))
            st.write("**Zutaten für diese Portion**")
            for food, grams in scaled.items():
                st.write(f"- {food}: {grams:.0f} g")
            st.write("**Zubereitung**")
            for step, instruction in enumerate(recipe["instructions"], 1):
                st.write(f"{step}. {instruction}")

        n1, n2, n3, n4 = st.columns(4)
        n1.metric("Kalorien", f"{macros['kcal']:.0f} kcal")
        n2.metric("Protein", f"{macros['protein']:.1f} g")
        n3.metric("Kohlenhydrate", f"{macros['carbs']:.1f} g")
        n4.metric("Fett", f"{macros['fat']:.1f} g")

        for macro in total:
            total[macro] += macros[macro]
        for food, grams in scaled.items():
            shopping[food] = shopping.get(food, 0) + grams

    # 5. Tagesbilanz
    st.header("5. Tagesbilanz")
    a, b, c, d = st.columns(4)
    a.metric(
        "Kalorien", f"{total['kcal']:.0f} kcal",
        f"{total['kcal'] - target_calories:+.0f} kcal"
    )
    b.metric(
        "Protein", f"{total['protein']:.0f} g",
        f"{total['protein'] - target_protein:+.0f} g"
    )
    c.metric(
        "Kohlenhydrate", f"{total['carbs']:.0f} g",
        f"{total['carbs'] - target_carbs:+.0f} g"
    )
    d.metric(
        "Fett", f"{total['fat']:.0f} g",
        f"{total['fat'] - target_fat:+.0f} g"
    )

    st.caption(
        "Die Tagesbilanz zeigt die ausgewählten Rezepte. "
        "Sie optimiert die Makros noch nicht automatisch."
    )

    # 6. Einkaufsliste
    st.header("6. Einkaufsliste")
    for food, grams in sorted(shopping.items()):
        st.write(f"- {food}: {grams:.0f} g")

    shopping_text = (
        "PACE Nutrition – Einkaufsliste\n\n"
        + "\n".join(
            f"- {food}: {grams:.0f} g"
            for food, grams in sorted(shopping.items())
        )
    )
    st.download_button(
        "📥 Einkaufsliste herunterladen",
        data=shopping_text,
        file_name="pace_einkaufsliste.txt",
        mime="text/plain",
    )

st.divider()
st.caption(
    "Nährwerte sind Richtwerte und können je nach Marke und Zubereitung "
    "abweichen. Bitte Mengen und Garzeiten an die verwendeten Lebensmittel "
    "anpassen. PACE Nutrition liefert Orientierung, keine medizinische Beratung."
)
