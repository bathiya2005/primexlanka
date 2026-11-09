# Primex Lanka Plastic — Website (HTML / CSS / Vanilla JS)

Open `index.html` in a browser, or upload the folder to any static host. No backend needed for browsing.

## Structure
- 11 pages in the root, `css/` (style, components, animations, responsive), `js/` (main, navigation, products, animations, forms, interactions), `assets/`, `sitemap.xml`, `robots.txt`.
- `tools/build.py` regenerates all HTML + `js/products.js` (`python3 tools/build.py`). Edit content there, then rebuild.

## Before launch — things YOU must supply
1. **Logo**: save the original as `assets/logos/primex-logo.png` (a text wordmark shows until then).
2. **Photos** (WebP): `assets/images/products/<slug>.webp` (+ `-2`, `-3`, `-4` for the gallery), `factory/factory-main.webp`, `about/about-main.webp`, `manufacturing/{extrusion,printing,converting}.webp`, `sustainability/recycling.webp`, optional `hero/hero.webp`. Until added, tidy placeholders show.
3. **Brand colours**: `--brand-primary:#E06800` etc. in `css/style.css` were sampled from the supplied skyline artwork, NOT from primexlanka.com (the site was not reachable from the build environment). Confirm and update.
4. **Forms**: set `Primex.config.formEndpoint` in `js/main.js`. Until then forms validate but show a "backend not connected" notice.
5. **Social links / certificates**: fill `Primex.config.social` and `Primex.config.certificates` in `js/main.js`.
6. **Verified email**: none is displayed (none was supplied).

## Verification checklist (content needing approval)
- [ ] Stats: 15+ years, 300 tons/month, 99.9% satisfaction (from brief, unconfirmed)
- [ ] Addresses, phone numbers, business hours; Google Maps pin
- [ ] Product names/descriptions/applications/customization lists (written generically; no specs invented)
- [ ] Biodegradable Bags wording; sustainability/recycling statements
- [ ] Quality Policy — replace draft with approved Primex policy (do NOT use the Selakta International text)
- [ ] Certifications (ISO 9001:2015, ISO 22000, GRS, RCS) — add only if valid and held by Primex
- [ ] Leadership, team, partners, testimonials — none shown
- [ ] Privacy Policy and Terms — legal review
