// ===== pages/profile.js =====
// Handles the onboarding/profile form: rendering, validation, BMI calc, saving.

function calculateBMI(weightKg, heightCm) {
  const heightM = heightCm / 100;
  const bmi = weightKg / (heightM * heightM);
  return Math.round(bmi * 10) / 10; // round to 1 decimal
}

function getBMICategory(bmi) {
  if (bmi < 18.5) return 'Underweight';
  if (bmi < 25) return 'Normal';
  if (bmi < 30) return 'Overweight';
  return 'Obese';
}

function initProfilePage() {
  const form = document.getElementById('profile-form');
  if (!form) return;

  // Pre-fill form if a profile already exists
  const existing = Storage.getProfile();
  if (existing) {
    Object.entries(existing).forEach(([key, value]) => {
      const field = form.elements[key];
      if (!field) return;
      if (field.type === 'checkbox') {
        // handled separately for allergies below
      } else {
        field.value = value;
      }
    });
    // Re-check allergy checkboxes
    if (existing.allergies) {
      existing.allergies.forEach(a => {
        const cb = form.querySelector(`input[name="allergies"][value="${a}"]`);
        if (cb) cb.checked = true;
      });
    }
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const allergies = formData.getAll('allergies');

    const profile = {
      name: formData.get('name'),
      age: Number(formData.get('age')),
      gender: formData.get('gender'),
      height: Number(formData.get('height')),
      weight: Number(formData.get('weight')),
      activityLevel: formData.get('activityLevel'),
      dietaryPreference: formData.get('dietaryPreference'),
      allergies: allergies,
      goal: formData.get('goal'),
      sport: formData.get('sport'),
      mealPreference: formData.get('mealPreference')
    };

    Storage.saveProfile(profile);
    showProfileSavedMessage();
  });
}

function showProfileSavedMessage() {
  const msg = document.getElementById('profile-saved-msg');
  if (!msg) return;
  msg.style.display = 'block';
  setTimeout(() => { msg.style.display = 'none'; }, 2500);
}