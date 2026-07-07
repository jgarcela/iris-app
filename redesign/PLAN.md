# IRIS Web Redesign Plan — Clay-Inspired Aesthetic

Source of truth for the visual system: [`DESIGN.md`](./DESIGN.md).

## Decisions
- **Typography:** Space Grotesk (Roobert substitute) + Space Mono, via Google Fonts. No commercial licensing.
- **Rollout:** Token + Bootstrap override layer first (Phases 0–2) for a fast global reskin, then iterate page-by-page.
- **Stack context:** Flask + Jinja, Bootstrap 5.3, FontAwesome, Lucide. ~478 `var(--…)` usages already flow through CSS variables — the primary leverage point.

## Architecture: layered CSS, loaded in order
1. `design-tokens.css` — Clay palette, shadows, radii, type scale (NEW, loaded first)
2. Bootstrap 5.3 (CDN)
3. `clay-bootstrap.css` — restyle Bootstrap primitives (NEW)
4. `styles.css` — existing `:root` retokenized to point at Clay tokens
5. Per-page CSS (admin/analysis/create_analysis/dashboard/difficulty_enhancements)

---

## Phase 0 — Foundations
- [ ] Add Space Grotesk + Space Mono to `base.html`.
- [ ] Create `static/css/design-tokens.css`: swatch palette (matcha/slushie/lemon/ube/pomegranate/blueberry), cream bg `#faf9f7`, oat borders `#dad4c8`/`#eee9df`, clay 3-layer shadow, hard-offset hover shadow `-7px 7px`, radius scale (4/8/12/24/40/pill), type scale.
- [ ] Load `design-tokens.css` first in `base.html`.

## Phase 1 — Retokenize `styles.css` `:root`
- [ ] Repoint existing variables to Clay tokens (bg→cream, borders→oat, shadows→clay, font→Space Grotesk).
- [ ] Instantly reskins nav, cards, footer, forms via existing `var()` refs.

## Phase 2 — Bootstrap override layer (`clay-bootstrap.css`)
- [x] `.btn` family + signature hover (rotateZ(-8deg) + translateY + `-7px 7px`), pill CTAs.
- [x] `.card`, `.navbar`, `.badge`, `.form-control`, `.modal`, `.table`, `.alert`.
- [x] Map `bg-*` / `text-muted` to swatch/warm-neutral tokens.

## Phase 3 — Per-page CSS
- [x] Retokenize admin.css, analysis.css, create_analysis.css, dashboard.css, difficulty_enhancements.css.

## Phase 4 — Landing + auth
- [x] index.html, login.html, register.html full Clay treatment (cream hero, 80px display, swatch sections).

## Phase 5 — Cleanup
- [x] Sweep 363→~42 hardcoded hex + 81 inline styles in templates → token classes.

## Phase 6 — Dark mode + QA
- [x] Reconcile `[data-theme="dark"]` with warm/deep-swatch palette.
- [ ] Walk every route at mobile/tablet/desktop.
