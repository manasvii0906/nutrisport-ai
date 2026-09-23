// ===== storage.js =====
// Centralized localStorage helpers for the whole app.

const STORAGE_KEYS = {
  PROFILE: 'nutrisport_profile',
  FOOD_LOG: 'nutrisport_food_log',
  WATER: 'nutrisport_water'
};

const Storage = {
  saveProfile(profile) {
    localStorage.setItem(STORAGE_KEYS.PROFILE, JSON.stringify(profile));
  },
  getProfile() {
    const data = localStorage.getItem(STORAGE_KEYS.PROFILE);
    return data ? JSON.parse(data) : null;
  },
  
  clearProfile() {
    localStorage.removeItem(STORAGE_KEYS.PROFILE);
  }
  
};
// ===== Meal Planner persistence =====
function saveMealPlan(plan) {
  localStorage.setItem('nutrisport_mealplan', JSON.stringify(plan));
}

function loadMealPlan() {
  const data = localStorage.getItem('nutrisport_mealplan');
  return data ? JSON.parse(data) : null;
}
// ===== Food Log persistence (keyed by date) =====
function getAllFoodLogs() {
  const data = localStorage.getItem(STORAGE_KEYS.FOOD_LOG);
  return data ? JSON.parse(data) : {};
}

function saveFoodLogForDate(dateStr, entries) {
  const all = getAllFoodLogs();
  all[dateStr] = entries;
  localStorage.setItem(STORAGE_KEYS.FOOD_LOG, JSON.stringify(all));
}

function getFoodLogForDate(dateStr) {
  const all = getAllFoodLogs();
  return all[dateStr] || [];
}

function getLoggedDatesSummary() {
  const all = getAllFoodLogs();
  return Object.keys(all)
    .sort((a, b) => b.localeCompare(a)) // newest first
    .map(date => {
      const entries = all[date];
      const totalCalories = entries.reduce((sum, f) => sum + f.calories, 0);
      return { date, totalCalories, count: entries.length };
    });
}