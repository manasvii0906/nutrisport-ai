// ===== pages/foodLog.js =====
// Daily food log: user picks a date, logs foods eaten that day,
// sees totals vs. targets, and can browse a history of past dates.

let currentLogDate = todayStr();
let currentLogEntries = [];

function todayStr() {
  const d = new Date();
  return d.toISOString().split('T')[0]; // YYYY-MM-DD
}

function initFoodLogPage() {
  const foodSelect = document.getElementById('fl-food-select');
  const datePicker = document.getElementById('fl-date-picker');
  if (!foodSelect || !datePicker) return; // page not in DOM yet

  foodSelect.innerHTML = FOOD_DATABASE
    .map(f => `<option value="${f.id}">${f.name}</option>`)
    .join('');

  datePicker.value = currentLogDate;
  currentLogEntries = getFoodLogForDate(currentLogDate);

  datePicker.addEventListener('change', () => {
    currentLogDate = datePicker.value;
    currentLogEntries = getFoodLogForDate(currentLogDate);
    renderFoodLog();
  });

  document.getElementById('fl-add-btn').addEventListener('click', handleAddLogFood);

  renderFoodLog();
}

function handleAddLogFood() {
  const foodId = document.getElementById('fl-food-select').value;
  const food = FOOD_DATABASE.find(f => f.id === Number(foodId));
  if (!food) return;

  currentLogEntries.push(food);
  saveFoodLogForDate(currentLogDate, currentLogEntries);
  renderFoodLog();
}

function removeLogEntry(index) {
  currentLogEntries.splice(index, 1);
  saveFoodLogForDate(currentLogDate, currentLogEntries);
  renderFoodLog();
}

function jumpToLogDate(dateStr) {
  currentLogDate = dateStr;
  currentLogEntries = getFoodLogForDate(dateStr);
  document.getElementById('fl-date-picker').value = dateStr;
  renderFoodLog();
}

function calculateLogTotals() {
  const totals = { calories: 0, protein: 0, carbs: 0, fat: 0 };
  currentLogEntries.forEach(food => {
    totals.calories += food.calories;
    totals.protein += food.protein;
    totals.carbs += food.carbs;
    totals.fat += food.fat;
  });
  return totals;
}

function renderFoodLog() {
  const container = document.getElementById('fl-entries-container');
  if (!container) return;

  container.innerHTML = currentLogEntries.length === 0
    ? `<p class="mp-empty">No foods logged for this date yet.</p>`
    : currentLogEntries.map((food, i) => `
        <div class="mp-food-row">
          <span>${food.name}</span>
          <span>${food.calories} kcal</span>
          <button type="button" class="mp-remove-btn" onclick="removeLogEntry(${i})">✕</button>
        </div>
      `).join('');

  renderLogTotals();
  renderLogHistory();
}

function renderLogTotals() {
  const grid = document.getElementById('fl-totals-grid');
  if (!grid) return;

  const totals = calculateLogTotals();
  const profile = Storage.getProfile();
  const targets = profile ? calculateNutritionTargets(profile) : null;

  grid.innerHTML = `
    <div class="target-item"><span>Calories</span><strong>${totals.calories}${targets ? ` / ${targets.calories}` : ''} kcal</strong></div>
    <div class="target-item"><span>Protein</span><strong>${totals.protein}${targets ? ` / ${targets.protein}` : ''} g</strong></div>
    <div class="target-item"><span>Carbs</span><strong>${totals.carbs}${targets ? ` / ${targets.carbs}` : ''} g</strong></div>
    <div class="target-item"><span>Fat</span><strong>${totals.fat}${targets ? ` / ${targets.fat}` : ''} g</strong></div>
  `;
}

function renderLogHistory() {
  const list = document.getElementById('fl-history-list');
  if (!list) return;

  const summary = getLoggedDatesSummary();

  list.innerHTML = summary.length === 0
    ? `<p class="mp-empty">No logged days yet.</p>`
    : summary.map(entry => `
        <div class="mp-food-row" style="cursor:pointer" onclick="jumpToLogDate('${entry.date}')">
          <span>${entry.date}${entry.date === currentLogDate ? ' (viewing)' : ''}</span>
          <span>${entry.count} items — ${entry.totalCalories} kcal</span>
        </div>
      `).join('');
}