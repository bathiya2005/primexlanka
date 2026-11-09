/* Primex — client-side validation + backend-ready submission */
(function () {
  'use strict';
  var P = window.Primex, qsa = P.qsa, qs = P.qs;

  function setError(field, msg) {
    var wrap = field.closest('.field'); if (!wrap) return;
    wrap.classList.toggle('invalid', !!msg);
    var err = qs('.error', wrap); if (err) err.textContent = msg || '';
    field.setAttribute('aria-invalid', msg ? 'true' : 'false');
  }
  function validate(field) {
    var v = field.value.trim();
    if (field.required && !v) return 'This field is required.';
    if (v && field.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return 'Enter a valid email address.';
    if (v && field.type === 'tel' && !/^[+\d][\d\s()-]{6,}$/.test(v)) return 'Enter a valid phone number.';
    if (v && field.name === 'quantity' && !/\S/.test(v)) return 'Enter a quantity.';
    return '';
  }

  qsa('form[data-form]').forEach(function (form) {
    var status = qs('.form-status', form);
    function show(kind, text) { if (!status) return; status.className = 'form-status show ' + kind; status.textContent = text; status.focus && status.focus(); }

    qsa('input,select,textarea', form).forEach(function (f) {
      f.addEventListener('blur', function () { if (f.name && f.type !== 'hidden') setError(f, validate(f)); });
      f.addEventListener('input', function () { if (f.closest('.field') && f.closest('.field').classList.contains('invalid')) setError(f, validate(f)); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      qsa('input,select,textarea', form).forEach(function (f) {
        if (!f.name || f.classList.contains('hp-input')) return;
        var m = validate(f); setError(f, m); if (m && !firstBad) firstBad = f;
      });
      if (firstBad) { firstBad.focus(); show('warn', 'Please correct the highlighted fields.'); return; }
      var hp = qs('.hp-input', form); if (hp && hp.value) return; // honeypot

      var data = {}; new FormData(form).forEach(function (v, k) { if (k !== 'website') data[k] = v; });
      data.page = location.pathname; data.submittedAt = new Date().toISOString();

      var endpoint = P.config.formEndpoint || form.getAttribute('data-endpoint');
      if (!endpoint) {
        show('warn', 'Your details are valid, but this form is not yet connected to a backend, so nothing was sent. Please call +94 11 283 7241 to reach our team.');
        return;
      }
      var btn = qs('button[type="submit"]', form); if (btn) btn.disabled = true;
      fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); form.reset(); show('ok', 'Thank you. Your inquiry has been sent and our team will respond shortly.'); })
        .catch(function () { show('warn', 'We could not send your inquiry. Please try again or call +94 11 283 7241.'); })
        .then(function () { if (btn) btn.disabled = false; });
    });
  });
})();
