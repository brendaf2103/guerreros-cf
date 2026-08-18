// ── HERO SLIDER ──
let hIdx = 0;
const hSlides = document.querySelectorAll('.hslide');
function heroSlide(d) {
  if (!hSlides.length) return;
  hSlides[hIdx].classList.remove('active');
  hIdx = (hIdx + d + hSlides.length) % hSlides.length;
  hSlides[hIdx].classList.add('active');
}
if (hSlides.length) setInterval(() => heroSlide(1), 4000);

// ── FILO SLIDER ──
let fIdx = 0;
const fSlides = document.querySelectorAll('.fslide');
const filoDotsWrap = document.getElementById('filoDots');
if (filoDotsWrap) {
  fSlides.forEach((_, i) => {
    const d = document.createElement('span');
    if (i === 0) d.classList.add('active');
    d.addEventListener('click', () => goFilo(i));
    filoDotsWrap.appendChild(d);
  });
}
function goFilo(idx) {
  if (!fSlides.length) return;
  fSlides[fIdx].classList.remove('active');
  if (filoDotsWrap) filoDotsWrap.children[fIdx].classList.remove('active');
  fIdx = (idx + fSlides.length) % fSlides.length;
  fSlides[fIdx].classList.add('active');
  if (filoDotsWrap) filoDotsWrap.children[fIdx].classList.add('active');
}
function filoSlide(d) {
  if (!fSlides.length) return;
  goFilo(fIdx + d);
}
if (fSlides.length) setInterval(() => filoSlide(1), 3500);

// ── MATERIAL SLIDER (Materiales de Entrenamiento) ──
let mIdx = 0;
const mSlides = document.querySelectorAll('.mslide');
const materialDotsWrap = document.getElementById('materialDots');
if (materialDotsWrap) {
  mSlides.forEach((_, i) => {
    const d = document.createElement('span');
    if (i === 0) d.classList.add('active');
    d.addEventListener('click', () => goMaterial(i));
    materialDotsWrap.appendChild(d);
  });
}
function goMaterial(idx) {
  if (!mSlides.length) return;
  mSlides[mIdx].classList.remove('active');
  if (materialDotsWrap) materialDotsWrap.children[mIdx].classList.remove('active');
  mIdx = (idx + mSlides.length) % mSlides.length;
  mSlides[mIdx].classList.add('active');
  if (materialDotsWrap) materialDotsWrap.children[mIdx].classList.add('active');
}
function materialSlide(d) {
  if (!mSlides.length) return;
  goMaterial(mIdx + d);
}
if (mSlides.length) setInterval(() => materialSlide(1), 3800);

// ── EVENTO SLIDER (los thumbs ya vienen renderizados desde Django) ──
let eIdx = 0;
const eSlides = document.querySelectorAll('.eslide');
function goEvento(idx) {
  if (!eSlides.length) return;
  eSlides[eIdx].classList.remove('active');
  document.querySelectorAll('.ethumb')[eIdx].classList.remove('active');
  eIdx = idx;
  eSlides[eIdx].classList.add('active');
  document.querySelectorAll('.ethumb')[eIdx].classList.add('active');
}
function eventoSlide(d) {
  if (!eSlides.length) return;
  goEvento((eIdx + d + eSlides.length) % eSlides.length);
}
document.querySelectorAll('.ethumb').forEach((t, i) => {
  t.addEventListener('click', () => goEvento(i));
});
if (eSlides.length) setInterval(() => eventoSlide(1), 5000);

// ── LIGHTBOX (galería masonry, renderizada desde la base de datos) ──
document.querySelectorAll('.masonry-item img, .camp-photo-sm img, .camp-photo-main img').forEach(img => {
  img.style.cursor = 'pointer';
  img.addEventListener('click', () => openLB(img.getAttribute('src')));
});
function openLB(src) {
  document.getElementById('lbImg').src = src;
  document.getElementById('lightbox').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeLB() {
  document.getElementById('lightbox').classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLB(); });

// ── NAV MOBILE ──
function toggleNav() {
  document.getElementById('navLinks').classList.toggle('open');
}
document.querySelectorAll('.nav-links a').forEach(a => {
  a.addEventListener('click', () => document.getElementById('navLinks').classList.remove('open'));
});

// ── NAV SCROLL ──
window.addEventListener('scroll', () => {
  const nav = document.getElementById('nav');
  if (nav) nav.style.background = window.scrollY > 50 ? 'rgba(10,22,40,0.98)' : 'rgba(10,22,40,0.92)';
});

// ── WHATSAPP FORM (envía por WhatsApp Y guarda el mensaje en Django) ──
function sendWA() {
  const nombre = document.querySelector('.c-form input[name="nombre"]').value;
  const tel = document.querySelector('.c-form input[name="telefono"]').value;
  const cat = document.querySelector('.c-form select[name="categoria"]').value;
  const msg = document.querySelector('.c-form textarea[name="mensaje"]').value;
  if (!nombre) { alert('Por favor ingresa tu nombre'); return; }
  const text = `Hola, me interesa la Academia Guerreros CF%0A%0ANombre: ${nombre}%0ATel: ${tel}%0ACategoría: ${cat}%0AMensaje: ${msg}`;
  window.open(`https://wa.me/522411055982?text=${text}`, '_blank');
  document.getElementById('contactoForm').submit();
}

// ── ANIMATE ON SCROLL ──
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.info-card,.c-item,.camp-ach-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
  el.style.transition = 'opacity .6s ease, transform .6s ease';
  observer.observe(el);
});
