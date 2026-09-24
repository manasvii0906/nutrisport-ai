# ===== app.py =====
# Simple Flask backend for NutriSport AI.
# Handles: BMI + daily nutrition target calculation, and food recommendations.
# This is the "Python / AI logic" layer of the project.

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows our HTML/JS frontend to call this API from the browser


# ---------- Small local food database for recommendations ----------
# Each food has: name, category, calories, protein, goals it suits, sports it suits, diet type, allergens
FOODS = [
    {"name": "Oats", "category": "Grains", "calories": 150, "protein": 5, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain", "Sports Performance"], "sports": ["Basketball", "Running", "General Fitness"], "allergens": []},
    {"name": "Banana", "category": "Fruits", "calories": 105, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance", "Weight Management"], "sports": ["Basketball", "Football", "Running", "Cycling"], "allergens": []},
    {"name": "Eggs", "category": "Eggs", "calories": 78, "protein": 6, "diet": "Eggetarian",
     "goals": ["Muscle Gain", "Sports Performance", "General Health"], "sports": ["Basketball", "Strength Training", "Swimming"], "allergens": ["Eggs"]},
    {"name": "Chicken Breast", "category": "Meat", "calories": 165, "protein": 31, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain", "Fat Loss", "Sports Performance"], "sports": ["Basketball", "Football", "Strength Training"], "allergens": []},
    {"name": "Paneer", "category": "Dairy", "calories": 265, "protein": 18, "diet": "Vegetarian",
     "goals": ["Muscle Gain", "Sports Performance", "General Health"], "sports": ["Basketball", "Strength Training"], "allergens": ["Dairy"]},
    {"name": "Dal (Lentils)", "category": "Pulses", "calories": 116, "protein": 9, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain", "Weight Management"], "sports": ["General Fitness", "Running"], "allergens": []},
    {"name": "Rajma (Kidney Beans)", "category": "Pulses", "calories": 127, "protein": 9, "diet": "Vegan",
     "goals": ["Muscle Gain", "General Health"], "sports": ["Strength Training", "General Fitness"], "allergens": []},
    {"name": "Greek Yogurt", "category": "Dairy", "calories": 100, "protein": 10, "diet": "Vegetarian",
     "goals": ["Muscle Gain", "Fat Loss", "Sports Performance"], "sports": ["Swimming", "Strength Training"], "allergens": ["Dairy"]},
    {"name": "Brown Rice", "category": "Grains", "calories": 216, "protein": 5, "diet": "Vegan",
     "goals": ["Sports Performance", "General Health", "Muscle Gain"], "sports": ["Football", "Running", "Cycling"], "allergens": []},
    {"name": "Almonds", "category": "Nuts", "calories": 164, "protein": 6, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain"], "sports": ["General Fitness"], "allergens": ["Nuts"]},
    {"name": "Tofu", "category": "Soy", "calories": 144, "protein": 17, "diet": "Vegan",
     "goals": ["Muscle Gain", "Sports Performance"], "sports": ["Strength Training", "General Fitness"], "allergens": ["Soy"]},
    {"name": "Spinach", "category": "Vegetables", "calories": 23, "protein": 3, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness", "Running"], "allergens": []},
    {"name": "Sweet Potato", "category": "Vegetables", "calories": 86, "protein": 2, "diet": "Vegan",
     "goals": ["Sports Performance", "General Health"], "sports": ["Football", "Running", "Cycling"], "allergens": []},
    {"name": "Apple", "category": "Fruits", "calories": 95, "protein": 0, "diet": "Vegan",
     "goals": ["General Health", "Weight Management", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Salmon", "category": "Fish", "calories": 208, "protein": 20, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain", "Sports Performance"], "sports": ["Swimming", "Strength Training"], "allergens": []},
]


# ---------- Route 1: BMI + Daily Nutrition Targets ----------
@app.route("/api/calculate-targets", methods=["POST"])
def calculate_targets():
    data = request.get_json()

    weight = float(data.get("weight", 0))
    height = float(data.get("height", 0))
    age = int(data.get("age", 0))
    gender = data.get("gender", "male")
    activity_level = data.get("activityLevel", "sedentary")
    goal = data.get("goal", "generalHealth")

    # --- BMI ---
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 1) if height_m > 0 else 0

    if bmi < 18.5:
        bmi_category = "Underweight"
    elif bmi < 25:
        bmi_category = "Normal"
    elif bmi < 30:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obese"

    # --- BMR (Mifflin-St Jeor Equation) ---
    bmr = (10 * weight) + (6.25 * height) - (5 * age)
    bmr += 5 if gender == "male" else -161

    # --- Activity multiplier (TDEE = BMR x activity factor) ---
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "veryActive": 1.725,
        "athlete": 1.9
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)

    # --- Goal-based calorie adjustment ---
    goal_adjustments = {
        "fatLoss": -0.15,
        "weightManagement": -0.05,
        "muscleGain": 0.10,
        "sportsPerformance": 0.05,
        "generalHealth": 0
    }
    calories = round(tdee * (1 + goal_adjustments.get(goal, 0)))

    # --- Protein target (varies by goal) ---
    protein_per_kg = 1.6
    if goal in ("muscleGain", "sportsPerformance"):
        protein_per_kg = 1.8
    if goal == "fatLoss":
        protein_per_kg = 2.0
    protein = round(weight * protein_per_kg)
    protein_cals = protein * 4

    # --- Fat target (~27% of calories) ---
    fat_cals = calories * 0.27
    fat = round(fat_cals / 9)

    # --- Carbs (remaining calories) ---
    remaining_cals = calories - protein_cals - fat_cals
    carbs = round(remaining_cals / 4)

    # --- Fiber & Water ---
    fiber = round((calories / 1000) * 14)
    water_liters = round(weight * 0.033, 1)

    return jsonify({
        "bmi": bmi,
        "bmiCategory": bmi_category,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "fiber": fiber,
        "waterLiters": water_liters
    })

# ---------- Route 2: Food Recommendations ----------
@app.route("/api/recommend", methods=["POST"])
def recommend_foods():
    data = request.get_json()

    goal = data.get("goal", "")
    sport = data.get("sport", "")
    diet = data.get("dietaryPreference", "")
    allergies = data.get("allergies", [])

    results = []
    for food in FOODS:
        # Skip if food doesn't match diet type (simple rule: Vegan fits all veg diets)
        if diet == "Non-Vegetarian":
            diet_ok = True  # non-veg eaters can eat anything
        elif diet == "Vegetarian":
            diet_ok = food["diet"] in ["Vegetarian", "Vegan", "Eggetarian"]
        elif diet == "Eggetarian":
            diet_ok = food["diet"] in ["Vegetarian", "Vegan", "Eggetarian"]
        elif diet == "Vegan":
            diet_ok = food["diet"] == "Vegan"
        else:
            diet_ok = True

        if not diet_ok:
            continue

        # Skip if food contains an allergen the user marked
        if any(a in food["allergens"] for a in allergies):
            continue

        # Score: does it match the goal and/or sport?
        score = 0
        if goal in food["goals"]:
            score += 2
        if sport in food["sports"]:
            score += 1

        if score > 0:
            results.append({**food, "score": score})

    # Sort by best match first, return top 8
    results.sort(key=lambda f: f["score"], reverse=True)
    return jsonify(results[:8])


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)