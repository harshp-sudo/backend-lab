# Dashboard Shell Acceptance

**Completed**: 2026-11-17 | **Feature**: 002-dashboard-shell | **Branch**: main

The production static dashboard is implemented in root `index.html`, `styles.css`, `app.js`, and `.nojekyll`, with three native modules in `assets/js/`. Committed Tailwind-generated CSS makes deployment independent of npm, a build, a backend, or route rewrites.

The dashboard integrates the existing manifest and all complete lesson/overview partials without changing their identities or source content. It provides a home learning view, recursive navigation, breadcrumbs, local fuzzy search, explicit status/confidence, review scheduling and sessions, persistent themes, validated JSON backup/restore, a mobile drawer, and complete print handling.

## Executed validation

| Gate | Result | Evidence |
| --- | --- | --- |
| Click and refresh all hubs/lessons | PASS: 21 destinations at each hosting base; 20 hub-child links per base | [Navigation](us1-navigation.json) |
| Repository-prefix resources | PASS: `/` and `/backend-lab/`; no wrong origin-root content requests | [Full browser report](final-acceptance.json) |
| Diagrams and recall | PASS: 22 diagrams and 61 keyboard-operated questions per base; no normal-path console or Mermaid errors | [Lessons](us3-learning.json) |
| Dashboard counts/next actions | PASS: empty/3-of-15/all-mastered and empty-catalog views | [Dashboard](us2-dashboard.json) |
| Reviews | PASS: boundary/model checks, explicit completion, reload/session replay and queue updates | [Review browser check](us4-reviews.json), [logic tests](unit-tests.json) |
| Search | PASS: title/path/typo ranking, both shortcuts, result keyboard activation, all 30 updates below 200ms in the final run | [Search](us5-search.json) |
| Mobile/theme/backup/recovery | PASS: 360px home/lesson, drawer/resize, keyboard status, persistent themes, exact roundtrip, invalid/cancelled imports and corrupt/quota storage | [Workspace](us6-workspace.json) |
| Actual print/PDF | PASS: all 21 articles from each theme, 42 PDFs; 1,260 paragraph comparisons; disclosure restoration | [Print results](final-acceptance.json) |
| Text contrast | PASS: 24 body/muted text/surface combinations, minimum 5.30:1 | [Contrast](contrast.json) |
| Catalog/state/search logic | PASS: 14 named tests on Node 20.19.4 | [Logic tests](unit-tests.json) |
| Existing content regression | PASS: 39 tests and content validator; original manifest/schema and all 21 partial hashes unchanged | [Content regression](content-regression.json), [baseline](content-baseline.json) |

Chromium 141.0.7390.37 with Playwright 1.56.0 exercised ten actual-shell browser scenario groups. Intentional network/storage faults were isolated from the normal-path console/Mermaid checks. Rendering-library failures preserved readable content and recovered through Retry. The final report maps all FR-001–FR-034 and SC-001–SC-010 outcomes.

PDF text checks cover every source paragraph, including hidden answers. Diagram and comparison-page contact sheets were reviewed; all 36 matched light/dark page pairs rendered identically, and an individual dark diagram was checked. The environment lacks decorative emoji font glyphs in printed section icons; section text, prose, diagrams, and answers remain complete and legible.

## Constitutional review

ELI5-first narratives and all six lesson modules remain complete and unchanged. Navigation/progress are manifest-driven with no fixed depth limit; a six-level browser catalog passed. Learning state uses immutable IDs and stable question keys, with explicit mastery and review actions. Rendering uses shared classes, preserved native disclosures and diagram sources, with truthful loading/failure states. The optional authoring-only Tailwind CLI and browser libraries follow the planned lightweight architecture. Mobile, theme, contrast, keyboard, persistence, backup and print requirements passed their affected checks.

The empty-root case is the documented runtime-only fallback; the canonical published schema remains unchanged. No constitutional exception or schema migration was introduced. Earlier fixture reports remain historical; these results come from the real dashboard.

## Delivery boundary

The static root is ready to serve through GitHub Pages after repository hosting is enabled. No GitHub settings, remote content, commits, pushes, or publication were changed by this implementation. CDN enhancements require connectivity and expose readable fallbacks/retry when unavailable; progress remains browser-local with JSON backup. PDF/screenshot bulk artifacts live under `/tmp`, not in deployment assets.

See the [run guide](../quickstart.md), [completed tasks](../tasks.md), and [runtime file hashes](runtime-hashes.json). No required feature task remains unimplemented.
