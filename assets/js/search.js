// Live Job Search & Category Filter Script

function filterCategory(cat) {
  // Update button active styling
  const buttons = document.querySelectorAll('.filter-btn');
  buttons.forEach(btn => {
    btn.classList.remove('bg-emerald-600', 'text-white');
    btn.classList.add('bg-slate-200', 'text-slate-700');
  });

  const activeBtn = event.target;
  activeBtn.classList.remove('bg-slate-200', 'text-slate-700');
  activeBtn.classList.add('bg-emerald-600', 'text-white');

  const cards = document.querySelectorAll('.job-card');
  let visibleCount = 0;

  cards.forEach(card => {
    const cardCategory = card.getAttribute('data-category') || '';
    if (cat === 'all' || cardCategory.includes(cat.toLowerCase())) {
      card.style.display = 'block';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });

  updateJobCount(visibleCount);
  checkEmptyState(visibleCount);
}

function handleSearch(query) {
  const searchTerm = query.toLowerCase().trim();
  const cards = document.querySelectorAll('.job-card');
  let visibleCount = 0;

  cards.forEach(card => {
    const title = card.getAttribute('data-title') || '';
    const category = card.getAttribute('data-category') || '';
    const department = card.getAttribute('data-department') || '';

    if (title.includes(searchTerm) || category.includes(searchTerm) || department.includes(searchTerm)) {
      card.style.display = 'block';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });

  updateJobCount(visibleCount);
  checkEmptyState(visibleCount);
}

function updateJobCount(count) {
  const display = document.getElementById('jobCountDisplay');
  if (display) {
    display.textContent = `বিজ্ঞপ্তি প্রদর্শিত হচ্ছে: ${count} টি`;
  }
}

function checkEmptyState(count) {
  const noResults = document.getElementById('noResults');
  if (noResults) {
    if (count === 0) {
      noResults.classList.remove('hidden');
    } else {
      noResults.classList.add('hidden');
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const liveSearch = document.getElementById('liveSearchInput');
  const headerSearch = document.getElementById('headerSearchInput');

  if (liveSearch) {
    liveSearch.addEventListener('input', (e) => handleSearch(e.target.value));
  }
  if (headerSearch) {
    headerSearch.addEventListener('input', (e) => {
      if (liveSearch) liveSearch.value = e.target.value;
      handleSearch(e.target.value);
    });
  }
});
