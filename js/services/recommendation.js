// ===== services/recommendation.js =====
// Personalized recommendation engine.
// Filters + scores foods from FOOD_DATABASE based on the user's profile.

function isSafeForProfile(food, profile) {
  // Exclude foods with allergens the user has marked (skip if "none" is selected)
  const userAllergies = (profile.allergies || []).filter(a => a !== 'none');
  const hasAllergen = food.allergens.some(a => userAllergies.includes(a));
  if (hasAllergen) return false;

  // Exclude non-vegetarian foods if user follows a vegetarian/vegan/eggetarian diet
  if (profile.dietaryPreference === 'vegetarian' && !food.vegetarian) return false;
  if (profile.dietaryPreference === 'vegan' && (!food.vegetarian || food.allergens.includes('dairy') || food.allergens.includes('eggs'))) return false;
  if (profile.dietaryPreference === 'eggetarian' && !food.vegetarian && !food.name.toLowerCase().includes('egg')) return false;

  return true;
}

function scoreFood(food, profile) {
  let score = 0;

  // +3 if this food explicitly matches the user's goal
  if (food.goals.includes(profile.goal)) score += 3;

  // +3 if this food explicitly matches the user's sport
  if (food.sports.includes(profile.sport)) score += 3;

  // +1 baseline for any food that isn't a pure snack (encourages whole foods)
  if (food.category !== 'Snacks') score += 1;

  return score;
}

function explainRecommendation(food, profile) {
  const reasons = [];
  const goalReadable = {
    generalHealth: "general health",
    weightManagement: "weight management",
    muscleGain: "muscle gain",
    fatLoss: "fat loss",
    sportsPerformance: "sports performance"
  };
  const sportReadable = {
    basketball: "basketball", football: "football", cricket: "cricket",
    running: "running", swimming: "swimming", cycling: "cycling",
    tennis: "tennis", badminton: "badminton", strengthTraining: "strength training",
    generalFitness: "general fitness", other: "your sport"
  };

  if (food.goals.includes(profile.goal)) {
    reasons.push(`fits your ${goalReadable[profile.goal] || profile.goal} goal`);
  }
  if (food.sports.includes(profile.sport)) {
    reasons.push(`commonly recommended for ${sportReadable[profile.sport] || profile.sport}`);
  }
  if (food.protein >= 15) {
    reasons.push("good protein content");
  }
  if (food.fiber >= 4) {
    reasons.push("good source of fiber");
  }

  if (reasons.length === 0) {
    return "A safe option based on your dietary preference and allergy filters.";
  }
  return "This may " + reasons.join(" and ") + ".";
}

function getRecommendations(profile, limit = 6) {
  const safeFoods = FOOD_DATABASE.filter(f => isSafeForProfile(f, profile));

  const scored = safeFoods.map(food => ({
    food,
    score: scoreFood(food, profile)
  }));

  // Sort highest score first; foods with score 0 still show, just last
  scored.sort((a, b) => b.score - a.score);

  return scored.slice(0, limit).map(item => ({
    ...item.food,
    reason: explainRecommendation(item.food, profile)
  }));
}