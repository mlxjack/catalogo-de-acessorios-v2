// Motion do catálogo — vanilla JS, sem dependências. Respeita prefers-reduced-motion.
// API: Motion.refresh() depois de cada render; Motion.lightbox(src, alt).
(function () {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const root = document.documentElement;
  const hasIO = 'IntersectionObserver' in window;
  if (hasIO) root.classList.add('js-motion');

  let io = null;
  if (hasIO) {
    io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  }

  // Contadores animados (hero)
  function countUp(el) {
    const to = parseInt(el.dataset.count, 10);
    if (reduce.matches || isNaN(to)) { el.textContent = to; return; }
    const t0 = performance.now(), dur = 1400;
    (function step(t) {
      const k = Math.min(1, (t - t0) / dur);
      el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3)));
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }

  // Parallax discreto: translateY proporcional à posição do elemento na viewport
  let parallaxEls = [];
  let ticking = false;
  function paint() {
    ticking = false;
    const vh = window.innerHeight;
    const y = window.scrollY;
    const bar = document.getElementById('scroll-progress');
    if (bar) {
      const max = document.documentElement.scrollHeight - vh;
      bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
    }
    const header = document.querySelector('.main-header');
    if (header) header.classList.toggle('is-scrolled', y > 24);
    if (reduce.matches) return;
    parallaxEls.forEach((el) => {
      const r = el.parentElement.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      const speed = parseFloat(el.dataset.parallax) || 0.1;
      const offset = (r.top + r.height / 2 - vh / 2) * speed;
      el.style.transform = 'translate3d(0,' + offset.toFixed(1) + 'px,0)';
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(paint); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });

  function refresh() {
    const scope = document;
    // Revelações
    scope.querySelectorAll('[data-reveal]:not(.is-in)').forEach((el) => {
      if (io) io.observe(el); else el.classList.add('is-in');
    });
    // Contadores
    scope.querySelectorAll('[data-count]').forEach((el) => {
      if (el.dataset.counted) return;
      el.dataset.counted = '1';
      if (io) {
        const o = new IntersectionObserver((es) => { if (es[0].isIntersecting) { countUp(el); o.disconnect(); } });
        o.observe(el);
      } else countUp(el);
    });
    parallaxEls = Array.from(scope.querySelectorAll('[data-parallax]'));
    paint();
  }

  // Lightbox simples (banners)
  function lightbox(src, alt) {
    let dlg = document.getElementById('lightbox');
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.id = 'lightbox';
      dlg.className = 'lightbox';
      dlg.setAttribute('aria-label', 'Imagem ampliada');
      dlg.innerHTML = '<button class="lightbox-close" type="button" aria-label="Fechar">×</button><div class="lightbox-inner"><img alt=""></div>';
      document.body.appendChild(dlg);
      dlg.addEventListener('click', (e) => { if (e.target === dlg || e.target.closest('.lightbox-close') || e.target.classList.contains('lightbox-inner')) dlg.close(); });
    }
    const img = dlg.querySelector('img');
    img.src = src; img.alt = alt || '';
    if (typeof dlg.showModal === 'function') dlg.showModal(); else window.open(src, '_blank');
  }

  window.Motion = { refresh, lightbox };
  if (document.readyState !== 'loading') paint(); else document.addEventListener('DOMContentLoaded', paint);
})();
