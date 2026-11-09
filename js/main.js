/* Primex — core namespace, configuration and small shared utilities */
(function () {
  'use strict';
  var P = (window.Primex = window.Primex || {});

  /* ---- Configuration: edit these once details are verified ---- */
  P.config = {
    formEndpoint: '',            // e.g. 'https://example.com/api/inquiry' — leave empty until a backend exists
    social: { facebook: '', linkedin: '', instagram: '', youtube: '' }, // add verified URLs; empty = not shown
    // Verified certificates only. Example: { name:'ISO 9001:2015', issuer:'…', number:'…', valid:'…', image:'assets/images/about/cert-iso9001.webp', note:'…' }
    certificates: []
  };

  P.qs = function (s, r) { return (r || document).querySelector(s); };
  P.qsa = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  P.reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function init() {
    var y = P.qs('#footerYear'); if (y) y.textContent = new Date().getFullYear();

    // Floating social button appears only when a verified URL is configured
    if (P.config.social.facebook) {
      var a = document.createElement('a');
      a.className = 'fab fab-social'; a.href = P.config.social.facebook; a.target = '_blank'; a.rel = 'noopener';
      a.setAttribute('aria-label', 'Primex on Facebook');
      a.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8V6.5c0-.7.3-1 1-1h2V2h-3a4 4 0 0 0-4 4.2V8H7v3.5h3V22h4V11.5h2.8L17.5 8z"/></svg>';
      document.body.appendChild(a);
    }

    // Certificates (certifications.html + homepage preview)
    P.qsa('[data-cert-list]').forEach(function (el) {
      if (!P.config.certificates.length) return;
      var limit = parseInt(el.getAttribute('data-limit') || '99', 10);
      el.innerHTML = P.config.certificates.slice(0, limit).map(function (c) {
        return '<article class="card">' +
          '<div class="media wide"><img src="' + (c.image || '') + '" alt="' + c.name + ' certificate" loading="lazy" onerror="this.hidden=true"></div>' +
          '<h3 style="margin-top:16px">' + c.name + '</h3>' +
          '<p><strong>Issued by:</strong> ' + (c.issuer || '—') + '</p>' +
          (c.number ? '<p><strong>Certificate no.:</strong> ' + c.number + '</p>' : '') +
          (c.valid ? '<p><strong>Valid:</strong> ' + c.valid + '</p>' : '') +
          (c.note ? '<p>' + c.note + '</p>' : '') + '</article>';
      }).join('');
      P.qsa('[data-cert-empty]').forEach(function (n) { n.hidden = true; });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
/* Social links on the contact page (rendered only for URLs set in Primex.config.social) */
(function () {
  var P = window.Primex;
  function run() {
    P.qsa('[data-social]').forEach(function (el) {
      var s = P.config.social, out = [];
      Object.keys(s).forEach(function (k) { if (s[k]) out.push('<a class="' + (el.getAttribute('data-social') === 'plain' ? 'social-link' : 'btn btn-outline btn-sm') + '" href="' + s[k] + '" target="_blank" rel="noopener">' + k.charAt(0).toUpperCase() + k.slice(1) + '</a>'); });
      if (out.length) { el.innerHTML = out.join(' '); } else { el.hidden = true; }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
