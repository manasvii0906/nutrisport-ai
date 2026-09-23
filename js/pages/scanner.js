// ===== pages/scanner.js =====
// Real client-side image recognition using TensorFlow.js + MobileNet.
// No API key, no server calls, no billing risk — model runs fully in-browser.

let mobilenetModel = null;
let modelLoadingPromise = null;

// Maps common ImageNet/MobileNet labels to entries in FOOD_DATABASE.
// MobileNet returns general ImageNet class names, so we match keywords.
const IMAGENET_TO_FOOD_KEYWORDS = {
  banana: ['banana'],
  pizza: ['pizza'],
  cheeseburger: ['burger'],
  hamburger: ['burger'],
  hotdog: ['hot dog', 'sausage'],
  bagel: ['bread', 'bagel'],
  pretzel: ['bread'],
  'French loaf': ['bread'],
  guacamole: ['avocado'],
  broccoli: ['broccoli'],
  cucumber: ['cucumber'],
  'bell pepper': ['pepper', 'capsicum'],
  mushroom: ['mushroom'],
  orange: ['orange'],
  lemon: ['lemon'],
  strawberry: ['strawberry'],
  pineapple: ['pineapple'],
  pomegranate: ['pomegranate'],
  fig: ['fig'],
  'ice cream': ['ice cream'],
  trifle: ['dessert'],
  chocolate: ['chocolate'],
  espresso: ['coffee'],
  cup: ['tea', 'coffee'],
  soup_bowl: ['soup', 'dal', 'curry'],
  potpie: ['curry', 'stew'],
  plate: ['rice', 'meal'],
  consomme: ['soup'],
  carbonara: ['pasta'],
  burrito: ['wrap', 'roti'],
  taco: ['wrap']
};

function initScannerPage() {
  const fileInput = document.getElementById('scanner-file-input');
  if (fileInput) {
    fileInput.addEventListener('change', handleScannerFileChange);
  }
}

function loadMobilenetModel() {
  if (mobilenetModel) return Promise.resolve(mobilenetModel);
  if (modelLoadingPromise) return modelLoadingPromise;

  const statusEl = document.getElementById('scanner-status');
  if (statusEl) statusEl.innerHTML = `<p class="mp-empty">Loading AI model (first time only, ~5-10s)...</p>`;

  modelLoadingPromise = mobilenet.load().then(model => {
    mobilenetModel = model;
    if (statusEl) statusEl.innerHTML = '';
    return model;
  }).catch(err => {
    if (statusEl) statusEl.innerHTML = `<p class="mp-empty">Failed to load AI model. Check your internet connection (CDN required to load the model file once).</p>`;
    throw err;
  });

  return modelLoadingPromise;
}

async function handleScannerFileChange(e) {
  const file = e.target.files[0];
  if (!file) return;

  const previewContainer = document.getElementById('scanner-preview-container');
  const resultsContainer = document.getElementById('scanner-results');
  const statusEl = document.getElementById('scanner-status');
  resultsContainer.innerHTML = '';

  const imgUrl = URL.createObjectURL(file);
  previewContainer.innerHTML = `<img id="scanner-img" src="${imgUrl}" class="scanner-preview-img" />`;

  const imgEl = document.getElementById('scanner-img');
  imgEl.onload = async () => {
    try {
      const model = await loadMobilenetModel();
      statusEl.innerHTML = `<p class="mp-empty">Analyzing image...</p>`;
      const predictions = await model.classify(imgEl, 5);
      statusEl.innerHTML = '';
      renderScannerResults(predictions);
    } catch (err) {
      console.error(err);
      statusEl.innerHTML = `<p class="mp-empty">Recognition failed. Try a different photo.</p>`;
    }
  };
}

function renderScannerResults(predictions) {
  const resultsContainer = document.getElementById('scanner-results');

  const matches = [];
  predictions.forEach(p => {
    const label = p.className.split(',')[0].trim();
    for (const [imagenetLabel, keywords] of Object.entries(IMAGENET_TO_FOOD_KEYWORDS)) {
      if (label.toLowerCase().includes(imagenetLabel.toLowerCase())) {
        keywords.forEach(kw => {
          const foodMatch = FOOD_DATABASE.find(f => f.name.toLowerCase().includes(kw.toLowerCase()));
          if (foodMatch && !matches.find(m => m.id === foodMatch.id)) {
            matches.push(foodMatch);
          }
        });
      }
    }
  });

  const rawLabelsHtml = predictions.map(p =>
    `<span class="scanner-raw-label">${p.className.split(',')[0]} (${Math.round(p.probability * 100)}%)</span>`
  ).join(' ');

  let matchesHtml = '';
  if (matches.length > 0) {
    matchesHtml = `
      <h3>Matched foods in database:</h3>
      <div class="scanner-match-grid">
        ${matches.map(f => `
          <div class="scanner-match-card">
            <strong>${f.name}</strong>
            <span>${f.calories} kcal per ${f.servingSize}</span>
            <button class="btn-secondary" onclick="quickAddToLog(${f.id})">+ Add to Food Log</button>
          </div>
        `).join('')}
      </div>
    `;
  } else {
    matchesHtml = `<p class="mp-empty">No direct match found in your food database. Raw AI labels are shown below — add the food manually via Food Log if needed.</p>`;
  }

  resultsContainer.innerHTML = `
    ${matchesHtml}
    <div class="scanner-raw-labels">
      <span class="scanner-raw-title">Raw AI labels:</span> ${rawLabelsHtml}
    </div>
  `;
}

// Quick-add helper: logs a food for today's date using default serving size.
function quickAddToLog(foodId) {
  const food = FOOD_DATABASE.find(f => f.id === foodId);
  if (!food) return;

  const today = new Date().toISOString().slice(0, 10);
  const existingEntries = getFoodLogForDate(today);
  existingEntries.push(food);
  saveFoodLogForDate(today, existingEntries);

  alert(`Added ${food.name} to today's Food Log.`);
}