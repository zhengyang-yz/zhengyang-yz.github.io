'use strict';

// The entire profile stays readable when JavaScript is unavailable.
const header = document.querySelector('.site-header');
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
if (header && menuButton && navigation) {
  header.setAttribute('data-menu-ready', '');
  menuButton.hidden = false;
  function closeMenu() {
    header.removeAttribute('data-menu-open');
    menuButton.setAttribute('aria-expanded', 'false');
  }
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    header.toggleAttribute('data-menu-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
  });
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && header.hasAttribute('data-menu-open')) {
      closeMenu();
      menuButton.focus();
    }
  });
}

const filters = document.querySelector('.publication-filters');
const search = document.querySelector('#publication-search');
const year = document.querySelector('#publication-year');
const cited = document.querySelector('#highly-cited');
const count = document.querySelector('#publication-count');
const empty = document.querySelector('#no-publications');
const reset = document.querySelector('#reset-filters');
const papers = [...document.querySelectorAll('#publication-list > li')];
if (filters && search && year && cited && count && empty && reset) {
  filters.hidden = false;
  const searchable = papers.map(element => ({element, text: element.textContent.toLocaleLowerCase()}));
  function updatePublications() {
    const query = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    searchable.forEach(({element, text}) => {
      const match = query.every(word => text.includes(word)) &&
        (year.value === 'all' || element.dataset.year === year.value) &&
        (!cited.checked || element.dataset.cited === 'true');
      element.hidden = !match;
      if (match) visible++;
    });
    count.textContent = `${visible} ${visible === 1 ? 'publication' : 'publications'}`;
    empty.hidden = visible !== 0;
  }
  filters.addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', updatePublications);
  year.addEventListener('change', updatePublications);
  cited.addEventListener('change', updatePublications);
  reset.addEventListener('click', () => {
    filters.reset();
    updatePublications();
    search.focus();
  });
  updatePublications();
}

const copyright = document.querySelector('#copyright-year');
if (copyright) copyright.textContent = String(new Date().getFullYear());
