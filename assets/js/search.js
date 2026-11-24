// Live Job Search & Pan-India Category / State Filter Script

const HASH_MAP = {
  '#all': { type: 'category', value: 'all' },
  '#central-jobs': { type: 'category', value: 'central' },
  '#railway-jobs': { type: 'category', value: 'railway' },
  '#bank-jobs': { type: 'category', value: 'bank' },
  '#defence-jobs': { type: 'category', value: 'defence' },
  '#police-jobs': { type: 'category', value: 'defence' },
  '#state-jobs': { type: 'category', value: 'state' },
  '#wb-jobs': { type: 'state', value: 'west bengal' },
  '#tenth-pass': { type: 'category', value: '10th' },
  '#twelfth-pass': { type: 'category', value: '12th' },
  '#iti-diploma': { type: 'category', value: 'diploma' },
  '#graduate-jobs': { type: 'category', value: 'graduate' },
  '#employment-news': { type: 'category', value: 'employment' },
  '#karmasangsthan': { type: 'category', value: 'employment' }
};

let currentCategoryFilter = 'all';
let currentStateFilter = 'all';
let currentSearchTerm = '';

function applyAllFilters() {
  const cards = document.querySelectorAll('.job-card');
  let visibleCount = 0;

  cards.forEach(card => {
    const title = (card.getAttribute('data-title') || '').toLowerCase();
    const category = (card.getAttribute('data-category') || '').toLowerCase();
    const department = (card.getAttribute('data-department') || '').toLowerCase();
    const qualification = (card.getAttribute('data-qualification') || '').toLowerCase();
    const state = (card.getAttribute('data-state') || '').toLowerCase();

    // 1. Category Check
    let matchesCategory = false;
    if (currentCategoryFilter === 'all') {
      matchesCategory = true;
    } else if (currentCategoryFilter === 'central') {
      matchesCategory = category.includes('central') || category.includes('ssc') || category.includes('upsc') || 
                        category.includes('কেন্দ্রীয়') || department.includes('staff selection') || department.includes('upsc');
    } else if (currentCategoryFilter === 'railway') {
      matchesCategory = category.includes('railway') || category.includes('রেলওয়ে') || category.includes('rrb') ||
                        department.includes('railway') || title.includes('railway') || title.includes('rrb');
    } else if (currentCategoryFilter === 'bank') {
      matchesCategory = category.includes('bank') || category.includes('ব্যাংক') || category.includes('ibps') ||
                        category.includes('sbi') || department.includes('bank') || department.includes('ibps');
    } else if (currentCategoryFilter === 'defence') {
      matchesCategory = category.includes('defence') || category.includes('police') || category.includes('পুলিশ') ||
                        category.includes('army') || category.includes('navy') || category.includes('air force') ||
                        department.includes('police') || department.includes('defence');
    } else if (currentCategoryFilter === 'state') {
      matchesCategory = !category.includes('central') && (
        category.includes('state') || category.includes('পশ্চিমবঙ্গ') || category.includes('west bengal') ||
        state !== 'all india' || category.includes('psc') || department.includes('psc')
      );
    } else if (currentCategoryFilter === '10th') {
      matchesCategory = qualification.includes('10th') || qualification.includes('matric') || qualification.includes('secondary') ||
                        qualification.includes('মাধ্যমিক') || qualification.includes('১০ম') || title.includes('10th') || title.includes('১০ম');
    } else if (currentCategoryFilter === '12th') {
      matchesCategory = qualification.includes('12th') || qualification.includes('inter') || qualification.includes('higher secondary') ||
                        qualification.includes('উচ্চ মাধ্যমিক') || qualification.includes('১২শ') || title.includes('12th');
    } else if (currentCategoryFilter === 'diploma') {
      matchesCategory = qualification.includes('iti') || qualification.includes('diploma') || qualification.includes('polytechnic') ||
                        title.includes('iti') || title.includes('diploma') || title.includes('apprentice');
    } else if (currentCategoryFilter === 'graduate') {
      matchesCategory = qualification.includes('graduate') || qualification.includes('degree') || qualification.includes('b.e') ||
                        qualification.includes('b.tech') || qualification.includes('স্নাতক');
    } else if (currentCategoryFilter === 'employment') {
      matchesCategory = category.includes('employment') || category.includes('কর্মসংস্থান') || category.includes('karmakshetra') ||
                        title.includes('employment news') || title.includes('karmasangsthan');
    } else {
      matchesCategory = category.includes(currentCategoryFilter) || title.includes(currentCategoryFilter);
    }

    // 2. State Check
    let matchesState = false;
    if (currentStateFilter === 'all') {
      matchesState = true;
    } else if (currentStateFilter === 'central') {
      matchesState = state.includes('all india') || state.includes('central') || category.includes('central') || category.includes('কেন্দ্রীয়');
    } else {
      matchesState = state.includes(currentStateFilter) || category.includes(currentStateFilter) || title.includes(currentStateFilter);
    }

    // 3. Search Query Check
    let matchesSearch = true;
    if (currentSearchTerm) {
      matchesSearch = title.includes(currentSearchTerm) || 
                      category.includes(currentSearchTerm) || 
                      department.includes(currentSearchTerm) || 
                      qualification.includes(currentSearchTerm) ||
                      state.includes(currentSearchTerm);
    }

    if (matchesCategory && matchesState && matchesSearch) {
      card.style.display = 'block';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });

  updateJobCount(visibleCount);
  checkEmptyState(visibleCount);
}

function filterCategory(cat, btnElement) {
  currentCategoryFilter = (cat || 'all').toLowerCase();

  const buttons = document.querySelectorAll('.filter-btn');
  buttons.forEach(btn => {
    btn.classList.remove('bg-emerald-600', 'text-white', 'font-bold');
    btn.classList.add('bg-slate-200', 'text-slate-700');
  });

  let targetBtn = btnElement;
  if (!targetBtn) {
    buttons.forEach(btn => {
      const onclickAttr = btn.getAttribute('onclick') || '';
      const filterAttr = btn.getAttribute('data-filter') || '';
      if (onclickAttr.includes(`'${cat}'`) || filterAttr.includes(cat)) {
        targetBtn = btn;
      }
    });
  }

  if (targetBtn) {
    targetBtn.classList.remove('bg-slate-200', 'text-slate-700');
    targetBtn.classList.add('bg-emerald-600', 'text-white', 'font-bold');
  }

  applyAllFilters();
}

function filterState(stateName) {
  currentStateFilter = (stateName || 'all').toLowerCase();

  const statePills = document.querySelectorAll('.state-pill');
  statePills.forEach(pill => {
    pill.classList.remove('bg-emerald-600', 'text-white', 'font-bold');
    pill.classList.add('bg-slate-100', 'text-slate-600');
  });

  statePills.forEach(pill => {
    const onclickAttr = pill.getAttribute('onclick') || '';
    if (onclickAttr.includes(`'${stateName}'`)) {
      pill.classList.remove('bg-slate-100', 'text-slate-600');
      pill.classList.add('bg-emerald-600', 'text-white', 'font-bold');
    }
  });

  applyAllFilters();
}

function handleSearch(query) {
  currentSearchTerm = (query || '').toLowerCase().trim();
  applyAllFilters();
}

function updateJobCount(count) {
  const display = document.getElementById('jobCountDisplay');
  if (display) {
    display.textContent = `Showing ${count} Active Recruitment Notice${count === 1 ? '' : 's'}`;
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
    const target = HASH_MAP[hash];
    if (target.type === 'category') {
      filterCategory(target.value);
    } else if (target.type === 'state') {
      filterState(target.value);
    }

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

  handleHashNavigation();
  window.addEventListener('hashchange', handleHashNavigation);
});
