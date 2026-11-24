/* Transiqe site motion: mobile menu, scroll reveals, parallax, pointer drift and
   a compact navigation bar that appears once the hero has scrolled away.
   Everything here is progressive: with JavaScript off, or with reduced motion
   requested, the page is fully visible and static. */
(function () {
  var doc = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- mobile menu ---- */
  var btn = document.getElementById('menu-btn'), menu = document.getElementById('mobile-menu');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ---- compact bar after the hero ---- */
  var firstNav = document.querySelector('.nav');
  if (firstNav) {
    var dock = document.createElement('div');
    dock.className = 'dock';
    dock.setAttribute('aria-hidden', 'true');
    var clone = firstNav.cloneNode(true);
    clone.classList.remove('on-image');
    clone.classList.add('on-paper');
    var b = clone.querySelector('.burger'); if (b) b.remove();
    var cta = clone.querySelector('.btn'); if (cta) { cta.classList.remove('white'); cta.classList.add('ink'); }
    [].forEach.call(clone.querySelectorAll('a,button'), function (a) { a.tabIndex = -1; });
    dock.appendChild(clone);
    document.body.appendChild(dock);
    var shown = false;
    var onDock = function () {
      var want = window.scrollY > 520;
      if (want === shown) return;
      shown = want;
      dock.classList.toggle('show', want);
      dock.setAttribute('aria-hidden', want ? 'false' : 'true');
      [].forEach.call(clone.querySelectorAll('a,button'), function (a) { a.tabIndex = want ? 0 : -1; });
    };
    window.addEventListener('scroll', onDock, { passive: true });
    onDock();
  }

  if (reduce || !('IntersectionObserver' in window)) return;
  doc.classList.add('fx');

  /* ---- scroll reveals ---- */
  var plan = [
    ['.head > *', 'up'], ['.part', 'up'], ['.route', 'up'], ['.bento > *', 'scale'],
    ['.rowx .txt', 'side'], ['.rowx .vis', 'scale'], ['.journey', 'up'], ['.feat', 'up'],
    ['.grid > *', 'up'], ['.split > *', 'up'], ['.stage', 'scale'], ['.plan', 'up'],
    ['.plainlist li', 'up'], ['.faq details', 'up'], ['.ask', 'up'], ['.closer', 'scale'],
    ['.panel.inview', 'scale'], ['.ruler', 'up']
  ];
  var tagged = [];
  plan.forEach(function (p) {
    [].forEach.call(document.querySelectorAll(p[0]), function (el) {
      if (el.closest('.doc') || el.closest('.panel:not(.inview)') || el.closest('[data-fx]') || el.hasAttribute('data-fx')) return;
      var kind = p[1];
      if (kind === 'side') {
        var row = el.closest('.rowx');
        var idx = row ? [].indexOf.call(row.parentNode.children, row) : 0;
        kind = idx % 2 ? 'right' : 'left';
      }
      el.setAttribute('data-fx', kind);
      tagged.push(el);
    });
  });
  tagged.forEach(function (el) {
    var sibs = [].filter.call(el.parentNode.children, function (c) { return c.hasAttribute('data-fx'); });
    el.style.setProperty('--i', Math.min(sibs.indexOf(el), 7));
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -7% 0px', threshold: 0.06 });
  tagged.forEach(function (el) { io.observe(el); });

  /* ---- parallax on banner and tile photos ---- */
  var layers = [].slice.call(document.querySelectorAll('.panel > picture img, .panel > img.bg, .tile.photo img, .closer > img.bg'));
  var ticking = false;
  function paint() {
    ticking = false;
    var vh = window.innerHeight;
    layers.forEach(function (img) {
      var host = img.closest('.panel, .tile.photo, .closer');
      var r = host.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      var mid = r.top + r.height / 2 - vh / 2;
      img.style.translate = '0 ' + (mid * -0.07).toFixed(1) + 'px';
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(paint); } }
  if (layers.length) { window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); paint(); }

  /* ---- pointer drift for the floating cards in banners ---- */
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    [].forEach.call(document.querySelectorAll('.panel'), function (panel) {
      var raf = null, tx = 0, ty = 0;
      panel.addEventListener('pointermove', function (ev) {
        var r = panel.getBoundingClientRect();
        tx = (ev.clientX - r.left) / r.width - 0.5;
        ty = (ev.clientY - r.top) / r.height - 0.5;
        if (!raf) raf = requestAnimationFrame(function () {
          raf = null;
          panel.style.setProperty('--mx', tx.toFixed(3));
          panel.style.setProperty('--my', ty.toFixed(3));
        });
      });
      panel.addEventListener('pointerleave', function () {
        panel.style.setProperty('--mx', 0); panel.style.setProperty('--my', 0);
      });
    });
  }
})();
