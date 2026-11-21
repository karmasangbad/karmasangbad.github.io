// Live Job Search & Category Filter Script

const HASH_MAP = {
  '#all': 'all',
  '#wb-jobs': 'পশ্চিমবঙ্গ',
  '#central-jobs': 'কেন্দ্রীয়',
  '#police-jobs': 'পুলিশ',
  '#tenth-pass': 'মাধ্যমিক',
  '#ssc-jobs': 'ssc',
  '#karmasangsthan': 'কর্মসংস্থান'
};

function filterCategory(cat, btnElement) {
  const buttons = document.querySelectorAll('.filter-btn');
  buttons.forEach(btn => {
    btn.classList.remove('bg-emerald-600', 'text-white');
    btn.classList.add('bg-slate-200', 'text-slate-700');
  });

  // Find button to activate
  let targetBtn = btnElement;
  if (!targetBtn) {
    buttons.forEach(btn => {
      const onclickAttr = btn.getAttribute('onclick') || '';
      const filterAttr = btn.getAttribute('data-filter') || '';
      if (onclickAttr.includes(`'${cat}'`) || filterAttr === cat) {
        targetBtn = btn;
      }
    });
  }

  if (targetBtn) {
    targetBtn.classList.remove('bg-slate-200', 'text-slate-700');
    targetBtn.classList.add('bg-emerald-600', 'text-white');
  }

  const cards = document.querySelectorAll('.job-card');
  let visibleCount = 0;
  const searchCat = (cat || '').toLowerCase();

  cards.forEach(card => {
    const cardCategory = (card.getAttribute('data-category') || '').toLowerCase();
    const cardTitle = (card.getAttribute('data-title') || '').toLowerCase();
    const cardQual = (card.getAttribute('data-qualification') || '').toLowerCase();
    const cardDept = (card.getAttribute('data-department') || '').toLowerCase();

    let matches = false;
    if (searchCat === 'all') {
      matches = true;
    } else if (searchCat === 'মাধ্যমিক' || searchCat === 'tenth-pass') {
      matches = cardQual.includes('মাধ্যমিক') || cardQual.includes('১০ম') || cardQual.includes('10th') ||
                cardTitle.includes('মাধ্যমিক') || cardTitle.includes('১০ম') || cardCategory.includes('মাধ্যমিক') ||
                cardCategory.includes('১০ম');
    } else {
      matches = cardCategory.includes(searchCat) || cardTitle.includes(searchCat) || cardDept.includes(searchCat);
    }

    if (matches) {
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
    const title = (card.getAttribute('data-title') || '').toLowerCase();
    const category = (card.getAttribute('data-category') || '').toLowerCase();
    const department = (card.getAttribute('data-department') || '').toLowerCase();
    const qual = (card.getAttribute('data-qualification') || '').toLowerCase();

    if (title.includes(searchTerm) || category.includes(searchTerm) || department.includes(searchTerm) || qual.includes(searchTerm)) {
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

function handleHashNavigation() {
  const hash = window.location.hash.toLowerCase();
  if (hash && HASH_MAP[hash]) {
    const targetCategory = HASH_MAP[hash];
    filterCategory(targetCategory);

    // Smooth scroll to jobs section
    const targetEl = document.getElementById('jobs-section') || document.getElementById('jobListingsContainer');
    if (targetEl) {
      targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

  // Handle URL hash on initial load
  handleHashNavigation();

  // Listen for hash change (e.g., clicking on #tenth-pass in footer)
  window.addEventListener('hashchange', handleHashNavigation);
});
