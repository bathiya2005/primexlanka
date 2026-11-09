/* Primex — sticky header, dropdowns, mobile menu */
(function () {
  'use strict';
  var P = window.Primex, qs = P.qs, qsa = P.qsa;
  var header = qs('.site-header'), toggle = qs('.nav-toggle'), menu = qs('#primary-menu');
  if (!header || !toggle || !menu) return;

  var scrim = document.createElement('div'); scrim.className = 'nav-scrim'; document.body.appendChild(scrim);

  var scrolled = false;
  function onScroll() {
    var y = window.scrollY;
    if (!scrolled && y > 80) scrolled = true; else if (scrolled && y < 20) scrolled = false; else return;
    header.classList.toggle('scrolled', scrolled);
  }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  function setMenu(open) {
    menu.classList.toggle('open', open); scrim.classList.toggle('show', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
  }
  var closeLi = document.createElement('li'); closeLi.className = 'nav-close-wrap';
  closeLi.innerHTML = '<button type="button" class="nav-close" aria-label="Close menu"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>';
  menu.insertBefore(closeLi, menu.firstChild);
  closeLi.firstChild.addEventListener('click', function () { setMenu(false); toggle.focus(); });
  toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
  scrim.addEventListener('click', function () { setMenu(false); });

  var items = qsa('.has-dropdown', menu);
  function closeAll(except) {
    items.forEach(function (li) {
      if (li !== except) { li.classList.remove('open'); var b = qs('.nav-link', li); if (b) b.setAttribute('aria-expanded', 'false'); }
    });
  }
  items.forEach(function (li) {
    var btn = qs('button.nav-link', li);
    if (!btn) return;
    btn.addEventListener('click', function () {
      var open = !li.classList.contains('open');
      closeAll(li); li.classList.toggle('open', open); btn.setAttribute('aria-expanded', String(open));
    });
    li.addEventListener('mouseenter', function () { if (window.innerWidth > 1100) btn.setAttribute('aria-expanded', 'true'); });
    li.addEventListener('mouseleave', function () { if (window.innerWidth > 1100) btn.setAttribute('aria-expanded', String(li.classList.contains('open'))); });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var wasOpen = toggle.getAttribute('aria-expanded') === 'true';
    var openItem = items.filter(function (li) { return li.classList.contains('open'); })[0];
    closeAll(); if (wasOpen) { setMenu(false); toggle.focus(); }
    if (openItem) { var b = qs('button.nav-link', openItem); if (b) b.focus(); }
  });
  document.addEventListener('click', function (e) { if (!menu.contains(e.target) && !toggle.contains(e.target)) closeAll(); });
  qsa('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  window.addEventListener('resize', function () { if (window.innerWidth > 1100) setMenu(false); });
})();