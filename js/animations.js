/* Primex — scroll reveal (IntersectionObserver) and animated counters */
(function () {
  'use strict';
  var P = window.Primex, qsa = P.qsa;
  var supports = 'IntersectionObserver' in window;

  function showAll() { qsa('.reveal').forEach(function (el) { el.classList.add('in'); }); qsa('[data-count]').forEach(setFinal); }
  function setFinal(el) { el.textContent = format(parseFloat(el.getAttribute('data-count')), el); }
  function format(v, el) {
    var d = parseInt(el.getAttribute('data-decimals') || '0', 10);
    return v.toFixed(d) + (el.getAttribute('data-suffix') || '');
  }
  function count(el) {
    var end = parseFloat(el.getAttribute('data-count')), dur = 1600, start = null;
    function step(t) {
      if (start === null) start = t;
      var p = Math.min((t - start) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(end * eased, el);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  if (!supports || P.reduceMotion) { showAll(); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('in'); io.unobserve(en.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  qsa('.reveal').forEach(function (el) { io.observe(el); });

  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { count(en.target); cio.unobserve(en.target); } });
  }, { threshold: 0.5 });
  qsa('[data-count]').forEach(function (el) { el.textContent = format(0, el); cio.observe(el); });
})();
