// ===== pages/progress.js =====
// Renders a simple bar chart of calorie intake per logged day (Progress page),
// and rule-based text observations from that same data (Insights page).

function initProgressPage() {
  renderProgressChart();
}

function initInsightsPage() {
  renderInsights();
}

function renderProgressChart() {
  const container = document.getElementById('progress-chart-container');
  if (!container) return;

  const summary = getLoggedDatesSummary().slice().reverse(); // oldest first for chart order

  if (summary.length === 0) {
    container.innerHTML = `<p class="mp-empty">No logged days yet. Add entries in Food Log to see your progress here.</p>`;
    return;
  }

  const maxCalories = Math.max(...summary.map(d => d.totalCalories), 1);

  container.innerHTML = `
    <div class="chart-bars">
      ${summary.map(d => `
        <div class="chart-bar-col">
          <div class="chart-bar" style="height:${Math.round((d.totalCalories / maxCalories) * 180)}px;">
            <span class="chart-bar-value">${d.totalCalories}</span>
          </div>
          <span class="chart-bar-label">${d.date.slice(5)}</span>
        </div>
      `).join('')}
    </div>
  `;
}

function renderInsights() {
  const container = document.getElementById('insights-container');
  if (!container) return;

  const summary = getLoggedDatesSummary();
  const profile = Storage.getProfile();

  if (summary.length === 0) {
    container.innerHTML = `<p class="mp-empty">No logged days yet. Add entries in Food Log to generate insights.</p>`;
    return;
  }

  const insights = [];
  const totalDays = summary.length;
  const avgCalories = Math.round(summary.reduce((sum, d) => sum + d.totalCalories, 0) / totalDays);

  insights.push(`You've logged food on <strong>${totalDays}</strong> day${totalDays > 1 ? 's' : ''}.`);
  insights.push(`Your average logged intake is <strong>${avgCalories} kcal/day</strong>.`);

  if (profile) {
    const targets = calculateNutritionTargets(profile);
    const diff = avgCalories - targets.calories;
    if (Math.abs(diff) <= 100) {
      insights.push(`This is close to your daily target of ${targets.calories} kcal — nice consistency.`);
    } else if (diff > 100) {
      insights.push(`This is <strong>${diff} kcal above</strong> your daily target of ${targets.calories} kcal on average.`);
    } else {
      insights.push(`This is <strong>${Math.abs(diff)} kcal below</strong> your daily target of ${targets.calories} kcal on average.`);
    }
  } else {
    insights.push(`Complete your Profile to compare this against a personalized target.`);
  }

  const highest = summary.reduce((a, b) => (a.totalCalories > b.totalCalories ? a : b));
  const lowest = summary.reduce((a, b) => (a.totalCalories < b.totalCalories ? a : b));
  insights.push(`Highest intake day: <strong>${highest.date}</strong> (${highest.totalCalories} kcal). Lowest: <strong>${lowest.date}</strong> (${lowest.totalCalories} kcal).`);

  container.innerHTML = `
    <div class="insights-list">
      ${insights.map(text => `<div class="insight-card">💡 ${text}</div>`).join('')}
    </div>
  `;
}