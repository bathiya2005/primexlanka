
(function () {
  'use strict';
  var P = window.Primex = window.Primex || {};
  var qs = function (s, r) { return (r || document).querySelector(s); };
  var qsa = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var CATS = {"rolls": "Rolls & Films", "bags": "Bags", "agri": "Agriculture"};
  var DATA = P.products = [
 {
  "slug": "general-purpose-rolls",
  "name": "General Purpose Rolls",
  "cat": "rolls",
  "desc": "Polyethylene rolls for general packaging, wrapping and protection needs.",
  "apps": [
   "General packaging and wrapping",
   "Covering and protection",
   "Further conversion into bags"
  ],
  "custom": [
   "Custom thickness (micron)",
   "Width and length",
   "Colour tinting"
  ]
 },
 {
  "slug": "general-purpose-rolls-110",
  "name": "General Purpose Rolls – Width up to 110",
  "cat": "rolls",
  "desc": "Wide-format polyethylene rolls for larger packaging and covering requirements.",
  "apps": [
   "Large-format packaging",
   "Industrial covering",
   "Bulk wrapping"
  ],
  "custom": [
   "Custom thickness (micron)",
   "Width and length",
   "Colour tinting"
  ]
 },
 {
  "slug": "shrink-purpose-rolls",
  "name": "Shrink Purpose Rolls",
  "cat": "rolls",
  "desc": "Shrink-purpose sheets and rolls for bundling and unit protection.",
  "apps": [
   "Bundling and multipacks",
   "Product protection",
   "Retail and industrial packing"
  ],
  "custom": [
   "Thickness and width",
   "Length",
   "Printing on request"
  ]
 },
 {
  "slug": "biodegradable-bags",
  "name": "Biodegradable Bags",
  "cat": "bags",
  "desc": "Bags from the Biodegradable range for customers looking for more environmentally considered packaging. Contact us to confirm suitability for your application.",
  "apps": [
   "Retail and shopping",
   "Food and general packaging",
   "Brand-conscious packaging"
  ],
  "custom": [
   "Size and thickness",
   "Printing and branding",
   "Handle styles"
  ]
 },
 {
  "slug": "side-seal-bags-without-adhesive",
  "name": "Side Seal Bags Without Adhesive",
  "cat": "bags",
  "desc": "Side-sealed polyethylene bags with an open mouth and no adhesive strip.",
  "apps": [
   "Apparel and textiles",
   "Food and confectionery",
   "General retail packing"
  ],
  "custom": [
   "Size and thickness",
   "Colour tinting",
   "Multi-colour printing"
  ]
 },
 {
  "slug": "side-seal-bags-with-adhesive",
  "name": "Side Seal Bags With Adhesive",
  "cat": "bags",
  "desc": "Side-sealed bags with an adhesive strip for convenient closing.",
  "apps": [
   "Apparel and garments",
   "Stationery and retail items",
   "Document and product packing"
  ],
  "custom": [
   "Size and thickness",
   "Printing and branding",
   "Barcodes"
  ]
 },
 {
  "slug": "shopping-bags",
  "name": "Shopping Bags",
  "cat": "bags",
  "desc": "Carry bags for supermarkets and retail outlets.",
  "apps": [
   "Supermarkets",
   "Retail stores",
   "Promotional carry bags"
  ],
  "custom": [
   "Size and thickness",
   "Punch handle cutting",
   "Logo printing"
  ]
 },
 {
  "slug": "perforation-bags",
  "name": "Perforation Bags",
  "cat": "bags",
  "desc": "Perforated polyethylene bags for products that need ventilation.",
  "apps": [
   "Produce and agriculture",
   "Bakery and food",
   "Industrial packing"
  ],
  "custom": [
   "Size and thickness",
   "Perforation pattern",
   "Printing on request"
  ]
 },
 {
  "slug": "garbage-bags",
  "name": "Garbage Bags",
  "cat": "bags",
  "desc": "Polyethylene bags for waste collection in homes, businesses and facilities.",
  "apps": [
   "Household waste",
   "Commercial and institutional use",
   "Industrial cleaning"
  ],
  "custom": [
   "Size and thickness",
   "Colour",
   "Packing format"
  ]
 },
 {
  "slug": "side-seal-bottom-gusset-bags",
  "name": "Side Seal Bottom Gusset Bags",
  "cat": "bags",
  "desc": "Side-sealed bags with a bottom gusset for fuller, more stable packing.",
  "apps": [
   "Food and confectionery",
   "Bulk products",
   "Retail packing"
  ],
  "custom": [
   "Size and gusset",
   "Thickness",
   "Printing and branding"
  ]
 },
 {
  "slug": "patch-handle-bags",
  "name": "Patch Handle Bags",
  "cat": "bags",
  "desc": "Bags with a reinforced patch handle for comfortable carrying.",
  "apps": [
   "Retail and boutique",
   "Supermarkets",
   "Promotional use"
  ],
  "custom": [
   "Size and thickness",
   "Colour",
   "Logo printing"
  ]
 },
 {
  "slug": "nursery-bags",
  "name": "Nursery Bags",
  "cat": "agri",
  "desc": "Polyethylene bags for raising and handling nursery plants.",
  "apps": [
   "Plant nurseries",
   "Seedling production",
   "Horticulture"
  ],
  "custom": [
   "Size and thickness",
   "Colour",
   "Perforation on request"
  ]
 },
 {
  "slug": "mulch-sheets",
  "name": "Mulch Sheets",
  "cat": "agri",
  "desc": "Polyethylene sheets for covering soil in agricultural use.",
  "apps": [
   "Crop cultivation",
   "Horticulture",
   "Soil covering"
  ],
  "custom": [
   "Width and length",
   "Thickness",
   "Colour"
  ]
 },
 {
  "slug": "hanger-bags",
  "name": "Hanger Bags",
  "cat": "bags",
  "desc": "Bags designed for hanging display and garment-style presentation.",
  "apps": [
   "Apparel and garments",
   "Retail display",
   "Accessories packing"
  ],
  "custom": [
   "Size and thickness",
   "Printing and branding",
   "Hanger style"
  ]
 },
 {
  "slug": "grow-bags",
  "name": "Grow Bags",
  "cat": "agri",
  "desc": "Polyethylene grow bags for container-based cultivation.",
  "apps": [
   "Container farming",
   "Home and commercial gardening",
   "Horticulture"
  ],
  "custom": [
   "Size and thickness",
   "Colour",
   "Perforation on request"
  ]
 },
 {
  "slug": "courier-bags",
  "name": "Courier Bags",
  "cat": "bags",
  "desc": "Courier and mailing bags for secure dispatch of parcels and orders.",
  "apps": [
   "E-commerce",
   "Courier and logistics",
   "Retail dispatch"
  ],
  "custom": [
   "Size and thickness",
   "Multi-colour printing",
   "Barcodes and branding"
  ]
 }
];
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function find(slug) { return DATA.filter(function (p) { return p.slug === slug; })[0]; }
  function media(src, label, cls) {
    return '<div class="media ' + (cls || '') + '"><span class="media-label"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-8 8"/></svg>' + esc(label) + '</span><img src="' + src + '" alt="' + esc(label) + '" loading="lazy" onerror="this.hidden=true"></div>';
  }

  /* Populate every product <select> */
  function fillSelects() {
    qsa('select[name="product"]').forEach(function (sel) {
      DATA.forEach(function (p) { var o = document.createElement('option'); o.value = p.name; o.textContent = p.name; sel.appendChild(o); });
    });
  }

  /* Catalogue: filter + search + sort over server-rendered cards */
  function initCatalogue() {
    var grid = qs('#productGrid'); if (!grid) return;
    var cards = qsa('.product-card', grid), chips = qsa('.chip'), search = qs('#productSearch'), sort = qs('#productSort');
    var none = qs('#noResults'), count = qs('#productCount'), cat = 'all';
    function apply() {
      var q = (search.value || '').trim().toLowerCase(), shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === 'all' || c.dataset.cat === cat) && (!q || c.dataset.text.indexOf(q) > -1);
        c.hidden = !ok; if (ok) { shown++; c.classList.add('in'); }
      });
      none.hidden = shown !== 0;
      count.textContent = shown + (shown === 1 ? ' product' : ' products');
    }
    function reorder() {
      var v = sort.value, list = cards.slice();
      if (v === 'az') list.sort(function (a, b) { return a.dataset.name.localeCompare(b.dataset.name); });
      if (v === 'za') list.sort(function (a, b) { return b.dataset.name.localeCompare(a.dataset.name); });
      list.forEach(function (c) { grid.appendChild(c); });
    }
    chips.forEach(function (ch) {
      ch.addEventListener('click', function () {
        cat = ch.dataset.filter; chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === ch)); }); apply();
      });
    });
    search.addEventListener('input', apply);
    sort.addEventListener('change', function () {
      if (sort.value === 'default') { cards.sort(function (a, b) { return DATA.map(function (d) { return d.name.toLowerCase(); }).indexOf(a.dataset.name) - DATA.map(function (d) { return d.name.toLowerCase(); }).indexOf(b.dataset.name); }); }
      reorder();
    });
    var pre = new URLSearchParams(location.search).get('cat'); if (pre && CATS[pre]) { var b = qs('.chip[data-filter="' + pre + '"]'); if (b) b.click(); }
    var qp = new URLSearchParams(location.search).get('q'); if (qp) search.value = qp;
    apply();
  }

  /* Product detail page rendered from ?p=slug */
  function initDetail() {
    var root = qs('#productDetail'); if (!root) return;
    var slug = new URLSearchParams(location.search).get('p'), p = find(slug);
    if (!p) {
      root.innerHTML = '<div class="container section"><h2>Product not found</h2><p>Please choose a product from our <a href="products.html">catalogue</a>.</p></div>';
      qs('#pdTitle').textContent = 'Product Not Found'; qs('#pdLead').textContent = ''; return;
    }
    var title = p.name + ' | Primex Lanka Plastic';
    document.title = title; qs('#pdTitle').textContent = p.name; qs('#pdLead').textContent = p.desc; qs('#pdCrumb').textContent = p.name;
    var md = qs('meta[name="description"]'); if (md) md.content = p.name + ' from Primex Lanka Plastic. ' + p.desc;
    var base = 'assets/images/products/' + p.slug;
    var thumbs = [base + '.webp', base + '-2.webp', base + '-3.webp', base + '-4.webp'].map(function (s, i) {
      return '<button class="thumb" type="button" data-src="' + s + '" data-alt="' + esc(p.name) + ' view ' + (i + 1) + '"' + (i === 0 ? ' aria-current="true"' : '') + ' aria-label="Show image ' + (i + 1) + '">' + media(s, 'View ' + (i + 1), 'square') + '</button>';
    }).join('');
    var li = function (a) { return a.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join(''); };
    var related = DATA.filter(function (r) { return r.cat === p.cat && r.slug !== p.slug; });
    if (related.length < 3) related = related.concat(DATA.filter(function (r) { return r.cat !== p.cat && r.slug !== p.slug; }));
    related = related.slice(0, 3).map(function (r) {
      return '<article class="card product-card reveal in">' + media('assets/images/products/' + r.slug + '.webp', r.name) + '<div class="body"><span class="cat">' + esc(CATS[r.cat]) + '</span><h3>' + esc(r.name) + '</h3><p>' + esc(r.desc) + '</p><div class="actions"><a class="link-arrow" href="product-details.html?p=' + r.slug + '">View Details</a></div></div></article>';
    }).join('');
    root.innerHTML =
      '<section class="section"><div class="container split">' +
      '<div data-gallery><div class="gallery-main">' + media(base + '.webp', p.name, 'wide') + '</div><div class="gallery-thumbs">' + thumbs + '</div></div>' +
      '<div><div class="detail-meta"><span class="tag">' + esc(CATS[p.cat]) + '</span></div><h2>Overview</h2><p class="lead">' + esc(p.desc) + '</p>' +
      '<p>Made from polyethylene. Material grade and technical specifications are confirmed with our team when you request a quote.</p>' +
      '<div class="hero-actions"><a class="btn btn-primary" href="#inquiry">Request a Quote</a><a class="btn btn-outline" href="tel:+94112837241">Call +94 11 283 7241</a></div></div></div></section>' +
      '<section class="section soft"><div class="container grid grid-3">' +
      '<div class="card"><div class="icon-box"><svg viewBox="0 0 24 24"><path d="m5 12 4 4 10-10"/></svg></div><h3>Applications</h3><ul class="check-list">' + li(p.apps) + '</ul></div>' +
      '<div class="card"><div class="icon-box"><svg viewBox="0 0 24 24"><path d="M12 3v18M3 12h18"/></svg></div><h3>Customization Options</h3><ul class="check-list">' + li(p.custom) + '</ul></div>' +
      '<div class="card"><div class="icon-box"><svg viewBox="0 0 24 24"><path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15z"/></svg></div><h3>Features</h3><ul class="check-list"><li>Made to order to your requirement</li><li>Printing and branding options</li><li>Produced in Sri Lanka</li></ul></div></div></section>' +
      '<section class="section"><div class="container"><div class="section-head"><h2>Related Products</h2></div><div class="grid grid-3">' + related + '</div></div></section>';

    var sel = qs('#inquiry-product'); if (sel) sel.value = p.name;
    var ld = { '@context': 'https://schema.org', '@type': 'Product', name: p.name, description: p.desc, category: CATS[p.cat], brand: { '@type': 'Brand', name: 'Primex Lanka Plastic' }, manufacturer: { '@type': 'Organization', name: 'Primex Lanka Plastic (Pvt) Ltd' } };
    var s = document.createElement('script'); s.type = 'application/ld+json'; s.textContent = JSON.stringify(ld); document.head.appendChild(s);
  }

  function init() { fillSelects(); initCatalogue(); initDetail(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
