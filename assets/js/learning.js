(() => {
  const root = document.querySelector('.learning');
  if (!root) return;
  const cards = [...root.querySelectorAll('.learn-card')];
  const filterButtons = [...root.querySelectorAll('[data-filter]')];
  const areaButtons = [...root.querySelectorAll('button[data-area]')];
  const en = document.documentElement.lang === 'en';
  function filter(area) {
    let count = 0;
    cards.forEach(card => { card.hidden = area !== 'all' && card.dataset.area !== area; if (!card.hidden) count++; });
    filterButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === area)));
    areaButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.area === area)));
    root.querySelector('#learn-results').textContent = en ? `${count} training ${count === 1 ? 'record' : 'records'}` : `${count} ${count === 1 ? 'registo' : 'registos'} de formação`;
    root.querySelector('#learn-empty').hidden = count !== 0;
    root.querySelectorAll('[data-evidence]').forEach(panel => { panel.hidden = panel.dataset.evidence !== area; });
  }
  filterButtons.forEach(button => button.addEventListener('click', () => filter(button.dataset.filter)));
  areaButtons.forEach(button => button.addEventListener('click', () => filter(button.dataset.area)));
  root.querySelectorAll('.learn-controls').forEach(control => { control.hidden = false; });
})();
