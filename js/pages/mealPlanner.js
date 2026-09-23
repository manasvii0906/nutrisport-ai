// ===== pages/mealPlanner.js =====
// Lets the user add foods to Breakfast/Lunch/Dinner/Snacks and
// compares the day's running totals against their nutrition targets.

let mealPlan = {
  Breakfast: [],
  Lunch: [],
  Dinner: [],
  Snacks: []
};

function initMealPlannerPage() {
  const foodSelect = document.getElementById('mp-food-select');
  if (!foodSelect) return; // page not in DOM yet

  // Populate food dropdown once from FOOD_DATABASE
  foodSelect.innerHTML = FOOD_DATABASE
    .map(f => `<option value="${f.id}">${f.name}</option>`)
    .join('');

  // Load any saved plan (persisted in localStorage)
  const saved = loadMealPlan();
  if (saved) mealPlan = saved;

  document.getElementById('mp-add-btn').addEventListener('click', handleAddFood);

  renderMealPlanner();
}

function handleAddFood() {
  const meal = document.getElementById('mp-meal-select').value;
  const foodId = document.getElementById('mp-food-select').value;
  const food = FOOD_DATABASE.find(f => f.id === Number(foodId));
  if (!food) return;

  mealPlan[meal].push(food);
  saveMealPlan(mealPlan);
  renderMealPlanner();
}

function removeFood(meal, index) {
  mealPlan[meal].splice(index, 1);
  saveMealPlan(mealPlan);
  renderMealPlanner();
}

function calculateTotals() {
  const totals = { calories: 0, protein: 0, carbs: 0, fat: 0 };
  Object.values(mealPlan).flat().forEach(food => {
    totals.calories += food.calories;
    totals.protein += food.protein;
    totals.carbs += food.carbs;
    totals.fat += food.fat;
  });
  return totals;
}

function renderMealPlanner() {
  const container = document.getElementById('mp-meals-container');
  if (!container) return;

  container.innerHTML = Object.keys(mealPlan).map(meal => `
    <div class="mp-meal-block">
      <h4>${meal}</h4>
      ${mealPlan[meal].length === 0
        ? `<p class="mp-empty">No items added yet.</p>`
        : mealPlan[meal].map((food, i) => `
            <div class="mp-food-row">
              <span>${food.name}</span>
              <span>${food.calories} kcal</span>
              <button type="button" class="mp-remove-btn" onclick="removeFood('${meal}', ${i})">✕</button>
            </div>
          `).join('')}
    </div>
  `).join('');

  renderTotals();
}

function renderTotals() {
  const grid = document.getElementById('mp-totals-grid');
  if (!grid) return;

  const totals = calculateTotals();
  const profile = Storage.getProfile();
  const targets = profile ? calculateNutritionTargets(profile) : null;

  grid.innerHTML = `
    <div class="target-item"><span>Calories</span><strong>${totals.calories}${targets ? ` / ${targets.calories}` : ''} kcal</strong></div>
    <div class="target-item"><span>Protein</span><strong>${totals.protein}${targets ? ` / ${targets.protein}` : ''} g</strong></div>
    <div class="target-item"><span>Carbs</span><strong>${totals.carbs}${targets ? ` / ${targets.carbs}` : ''} g</strong></div>
    <div class="target-item"><span>Fat</span><strong>${totals.fat}${targets ? ` / ${targets.fat}` : ''} g</strong></div>
  `;
}