// ===== pages/foodDatabase.js =====
// Search and display foods from FOOD_DATABASE.

function goalFitMessage(food) {
  if (food.goals.length === 0) return "General snack — best in moderation, not tied to a specific fitness goal.";
  const readable = {
    generalHealth: "general health",
    weightManagement: "weight management",
    muscleGain: "muscle gain",
    fatLoss: "fat loss",
    sportsPerformance: "sports performance"
  };
  const goalNames = food.goals.map(g => readable[g] || g).join(", ");
  return `May fit a diet focused on: ${goalNames}.`;
}

function renderFoodCard(food) {
  return `
    <div class="food-result-card">
      <div class="food-result-header">
        <h4>${food.name}</h4>
        <span class="food-category-tag">${food.category}</span>
      </div>
      <p class="food-serving">Serving: ${food.servingSize}</p>
      <div class="targets-grid">
        <div class="target-item"><span>Calories</span><strong>${food.calories}</strong></div>
        <div class="target-item"><span>Protein</span><strong>${food.protein}g</strong></div>
        <div class="target-item"><span>Carbs</span><strong>${food.carbs}g</strong></div>
        <div class="target-item"><span>Fat</span><strong>${food.fat}g</strong></div>
        <div class="target-item"><span>Fiber</span><strong>${food.fiber}g</strong></div>
      </div>
      ${food.allergens.length > 0 ? `<p class="allergen-tag">⚠ Contains: ${food.allergens.join(", ")}</p>` : ""}
      <p class="fit-message">💡 ${goalFitMessage(food)}</p>
    </div>
  `;
}

function searchFoods(query) {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  return FOOD_DATABASE.filter(f => f.name.toLowerCase().includes(q));
}

function initFoodDatabasePage() {
  const input = document.getElementById('food-search-input');
  const resultsContainer = document.getElementById('food-search-results');
  if (!input) return;

  input.addEventListener('input', () => {
    const results = searchFoods(input.value);
    if (input.value.trim() === "") {
      resultsContainer.innerHTML = `<p class="search-hint">Start typing a food name (e.g. "egg", "banana", "rice") to search.</p>`;
      return;
    }
    if (results.length === 0) {
      resultsContainer.innerHTML = `<p class="search-hint">No foods found matching "${input.value}".</p>`;
      return;
    }
    resultsContainer.innerHTML = results.map(renderFoodCard).join("");
  });
}