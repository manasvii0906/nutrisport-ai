// ===== pages/dashboard.js =====
// Calculates BMI + estimated daily nutrition targets, renders the dashboard.

function calculateBMR(profile) {
  // Mifflin-St Jeor Equation (widely used, reasonably accurate estimate)
  const { weight, height, age, gender } = profile;
  let bmr = (10 * weight) + (6.25 * height) - (5 * age);
  bmr += (gender === 'male') ? 5 : -161; // 'other' defaults to female offset
  return bmr;
}

function getActivityMultiplier(activityLevel) {
  const multipliers = {
    sedentary: 1.2,
    light: 1.375,
    moderate: 1.55,
    veryActive: 1.725,
    athlete: 1.9
  };
  return multipliers[activityLevel] || 1.2;
}

function getGoalAdjustment(goal) {
  // Simple calorie adjustment based on goal (educational estimate, not prescriptive)
  const adjustments = {
    fatLoss: -0.15,          // ~15% deficit
    weightManagement: -0.05, // slight deficit
    muscleGain: 0.10,        // ~10% surplus
    sportsPerformance: 0.05, // slight surplus for fueling
    generalHealth: 0
  };
  return adjustments[goal] ?? 0;
}

function calculateNutritionTargets(profile) {
  const bmr = calculateBMR(profile);
  const tdee = bmr * getActivityMultiplier(profile.activityLevel);
  const goalAdjustment = getGoalAdjustment(profile.goal);
  const calories = Math.round(tdee * (1 + goalAdjustment));

  // Macro split varies slightly by goal (educational approximation)
  let proteinPerKg = 1.6; // default g/kg bodyweight
  if (profile.goal === 'muscleGain' || profile.goal === 'sportsPerformance') proteinPerKg = 1.8;
  if (profile.goal === 'fatLoss') proteinPerKg = 2.0; // higher protein helps preserve muscle in a deficit

  const protein = Math.round(profile.weight * proteinPerKg);
  const proteinCals = protein * 4;

  const fatCals = calories * 0.27; // ~27% of calories from fat
  const fat = Math.round(fatCals / 9);

  const remainingCals = calories - proteinCals - fatCals;
  const carbs = Math.round(remainingCals / 4);

  const fiber = Math.round((calories / 1000) * 14); // standard 14g per 1000 kcal guideline
  const waterLiters = Math.round((profile.weight * 0.033) * 10) / 10; // ~33ml per kg bodyweight

  return { calories, protein, carbs, fat, fiber, waterLiters };
}

function renderDashboard() {
  const container = document.getElementById('page-dashboard');
  const profile = Storage.getProfile();

  if (!profile) {
    container.innerHTML = `
      <div class="placeholder-card">
        <h2>📊 Dashboard</h2>
        <p>No profile found yet. Please fill out your Profile first to see your personalized dashboard.</p>
      </div>
    `;
    return;
  }

  const bmi = calculateBMI(profile.weight, profile.height);
  const bmiCategory = getBMICategory(bmi);
  const targets = calculateNutritionTargets(profile);

  container.innerHTML = `
    <div class="dashboard-grid">

      <div class="dash-card profile-summary">
        <h3>👤 ${profile.name}'s Profile</h3>
        <div class="summary-row"><span>Height</span><strong>${profile.height} cm</strong></div>
        <div class="summary-row"><span>Weight</span><strong>${profile.weight} kg</strong></div>
        <div class="summary-row"><span>Activity Level</span><strong>${profile.activityLevel}</strong></div>
        <div class="summary-row"><span>Goal</span><strong>${profile.goal}</strong></div>
        <div class="summary-row"><span>Sport</span><strong>${profile.sport}</strong></div>
      </div>

      <div class="dash-card bmi-card">
        <h3>⚖️ BMI</h3>
        <div class="bmi-value">${bmi}</div>
        <div class="bmi-category ${bmiCategory.toLowerCase()}">${bmiCategory}</div>
        <p class="disclaimer-small">BMI is a general screening measure only and does not account for muscle mass or body composition.</p>
      </div>

            <div class="dash-card targets-card full-width">
        <h3>🎯 Estimated Daily Nutrition Targets</h3>
        <div class="targets-grid">
          <div class="target-item"><span>Calories</span><strong>${targets.calories} kcal</strong></div>
          <div class="target-item"><span>Protein</span><strong>${targets.protein} g</strong></div>
          <div class="target-item"><span>Carbohydrates</span><strong>${targets.carbs} g</strong></div>
          <div class="target-item"><span>Fats</span><strong>${targets.fat} g</strong></div>
          <div class="target-item"><span>Fiber</span><strong>${targets.fiber} g</strong></div>
          <div class="target-item"><span>Water</span><strong>${targets.waterLiters} L</strong></div>
        </div>
        <p class="disclaimer-small">These are estimated targets based on standard formulas, not a medical prescription. Actual needs vary by individual.</p>
      </div>

      <div class="dash-card full-width">
        <h3>🍽️ What Should I Eat?</h3>
        <p class="form-subtitle">Based on your goal (${profile.goal}), sport (${profile.sport}), diet, and allergies.</p>
        <div class="rec-grid">
          ${getRecommendations(profile).map(food => `
            <div class="rec-card">
              <div class="rec-card-header">
                <h4>${food.name}</h4>
                <span class="food-category-tag">${food.category}</span>
              </div>
              <div class="rec-macros">
                <span>${food.calories} kcal</span>
                <span>${food.protein}g protein</span>
              </div>
              <p class="fit-message">💡 ${food.reason}</p>
            </div>
          `).join("")}
        </div>
      </div>

    </div>
  `;
}


function initDashboardPage() {
  renderDashboard();
}