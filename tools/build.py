#!/usr/bin/env python3
"""Static page generator for the Primex website.
Run:  python3 tools/build.py      (from the project root)
Outputs plain HTML/JS files; no runtime dependency. Edit content here, rebuild, deploy."""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://primexlanka.com/"
PHONES = [("+94 11 283 7241", "+94112837241"), ("+94 11 289 5155", "+94112895155")]
HEAD_OFFICE = "No. 27/6, Old Kottawa Road, Maharagama, Sri Lanka."
FACTORY = "No. 131/A, Katuwana Industrial Estate, Katuwana Road, Homagama, Sri Lanka."
E = html.escape

# ---------------------------------------------------------------- icons
ICON = {
 "award": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14 7 22l5-3 5 3-1.5-8"/>',
 "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
 "cog": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
 "pen": '<path d="m4 20 1-4L16 5l3 3L8 19z"/><path d="m14 7 3 3"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.5-4 3-6 6.5-6s6 2 6.5 6"/><circle cx="17.5" cy="9" r="2.5"/><path d="M17 14c3 0 4.5 1.5 5 4.5"/>',
 "leaf": '<path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15z"/><path d="M5 19 13 11"/>',
 "box": '<path d="m12 3 8 4v10l-8 4-8-4V7z"/><path d="m4 7 8 4 8-4M12 11v10"/>',
 "print": '<path d="M6 9V3h12v6"/><rect x="3" y="9" width="18" height="8" rx="1"/><path d="M7 14h10v7H7z"/>',
 "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
 "truck": '<path d="M2 6h11v10H2zM13 9h4l3 3v4h-7z"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
 "sprout": '<path d="M12 21v-9"/><path d="M12 12C12 8 9 6 4 6c0 4 3 6 8 6zM12 14c0-3 2-5 7-5 0 3-2 5-7 5z"/>',
 "shirt": '<path d="m8 3-5 3 2 4 3-1v12h8V9l3 1 2-4-5-3c-1 2-2.5 3-4 3S9 5 8 3z"/>',
 "cup": '<path d="M5 4h14l-2 17H7z"/><path d="M6 9h12"/>',
 "candy": '<circle cx="12" cy="12" r="4.5"/><path d="m7.5 9-4-3v12l4-3M16.5 9l4-3v12l-4-3"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12H19l2-8H6"/>',
 "factory": '<path d="M3 21V10l6 4v-4l6 4V6h3v15z"/>',
 "recycle": '<path d="M7 19H4l3-5M7 19l-2-3M17 5l3 5M17 5l-5-1M12 4 9 9M17 19h-5M15 16l-3 3 3 3M5 9l2-5 4 1"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
 "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "heart": '<path d="M12 21s-8-5.5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 10c0 5.5-8 11-8 11z"/>',
 "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
 "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-8 8"/>',
 "pin": '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 "tools": '<path d="M14.5 6.5a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8zM4 20l5-5"/>',
}
def icon(name, cls=""):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" class="{cls}">{ICON[name]}</svg>'
def ibox(name):
    return f'<div class="icon-box">{icon(name)}</div>'

def media(path, label, cls="", alt=None):
    a = E(alt if alt is not None else label)
    return (f'<div class="media {cls}"><span class="media-label">{icon("image")}{E(label)}</span>'
            f'<img src="{path}" alt="{a}" loading="lazy" onerror="this.hidden=true"></div>')

# ---------------------------------------------------------------- products
RAW = [
 ("general-purpose-rolls","General Purpose Rolls","rolls","Polyethylene rolls for general packaging, wrapping and protection needs.",
  ["General packaging and wrapping","Covering and protection","Further conversion into bags"],["Custom thickness (micron)","Width and length","Colour tinting"]),
 ("general-purpose-rolls-110","General Purpose Rolls – Width up to 110","rolls","Wide-format polyethylene rolls for larger packaging and covering requirements.",
  ["Large-format packaging","Industrial covering","Bulk wrapping"],["Custom thickness (micron)","Width and length","Colour tinting"]),
 ("shrink-purpose-rolls","Shrink Purpose Rolls","rolls","Shrink-purpose sheets and rolls for bundling and unit protection.",
  ["Bundling and multipacks","Product protection","Retail and industrial packing"],["Thickness and width","Length","Printing on request"]),
 ("biodegradable-bags","Biodegradable Bags","bags","Bags from the Biodegradable range for customers looking for more environmentally considered packaging. Contact us to confirm suitability for your application.",
  ["Retail and shopping","Food and general packaging","Brand-conscious packaging"],["Size and thickness","Printing and branding","Handle styles"]),
 ("side-seal-bags-without-adhesive","Side Seal Bags Without Adhesive","bags","Side-sealed polyethylene bags with an open mouth and no adhesive strip.",
  ["Apparel and textiles","Food and confectionery","General retail packing"],["Size and thickness","Colour tinting","Multi-colour printing"]),
 ("side-seal-bags-with-adhesive","Side Seal Bags With Adhesive","bags","Side-sealed bags with an adhesive strip for convenient closing.",
  ["Apparel and garments","Stationery and retail items","Document and product packing"],["Size and thickness","Printing and branding","Barcodes"]),
 ("shopping-bags","Shopping Bags","bags","Carry bags for supermarkets and retail outlets.",
  ["Supermarkets","Retail stores","Promotional carry bags"],["Size and thickness","Punch handle cutting","Logo printing"]),
 ("perforation-bags","Perforation Bags","bags","Perforated polyethylene bags for products that need ventilation.",
  ["Produce and agriculture","Bakery and food","Industrial packing"],["Size and thickness","Perforation pattern","Printing on request"]),
 ("garbage-bags","Garbage Bags","bags","Polyethylene bags for waste collection in homes, businesses and facilities.",
  ["Household waste","Commercial and institutional use","Industrial cleaning"],["Size and thickness","Colour","Packing format"]),
 ("side-seal-bottom-gusset-bags","Side Seal Bottom Gusset Bags","bags","Side-sealed bags with a bottom gusset for fuller, more stable packing.",
  ["Food and confectionery","Bulk products","Retail packing"],["Size and gusset","Thickness","Printing and branding"]),
 ("patch-handle-bags","Patch Handle Bags","bags","Bags with a reinforced patch handle for comfortable carrying.",
  ["Retail and boutique","Supermarkets","Promotional use"],["Size and thickness","Colour","Logo printing"]),
 ("nursery-bags","Nursery Bags","agri","Polyethylene bags for raising and handling nursery plants.",
  ["Plant nurseries","Seedling production","Horticulture"],["Size and thickness","Colour","Perforation on request"]),
 ("mulch-sheets","Mulch Sheets","agri","Polyethylene sheets for covering soil in agricultural use.",
  ["Crop cultivation","Horticulture","Soil covering"],["Width and length","Thickness","Colour"]),
 ("hanger-bags","Hanger Bags","bags","Bags designed for hanging display and garment-style presentation.",
  ["Apparel and garments","Retail display","Accessories packing"],["Size and thickness","Printing and branding","Hanger style"]),
 ("grow-bags","Grow Bags","agri","Polyethylene grow bags for container-based cultivation.",
  ["Container farming","Home and commercial gardening","Horticulture"],["Size and thickness","Colour","Perforation on request"]),
 ("courier-bags","Courier Bags","bags","Courier and mailing bags for secure dispatch of parcels and orders.",
  ["E-commerce","Courier and logistics","Retail dispatch"],["Size and thickness","Multi-colour printing","Barcodes and branding"]),
 ("customized-packaging","Customized Packaging","custom","Packaging developed to your specification, from extrusion to printing and converting.",
  ["Brand-specific packaging","Special formats","Industry-specific requirements"],["Thickness and micron","Printing, logos and barcodes","Sealing and converting options"]),
]
CATS = {"all":"All Products","rolls":"Rolls & Films","bags":"Bags","agri":"Agriculture","custom":"Custom"}
CATNAME = {k:v for k,v in CATS.items() if k!="all"}
PRODUCTS = [dict(slug=s,name=n,cat=c,desc=d,apps=a,custom=cu) for (s,n,c,d,a,cu) in RAW]
PBY = {p["slug"]:p for p in PRODUCTS}
HOME6 = ["courier-bags","grow-bags","general-purpose-rolls","biodegradable-bags","shrink-purpose-rolls","perforation-bags"]
NAV_PRODUCTS = [("courier-bags","Courier Bags"),("grow-bags","Grow Bags"),("biodegradable-bags","Biodegradable Bags"),
 ("shrink-purpose-rolls","Shrink Films"),("perforation-bags","Perforation Bags"),("general-purpose-rolls","General Purpose Rolls"),("customized-packaging","Customized Packaging")]

def pdetail(slug): return f"product-details.html?p={slug}"

def product_card(p, home=False):
    name = "Shrink Purpose Sheets &amp; Rolls" if (home and p["slug"]=="shrink-purpose-rolls") else E(p["name"])
    text = " ".join([p["name"],p["desc"]," ".join(p["apps"])," ".join(p["custom"])]).lower()
    return f'''<article class="card product-card reveal" data-cat="{p["cat"]}" data-name="{E(p["name"].lower())}" data-text="{E(text)}">
  {media(f"assets/images/products/{p['slug']}.webp", p["name"], "", p["name"])}
  <div class="body"><span class="cat">{CATNAME[p["cat"]]}</span><h3>{name}</h3><p>{E(p["desc"])}</p>
  <div class="actions"><a class="link-arrow" href="{pdetail(p['slug'])}">View Details</a>
  <a class="btn btn-outline btn-sm" href="{pdetail(p['slug'])}#inquiry">Request a Quote</a></div></div></article>'''

# ---------------------------------------------------------------- layout
NAV = [("index.html","Home","home"),("about.html","About","about"),("sustainability.html","Sustainability","sustainability"),
       ("products.html","Products","products"),("contact.html","Contact Us","contact")]

def header(active):
    def cur(k): return ' aria-current="page"' if k==active else ""
    li = []
    for href,label,key in NAV:
        if True:
            li.append(f'<li><a class="nav-link" href="{href}"{cur(key)}>{label}</a></li>')
    li.append('<li class="mobile-cta"><a class="btn btn-primary" href="contact.html#quote">Request a Quote</a></li>')
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container header-inner">
<a class="logo logo-box" href="index.html" aria-label="Primex Lanka Plastic — Home"><img src="assets/logos/primex-logo.png" alt="Primex Lanka Plastic" height="56" onerror="this.hidden=true;this.nextElementSibling.hidden=false"><span class="logo-text" hidden>PRIMEX<small>LANKA PLASTIC</small></span></a>
<div class="header-right">
<div class="utility"><div class="utility-info"><a href="tel:{PHONES[0][1]}">☎ {PHONES[0][0]}</a><a href="tel:{PHONES[1][1]}">{PHONES[1][0]}</a><span class="util-addr"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.1-7-11a7 7 0 0 1 14 0c0 4.9-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>No. 27/6, Old Kottawa Road, Maharagama</span><span class="hide-md">Mon–Fri 8:30 AM–5:00 PM · Sat 8:30 AM–1:00 PM</span></div>
<div class="utility-tools"><div class="social-icons" aria-label="Social media">
<a href="#" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg></a>
<a href="#" target="_blank" rel="noopener" aria-label="X (Twitter)"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.2 2.3h3.3l-7.2 8.2 8.5 11.2h-6.6l-5.2-6.8-6 6.8H1.7l7.7-8.8L1.3 2.3h6.8l4.7 6.2zm-1.2 17.5h1.8L7 4.1H5z"/></svg></a>
<a href="#" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true" class="line"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" class="dot"/></svg></a>
<a href="#" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2C2 8.8 2 12 2 12s0 3.2.4 4.8a2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8c.4-1.6.4-4.8.4-4.8s0-3.2-.4-4.8zM10 15V9l5.2 3z"/></svg></a>
<a href="#" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.1c.5-1 1.8-1.9 3.7-1.9 4 0 4.7 2.6 4.7 6V21h-4v-5c0-1.2 0-2.8-1.7-2.8s-2 1.3-2 2.7V21h-4z"/></svg></a>
</div></div></div>
<div class="nav-row"><nav aria-label="Primary"><ul class="nav-menu" id="primary-menu">{"".join(li)}</ul></nav>
<a class="btn btn-primary btn-sm nav-cta" href="contact.html#quote">Request a Quote</a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-menu" aria-label="Open menu"><span></span><span></span><span></span></button></div>
</div></div></header>'''

def footer():
    return f'''<footer class="site-footer">
<picture><source srcset="assets/images/footer-skyline.webp" type="image/webp"><img class="footer-skyline" src="assets/images/footer-skyline.png" alt="" aria-hidden="true" loading="lazy" width="2576" height="345"></picture>
<div class="footer-band"><div class="container">
<div class="footer-grid">
<div class="footer-col"><div class="footer-logo-box"><img src="assets/logos/primex-logo.png" alt="Primex Lanka Plastic (Pvt) Ltd" onerror="this.hidden=true;this.nextElementSibling.hidden=false"><span class="logo-text" hidden>PRIMEX<small>LANKA PLASTIC</small></span></div>
<p>© <span id="footerYear">2026</span> Primex Lanka Plastic (Pvt) Ltd.<br>All Rights Reserved.</p><p><em>Infinite of Ideas – Powering the Packaging</em></p></div>
<div class="footer-col">{icon("pin")}<h3>Address</h3><p><strong>Head Office</strong><br>{HEAD_OFFICE.replace(", Maharagama",",<br>Maharagama")}</p><p><strong>Factory</strong><br>{FACTORY.replace("Estate, ","Estate,<br>")}</p></div>
<div class="footer-col">{icon("phone")}<h3>Telephone</h3><p><a href="tel:{PHONES[0][1]}">{PHONES[0][0]}</a><br><a href="tel:{PHONES[1][1]}">{PHONES[1][0]}</a></p></div>
<div class="footer-col">{icon("clock")}<h3>Business Hours</h3><p>Mon – Fri: 8:30 AM – 5:00 PM<br>Saturday: 8:30 AM – 1:00 PM</p></div>
</div>
<nav class="footer-links" aria-label="Footer"><a href="index.html">Home</a><a href="about.html">About Us</a><a href="products.html">Products</a><a href="manufacturing.html">Manufacturing</a><a href="sustainability.html">Sustainability</a><a href="quality-policy.html">Quality Policy</a><a href="certifications.html">Certifications</a><a href="contact.html">Contact</a><a href="privacy-policy.html">Privacy Policy</a><a href="terms.html">Terms &amp; Conditions</a></nav>
</div></div>
<button class="fab fab-top" id="backToTop" type="button" aria-label="Back to top"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
</footer>'''

ORG_LD = {"@context":"https://schema.org","@type":"Organization","name":"Primex Lanka Plastic (Pvt) Ltd","url":BASE,
  "slogan":"Infinite of Ideas – Powering the Packaging","telephone":PHONES[0][0],
  "address":{"@type":"PostalAddress","streetAddress":"No. 27/6, Old Kottawa Road","addressLocality":"Maharagama","addressCountry":"LK"}}
LOCAL_LD = {"@context":"https://schema.org","@type":"LocalBusiness","name":"Primex Lanka Plastic (Pvt) Ltd","url":BASE,
  "telephone":[p[0] for p in PHONES],
  "address":{"@type":"PostalAddress","streetAddress":"No. 27/6, Old Kottawa Road","addressLocality":"Maharagama","addressCountry":"LK"},
  "openingHoursSpecification":[
   {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:30","closes":"17:00"},
   {"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"08:30","closes":"13:00"}]}

def page(fname, title, desc, active, main, ld=None, hero=None):
    ldtag = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    canon = BASE + ("" if fname=="index.html" else fname)
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#E06800">
<meta property="og:type" content="website"><meta property="og:site_name" content="Primex Lanka Plastic (Pvt) Ltd">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}assets/images/hero/hero.webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@600;700;800&display=swap">
<link rel="stylesheet" href="css/style.css"><link rel="stylesheet" href="css/components.css"><link rel="stylesheet" href="css/animations.css"><link rel="stylesheet" href="css/responsive.css">
<script>document.documentElement.classList.add('js')</script>
{ldtag}
</head>
<body>
{header(active)}
<main id="main">
{main}
</main>
{footer()}
<script src="js/main.js" defer></script><script src="js/navigation.js" defer></script><script src="js/products.js" defer></script>
<script src="js/animations.js" defer></script><script src="js/forms.js" defer></script><script src="js/interactions.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(out)

def inner_hero(h1, lead, crumbs):
    bc = "".join(f'<li><a href="{h}">{l}</a></li>' for h,l in crumbs[:-1]) + f'<li aria-current="page">{crumbs[-1][1]}</li>'
    return f'<section class="page-hero"><div class="container"><ol class="breadcrumb" aria-label="Breadcrumb">{bc}</ol><h1>{h1}</h1><p>{lead}</p></div></section>'

def cta(title="Let's Build Better Packaging Together.", text="Have a packaging requirement? Our team is ready to help you find the right solution for your business.", b1="Contact Our Team", l1="contact.html"):
    return f'''<section class="cta-band"><div class="container reveal"><h2>{title}</h2><p>{text}</p>
<div class="hero-actions"><a class="btn btn-white" href="{l1}">{b1}</a><a class="btn btn-light" href="contact.html#quote">Request a Quote</a></div></div></section>'''

def sec_head(eyebrow, h, lead="", center=False):
    return f'<div class="section-head{" center" if center else ""} reveal"><span class="eyebrow">{eyebrow}</span><h2>{h}</h2>{f"<p class=lead>{lead}</p>" if lead else ""}</div>'

def inquiry_form(idv="quote", product_field=True, title="Send Us Your Requirement", lead=""):
    prod = '<div class="field"><label for="f-product">Product</label><select id="f-product" name="product"><option value="">Select a product</option></select></div>' if product_field else ""
    return f'''<div class="form-card" id="{idv}"><h3>{title}</h3>{f"<p>{lead}</p>" if lead else ""}
<form class="form" data-form novalidate>
<div class="form-row"><div class="field"><label for="{idv}-name">Full Name <span class="req">*</span></label><input id="{idv}-name" name="name" type="text" autocomplete="name" required><span class="error" role="alert"></span></div>
<div class="field"><label for="{idv}-company">Company Name</label><input id="{idv}-company" name="company" type="text" autocomplete="organization"><span class="error"></span></div></div>
<div class="form-row"><div class="field"><label for="{idv}-email">Email <span class="req">*</span></label><input id="{idv}-email" name="email" type="email" autocomplete="email" required><span class="error" role="alert"></span></div>
<div class="field"><label for="{idv}-phone">Phone <span class="req">*</span></label><input id="{idv}-phone" name="phone" type="tel" autocomplete="tel" required><span class="error" role="alert"></span></div></div>
<div class="form-row">{prod.replace('id="f-product"', f'id="{idv}-product"').replace('for="f-product"', f'for="{idv}-product"')}
<div class="field"><label for="{idv}-qty">Required Quantity</label><input id="{idv}-qty" name="quantity" type="text" placeholder="e.g. 500 kg / 10,000 pcs"><span class="error"></span></div></div>
<div class="field"><label for="{idv}-spec">Specifications</label><textarea id="{idv}-spec" name="specifications" placeholder="Size, thickness (micron), colour, printing, sealing…"></textarea></div>
<div class="field"><label for="{idv}-msg">Additional Message</label><textarea id="{idv}-msg" name="message"></textarea></div>
<div class="hp" aria-hidden="true"><label>Website<input class="hp-input" name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="form-status" role="status" tabindex="-1"></div>
<button class="btn btn-primary" type="submit">Submit Inquiry</button>
<p class="notice"><strong>Backend required:</strong> this form validates in the browser. Connect it to a server endpoint (see <code>js/main.js</code> → <code>formEndpoint</code>) before launch.</p>
</form></div>'''

# ---------------------------------------------------------------- pages
def build_home():
    cards = "".join(product_card(PBY[s], home=True) for s in HOME6)
    why = [("award","Manufacturing Experience","Years of hands-on experience, growing from a single cutter and extruder machine."),
           ("shield","Quality Commitment","A focus on consistent quality across every order."),
           ("cog","Advanced Production Capabilities","In-house extrusion, flexographic printing and converting."),
           ("pen","Customized Packaging Solutions","Packaging made to your size, thickness, colour and branding."),
           ("users","Customer-Centric Service","A team ready to understand your requirement and respond."),
           ("leaf","Sustainability Commitment","A closed-loop approach to production waste.")]
    whyh = "".join(f'<div class="card reveal" data-delay="{n%3}">{ibox(i)}<h3>{t}</h3><p>{d}</p></div>' for n,(i,t,d) in enumerate(why))
    inds = [("sprout","Agriculture"),("shirt","Apparel"),("cup","Food &amp; Beverage"),("candy","Confectionery"),("cart","Retail &amp; Supermarkets"),("truck","E-commerce &amp; Logistics"),("factory","Industrial Manufacturing")]
    indh = "".join(f'<div class="industry reveal">{ibox(i)}<span>{n}</span></div>' for i,n in inds)
    main = f'''
<section class="hero hero-slider" aria-roledescription="carousel" aria-label="Featured messages" data-video="assets/videos/hero.mp4" data-interval="6500">
<video class="hero-video" muted loop playsinline preload="metadata" aria-hidden="true" tabindex="-1"></video>
<div class="hero-track" aria-live="off">
<div class="slide slide-1 active" data-video="assets/videos/slide-1.mp4" role="group" aria-roledescription="slide" aria-label="1 of 3"><div class="slide-bg"><video class="slide-video" muted loop playsinline preload="none" aria-hidden="true"></video></div><div class="container slide-content">
<span class="eyebrow">Printing</span><h1 class="slide-title">Experts <em>In Printing</em></h1>
<p class="desc">Cutting-edge designs for packaging with top-tier quality for your products.</p>
<div class="hero-actions"><a class="btn btn-primary" href="manufacturing.html">Our Printing Capability</a><a class="btn btn-light" href="contact.html#quote">Request a Quote</a></div></div></div>
<div class="slide slide-2" data-video="assets/videos/slide-2.mp4" role="group" aria-roledescription="slide" aria-label="2 of 3"><div class="slide-bg"><video class="slide-video" muted loop playsinline preload="none" aria-hidden="true"></video></div><div class="container slide-content">
<span class="eyebrow">Brand Packaging</span><h2 class="slide-title">Transforming Packaging, <em>Elevating Brands</em></h2>
<p class="desc">Stylish, functional packaging that boosts brand image.</p>
<div class="hero-actions"><a class="btn btn-primary" href="products.html">Explore Our Products</a><a class="btn btn-light" href="contact.html#quote">Request a Quote</a></div></div></div>
<div class="slide slide-3" data-video="assets/videos/slide-3.mp4" role="group" aria-roledescription="slide" aria-label="3 of 3"><div class="slide-bg"><video class="slide-video" muted loop playsinline preload="none" aria-hidden="true"></video></div><div class="container slide-content">
<span class="eyebrow">Infinite of Ideas</span><h2 class="slide-title"><span class="thin">POWERING the</span> <em>PACKAGING</em></h2>
<p class="desc">A Legacy of Excellence in Packaging</p>
<div class="hero-actions"><a class="btn btn-primary" href="about.html">About Primex</a><a class="btn btn-light" href="sustainability.html">Sustainability</a></div></div></div>
</div>
<div class="hero-controls"><div class="container hero-controls-inner">
<button class="hc-btn" type="button" data-hero="prev" aria-label="Previous slide"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 5-7 7 7 7"/></svg></button>
<div class="hero-dots" role="group" aria-label="Choose slide"><button type="button" class="dot active" aria-label="Slide 1" aria-current="true"></button><button type="button" class="dot" aria-label="Slide 2"></button><button type="button" class="dot" aria-label="Slide 3"></button></div>
<button class="hc-btn" type="button" data-hero="next" aria-label="Next slide"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg></button>
</div></div>
</section>

<section class="section bs" aria-labelledby="bs-title"><div class="container bs-container">
<div class="bs-head reveal"><div class="section-head"><h2 id="bs-title">Our Trusted Partners</h2></div>
<div class="bs-nav"><button type="button" class="bs-btn" data-bs="prev" aria-label="Previous"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 5-7 7 7 7"/></svg></button><button type="button" class="bs-btn" data-bs="next" aria-label="Next"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg></button></div></div>
<div class="bs-wrap"><div class="bs-track" tabindex="0" aria-label="Our trusted partners">
<div class="bs-card"><span class="bs-ph">Partner 1 — add photo</span><img src="assets/images/partners/partner-1.webp" alt="CTM Group" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>CTM Group</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 2 — add photo</span><img src="assets/images/partners/partner-2.webp" alt="DSI" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>DSI</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 3 — add photo</span><img src="assets/images/partners/partner-3.webp" alt="Hayleys Agriculture" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Hayleys Agriculture</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 4 — add photo</span><img src="assets/images/partners/partner-4.webp" alt="Hela" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Hela</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 5 — add photo</span><img src="assets/images/partners/partner-5.webp" alt="Partner 5" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 5</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 6 — add photo</span><img src="assets/images/partners/partner-6.webp" alt="Partner 6" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 6</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 7 — add photo</span><img src="assets/images/partners/partner-7.webp" alt="Partner 7" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 7</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 8 — add photo</span><img src="assets/images/partners/partner-8.webp" alt="Partner 8" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 8</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 9 — add photo</span><img src="assets/images/partners/partner-9.webp" alt="Partner 9" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 9</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 10 — add photo</span><img src="assets/images/partners/partner-10.webp" alt="Partner 10" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 10</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 11 — add photo</span><img src="assets/images/partners/partner-11.webp" alt="Partner 11" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 11</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 12 — add photo</span><img src="assets/images/partners/partner-12.webp" alt="Partner 12" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 12</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 13 — add photo</span><img src="assets/images/partners/partner-13.webp" alt="Partner 13" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 13</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 14 — add photo</span><img src="assets/images/partners/partner-14.webp" alt="Partner 14" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 14</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 15 — add photo</span><img src="assets/images/partners/partner-15.webp" alt="Partner 15" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 15</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 16 — add photo</span><img src="assets/images/partners/partner-16.webp" alt="Partner 16" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 16</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 17 — add photo</span><img src="assets/images/partners/partner-17.webp" alt="Partner 17" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 17</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 18 — add photo</span><img src="assets/images/partners/partner-18.webp" alt="Partner 18" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 18</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 19 — add photo</span><img src="assets/images/partners/partner-19.webp" alt="Partner 19" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 19</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 20 — add photo</span><img src="assets/images/partners/partner-20.webp" alt="Partner 20" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 20</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 21 — add photo</span><img src="assets/images/partners/partner-21.webp" alt="Partner 21" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 21</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 22 — add photo</span><img src="assets/images/partners/partner-22.webp" alt="Partner 22" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 22</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 23 — add photo</span><img src="assets/images/partners/partner-23.webp" alt="Partner 23" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 23</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 24 — add photo</span><img src="assets/images/partners/partner-24.webp" alt="Partner 24" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 24</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 25 — add photo</span><img src="assets/images/partners/partner-25.webp" alt="Partner 25" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 25</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 26 — add photo</span><img src="assets/images/partners/partner-26.webp" alt="Partner 26" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 26</strong></span></div>
<div class="bs-card"><span class="bs-ph">Partner 27 — add photo</span><img src="assets/images/partners/partner-27.webp" alt="Partner 27" loading="lazy" onerror="this.hidden=true"><span class="bs-label"><small>Trusted Partner</small><strong>Partner 27</strong></span></div>
</div>
<aside class="bs-panel"><a class="bs-main" href="contact.html#quote"><strong>Request a Quote</strong><span>Tell us your packaging requirement</span></a><hr><a class="bs-main" href="products.html"><strong>Our Products</strong></a><svg class="bs-cubes" viewBox="0 0 190 260" aria-hidden="true"><path d="M52 16 L90 38 L90 82 L52 104 L14 82 L14 38Z M52 60 L14 38 M52 60 L90 38 M52 60 L52 104 M128 54 L166 76 L166 120 L128 142 L90 120 L90 76Z M128 98 L90 76 M128 98 L166 76 M128 98 L128 142 M52 92 L90 114 L90 158 L52 180 L14 158 L14 114Z M52 136 L14 114 M52 136 L90 114 M52 136 L52 180 M128 130 L166 152 L166 196 L128 218 L90 196 L90 152Z M128 174 L90 152 M128 174 L166 152 M128 174 L128 218 M52 168 L90 190 L90 234 L52 256 L14 234 L14 190Z M52 212 L14 190 M52 212 L90 190 M52 212 L52 256"/></svg><a class="bs-arrow" href="products.html" aria-label="Our Products"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg></a></aside></div>
</div></section>

<section class="stats" aria-label="Company highlights"><div class="container grid grid-3">
<!-- VERIFY: figures supplied in the brief; confirm with Primex before launch -->
<div class="reveal"><div class="stat-num" data-count="15" data-suffix="+">15+</div><div class="stat-label">Years of Experience</div></div>
<div class="reveal" data-delay="1"><div class="stat-num" data-count="300">300</div><div class="stat-label">Tons Monthly Production Capacity</div></div>
<div class="reveal" data-delay="2"><div class="stat-num" data-count="99.9" data-decimals="1" data-suffix="%">99.9%</div><div class="stat-label">Customer Satisfaction</div></div>
</div></section>

<section class="section"><div class="container split">
<div class="reveal"><span class="eyebrow">About Primex</span><h2>More Than Packaging. A Commitment to Excellence.</h2>
<p class="lead">Primex Lanka Plastic (Pvt) Ltd began its journey with a single cutter and extruder machine. Today, the company serves the packaging industry through its manufacturing capabilities, commitment to innovation and focus on quality.</p>
<a class="btn btn-primary" href="about.html">Read More</a></div>
<div class="reveal" data-delay="1">{media("assets/images/factory/factory-main.webp","Primex factory — add authentic photo","wide","Primex Lanka Plastic factory")}</div>
</div></section>

<section class="section soft"><div class="container">
{sec_head("Products","Discover Our Packaging Solutions","Polyethylene and flexible packaging for agriculture, retail, logistics and industry.")}
<div class="grid grid-3">{cards}</div>
<p style="text-align:center;margin-top:40px"><a class="btn btn-outline" href="products.html">View All Products</a></p>
</div></section>

<section class="section"><div class="container">
{sec_head("Why Primex","Why Businesses Choose Primex","",True)}
<div class="grid grid-3">{whyh}</div></div></section>

<section class="section dark"><div class="container">
{sec_head("Capabilities","Precision. Innovation. Manufacturing Excellence.","",True)}
<div class="grid grid-3">
<div class="reveal"><div class="cap-num">01</div><h3>Custom Extrusion</h3><ul class="cap-list"><li>Custom thickness</li><li>Micron specifications</li><li>Width and length customization</li><li>Colour tinting</li></ul></div>
<div class="reveal" data-delay="1"><div class="cap-num">02</div><h3>Flexographic Printing</h3><ul class="cap-list"><li>Multi-colour printing</li><li>Custom branding</li><li>Logos and barcodes</li></ul></div>
<div class="reveal" data-delay="2"><div class="cap-num">03</div><h3>Converting &amp; Finishing</h3><ul class="cap-list"><li>Bottom sealing</li><li>Side sealing</li><li>Punch handle cutting</li><li>Specialized pouch converting</li></ul></div>
</div><p style="text-align:center;margin-top:40px"><a class="btn btn-light" href="manufacturing.html">Explore Manufacturing</a></p></div></section>

<section class="section"><div class="container">
{sec_head("Industries","Industries We Serve","",True)}
<div class="grid grid-4">{indh}</div></div></section>

<section class="section soft"><div class="container">
{sec_head("Sustainability","Creating a More Sustainable Packaging Future","Primex runs a closed-loop recycling approach for its production waste.",True)}
<ol class="flow">
<li class="reveal"><h3>Production Waste Collection</h3><p>Offcuts and production waste are collected at the factory.</p></li>
<li class="reveal" data-delay="1"><h3>Recycling</h3><p>Collected material is recycled in-house.</p></li>
<li class="reveal" data-delay="2"><h3>Reusable Raw Materials</h3><p>Recycled material returns to production as raw material.</p></li>
<li class="reveal" data-delay="3"><h3>Environmental Responsibility</h3><p>Reducing waste is part of how we operate.</p></li></ol>
<p style="text-align:center;margin-top:40px"><a class="btn btn-primary" href="sustainability.html">Explore Our Sustainability Commitment</a></p>
</div></section>

<section class="section"><div class="container split">
<div class="reveal"><span class="eyebrow">Quality &amp; Certifications</span><h2>Quality You Can Verify</h2>
<p class="lead">Certificates are published here only once their validity has been confirmed.</p>
<a class="btn btn-outline" href="certifications.html">View Certifications</a> <a class="btn btn-outline" href="quality-policy.html">Quality Policy</a></div>
<div data-cert-list data-limit="2" class="grid grid-2"><div class="notice" data-cert-empty><strong>Certificates pending verification.</strong> Genuine certificate images will appear here after Primex confirms them.</div></div>
</div></section>

<section class="section soft"><div class="container">
{sec_head("Our Promise","Packaging Built Around Your Business","",True)}
<div class="grid grid-3">
<div class="card reveal">{ibox("target")}<h3>Made to Your Specification</h3><p>Tell us the size, thickness, colour and print — we manufacture to your requirement.</p></div>
<div class="card reveal" data-delay="1">{ibox("layers")}<h3>One Partner, Start to Finish</h3><p>Extrusion, printing and converting under one roof.</p></div>
<div class="card reveal" data-delay="2">{ibox("recycle")}<h3>Responsible Production</h3><p>Production waste is recycled back into the process.</p></div>
</div></div></section>
{cta()}'''
    page("index.html","Plastic Packaging Manufacturer in Sri Lanka | Primex Lanka Plastic",
         "Primex Lanka Plastic (Pvt) Ltd manufactures polyethylene rolls, courier bags, grow bags, biodegradable bags and customized flexible packaging in Sri Lanka.",
         "home", main, ORG_LD)

def build_about():
    vals = [("bulb","Innovation"),("shield","Quality Assurance"),("heart","Customer-Centric Approach"),("award","Experience"),("leaf","Sustainability")]
    valh = "".join(f'<div class="card reveal">{ibox(i)}<h3>{n}</h3></div>' for i,n in vals)
    main = inner_hero("About Primex Lanka Plastic","A Sri Lankan manufacturer of polyethylene and flexible packaging.",[("index.html","Home"),("about.html","About Us")]) + f'''
<section class="section"><div class="container split">
<div class="reveal"><span class="eyebrow">Company Introduction</span><h2>More Than Packaging. A Commitment to Excellence.</h2>
<p class="lead">Primex Lanka Plastic (Pvt) Ltd began its journey with a single cutter and extruder machine. Today, the company serves the packaging industry through its manufacturing capabilities, commitment to innovation and focus on quality.</p>
<p>Based in Sri Lanka, Primex produces polyethylene rolls and bags for agriculture, retail, logistics and industrial customers.</p></div>
<div class="reveal" data-delay="1">{media("assets/images/about/about-main.webp","Primex team or factory — add authentic photo","wide","Primex Lanka Plastic")}</div></div></section>

<section class="section soft"><div class="container">{sec_head("Company History","Our Journey")}
<div class="grid grid-2"><div class="card reveal">{ibox("factory")}<h3>The Beginning</h3><p>Primex began with a single cutter and extruder machine.</p></div>
<div class="card reveal" data-delay="1">{ibox("layers")}<h3>Today</h3><p>The company now serves the packaging industry through its manufacturing capabilities, innovation and focus on quality.</p></div></div>
<div class="notice reveal" style="margin-top:24px"><strong>To complete:</strong> add verified milestones (founding year, expansions, key investments) supplied by Primex.</div></div></section>

<section class="section"><div class="container">{sec_head("Purpose, Vision &amp; Mission","What Drives Us","",True)}
<div class="grid grid-3">
<div class="card reveal">{ibox("target")}<h3>Our Purpose</h3><p>To help businesses succeed through exceptional packaging.</p></div>
<div class="card reveal" data-delay="1">{ibox("eye")}<h3>Vision</h3><p>Empowering Businesses with Exceptional Packaging.</p></div>
<div class="card reveal" data-delay="2">{ibox("award")}<h3>Mission</h3><p>To deliver innovative, sustainable, and high-quality packaging solutions that empower businesses to thrive and achieve their fullest potential.</p></div></div></div></section>

<section class="section soft"><div class="container">{sec_head("Core Values","What We Stand For","",True)}<div class="grid grid-3">{valh}</div></div></section>

<section class="section"><div class="container split">
<div class="reveal"><span class="eyebrow">Manufacturing Expertise</span><h2>Extrusion, Printing and Converting</h2>
<ul class="check-list"><li>Custom extrusion with thickness, width, length and colour options</li><li>Flexographic printing with logos and barcodes</li><li>Converting and finishing: sealing, handle cutting, pouches</li></ul>
<a class="btn btn-primary" href="manufacturing.html" style="margin-top:16px">See Manufacturing</a></div>
<div class="reveal" data-delay="1">{media("assets/images/manufacturing/extrusion.webp","Extrusion line — add authentic photo","wide","Primex extrusion")}</div></div></section>

<section class="section soft"><div class="container">{sec_head("Leadership, Team &amp; Partners","The People Behind Primex")}
<div class="notice reveal"><strong>Pending approval:</strong> leadership profiles, team photographs and partner logos are shown only when verified and approved by Primex. Nothing has been invented here.</div></div></section>
{cta("Work With Primex","Tell us about your packaging requirement and our team will get back to you.")}'''
    page("about.html","About Us | Primex Lanka Plastic (Pvt) Ltd","Learn about Primex Lanka Plastic: our journey from a single extruder, our vision, mission, values and manufacturing expertise.","about",main)

def build_products():
    chips = "".join(f'<button class="chip" type="button" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{v}</button>' for k,v in CATS.items())
    cards = "".join(product_card(p) for p in PRODUCTS)
    main = inner_hero("Products &amp; Services","Polyethylene rolls, bags and customized packaging for every industry.",[("index.html","Home"),("products.html","Products")]) + f'''
<section class="section"><div class="container">
<div class="filter-bar"><div class="chips" role="group" aria-label="Filter by category">{chips}</div>
<div class="tools"><label class="sr" for="productSearch" style="position:absolute;left:-9999px">Search products</label><input id="productSearch" type="search" placeholder="Search products…" autocomplete="off">
<label for="productSort" style="position:absolute;left:-9999px">Sort products</label><select id="productSort"><option value="default">Sort: Default</option><option value="az">Name A–Z</option><option value="za">Name Z–A</option></select></div></div>
<p id="productCount" aria-live="polite" style="color:var(--text-secondary)"></p>
<div class="grid grid-3" id="productGrid">{cards}</div>
<div class="empty-state" id="noResults" hidden><h3>No products found</h3><p>Try a different search or category — or <a href="contact.html#quote">tell us what you need</a>.</p></div>
<div class="notice" style="margin-top:40px"><strong>Specifications:</strong> thickness, sizes and printing are made to order. Technical specifications are confirmed with our team when you request a quote.</div>
</div></section>
{cta("Can't Find What You Need?","Primex manufactures to specification. Share your requirement and we will advise on the right solution.")}'''
    page("products.html","Products | Polythene Bags, Rolls, Courier & Grow Bags | Primex Lanka","Browse Primex Lanka Plastic products: general purpose rolls, shrink rolls, biodegradable bags, courier bags, grow bags, perforation bags and customized packaging.","products",main)

def build_product_details():
    main = f'''<section class="page-hero"><div class="container"><ol class="breadcrumb" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li><a href="products.html">Products</a></li><li aria-current="page" id="pdCrumb">Product</li></ol>
<h1 id="pdTitle">Product Details</h1><p id="pdLead">Loading product information…</p></div></section>
<div id="productDetail"><noscript><div class="container section"><p>Please enable JavaScript to view product details, or <a href="products.html">browse all products</a>.</p></div></noscript></div>
<section class="section soft"><div class="container"><div class="qr-split"><div><span class="eyebrow">Inquiry</span><h2>Request a Quote for This Product</h2><p class="lead">Share your required quantity and specifications and our team will respond.</p>
<p><a href="tel:{PHONES[0][1]}">{PHONES[0][0]}</a><br><a href="tel:{PHONES[1][1]}">{PHONES[1][0]}</a></p></div>{inquiry_form("inquiry", True, "Product Inquiry")}</div></div></section>'''
    page("product-details.html","Product Details | Primex Lanka Plastic","Product details, applications and customization options from Primex Lanka Plastic.","products",main)

def build_manufacturing():
    def capblock(n, title, items, img, label, flip=False):
        lis = "".join(f"<li>{i}</li>" for i in items)
        left = f'<div class="reveal"><div class="cap-num">{n}</div><h2>{title}</h2><ul class="cap-list">{lis}</ul></div>'
        right = f'<div class="reveal" data-delay="1">{media(img,label,"wide",title)}</div>'
        return f'<section class="section{" soft" if flip else ""}"><div class="container split">{right+left if flip else left+right}</div></section>'
    main = inner_hero("Precision. Innovation. Manufacturing Excellence.","From extrusion to finished product, under one roof in Sri Lanka.",[("index.html","Home"),("manufacturing.html","Manufacturing")]) + f'''
<section class="section"><div class="container"><div class="split"><div class="reveal"><span class="eyebrow">Overview</span><h2>Integrated Polyethylene Manufacturing</h2>
<p class="lead">Primex began with a single cutter and extruder machine. Today our capabilities span custom extrusion, flexographic printing, and converting &amp; finishing.</p></div>
<ol class="flow" style="grid-template-columns:1fr 1fr"><li class="reveal"><h3>Extrusion</h3><p>Film made to your thickness, width and colour.</p></li><li class="reveal"><h3>Printing</h3><p>Flexographic printing for brands.</p></li><li class="reveal"><h3>Converting</h3><p>Sealing, cutting and pouch-making.</p></li><li class="reveal"><h3>Recycling</h3><p>Production waste returns to the process.</p></li></ol></div></div></section>
{capblock("01","Extrusion Capabilities",["Custom thickness","Micron specifications","Width and length customization","Colour tinting"],"assets/images/manufacturing/extrusion.webp","Extrusion — add authentic photo",True)}
{capblock("02","Flexographic Printing",["Multi-colour printing","Custom branding","Logos and barcodes"],"assets/images/manufacturing/printing.webp","Flexographic printing — add authentic photo")}
{capblock("03","Converting &amp; Finishing",["Bottom sealing","Side sealing","Punch handle cutting","Specialized pouch converting"],"assets/images/manufacturing/converting.webp","Converting — add authentic photo",True)}
<section class="section"><div class="container split"><div class="reveal"><span class="eyebrow">Factory Facilities</span><h2>Our Primary Factory</h2><p class="lead">{FACTORY}</p><p>Head Office: {HEAD_OFFICE}</p><a class="btn btn-outline" href="contact.html#map">View Location</a></div>
<div class="reveal" data-delay="1">{media("assets/images/factory/factory-main.webp","Factory exterior — add authentic photo","wide","Primex factory at Katuwana Industrial Estate")}</div></div></section>
<section class="section soft"><div class="container"><div class="grid grid-2">
<div class="card reveal">{ibox("shield")}<h3>Quality Control</h3><p>Our approach to quality is set out on the <a href="quality-policy.html">Quality Policy</a> page.</p></div>
<div class="card reveal" data-delay="1">{ibox("tools")}<h3>Custom Manufacturing</h3><p>Thickness, micron, size, colour, printing, sealing and handles — made to your specification. <a href="contact.html#quote">Request a quote</a>.</p></div></div></div></section>
<section class="section"><div class="container">{sec_head("Industries Served","Packaging for Many Industries","",True)}
<div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center"><span class="tag">Agriculture</span><span class="tag">Apparel</span><span class="tag">Food &amp; Beverage</span><span class="tag">Confectionery</span><span class="tag">Retail &amp; Supermarkets</span><span class="tag">E-commerce &amp; Logistics</span><span class="tag">Industrial Manufacturing</span></div></div></section>
{cta("Discuss Your Production Requirement","Send us your specification and we will advise on the best manufacturing route.","Make an Inquiry","contact.html#quote")}'''
    page("manufacturing.html","Manufacturing | Extrusion, Printing & Converting | Primex Lanka Plastic","Primex Lanka Plastic manufacturing: custom extrusion, flexographic printing and converting & finishing at Katuwana Industrial Estate, Homagama.","manufacturing",main)

def build_sustain():
    main = inner_hero("Moving Towards a Sustainable Packaging Future.","How Primex reduces waste through closed-loop recycling.",[("index.html","Home"),("sustainability.html","Sustainability")]) + f'''
<section class="section"><div class="container split"><div class="reveal"><span class="eyebrow">Overview</span><h2>Sustainability at Primex</h2>
<p class="lead">We aim to reduce waste in our own production and to offer packaging options that help customers meet their environmental goals.</p>
<p>Plastic packaging has an environmental impact, and we do not claim that all products are biodegradable or environmentally harmless. Where a product belongs to our Biodegradable range, please contact us to confirm suitability for your application.</p></div>
<div class="reveal" data-delay="1">{media("assets/images/sustainability/recycling.webp","Recycling operation — add authentic photo","wide","Primex recycling")}</div></div></section>
<section class="section soft"><div class="container">{sec_head("Closed-Loop Recycling","From Waste to Raw Material","",True)}
<ol class="flow"><li class="reveal"><h3>Collect</h3><p>Production waste is collected at the factory.</p></li><li class="reveal" data-delay="1"><h3>Recycle</h3><p>The material is recycled.</p></li><li class="reveal" data-delay="2"><h3>Reuse</h3><p>Recycled material becomes reusable raw material.</p></li><li class="reveal" data-delay="3"><h3>Produce</h3><p>It returns to production, closing the loop.</p></li></ol></div></section>
<section class="section"><div class="container"><div class="grid grid-3">
<div class="card reveal">{ibox("leaf")}<h3>Environmental Sustainability</h3><p>Recycling production waste helps reduce material that would otherwise be discarded.</p></div>
<div class="card reveal" data-delay="1">{ibox("layers")}<h3>Economic Sustainability</h3><p>Reusing raw material makes production more efficient and supports long-term business resilience.</p></div>
<div class="card reveal" data-delay="2">{ibox("users")}<h3>Social Sustainability</h3><p>We aim to provide steady work and a responsible workplace for our team and community.</p></div>
<div class="card reveal">{ibox("recycle")}<h3>Waste Management</h3><p>Waste from cutting and converting is collected for recycling.</p></div>
<div class="card reveal" data-delay="1">{ibox("target")}<h3>Environmental Responsibility</h3><p>We continue to look for ways to reduce waste across production.</p></div>
<div class="card reveal" data-delay="2">{ibox("sprout")}<h3>Biodegradable Range</h3><p>A Biodegradable Bags range is available. <a href="{pdetail("biodegradable-bags")}">View details</a>.</p></div></div>
<div class="notice reveal" style="margin-top:32px"><strong>To confirm with Primex:</strong> recycling capacity, percentage of waste recycled and any environmental claims before publishing numbers.</div></div></section>
{cta("Talk to Us About Sustainable Options","Ask our team about our recycling approach and the Biodegradable Bags range.")}'''
    page("sustainability.html","Sustainability & Closed-Loop Recycling | Primex Lanka Plastic","Primex Lanka Plastic's approach to sustainability: closed-loop recycling of production waste and a biodegradable bags range.","sustainability",main)

def build_quality():
    secs = [("Quality Commitment","We aim to deliver consistent, reliable packaging that meets agreed customer requirements."),
            ("Product Safety","We aim to produce packaging that is safe for its intended use."),
            ("Quality Assurance","Quality is checked through the production process, from material to finished product."),
            ("Raw Material Inspection","Incoming raw material is inspected before it is used in production."),
            ("Production Monitoring","Production is monitored to maintain consistency."),
            ("Finished Product Inspection","Finished products are inspected before dispatch."),
            ("Hygiene and Safety","We maintain a clean and safe working environment."),
            ("Continuous Improvement","We review our processes and look for ways to improve."),
            ("Customer Satisfaction","We listen to customer feedback and act on it.")]
    cards = "".join(f'<div class="card reveal"><span class="cap-num" style="font-size:1.6rem">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(secs))
    main = inner_hero("Quality Policy","Our commitment to quality, safety and customer satisfaction.",[("index.html","Home"),("quality-policy.html","Quality Policy")]) + f'''
<section class="section"><div class="container"><div class="notice reveal" style="margin-bottom:32px"><strong>Draft wording — approval required.</strong> The existing website's policy text refers to another company (Selakta International (Pvt) Ltd) and has not been used. Replace the statements below with Primex's approved quality policy before launch.</div>
<div class="grid grid-3">{cards}</div></div></section>
<section class="section soft"><div class="container"><div class="grid grid-2"><div class="reveal"><h2>Certifications</h2><p class="lead">See the verified certificates held by Primex Lanka Plastic.</p></div><div class="reveal" style="align-self:center"><a class="btn btn-primary" href="certifications.html">View Certifications</a></div></div></div></section>
{cta("Questions About Quality?","Our team can discuss your quality requirements.")}'''
    page("quality-policy.html","Quality Policy | Primex Lanka Plastic","Primex Lanka Plastic's quality commitment: product safety, inspection, monitoring and continuous improvement.","quality",main)

def build_certs():
    main = inner_hero("Certifications","Verified certificates held by Primex Lanka Plastic.",[("index.html","Home"),("quality-policy.html","Quality"),("certifications.html","Certifications")]) + f'''
<section class="section"><div class="container">
<div data-cert-list class="grid grid-3"><div class="notice" data-cert-empty style="grid-column:1/-1"><strong>Certificates will appear here once verified.</strong> We publish only certificates confirmed as valid and issued to Primex Lanka Plastic (Pvt) Ltd, each with its genuine certificate image, issuing organization, number and validity.</div></div>
<div class="card reveal" style="margin-top:32px"><h3>For Primex: how to add a certificate</h3><p>Add each verified certificate to <code>certificates</code> in <code>js/main.js</code> (name, issuer, number, valid, image, note) and place the image in <code>assets/images/about/</code>. It will display on this page and the homepage automatically.</p></div>
</div></section>
<section class="section soft"><div class="container"><div class="section-head reveal"><h2>Frequently Asked Questions</h2></div>
<div class="accordion reveal">
<div class="acc-item"><h3><button class="acc-btn" type="button" aria-expanded="false" aria-controls="a1" id="b1">Can I ask for a certificate copy?</button></h3><div class="acc-panel" id="a1" role="region" aria-labelledby="b1"><div><p>Yes. Contact our team and we will share the relevant documents once verified.</p></div></div></div>
<div class="acc-item"><h3><button class="acc-btn" type="button" aria-expanded="false" aria-controls="a2" id="b2">Where can I read the quality policy?</button></h3><div class="acc-panel" id="a2" role="region" aria-labelledby="b2"><div><p>See the <a href="quality-policy.html">Quality Policy</a> page.</p></div></div></div>
</div></div></section>
{cta("Need Documentation for Your Business?","Contact us and we will advise on available documents.")}'''
    page("certifications.html","Certifications | Primex Lanka Plastic","Verified certifications held by Primex Lanka Plastic (Pvt) Ltd.","quality",main)

def build_contact():
    faqs = [("How do I request a quote?","Use the form on this page or call us. Share the product, quantity and specifications."),
            ("Can I order custom sizes or printing?","Yes. Primex offers custom thickness, width, length, colour tinting and flexographic printing."),
            ("Do you offer biodegradable options?","We list a Biodegradable Bags range. Contact us to confirm suitability for your application."),
            ("Where are you located?","Head Office in Maharagama; factory at Katuwana Industrial Estate, Homagama.")]
    acc = "".join(f'<div class="acc-item"><h3><button class="acc-btn" type="button" aria-expanded="false" aria-controls="f{i}" id="fb{i}">{q}</button></h3><div class="acc-panel" id="f{i}" role="region" aria-labelledby="fb{i}"><div><p>{a}</p></div></div></div>' for i,(q,a) in enumerate(faqs))
    q = "Primex+Lanka+Plastic+Katuwana+Industrial+Estate+Homagama+Sri+Lanka"
    main = inner_hero("Contact Us","Speak to our team about your packaging requirement.",[("index.html","Home"),("contact.html","Contact")]) + f'''
<section class="section"><div class="container"><div class="grid grid-4">
<div class="card contact-card reveal">{ibox("pin")}<h3>Head Office</h3><p>{HEAD_OFFICE}</p></div>
<div class="card contact-card reveal" data-delay="1">{ibox("factory")}<h3>Primary Factory</h3><p>{FACTORY}</p></div>
<div class="card contact-card reveal" data-delay="2">{ibox("phone")}<h3>Telephone</h3><p><a href="tel:{PHONES[0][1]}">{PHONES[0][0]}</a><br><a href="tel:{PHONES[1][1]}">{PHONES[1][0]}</a></p></div>
<div class="card contact-card reveal" data-delay="3">{ibox("clock")}<h3>Business Hours</h3><p>Mon – Fri: 8:30 AM – 5:00 PM<br>Saturday: 8:30 AM – 1:00 PM</p></div></div>
<p style="text-align:center;margin-top:24px" data-social></p></div></section>
<section class="section soft"><div class="container"><div class="qr-split"><div class="reveal"><span class="eyebrow">Request a Quote</span><h2>Tell Us What You Need</h2><p class="lead">Share your product, quantity and specifications. Prefer to talk? Call <a href="tel:{PHONES[0][1]}">{PHONES[0][0]}</a>.</p></div>{inquiry_form("quote", True, "Inquiry Form")}</div></div></section>
<section class="section" id="map"><div class="container">{sec_head("Find Us","Factory Location")}
<div class="map-wrap reveal"><iframe title="Map showing the Primex factory location" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={q}&amp;output=embed"></iframe></div>
<p style="margin-top:12px"><a href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener">Open in Google Maps</a> · <span style="color:var(--text-secondary)">Verify the pin against the factory address before launch.</span></p></div></section>
<section class="section soft"><div class="container prose" style="margin-inline:auto"><div class="section-head"><h2>Frequently Asked Questions</h2></div><div class="accordion">{acc}</div></div></section>'''
    page("contact.html","Contact Us | Primex Lanka Plastic (Pvt) Ltd","Contact Primex Lanka Plastic: head office in Maharagama, factory in Homagama, phone numbers, business hours and a quote request form.","contact",main,LOCAL_LD)

def legal(fname, title, desc, h1, body):
    main = inner_hero(h1, "Last updated: November 2026", [("index.html","Home"),(fname,h1)]) + f'<section class="section"><div class="container prose"><div class="notice"><strong>Draft — legal review required.</strong> Have this text reviewed by Primex\'s legal adviser before launch.</div>{body}</div></section>'
    page(fname,title,desc,"",main)

def build_legal():
    legal("privacy-policy.html","Privacy Policy | Primex Lanka Plastic","How Primex Lanka Plastic handles personal information submitted through this website.","Privacy Policy",'''
<h2>Information we collect</h2><p>When you submit an inquiry we collect the details you provide: name, company, email, phone, product, quantity and message.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry or quote request</li><li>To communicate about products and orders</li></ul>
<h2>Sharing</h2><p>We do not sell your personal information. We may share it with service providers who help us operate this website or respond to you.</p>
<h2>Third-party services</h2><p>This website loads fonts from Google Fonts and may show an embedded Google Map. These services may process technical data such as your IP address under their own policies.</p>
<h2>Retention and your rights</h2><p>We keep inquiry details only as long as needed for the purpose above. You may ask us to access, correct or delete your information.</p>
<h2>Contact</h2><p>Primex Lanka Plastic (Pvt) Ltd, No. 27/6, Old Kottawa Road, Maharagama, Sri Lanka. Telephone: +94 11 283 7241.</p>''')
    legal("terms.html","Terms & Conditions | Primex Lanka Plastic","Terms governing the use of the Primex Lanka Plastic website.","Terms &amp; Conditions",'''
<h2>Use of this website</h2><p>By using this website you agree to these terms. Content is provided for general information about Primex Lanka Plastic (Pvt) Ltd and its products.</p>
<h2>Product information</h2><p>Descriptions, images and specifications are indicative. Final specifications, pricing and availability are confirmed in a written quotation.</p>
<h2>Intellectual property</h2><p>The Primex name, logo and website content belong to Primex Lanka Plastic (Pvt) Ltd and may not be reused without permission.</p>
<h2>Liability</h2><p>We make reasonable efforts to keep this website accurate but do not guarantee it is free of errors or interruptions.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of Sri Lanka.</p>
<h2>Contact</h2><p>Telephone: +94 11 283 7241 · +94 11 289 5155.</p>''')

# ---------------------------------------------------------------- products.js
PRODUCTS_JS = r'''
(function () {
  'use strict';
  var P = window.Primex = window.Primex || {};
  var qs = function (s, r) { return (r || document).querySelector(s); };
  var qsa = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var CATS = __CATS__;
  var DATA = P.products = __DATA__;
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
'''

def write_support():
    js = PRODUCTS_JS.replace("__DATA__", json.dumps(PRODUCTS, ensure_ascii=False, indent=1)).replace("__CATS__", json.dumps(CATNAME, ensure_ascii=False))
    with open(os.path.join(ROOT,"js","products.js"),"w",encoding="utf-8") as f: f.write(js)
    pages = ["index","about","products","product-details","manufacturing","sustainability","quality-policy","certifications","contact","privacy-policy","terms"]
    urls = "".join(f"  <url><loc>{BASE}{'' if p=='index' else p+'.html'}</loc></url>\n" for p in pages)
    urls += "".join(f"  <url><loc>{BASE}product-details.html?p={p['slug']}</loc></url>\n" for p in PRODUCTS)
    with open(os.path.join(ROOT,"sitemap.xml"),"w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls.replace("&","&amp;")+'</urlset>\n')
    with open(os.path.join(ROOT,"robots.txt"),"w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")

if __name__ == "__main__":
    for fn in (build_home,build_about,build_products,build_product_details,build_manufacturing,build_sustain,build_quality,build_certs,build_contact,build_legal):
        fn()
    write_support()
    print("built")