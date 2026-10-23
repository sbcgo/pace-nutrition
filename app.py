
import itertools
import streamlit as st

st.set_page_config(page_title="PACE Nutrition", page_icon="🥗", layout="wide")

st.title("🥗 PACE Nutrition")
st.caption("Deine Lebensmittel. Deine Menüs. Dein Trainingsziel.")

# Nährwerte je 100 g, ungefähr
FOODS = {
    "Haferflocken": (372, 13.5, 58.7, 7.0, "carb"),
    "Reis (trocken)": (360, 7, 80, 0.8, "carb"),
    "Vollkornpasta (trocken)": (350, 13, 65, 2.5, "carb"),
    "Kartoffeln": (77, 2, 17, 0.1, "carb"),
    "Vollkornbrot": (240, 9, 41, 3.5, "carb"),
    "Banane": (89, 1.1, 22.8, 0.3, "fruit"),
    "Apfel": (52, 0.3, 14, 0.2, "fruit"),
    "Beeren": (50, 1, 8, 0.5, "fruit"),
    "Gemüse": (35, 2, 5, 0.5, "veg"),
    "Brokkoli": (34, 2.8, 7, 0.4, "veg"),
    "Pouletbrust": (120, 23, 0, 2.5, "protein"),
    "Lachs": (208, 20, 0, 13, "protein"),
    "Tofu": (145, 16, 2, 9, "protein"),
    "Eier": (143, 12.6, 0.7, 9.5, "protein"),
    "Skyr": (63, 11, 4, 0.2, "dairy"),
    "Magerquark": (67, 12, 4, 0.2, "dairy"),
    "Hüttenkäse": (98, 12.5, 3, 4.3, "dairy"),
    "Linsen (gekocht)": (116, 9, 20, 0.4, "protein"),
    "Kichererbsen (gekocht)": (164, 8.9, 27.4, 2.6, "protein"),
    "Olivenöl": (884, 0, 0, 100, "fat"),
    "Nüsse": (607, 20, 21, 54, "fat"),
    "Milch": (47, 3.4, 4.8, 1.5, "dairy"),
}

GROUPS = {
    "Kohlenhydrate": ["Haferflocken", "Reis (trocken)", "Vollkornpasta (trocken)", "Kartoffeln", "Vollkornbrot"],
    "Proteinreiche Lebensmittel": ["Pouletbrust", "Lachs", "Tofu", "Eier", "Linsen (gekocht)", "Kichererbsen (gekocht)"],
    "Milchprodukte": ["Skyr", "Magerquark", "Hüttenkäse", "Milch"],
    "Früchte": ["Banane", "Apfel", "Beeren"],
    "Gemüse": ["Gemüse", "Brokkoli"],
    "Fette": ["Olivenöl", "Nüsse"],
}

def nutrition(ingredients):
    result = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for food, grams in ingredients.items():
        kcal, protein, carbs, fat, _ = FOODS[food]
        result["kcal"] += kcal * grams / 100
        result["protein"] += protein * grams / 100
        result["carbs"] += carbs * grams / 100
        result["fat"] += fat * grams / 100
    return result

def make_recipe(name, category, ingredients):
    return {"name": name, "category": category, "ingredients": ingredients}

def generate_recipes(favorites):
    """Erzeugt sinnvolle Rezeptvorschläge aus ausgewählten Lebensmitteln."""
    recipes = {"Frühstück": [], "Mittagessen": [], "Snack": [], "Abendessen": []}

    carbs = [f for f in favorites if FOODS[f][4] == "carb"]
    proteins = [f for f in favorites if FOODS[f][4] == "protein"]
    dairy = [f for f in favorites if FOODS[f][4] == "dairy"]
    fruits = [f for f in favorites if FOODS[f][4] == "fruit"]
    vegetables = [f for f in favorites if FOODS[f][4] == "veg"]
    fats = [f for f in favorites if FOODS[f][4] == "fat"]

    # Frühstück: Haferflocken oder Brot, kombiniert mit Milchprodukt,
    # Früchten oder Eiern, falls ausgewählt.
    for carb in carbs:
        for dairy_food in dairy:
            if carb == "Haferflocken":
                for fruit in fruits or [None]:
                    ingredients = {carb: 60, dairy_food: 200}
                    if fruit:
                        ingredients[fruit] = 100
                    recipes["Frühstück"].append(
                        make_recipe(
                            f"Porridge mit {dairy_food}" + (f" und {fruit}" if fruit else ""),
                            "Frühstück", ingredients
                        )
                    )
            elif carb == "Vollkornbrot":
                recipes["Frühstück"].append(
                    make_recipe(
                        f"Brot mit {dairy_food}", "Frühstück",
                        {carb: 100, dairy_food: 150}
                    )
                )

    if "Eier" in favorites and "Vollkornbrot" in favorites:
        recipes["Frühstück"].append(
            make_recipe("Eier mit Vollkornbrot", "Frühstück",
                        {"Eier": 100, "Vollkornbrot": 100})
        )

    # Hauptgerichte: Kohlenhydratquelle + Protein + Gemüse, wenn verfügbar.
    for carb in carbs:
        for protein in proteins:
            for veg in vegetables or [None]:
                ingredients = {carb: 80 if "Reis" in carb or "Pasta" in carb else 250,
                               protein: 150}
                if veg:
                    ingredients[veg] = 200
                if fats and protein not in ["Lachs"]:
                    ingredients[fats[0]] = 5
                dish_name = f"{protein} mit {carb}"
                if veg:
                    dish_name += f" und {veg}"
                for category in ["Mittagessen", "Abendessen"]:
                    recipes[category].append(
                        make_recipe(dish_name, category, ingredients.copy())
                    )

    # Snacks aus den gewählten Zutaten.
    for dairy_food in dairy:
        for fruit in fruits:
            recipes["Snack"].append(
                make_recipe(
                    f"{dairy_food} mit {fruit}", "Snack",
                    {dairy_food: 200, fruit: 120}
                )
            )
    if "Vollkornbrot" in favorites and "Hüttenkäse" in favorites:
        recipes["Snack"].append(
            make_recipe("Vollkornbrot mit Hüttenkäse", "Snack",
                        {"Vollkornbrot": 80, "Hüttenkäse": 120})
        )
    if "Nüsse" in favorites and fruits:
        for fruit in fruits:
            recipes["Snack"].append(
                make_recipe(f"{fruit} mit Nüssen", "Snack",
                            {fruit: 150, "Nüsse": 15})
            )

    # Duplikate entfernen und Rezepte mit nicht ausgewählten Zutaten vermeiden.
    for category in recipes:
        unique = {}
        for recipe in recipes[category]:
            if all(food in favorites for food in recipe["ingredients"]):
                unique[(recipe["name"], tuple(sorted(recipe["ingredients"].items())))] = recipe
        recipes[category] = list(unique.values())

    return recipes

def scale_recipe(recipe, factor):
    return {food: grams * factor for food, grams in recipe["ingredients"].items()}

def optimize_portion(recipe, target_kcal):
    # Einfache Portionsanpassung an den Kalorienanteil der Mahlzeit.
    base = nutrition(recipe["ingredients"])["kcal"]
    if base <= 0:
        return 1.0
    return max(0.5, min(2.5, target_kcal / base))

st.header("1. Wähle deine Lieblingslebensmittel")
st.write("Markiere, was du gerne isst. PACE verwendet diese Auswahl als Grundlage für deine Menüvorschläge.")

favorites = []
columns = st.columns(2)
group_items = list(GROUPS.items())

for i, (group, foods) in enumerate(group_items):
    with columns[i % 2]:
        chosen = st.multiselect(
            group,
            foods,
            default=foods[:2] if group in ["Kohlenhydrate", "Proteinreiche Lebensmittel", "Milchprodukte"] else [],
            key=f"favorites_{group}",
        )
        favorites.extend(chosen)

st.header("2. Deine Tagesziele")
c1, c2, c3 = st.columns(3)
with c1:
    target_kcal = st.number_input("Kalorien pro Tag", 1200, 6000, 2500, step=100)
with c2:
    target_protein = st.number_input("Protein (g)", 40, 300, 120, step=5)
with c3:
    target_carbs = st.number_input("Kohlenhydrate (g)", 50, 800, 300, step=10)

st.caption("Du kannst diese Werte später mit einer individuellen Profil- und Trainingsberechnung verbinden.")

if st.button("✨ Menüs aus meinen Favoriten generieren", type="primary"):
    if not favorites:
        st.warning("Bitte wähle zuerst einige Lebensmittel aus.")
    else:
        st.session_state["generated_recipes"] = generate_recipes(favorites)
        st.session_state["generated_favorites"] = favorites.copy()
        st.session_state["selected_recipe_names"] = {}
        st.rerun()

if "generated_recipes" in st.session_state:
    recipes_by_category = st.session_state["generated_recipes"]
    st.header("3. Deine persönlichen Menüs")

    if not any(recipes_by_category.values()):
        st.warning(
            "Aus dieser Auswahl konnten noch keine passenden Rezepte erstellt werden. "
            "Wähle beispielsweise eine Kohlenhydratquelle, ein Protein und Gemüse "
            "sowie für Frühstück oder Snacks Milchprodukte oder Früchte."
        )
    else:
        slots = [
            ("Frühstück", 0.25),
            ("Mittagessen", 0.30),
            ("Snack", 0.15),
            ("Abendessen", 0.30),
        ]
        chosen_recipes = []
        plan_totals = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
        all_ingredients = {}

        for category, calorie_share in slots:
            options = recipes_by_category[category]
            if not options:
                st.warning(f"Für {category} gibt es noch keine Vorschläge. Wähle weitere passende Lebensmittel.")
                continue

            st.subheader(category)
            option_labels = [
                f"{r['name']} ({nutrition(r['ingredients'])['kcal']:.0f} kcal pro Grundportion)"
                for r in options
            ]

            saved_name = st.session_state.get("selected_recipe_names", {}).get(category)
            default_index = next(
                (i for i, r in enumerate(options) if r["name"] == saved_name), 0
            )

            chosen_index = st.selectbox(
                f"{category} auswählen",
                range(len(options)),
                index=default_index,
                format_func=lambda i, labels=option_labels: labels[i],
                key=f"recipe_choice_{category}",
            )
            recipe = options[chosen_index]
            portion = optimize_portion(recipe, target_kcal * calorie_share)
            ingredients = scale_recipe(recipe, portion)
            macros = nutrition(ingredients)

            chosen_recipes.append((category, recipe, portion, ingredients, macros))
            for macro in plan_totals:
                plan_totals[macro] += macros[macro]
            for food, grams in ingredients.items():
                all_ingredients[food] = all_ingredients.get(food, 0) + grams

            st.write(f"**Portion:** {portion:.2f} × Grundportion")
            st.write(
                f"{macros['kcal']:.0f} kcal · Protein {macros['protein']:.1f} g · "
                f"Kohlenhydrate {macros['carbs']:.1f} g · Fett {macros['fat']:.1f} g"
            )
            st.caption("Zutaten: " + ", ".join(
                f"{food} {grams:.0f} g" for food, grams in ingredients.items()
            ))

            if st.button(f"🔄 Anderes Menü für {category}", key=f"swap_{category}"):
                if len(options) > 1:
                    next_index = (chosen_index + 1) % len(options)
                    st.session_state[f"recipe_choice_{category}"] = next_index
                    st.rerun()

        st.header("4. Tagesbilanz")
        a, b, c, d = st.columns(4)
        a.metric("Kalorien", f"{plan_totals['kcal']:.0f} kcal", f"{plan_totals['kcal'] - target_kcal:+.0f}")
        b.metric("Protein", f"{plan_totals['protein']:.0f} g", f"{plan_totals['protein'] - target_protein:+.0f}")
        c.metric("Kohlenhydrate", f"{plan_totals['carbs']:.0f} g", f"{plan_totals['carbs'] - target_carbs:+.0f}")
        d.metric("Fett", f"{plan_totals['fat']:.0f} g")

        st.header("5. Einkaufsliste")
        for food, grams in sorted(all_ingredients.items()):
            st.write(f"- {food}: {grams:.0f} g")

        download_text = "PACE Nutrition – Einkaufsliste\n\n"
        download_text += "\n".join(
            f"- {food}: {grams:.0f} g" for food, grams in sorted(all_ingredients.items())
        )
        st.download_button(
            "📥 Einkaufsliste herunterladen",
            data=download_text,
            file_name="pace_einkaufsliste.txt",
            mime="text/plain",
        )

st.divider()
st.caption(
    "Die Rezeptgenerierung verwendet einfache Kombinationsregeln und ungefähre Nährwerte. "
    "Sie ist ein erster Prototyp und ersetzt keine professionelle Ernährungsberatung."
)
