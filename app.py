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
    
    # ---- Grains ----
    {"name": "Oats", "category": "Grains", "calories": 150, "protein": 5, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain", "Sports Performance"], "sports": ["Basketball", "Running", "General Fitness"], "allergens": []},
    {"name": "Brown Rice", "category": "Grains", "calories": 216, "protein": 5, "diet": "Vegan",
     "goals": ["Sports Performance", "General Health", "Muscle Gain"], "sports": ["Football", "Running", "Cycling"], "allergens": []},
    {"name": "White Rice", "category": "Grains", "calories": 205, "protein": 4, "diet": "Vegan",
     "goals": ["Sports Performance", "General Health"], "sports": ["Basketball", "Football", "Cricket"], "allergens": []},
    {"name": "Whole Wheat Roti", "category": "Grains", "calories": 120, "protein": 4, "diet": "Vegan",
     "goals": ["General Health", "Weight Management"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Quinoa", "category": "Grains", "calories": 222, "protein": 8, "diet": "Vegan",
     "goals": ["Muscle Gain", "Sports Performance", "General Health"], "sports": ["Running", "Strength Training"], "allergens": []},
    {"name": "Whole Wheat Bread", "category": "Grains", "calories": 80, "protein": 4, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Pasta", "category": "Grains", "calories": 220, "protein": 8, "diet": "Vegetarian",
     "goals": ["Sports Performance", "General Health"], "sports": ["Running", "Cycling", "Football"], "allergens": ["Gluten"]},
    {"name": "Poha", "category": "Grains", "calories": 180, "protein": 4, "diet": "Vegan",
     "goals": ["General Health", "Weight Management"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Idli", "category": "Grains", "calories": 39, "protein": 2, "diet": "Vegan",
     "goals": ["General Health", "Weight Management"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Muesli", "category": "Grains", "calories": 289, "protein": 8, "diet": "Vegetarian",
     "goals": ["General Health", "Sports Performance"], "sports": ["Running", "Cycling"], "allergens": ["Nuts", "Gluten"]},

    # ---- Fruits ----
    {"name": "Banana", "category": "Fruits", "calories": 105, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance", "Weight Management"], "sports": ["Basketball", "Football", "Running", "Cycling"], "allergens": []},
    {"name": "Apple", "category": "Fruits", "calories": 95, "protein": 0, "diet": "Vegan",
     "goals": ["General Health", "Weight Management", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Orange", "category": "Fruits", "calories": 62, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness", "Tennis"], "allergens": []},
    {"name": "Mango", "category": "Fruits", "calories": 99, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance"], "sports": ["Cricket", "Badminton"], "allergens": []},
    {"name": "Watermelon", "category": "Fruits", "calories": 46, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance", "Weight Management"], "sports": ["Running", "Cycling"], "allergens": []},
    {"name": "Grapes", "category": "Fruits", "calories": 62, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Papaya", "category": "Fruits", "calories": 59, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Pineapple", "category": "Fruits", "calories": 82, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance"], "sports": ["Tennis", "Badminton"], "allergens": []},
    {"name": "Strawberries", "category": "Fruits", "calories": 32, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Avocado", "category": "Fruits", "calories": 234, "protein": 3, "diet": "Vegan",
     "goals": ["Muscle Gain", "General Health"], "sports": ["Strength Training", "Swimming"], "allergens": []},

    # ---- Vegetables ----
    {"name": "Spinach", "category": "Vegetables", "calories": 23, "protein": 3, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness", "Running"], "allergens": []},
    {"name": "Sweet Potato", "category": "Vegetables", "calories": 86, "protein": 2, "diet": "Vegan",
     "goals": ["Sports Performance", "General Health"], "sports": ["Football", "Running", "Cycling"], "allergens": []},
    {"name": "Broccoli", "category": "Vegetables", "calories": 55, "protein": 4, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss", "Muscle Gain"], "sports": ["General Fitness", "Strength Training"], "allergens": []},
    {"name": "Carrot", "category": "Vegetables", "calories": 41, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Potato (Boiled)", "category": "Vegetables", "calories": 87, "protein": 2, "diet": "Vegan",
     "goals": ["Sports Performance", "General Health"], "sports": ["Football", "Cricket"], "allergens": []},
    {"name": "Cauliflower", "category": "Vegetables", "calories": 25, "protein": 2, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Bell Pepper", "category": "Vegetables", "calories": 31, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Mixed Salad", "category": "Vegetables", "calories": 50, "protein": 2, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss", "Weight Management"], "sports": ["General Fitness"], "allergens": []},

    # ---- Pulses ----
    {"name": "Dal (Lentils)", "category": "Pulses", "calories": 116, "protein": 9, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain", "Weight Management"], "sports": ["General Fitness", "Running"], "allergens": []},
    {"name": "Rajma (Kidney Beans)", "category": "Pulses", "calories": 127, "protein": 9, "diet": "Vegan",
     "goals": ["Muscle Gain", "General Health"], "sports": ["Strength Training", "General Fitness"], "allergens": []},
    {"name": "Chickpeas (Chana)", "category": "Pulses", "calories": 164, "protein": 9, "diet": "Vegan",
     "goals": ["Muscle Gain", "General Health"], "sports": ["Strength Training", "General Fitness"], "allergens": []},
    {"name": "Black Beans", "category": "Pulses", "calories": 132, "protein": 9, "diet": "Vegan",
     "goals": ["Muscle Gain", "General Health"], "sports": ["Strength Training"], "allergens": []},
    {"name": "Sprouts", "category": "Pulses", "calories": 30, "protein": 3, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},

    # ---- Dairy ----
    {"name": "Paneer", "category": "Dairy", "calories": 265, "protein": 18, "diet": "Vegetarian",
     "goals": ["Muscle Gain", "Sports Performance", "General Health"], "sports": ["Basketball", "Strength Training"], "allergens": ["Dairy"]},
    {"name": "Greek Yogurt", "category": "Dairy", "calories": 100, "protein": 10, "diet": "Vegetarian",
     "goals": ["Muscle Gain", "Fat Loss", "Sports Performance"], "sports": ["Swimming", "Strength Training"], "allergens": ["Dairy"]},
    {"name": "Milk", "category": "Dairy", "calories": 103, "protein": 8, "diet": "Vegetarian",
     "goals": ["Muscle Gain", "General Health"], "sports": ["Strength Training", "General Fitness"], "allergens": ["Dairy"]},
    {"name": "Cheese", "category": "Dairy", "calories": 113, "protein": 7, "diet": "Vegetarian",
     "goals": ["Muscle Gain"], "sports": ["Strength Training"], "allergens": ["Dairy"]},
    {"name": "Curd (Dahi)", "category": "Dairy", "calories": 98, "protein": 11, "diet": "Vegetarian",
     "goals": ["General Health", "Sports Performance"], "sports": ["General Fitness", "Cricket"], "allergens": ["Dairy"]},

    # ---- Eggs ----
    {"name": "Eggs", "category": "Eggs", "calories": 78, "protein": 6, "diet": "Eggetarian",
     "goals": ["Muscle Gain", "Sports Performance", "General Health"], "sports": ["Basketball", "Strength Training", "Swimming"], "allergens": ["Eggs"]},
    {"name": "Boiled Egg", "category": "Eggs", "calories": 78, "protein": 6, "diet": "Eggetarian",
     "goals": ["Muscle Gain", "Sports Performance"], "sports": ["Strength Training", "Swimming"], "allergens": ["Eggs"]},
    {"name": "Omelette", "category": "Eggs", "calories": 154, "protein": 11, "diet": "Eggetarian",
     "goals": ["Muscle Gain", "Sports Performance"], "sports": ["Strength Training", "Basketball"], "allergens": ["Eggs"]},

    # ---- Meat / Fish ----
    {"name": "Chicken Breast", "category": "Meat", "calories": 165, "protein": 31, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain", "Fat Loss", "Sports Performance"], "sports": ["Basketball", "Football", "Strength Training"], "allergens": []},
    {"name": "Grilled Chicken", "category": "Meat", "calories": 187, "protein": 28, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain", "Fat Loss", "Sports Performance"], "sports": ["Strength Training", "Football"], "allergens": []},
    {"name": "Mutton Curry", "category": "Meat", "calories": 294, "protein": 25, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain"], "sports": ["Strength Training"], "allergens": []},
    {"name": "Salmon", "category": "Fish", "calories": 208, "protein": 20, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain", "Sports Performance"], "sports": ["Swimming", "Strength Training"], "allergens": []},
    {"name": "Tuna", "category": "Fish", "calories": 132, "protein": 28, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain", "Fat Loss", "Sports Performance"], "sports": ["Swimming", "Strength Training"], "allergens": []},
    {"name": "Fish Curry", "category": "Fish", "calories": 180, "protein": 22, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain", "General Health"], "sports": ["Swimming"], "allergens": []},

    # ---- Nuts / Seeds ----
    {"name": "Almonds", "category": "Nuts", "calories": 164, "protein": 6, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain"], "sports": ["General Fitness"], "allergens": ["Nuts"]},
    {"name": "Walnuts", "category": "Nuts", "calories": 185, "protein": 4, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain"], "sports": ["General Fitness"], "allergens": ["Nuts"]},
    {"name": "Peanut Butter", "category": "Nuts", "calories": 190, "protein": 7, "diet": "Vegan",
     "goals": ["Muscle Gain", "Sports Performance"], "sports": ["Strength Training", "Basketball"], "allergens": ["Nuts"]},
    {"name": "Chia Seeds", "category": "Nuts", "calories": 138, "protein": 5, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["Running", "Cycling"], "allergens": []},
    {"name": "Flax Seeds", "category": "Nuts", "calories": 150, "protein": 5, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},

    # ---- Soy ----
    {"name": "Tofu", "category": "Soy", "calories": 144, "protein": 17, "diet": "Vegan",
     "goals": ["Muscle Gain", "Sports Performance"], "sports": ["Strength Training", "General Fitness"], "allergens": ["Soy"]},
    {"name": "Soy Milk", "category": "Soy", "calories": 80, "protein": 7, "diet": "Vegan",
     "goals": ["Muscle Gain", "General Health"], "sports": ["General Fitness"], "allergens": ["Soy"]},
    {"name": "Edamame", "category": "Soy", "calories": 121, "protein": 11, "diet": "Vegan",
     "goals": ["Muscle Gain", "General Health"], "sports": ["Strength Training"], "allergens": ["Soy"]},

    # ---- Common "Scanned" / Prepared Foods ----
    {"name": "Pizza", "category": "Snacks", "calories": 285, "protein": 12, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy", "Gluten"]},
    {"name": "Sandwich", "category": "Snacks", "calories": 250, "protein": 10, "diet": "Vegetarian",
     "goals": ["General Health", "Weight Management"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Burger", "category": "Snacks", "calories": 354, "protein": 17, "diet": "Non-Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy", "Gluten"]},
    {"name": "French Fries", "category": "Snacks", "calories": 312, "protein": 4, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Samosa", "category": "Snacks", "calories": 262, "protein": 4, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Dosa", "category": "Snacks", "calories": 133, "protein": 4, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Fried Rice", "category": "Snacks", "calories": 238, "protein": 6, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Protein Bar", "category": "Snacks", "calories": 200, "protein": 20, "diet": "Vegetarian",
     "goals": ["Muscle Gain", "Sports Performance"], "sports": ["Strength Training", "Basketball"], "allergens": ["Nuts", "Dairy"]},
    {"name": "Granola Bar", "category": "Snacks", "calories": 132, "protein": 3, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance"], "sports": ["Running", "Cycling"], "allergens": ["Nuts", "Gluten"]},
    {"name": "Popcorn", "category": "Snacks", "calories": 106, "protein": 3, "diet": "Vegan",
     "goals": ["General Health", "Weight Management"], "sports": ["General Fitness"], "allergens": []},

    # ---- Beverages ----
    {"name": "Protein Shake", "category": "Beverages", "calories": 150, "protein": 25, "diet": "Vegetarian",
     "goals": ["Muscle Gain", "Sports Performance"], "sports": ["Strength Training", "Basketball", "Swimming"], "allergens": ["Dairy"]},
    {"name": "Coconut Water", "category": "Beverages", "calories": 46, "protein": 2, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance"], "sports": ["Running", "Cricket", "Tennis"], "allergens": []},
    {"name": "Green Tea", "category": "Beverages", "calories": 2, "protein": 0, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Sports Drink", "category": "Beverages", "calories": 80, "protein": 0, "diet": "Vegan",
     "goals": ["Sports Performance"], "sports": ["Running", "Football", "Basketball", "Cricket"], "allergens": []},
    {"name": "Buttermilk (Chaas)", "category": "Beverages", "calories": 40, "protein": 2, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},
    {"name": "Fruit Smoothie", "category": "Beverages", "calories": 150, "protein": 3, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance"], "sports": ["General Fitness", "Running"], "allergens": []},
         {"name": "Fruit Smoothie", "category": "Beverages", "calories": 150, "protein": 3, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance"], "sports": ["General Fitness", "Running"], "allergens": []},

    # ---- More Grains ----
    {"name": "Corn", "category": "Grains", "calories": 96, "protein": 3, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Millet (Bajra)", "category": "Grains", "calories": 207, "protein": 6, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance"], "sports": ["Running", "General Fitness"], "allergens": []},
    {"name": "Jowar Roti", "category": "Grains", "calories": 100, "protein": 3, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Naan", "category": "Grains", "calories": 262, "protein": 9, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten", "Dairy"]},
    {"name": "Paratha", "category": "Grains", "calories": 260, "protein": 6, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Upma", "category": "Grains", "calories": 192, "protein": 5, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Cornflakes", "category": "Grains", "calories": 100, "protein": 2, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Bagel", "category": "Grains", "calories": 245, "protein": 10, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Noodles", "category": "Grains", "calories": 220, "protein": 6, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Couscous", "category": "Grains", "calories": 176, "protein": 6, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance"], "sports": ["Running"], "allergens": ["Gluten"]},

    # ---- More Fruits ----
    {"name": "Pomegranate", "category": "Fruits", "calories": 83, "protein": 2, "diet": "Vegan",
     "goals": ["General Health", "Sports Performance"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Kiwi", "category": "Fruits", "calories": 42, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Guava", "category": "Fruits", "calories": 37, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Pear", "category": "Fruits", "calories": 101, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Peach", "category": "Fruits", "calories": 59, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Blueberries", "category": "Fruits", "calories": 57, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Dates", "category": "Fruits", "calories": 66, "protein": 0, "diet": "Vegan",
     "goals": ["Sports Performance", "General Health"], "sports": ["Running", "Cricket"], "allergens": []},
    {"name": "Raisins", "category": "Fruits", "calories": 85, "protein": 1, "diet": "Vegan",
     "goals": ["Sports Performance", "General Health"], "sports": ["Running", "Cycling"], "allergens": []},
    {"name": "Lychee", "category": "Fruits", "calories": 66, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Coconut (Fresh)", "category": "Fruits", "calories": 159, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},

    # ---- More Vegetables ----
    {"name": "Cabbage", "category": "Vegetables", "calories": 22, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Cucumber", "category": "Vegetables", "calories": 16, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss", "Weight Management"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Tomato", "category": "Vegetables", "calories": 18, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Onion", "category": "Vegetables", "calories": 40, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Mushroom", "category": "Vegetables", "calories": 22, "protein": 3, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Beetroot", "category": "Vegetables", "calories": 43, "protein": 2, "diet": "Vegan",
     "goals": ["Sports Performance", "General Health"], "sports": ["Running", "Cycling"], "allergens": []},
    {"name": "Zucchini", "category": "Vegetables", "calories": 17, "protein": 1, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Green Peas", "category": "Vegetables", "calories": 81, "protein": 5, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Bitter Gourd (Karela)", "category": "Vegetables", "calories": 20, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Okra (Bhindi)", "category": "Vegetables", "calories": 33, "protein": 2, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},

    # ---- More Meat / Fish / Poultry ----
    {"name": "Turkey Breast", "category": "Meat", "calories": 135, "protein": 30, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain", "Fat Loss"], "sports": ["Strength Training"], "allergens": []},
    {"name": "Lamb Chops", "category": "Meat", "calories": 294, "protein": 25, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain"], "sports": ["Strength Training"], "allergens": []},
    {"name": "Shrimp/Prawns", "category": "Fish", "calories": 99, "protein": 24, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain", "Fat Loss"], "sports": ["Swimming"], "allergens": []},
    {"name": "Crab", "category": "Fish", "calories": 97, "protein": 19, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain"], "sports": ["Swimming"], "allergens": []},
    {"name": "Pomfret Fry", "category": "Fish", "calories": 200, "protein": 22, "diet": "Non-Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Chicken Curry", "category": "Meat", "calories": 243, "protein": 22, "diet": "Non-Vegetarian",
     "goals": ["General Health", "Muscle Gain"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Kebab", "category": "Meat", "calories": 250, "protein": 20, "diet": "Non-Vegetarian",
     "goals": ["Muscle Gain"], "sports": ["Strength Training"], "allergens": []},

    # ---- More Dairy ----
    {"name": "Cottage Cheese", "category": "Dairy", "calories": 98, "protein": 11, "diet": "Vegetarian",
     "goals": ["Muscle Gain", "Fat Loss"], "sports": ["Strength Training"], "allergens": ["Dairy"]},
    {"name": "Butter", "category": "Dairy", "calories": 102, "protein": 0, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},
    {"name": "Ghee", "category": "Dairy", "calories": 112, "protein": 0, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},
    {"name": "Ice Cream", "category": "Dairy", "calories": 207, "protein": 4, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},
    {"name": "Lassi", "category": "Dairy", "calories": 150, "protein": 6, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},

    # ---- More Nuts / Seeds ----
    {"name": "Cashews", "category": "Nuts", "calories": 157, "protein": 5, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain"], "sports": ["General Fitness"], "allergens": ["Nuts"]},
    {"name": "Pistachios", "category": "Nuts", "calories": 159, "protein": 6, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Nuts"]},
    {"name": "Pumpkin Seeds", "category": "Nuts", "calories": 151, "protein": 7, "diet": "Vegan",
     "goals": ["General Health", "Muscle Gain"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Sunflower Seeds", "category": "Nuts", "calories": 164, "protein": 6, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},

    # ---- More Snacks / Prepared Foods (common scanner targets) ----
    {"name": "Pasta with Sauce", "category": "Snacks", "calories": 280, "protein": 9, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Biryani", "category": "Snacks", "calories": 350, "protein": 15, "diet": "Non-Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Pav Bhaji", "category": "Snacks", "calories": 300, "protein": 7, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten", "Dairy"]},
    {"name": "Pakora", "category": "Snacks", "calories": 315, "protein": 6, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Spring Roll", "category": "Snacks", "calories": 220, "protein": 4, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Momos", "category": "Snacks", "calories": 210, "protein": 6, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Chowmein", "category": "Snacks", "calories": 280, "protein": 8, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Vada Pav", "category": "Snacks", "calories": 290, "protein": 6, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Chaat", "category": "Snacks", "calories": 250, "protein": 5, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Donut", "category": "Snacks", "calories": 253, "protein": 3, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten", "Dairy"]},
    {"name": "Chocolate", "category": "Snacks", "calories": 155, "protein": 2, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},
    {"name": "Cookies", "category": "Snacks", "calories": 160, "protein": 2, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten", "Dairy"]},
    {"name": "Cake", "category": "Snacks", "calories": 235, "protein": 3, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten", "Dairy", "Eggs"]},
    {"name": "Gulab Jamun", "category": "Snacks", "calories": 175, "protein": 3, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy", "Gluten"]},
    {"name": "Jalebi", "category": "Snacks", "calories": 150, "protein": 1, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Chips (Potato)", "category": "Snacks", "calories": 152, "protein": 2, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Nachos", "category": "Snacks", "calories": 346, "protein": 8, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},
    {"name": "Waffle", "category": "Snacks", "calories": 218, "protein": 6, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten", "Eggs", "Dairy"]},
    {"name": "Pancake", "category": "Snacks", "calories": 175, "protein": 5, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten", "Eggs", "Dairy"]},
    {"name": "Sushi", "category": "Snacks", "calories": 200, "protein": 7, "diet": "Non-Vegetarian",
     "goals": ["General Health", "Sports Performance"], "sports": ["Swimming"], "allergens": []},
    {"name": "Taco", "category": "Snacks", "calories": 210, "protein": 9, "diet": "Non-Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy", "Gluten"]},
    {"name": "Hot Dog", "category": "Snacks", "calories": 290, "protein": 10, "diet": "Non-Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Fried Chicken", "category": "Snacks", "calories": 320, "protein": 22, "diet": "Non-Vegetarian",
     "goals": ["General Health", "Muscle Gain"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Wrap/Roll", "category": "Snacks", "calories": 245, "protein": 10, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Gluten"]},
    {"name": "Idli Sambhar", "category": "Snacks", "calories": 180, "protein": 6, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},

    # ---- More Beverages ----
    {"name": "Black Coffee", "category": "Beverages", "calories": 2, "protein": 0, "diet": "Vegan",
     "goals": ["General Health", "Fat Loss"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Masala Chai", "category": "Beverages", "calories": 60, "protein": 2, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},
    {"name": "Orange Juice", "category": "Beverages", "calories": 112, "protein": 2, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Soda/Cola", "category": "Beverages", "calories": 140, "protein": 0, "diet": "Vegan",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Energy Drink", "category": "Beverages", "calories": 110, "protein": 0, "diet": "Vegan",
     "goals": ["Sports Performance"], "sports": ["General Fitness"], "allergens": []},
    {"name": "Mango Lassi", "category": "Beverages", "calories": 180, "protein": 5, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},
    {"name": "Hot Chocolate", "category": "Beverages", "calories": 190, "protein": 8, "diet": "Vegetarian",
     "goals": ["General Health"], "sports": ["General Fitness"], "allergens": ["Dairy"]},
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