
import streamlit as st
from collections import defaultdict
from itertools import product

st.set_page_config(page_title="PACE Nutrition", page_icon="🥗", layout="wide")
st.title("🥗 PACE Nutrition")
st.caption("Deine Ernährung. Dein Training. Dein Wochenplan.")

# Nährwerte pro 100 g/ml: kcal, Protein, Kohlenhydrate, Fett, Kategorie
FOODS = {
    "Haferflocken": (372, 13.5, 58.7, 7, "Kohlenhydrate"),
    "Müsli": (370, 10, 64, 7, "Kohlenhydrate"),
    "Reis (trocken)": (360, 7, 80, 1, "Kohlenhydrate"),
    "Vollkornpasta (trocken)": (350, 13, 67, 2.5, "Kohlenhydrate"),
    "Pasta (trocken)": (359, 12.5, 72, 1.5, "Kohlenhydrate"),
    "Couscous (trocken)": (376, 12.8, 77, 0.6, "Kohlenhydrate"),
    "Quinoa (trocken)": (368, 14, 64, 6, "Kohlenhydrate"),
    "Kartoffeln": (77, 2, 17, 0.1, "Kohlenhydrate"),
    "Süsskartoffeln": (86, 1.6, 20, 0.1, "Kohlenhydrate"),
    "Vollkornbrot": (247, 9, 41, 4, "Kohlenhydrate"),
    "Wraps": (310, 8, 52, 8, "Kohlenhydrate"),
    "Reiswaffeln": (387, 8, 81, 3, "Kohlenhydrate"),
    "Pouletbrust": (120, 23, 0, 2.5, "Protein"),
    "Truthahn": (114, 24, 0, 1.5, "Protein"),
    "Rindfleisch mager": (150, 21, 0, 7, "Protein"),
    "Hackfleisch mager": (170, 21, 0, 9, "Protein"),
    "Lachs": (208, 20, 0, 13, "Protein"),
    "Thunfisch (abgetropft)": (116, 26, 0, 1, "Protein"),
    "Eier": (143, 13, 1, 10, "Protein"),
    "Tofu": (145, 16, 2, 9, "Protein"),
    "Tempeh": (193, 20, 8, 11, "Protein"),
    "Linsen (gekocht)": (116, 9, 20, 0.4, "Protein"),
    "Kichererbsen (gekocht)": (164, 8.9, 27, 2.6, "Protein"),
    "Kidneybohnen (gekocht)": (127, 8.7, 22.8, 0.5, "Protein"),
    "Skyr": (63, 11, 4, 0.2, "Milchprodukte"),
    "Magerquark": (67, 12, 4, 0.2, "Milchprodukte"),
    "Hüttenkäse": (98, 12.5, 3, 4.3, "Milchprodukte"),
    "Griechischer Joghurt": (120, 6, 4, 9, "Milchprodukte"),
    "Naturjoghurt": (62, 3.5, 4.7, 3.3, "Milchprodukte"),
    "Milch": (47, 3.4, 4.8, 1.5, "Milchprodukte"),
    "Käse": (350, 25, 1, 27, "Milchprodukte"),
    "Parmesan": (402, 32, 0, 29, "Milchprodukte"),
    "Whey": (400, 80, 8, 6, "Milchprodukte"),
    "Banane": (89, 1.1, 23, 0.3, "Obst"),
    "Apfel": (52, 0.3, 14, 0.2, "Obst"),
    "Beeren": (50, 1, 10, 0.5, "Obst"),
    "Orange": (47, 0.9, 12, 0.1, "Obst"),
    "Birne": (57, 0.4, 15, 0.1, "Obst"),
    "Kiwi": (61, 1.1, 15, 0.5, "Obst"),
    "Mango": (60, 0.8, 15, 0.4, "Obst"),
    "Brokkoli": (34, 2.8, 7, 0.4, "Gemüse"),
    "Spinat": (23, 2.9, 3.6, 0.4, "Gemüse"),
    "Zucchetti": (17, 1.2, 3.1, 0.3, "Gemüse"),
    "Tomaten": (18, 0.9, 3.9, 0.2, "Gemüse"),
    "Peperoni": (31, 1, 6, 0.3, "Gemüse"),
    "Karotten": (41, 0.9, 10, 0.2, "Gemüse"),
    "Gurken": (15, 0.7, 3.6, 0.1, "Gemüse"),
    "Champignons": (22, 3.1, 3.3, 0.3, "Gemüse"),
    "Gemüsemix": (40, 2, 7, 0.5, "Gemüse"),
    "Salat": (17, 1.2, 3, 0.2, "Gemüse"),
    "Avocado": (160, 2, 9, 15, "Fette"),
    "Olivenöl": (884, 0, 0, 100, "Fette"),
    "Nüsse": (600, 20, 20, 54, "Fette"),
    "Erdnussbutter": (600, 25, 20, 50, "Fette"),
    "Chiasamen": (486, 17, 42, 31, "Fette"),
}

GROUPS = [
    "Kohlenhydrate", "Protein", "Milchprodukte",
    "Obst", "Gemüse", "Fette"
]
SPORTS = {
    "Laufen": 8.5, "Krafttraining": 4.5,
    "Radfahren": 7.0, "Schwimmen": 6.0,
    "Tennis": 7.0, "Gehen/Wandern": 3.5,
    "Ruhetag / Mobilität": 2.0, "Andere": 5.0
}
INTENSITY = {"Locker": 0.8, "Mittel": 1.0, "Intensiv": 1.2}
DAYS = [
    "Montag", "Dienstag", "Mittwoch", "Donnerstag",
    "Freitag", "Samstag", "Sonntag"
]
MEALS = ["Frühstück", "Mittagessen", "Snack", "Abendessen"]

DEFAULT_FAVOURITES = [
    "Haferflocken", "Reis (trocken)", "Vollkornpasta (trocken)",
    "Kartoffeln", "Vollkornbrot", "Pouletbrust", "Lachs",
    "Eier", "Thunfisch (abgetropft)", "Skyr", "Magerquark",
    "Hüttenkäse", "Whey", "Banane", "Beeren", "Brokkoli",
    "Zucchetti", "Tomaten", "Olivenöl", "Nüsse"
]


def nutrition(ingredients):
    totals = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for food, grams in ingredients.items():
        if food not in FOODS:
            continue
        kcal, p, c, f, _ = FOODS[food]
        factor = grams / 100
        totals["kcal"] += kcal * factor
        totals["protein"] += p * factor
        totals["carbs"] += c * factor
        totals["fat"] += f * factor
    return totals


def make_recipes(favourites):
    recipes = {meal: [] for meal in MEALS}

    def add(meal, name, ingredients):
        if ingredients and all(food in favourites for food in ingredients):
            recipes[meal].append({
                "name": name,
                "ingredients": ingredients
            })

    carbs = [
        x for x in [
            "Reis (trocken)", "Vollkornpasta (trocken)",
            "Pasta (trocken)", "Couscous (trocken)",
            "Quinoa (trocken)", "Kartoffeln", "Süsskartoffeln"
        ] if x in favourites
    ]
    proteins = [
        x for x in [
            "Pouletbrust", "Truthahn", "Rindfleisch mager",
            "Hackfleisch mager", "Lachs", "Thunfisch (abgetropft)",
            "Tofu", "Tempeh", "Linsen (gekocht)",
            "Kichererbsen (gekocht)", "Kidneybohnen (gekocht)"
        ] if x in favourites
    ]
    veg = [
        x for x in [
            "Brokkoli", "Spinat", "Zucchetti", "Tomaten",
            "Peperoni", "Karotten", "Champignons", "Gemüsemix"
        ] if x in favourites
    ]
    dairy = [
        x for x in [
            "Skyr", "Magerquark", "Griechischer Joghurt",
            "Naturjoghurt", "Hüttenkäse"
        ] if x in favourites
    ]
    fruit = [
        x for x in [
            "Banane", "Apfel", "Beeren", "Orange",
            "Birne", "Kiwi", "Mango"
        ] if x in favourites
    ]

    for base in ["Haferflocken", "Müsli"]:
        if base in favourites:
            for d in dairy:
                for fr in fruit:
                    add("Frühstück", f"{base} mit {d} und {fr}",
                        {base: 60, d: 200, fr: 100})

    for bread in ["Vollkornbrot", "Wraps"]:
        if bread in favourites:
            for p in ["Eier", "Thunfisch (abgetropft)", "Tofu", "Hüttenkäse"]:
                if p in favourites:
                    ingredients = {
                        bread: 100 if bread == "Vollkornbrot" else 70,
                        p: 100
                    }
                    if "Tomaten" in favourites:
                        ingredients["Tomaten"] = 80
                    add("Frühstück", f"{bread} mit {p}", ingredients)

    for d in dairy:
        for fr in fruit:
            add("Snack", f"{d} mit {fr}", {d: 200, fr: 100})
        for fat in ["Nüsse", "Erdnussbutter", "Chiasamen"]:
            if fat in favourites:
                add("Snack", f"{d} mit {fat}", {d: 200, fat: 15})

    for fr in fruit:
        for fat in ["Nüsse", "Erdnussbutter"]:
            if fat in favourites:
                add("Snack", f"{fr} mit {fat}", {fr: 120, fat: 15})

    for carb, protein, vegetable in product(carbs, proteins, veg):
        ingredients = {
            carb: 80 if "trocken" in carb else 250,
            protein: 150,
            vegetable: 150
        }
        if "Olivenöl" in favourites:
            ingredients["Olivenöl"] = 5
        add("Mittagessen", f"{carb} mit {protein} und {vegetable}", ingredients)
        add("Abendessen", f"{protein} mit {carb} und {vegetable}", ingredients)

    for carb, protein in product(carbs, proteins):
        ingredients = {
            carb: 80 if "trocken" in carb else 250,
            protein: 150
        }
        add("Mittagessen", f"{carb} mit {protein}", ingredients)
        add("Abendessen", f"{protein} mit {carb}", ingredients)

    for meal in recipes:
        seen, cleaned = set(), []
        for recipe in recipes[meal]:
            if recipe["name"] not in seen:
                cleaned.append(recipe)
                seen.add(recipe["name"])
        recipes[meal] = cleaned[:100]

    return recipes


def training_burn(sessions, weight):
    total = 0.0
    for session in sessions:
        met = SPORTS[session["sport"]] * INTENSITY[session["intensity"]]
        total += max(0, (met - 1) * 3.5 * weight / 200 * session["minutes"])
    return total


def targets_for_day(age, weight, height, sex, goal, activity, sessions):
    if sex == "Mann":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex == "Frau":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 78

    activity_factor = {
        "Sitzend": 1.2, "Leicht aktiv": 1.35, "Aktiv": 1.5
    }[activity]
    goal_factor = {
        "Leistung erhalten": 1.0,
        "Muskelaufbau": 1.08,
        "Fettverlust": 0.92
    }[goal]

    base = bmr * activity_factor * goal_factor
    kcal = max(1200, base + training_burn(sessions, weight))
    protein = weight * (2.0 if goal == "Muskelaufbau" else 1.8)
    fat = weight * 0.9
    carbs = max(0, (kcal - protein * 4 - fat * 9) / 4)

    return {
        "kcal": kcal, "protein": protein, "carbs": carbs,
        "fat": fat, "bmr": bmr, "base": base
    }


def scaled(ingredients, factor):
    return {food: grams * factor for food, grams in ingredients.items()}


def optimize_portions(recipes, targets):
    factors = {meal: 1.0 for meal in MEALS}
    steps = [0.5, 0.25, 0.1, 0.05]

    def score(candidate):
        total = {"kcal": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
        for meal in MEALS:
            values = nutrition(scaled(
                recipes[meal]["ingredients"], candidate[meal]
            ))
            for key in total:
                total[key] += values[key]

        return (
            abs(total["kcal"] - targets["kcal"]) / max(targets["kcal"], 1) * 3
            + abs(total["protein"] - targets["protein"]) / max(targets["protein"], 1) * 2
            + abs(total["carbs"] - targets["carbs"]) / max(targets["carbs"], 1) * 1.2
            + abs(total["fat"] - targets["fat"]) / max(targets["fat"], 1)
        )

    best_score = score(factors)
    for step in steps:
        improved = True
        while improved:
            improved = False
            for meal in MEALS:
                local_best, local_factor = best_score, factors[meal]
                for direction in (-1, 1):
                    trial = max(0.5, min(2.5, factors[meal] + direction * step))
                    candidate = dict(factors)
                    candidate[meal] = trial
                    candidate_score = score(candidate)
                    if candidate_score < local_best:
                        local_best, local_factor = candidate_score, trial
                if local_best < best_score:
                    factors[meal] = local_factor
                    best_score = local_best
                    improved = True
    return factors

with st.sidebar:
    st.header("Dein Profil")
    age = st.number_input("Alter", 16, 100, 30)
    weight = st.number_input("Gewicht (kg)", 35.0, 250.0, 62.0, 0.5)
    height = st.number_input("Grösse (cm)", 130, 230, 165)
    sex = st.selectbox(
        "Geschlecht für Grundumsatz",
        ["Mann", "Frau", "Andere / keine Angabe"]
    )
    goal = st.selectbox(
        "Ernährungsziel",
        ["Leistung erhalten", "Muskelaufbau", "Fettverlust"]
    )
    activity = st.selectbox(
        "Alltag ausserhalb des Trainings",
        ["Sitzend", "Leicht aktiv", "Aktiv"],
        index=1
    )
    st.caption(
        "Kalorien und Makros sind Schätzungen. Passe sie anhand "
        "von Hunger, Gewichtsentwicklung und Trainingsleistung an."
    )

st.header("1. Wochen-Training planen")
st.write(
    "Trage deine Trainingseinheiten für jeden Tag ein. "
    "Mehrere Einheiten pro Tag sind möglich."
)

if "weekly_sessions" not in st.session_state:
    st.session_state.weekly_sessions = {day: [] for day in DAYS}

with st.form("add_session_form", clear_on_submit=True):
    c1, c2, c3, c4 = st.columns(4)
    day_choice = c1.selectbox("Tag", DAYS)
    sport_choice = c2.selectbox("Sport", list(SPORTS.keys()))
    duration = c3.number_input("Dauer (Min.)", 10, 360, 60, 5)
    intensity = c4.selectbox("Intensität", list(INTENSITY.keys()))
    submitted = st.form_submit_button("Einheit hinzufügen")

    if submitted:
        st.session_state.weekly_sessions[day_choice].append({
            "sport": sport_choice,
            "minutes": int(duration),
            "intensity": intensity
        })
        st.rerun()

with st.expander("Wochenplan bearbeiten / Einheiten entfernen", expanded=True):
    for day in DAYS:
        sessions = st.session_state.weekly_sessions[day]
        with st.container(border=True):
            st.markdown(f"**{day}**")
            if not sessions:
                st.caption("Noch keine Einheit geplant")
            for idx, session in enumerate(list(sessions)):
                col1, col2 = st.columns([5, 1])
                col1.write(
                    f"{session['sport']} · {session['minutes']} Min. · "
                    f"{session['intensity']}"
                )
                if col2.button("Entfernen", key=f"remove_{day}_{idx}"):
                    st.session_state.weekly_sessions[day].pop(idx)
                    st.rerun()

st.header("2. Lieblingslebensmittel")
st.write(
    "Wähle Lebensmittel aus, die du gerne isst. "
    "Rezepte werden aus deiner Auswahl zusammengestellt."
)

favourite_groups = {}
cols = st.columns(3)
for i, group in enumerate(GROUPS):
    with cols[i % 3]:
        options = [
            name for name, values in FOODS.items()
            if values[4] == group
        ]
        defaults = [x for x in DEFAULT_FAVOURITES if x in options]
        favourite_groups[group] = st.multiselect(
            group, options, default=defaults, key=f"fav_{group}"
        )

favourites = set(
    food for values in favourite_groups.values() for food in values
)
recipes_by_meal = make_recipes(favourites) if favourites else {
    meal: [] for meal in MEALS
}
missing = [meal for meal in MEALS if not recipes_by_meal[meal]]

if missing:
    st.warning(
        "Für diese Mahlzeiten fehlen passende Rezepte: "
        + ", ".join(missing)
        + ". Wähle z. B. Haferflocken, ein Milchprodukt und Obst "
        "sowie eine Kohlenhydratquelle und eine Proteinquelle."
    )

st.header("3. Wochenmenü zusammenstellen")
st.write(
    "Wähle für jeden Tag ein Rezept pro Mahlzeit. Wiederholungen sind "
    "möglich. Die Einkaufsliste summiert die Zutaten für die ganze Woche."
)

if "weekly_choices" not in st.session_state:
    st.session_state.weekly_choices = {
        day: {meal: 0 for meal in MEALS} for day in DAYS
    }
if "weekly_portions" not in st.session_state:
    st.session_state.weekly_portions = {
        day: {meal: 1.0 for meal in MEALS} for day in DAYS
    }
if "last_favourites" not in st.session_state:
    st.session_state.last_favourites = sorted(favourites)
elif st.session_state.last_favourites != sorted(favourites):
    st.session_state.weekly_choices = {
        day: {meal: 0 for meal in MEALS} for day in DAYS
    }
    st.session_state.weekly_portions = {
        day: {meal: 1.0 for meal in MEALS} for day in DAYS
    }
    st.session_state.last_favourites = sorted(favourites)

if not missing:
    tabs = st.tabs(DAYS)
    for day, tab in zip(DAYS, tabs):
        with tab:
            sessions = st.session_state.weekly_sessions[day]
            targets = targets_for_day(
                age, weight, height, sex, goal, activity, sessions
            )
            burn = training_burn(sessions, weight)

            st.subheader(f"{day}: Tagesziel")
            metric_cols = st.columns(4)
            metric_cols[0].metric("Kalorien", f"{targets['kcal']:.0f} kcal")
            metric_cols[1].metric("Protein", f"{targets['protein']:.0f} g")
            metric_cols[2].metric("Kohlenhydrate", f"{targets['carbs']:.0f} g")
            metric_cols[3].metric("Fett", f"{targets['fat']:.0f} g")
            planned = ", ".join(
                f"{s['sport']} {s['minutes']} min" for s in sessions
            ) or "Keine Einheiten"
            st.caption(
                f"Geschätzter zusätzlicher Trainingsverbrauch: {burn:.0f} kcal. "
                f"Training: {planned}"
            )

            day_recipes = {}
            for meal in MEALS:
                options = recipes_by_meal[meal]
                labels = [r["name"] for r in options]
                selected_idx = min(
                    st.session_state.weekly_choices[day][meal],
                    len(labels) - 1
                )
                chosen_idx = st.selectbox(
                    meal,
                    range(len(labels)),
                    index=selected_idx,
                    format_func=lambda i, labels=labels: labels[i],
                    key=f"recipe_{day}_{meal}"
                )
                st.session_state.weekly_choices[day][meal] = chosen_idx

                portion = st.slider(
                    f"Portion {meal.lower()} (Faktor)",
                    0.5, 2.5,
                    float(st.session_state.weekly_portions[day][meal]),
                    0.05,
                    key=f"portion_{day}_{meal}"
                )
                st.session_state.weekly_portions[day][meal] = portion
                recipe = options[chosen_idx]
                day_recipes[meal] = {
                    "name": recipe["name"],
                    "ingredients": recipe["ingredients"]
                }

            if st.button(
                f"Portionen für {day} automatisch optimieren",
                key=f"optimize_{day}"
            ):
                factors = optimize_portions(day_recipes, targets)
                for meal in MEALS:
                    st.session_state.weekly_portions[day][meal] = max(
                        0.5, min(2.5, factors[meal])
                    )
                st.rerun()

            totals = {"kcal": 0, "protein": 0, "carbs": 0, "fat": 0}
            for meal, recipe in day_recipes.items():
                ingredients = scaled(
                    recipe["ingredients"],
                    st.session_state.weekly_portions[day][meal]
                )
                values = nutrition(ingredients)
                for key in totals:
                    totals[key] += values[key]

            st.subheader("Tagesbilanz der gewählten Mahlzeiten")
            metric_cols = st.columns(4)
            for col, key, label, unit in zip(
                metric_cols,
                ["kcal", "protein", "carbs", "fat"],
                ["Kalorien", "Protein", "Kohlenhydrate", "Fett"],
                ["kcal", "g", "g", "g"]
            ):
                col.metric(
                    label,
                    f"{totals[key]:.0f} {unit}",
                    f"{totals[key] - targets[key]:+.0f} {unit} zum Ziel"
                )

            kcal_gap = abs(
                totals["kcal"] - targets["kcal"]
            ) / max(targets["kcal"], 1)
            if kcal_gap > 0.15:
                st.warning(
                    "Die gewählten Mahlzeiten liegen mehr als 15 % vom "
                    "Kalorienziel entfernt. Passe Portionen an oder wähle "
                    "andere Rezepte. Die Optimierung ist eine Näherung."
                )

st.header("4. Wochenübersicht")
summary_rows = []
weekly_shopping = defaultdict(float)

if not missing:
    for day in DAYS:
        sessions = st.session_state.weekly_sessions[day]
        targets = targets_for_day(
            age, weight, height, sex, goal, activity, sessions
        )
        day_total = {"kcal": 0, "protein": 0, "carbs": 0, "fat": 0}
        training_text = ", ".join(
            f"{s['sport']} ({s['minutes']} min)" for s in sessions
        ) or "Ruhetag"

        for meal in MEALS:
            recipe = recipes_by_meal[meal][
                st.session_state.weekly_choices[day][meal]
            ]
            ingredients = scaled(
                recipe["ingredients"],
                st.session_state.weekly_portions[day][meal]
            )
            values = nutrition(ingredients)
            for key in day_total:
                day_total[key] += values[key]
            for food, grams in ingredients.items():
                weekly_shopping[food] += grams

        summary_rows.append({
            "Tag": day,
            "Training": training_text,
            "Ziel kcal": round(targets["kcal"]),
            "Menü kcal": round(day_total["kcal"]),
            "Protein g": round(day_total["protein"]),
            "Kohlenhydrate g": round(day_total["carbs"]),
            "Fett g": round(day_total["fat"])
        })

    st.dataframe(summary_rows, use_container_width=True, hide_index=True)
    st.caption(
        "Tagesziele sind Schätzungen. Der tatsächliche Energieverbrauch "
        "kann abweichen."
    )

    st.header("5. Gesamte Einkaufsliste")
    shopping_lines = ["PACE Nutrition – Einkaufsliste für 7 Tage", ""]
    shopping_categories = defaultdict(list)

    for food, grams in weekly_shopping.items():
        shopping_categories[FOODS[food][4]].append((food, grams))

    for category in GROUPS:
        if shopping_categories[category]:
            st.subheader(category)
            for food, grams in sorted(shopping_categories[category]):
                line = (
                    f"{food}: {grams / 1000:.2f} kg"
                    if grams >= 1000 else f"{food}: {grams:.0f} g"
                )
                st.write(f"- {line}")
                shopping_lines.append(line)

    st.download_button(
        "Einkaufsliste als TXT herunterladen",
        "\n".join(shopping_lines),
        file_name="pace_wochen_einkaufsliste.txt",
        mime="text/plain"
    )

st.divider()
st.caption(
    "PACE Nutrition liefert unverbindliche Schätzwerte und ersetzt "
    "keine medizinische oder ernährungstherapeutische Beratung."
)
