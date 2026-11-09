/* Primex — accordion, back-to-top, gallery */
(function () {
  'use strict';
  var P = window.Primex, qs = P.qs, qsa = P.qsa;

  // Back to top
  var top = qs('#backToTop');
  if (top) {
    var anchor = qs('.bs'); // home page: show the arrow only after scrolling into the Trusted Partners section
    var OFFSET = 200;       // px scrolled past the section's top before the arrow appears (increase = appears later)
    function toggleTop() {
      var after = anchor ? anchor.getBoundingClientRect().top < -OFFSET : window.scrollY > 500;
      top.classList.toggle('show', after);
    }
    window.addEventListener('scroll', toggleTop, { passive: true });
    toggleTop();
    top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: P.reduceMotion ? 'auto' : 'smooth' }); });
  }

  // Accordion (FAQ)
  qsa('.accordion').forEach(function (acc) {
    qsa('.acc-btn', acc).forEach(function (btn) {
      btn.addEventListener('click', function () {
        var panel = document.getElementById(btn.getAttribute('aria-controls'));
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!open));
        panel.classList.toggle('open', !open);
      });
    });
  });

  // Gallery (delegated so it works with JS-rendered product pages)
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('.thumb') : null;
    if (!t) return;
    var g = t.closest('[data-gallery]'); if (!g) return;
    var main = qs('.gallery-main .media', g), src = t.getAttribute('data-src');
    qsa('.thumb', g).forEach(function (b) { b.removeAttribute('aria-current'); });
    t.setAttribute('aria-current', 'true');
    var img = qs('img', main);
    if (img) { img.hidden = false; img.src = src; img.alt = t.getAttribute('data-alt') || ''; }
  });
})();

/* Hero slider (+ optional background video) */
(function () {
  'use strict';
  var P = window.Primex, qs = P.qs, qsa = P.qsa;
  var hero = qs('.hero-slider'); if (!hero) return;
  var slides = qsa('.slide', hero), dots = qsa('.dot', hero), track = qs('.hero-track', hero);
  var pauseBtn = qs('[data-hero="pause"]', hero), interval = parseInt(hero.getAttribute('data-interval') || '6500', 10);
  var idx = 0, timer = null, userPaused = P.reduceMotion, hoverPaused = false;

  function show(n) {
    idx = (n + slides.length) % slides.length;
    slides.forEach(function (s, i) { s.classList.toggle('active', i === idx); s.setAttribute('aria-hidden', String(i !== idx)); });
    dots.forEach(function (d, i) { d.classList.toggle('active', i === idx); if (i === idx) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
    syncVideos();
  }
  function syncVideos() {
    slides.forEach(function (s, i) {
      var v = qs('.slide-video', s); if (!v) return;
      clearTimeout(v._t);
      if (i === idx) {
        v._adv = false;
        try { v.currentTime = 0; } catch (e) {}
        var p = v.play(); if (p && p.catch) p.catch(function () {});
      } else {
        v._t = setTimeout(function () { v.pause(); }, 1000); /* fade-out ivara wenakan pause nokarai */
      }
    });
  }
  function loadVideos() { /* videos okkoma kalin load karanawa, slide maru wenakota blank flash ekak nethi wenna */
    if (P.reduceMotion || (navigator.connection && navigator.connection.saveData)) return;
    slides.forEach(function (s) {
      var v = qs('.slide-video', s), src = s.getAttribute('data-video'); if (!v || !src) return;
      v.addEventListener('loadeddata', function () {
        s.classList.add('has-slide-video');
        if (s.classList.contains('active')) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      }, { once: true });
      v.loop = false;
      /* video eka iwara wenna kalin (0.4s) ikmanata ara next slide ekata maru wenawa; hover karala hitiyath maru wenawa */
      function advance() {
        if (v._adv || !s.classList.contains('active') || userPaused) return;
        v._adv = true; show(idx + 1); start();
      }
      v.addEventListener('timeupdate', function () {
        if (v.duration && isFinite(v.duration) && v.duration - v.currentTime <= 0.4) advance();
      });
      v.addEventListener('ended', advance);
      v.preload = 'auto'; v.src = src;
    });
  }
  function stop() { clearInterval(timer); timer = null; }
  function start() {
    stop();
    if (!userPaused && !hoverPaused && slides.length > 1) {
      /* video thiyena slide eka, video eka iwara wenakota maru wenawa. video nathi slide eka interval ekata maru wenawa */
      timer = setInterval(function () { if (!slides[idx].classList.contains('has-slide-video')) show(idx + 1); }, interval);
      var cv = qs('.slide-video', slides[idx]);
      if (cv && cv.ended) show(idx + 1);
    }
  }
  function syncPause() {
    if (pauseBtn) {
      pauseBtn.setAttribute('aria-label', userPaused ? 'Play slideshow' : 'Pause slideshow');
      qs('.i-pause', pauseBtn).hidden = userPaused; qs('.i-play', pauseBtn).hidden = !userPaused;
    }
    track.setAttribute('aria-live', userPaused ? 'polite' : 'off');
  }

  qs('[data-hero="prev"]', hero).addEventListener('click', function () { show(idx - 1); start(); });
  qs('[data-hero="next"]', hero).addEventListener('click', function () { show(idx + 1); start(); });
  dots.forEach(function (d, i) { d.addEventListener('click', function () { show(i); start(); }); });
  if (pauseBtn) pauseBtn.addEventListener('click', function () { userPaused = !userPaused; syncPause(); start(); });
  hero.addEventListener('mouseenter', function () { hoverPaused = true; stop(); });
  hero.addEventListener('mouseleave', function () { hoverPaused = false; start(); });
  hero.addEventListener('focusin', function () { hoverPaused = true; stop(); });
  hero.addEventListener('focusout', function () { hoverPaused = false; start(); });
  hero.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { show(idx - 1); start(); } else if (e.key === 'ArrowRight') { show(idx + 1); start(); }
  });
  var x0 = null;
  hero.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  hero.addEventListener('touchend', function (e) {
    if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) { show(idx + (dx < 0 ? 1 : -1)); start(); }
  }, { passive: true });
  document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); else start(); });

  /* Optional video: if assets/videos/hero.mp4 exists it plays behind the slides; otherwise the image slider shows. */
  var video = qs('.hero-video', hero), src = hero.getAttribute('data-video');
  if (video && src && !P.reduceMotion && !(navigator.connection && navigator.connection.saveData)) {
    video.addEventListener('loadeddata', function () { hero.classList.add('has-video'); var p = video.play(); if (p && p.catch) p.catch(function () {}); });
    video.addEventListener('error', function () { video.removeAttribute('src'); });
    video.src = src;
  }
  loadVideos();
  show(0); syncPause(); start();
})();

/* Trusted Partners slider (under hero): auto-slide + arrows + swipe */
(function () {
  'use strict';
  var P = window.Primex, qs = P.qs;
  var track = qs('.bs-track'); if (!track) return;
  var timer = null;
  function step() { var c = qs('.bs-card', track); return c ? c.offsetWidth + (parseFloat(getComputedStyle(track).columnGap) || 28) : 250; }
  function next() {
    if (track.scrollLeft + track.clientWidth >= track.scrollWidth - 4) track.scrollTo({ left: 0, behavior: 'smooth' });
    else track.scrollBy({ left: step(), behavior: 'smooth' });
  }
  function prev() { track.scrollBy({ left: -step(), behavior: 'smooth' }); }
  function stop() { clearInterval(timer); timer = null; }
  function start() { stop(); if (!P.reduceMotion) timer = setInterval(next, 2000); }
  qs('[data-bs="next"]').addEventListener('click', function () { next(); start(); });
  qs('[data-bs="prev"]').addEventListener('click', function () { prev(); start(); });
  track.addEventListener('mouseenter', stop); track.addEventListener('mouseleave', start);
  track.addEventListener('focusin', stop); track.addEventListener('focusout', start);
  document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); else start(); });
  start();
})();