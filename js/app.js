// ===== app.js =====
// Handles sidebar navigation: switching between "pages" without reloading.

document.addEventListener('DOMContentLoaded', () => {
  const navItems = document.querySelectorAll('.nav-item');
  const pages = document.querySelectorAll('.page');
  const pageTitle = document.getElementById('page-title');

  initProfilePage();

  // Human-readable titles for the header
  const titles = {
    dashboard: 'Dashboard',
    profile: 'Profile',
    mealPlanner: 'Meal Planner',
    foodDatabase: 'Food Database',
    scanner: 'AI Food Scanner',
    foodLog: 'Food Log',
    progress: 'Progress',
    insights: 'Insights'
  };

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const pageKey = item.getAttribute('data-page');

      // Update active nav button
      navItems.forEach(nav => nav.classList.remove('active'));
      item.classList.add('active');

      // Show the matching page, hide the rest
      pages.forEach(page => page.classList.remove('active'));
      document.getElementById('page-' + pageKey).classList.add('active');

      // Update header title
      pageTitle.textContent = titles[pageKey] || pageKey;
    });
  });
});