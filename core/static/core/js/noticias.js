/* ══════════════════════════════════════════════════════════
   APARTADO: NOTICIAS
   Lógica exclusiva del modal de noticias usado en
   core/templates/core/partials/noticias.html
   ══════════════════════════════════════════════════════════ */

function openNoticia(el) {
  document.getElementById('noticiaModalImg').src = el.dataset.img || '';
  document.getElementById('noticiaModalCat').textContent = el.dataset.categoria || '';
  document.getElementById('noticiaModalTitulo').textContent = el.dataset.titulo || '';
  document.getElementById('noticiaModalFecha').textContent = el.dataset.fecha || '';
  document.getElementById('noticiaModalResumen').textContent = el.dataset.resumen || '';
  document.getElementById('noticiaModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeNoticia() {
  document.getElementById('noticiaModal').classList.remove('open');
  document.body.style.overflow = '';
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeNoticia(); });
