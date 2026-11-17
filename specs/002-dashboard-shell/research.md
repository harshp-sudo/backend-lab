# Research: Static Learning Dashboard Shell

**Feature**: [spec.md](spec.md) | **Date**: 2026-11-17
**Status**: Phase 0 complete; all design questions resolved. No application implementation or browser acceptance is claimed.

## 1. Exact catalog and content audit

**Decision:** Consume the existing manifest shape without adding route, file, parent, or progress properties. Keep the published [Manifest v1 schema](../001-backend-architecture/contracts/manifest.schema.json) authoritative for nonempty catalogs, with runtime checks for global ID and route uniqueness.

**Evidence:** Read the complete root `manifest.json`, canonical schema, [content contract](../001-backend-architecture/contracts/content-contract.md), full `topics/system-design/backend-architecture/code-and-domain-organization/clean-architecture.html`, and `topics/system-design/backend-architecture/_overview.html`. Also inspected the fixture's actual CSS and JS. The machine-readable [audit](contracts/manifest-audit.json) records hashes, all 21 IDs and derived targets, selectors, section keys, and question keys.

- Envelope: `schemaVersion: 1`, `roots: Node[]`.
- Every node: nonempty opaque whitespace-free `id`, `kind: hub|topic`, nonblank `title`, kebab-case `slug`.
- Roots are hubs. Hub `children` is required and nonempty; topics must omit `children`. Extra metadata is allowed and preserved.
- Actual inventory: six hubs, 15 lessons, 22 diagrams, 153 disclosures including 61 recall questions; code languages are JSON and SQL.
- Clean Architecture has six ordered sections, six mechanics disclosures, four recall disclosures, and two diagrams. One diagram is nested inside mechanics, so rendering must search all article descendants.

**Rationale:** Integration must use the generated lessons' real hooks rather than an imagined `path` field or replacement flashcard format.

**Alternatives considered:** Flattening or rewriting the catalog would break the recursive source of truth. Copying the fixture's abbreviated validator misses canonical restrictions.

**Empty-catalog resolution:** The published schema requires at least one root. The shell will tolerate exactly the otherwise-well-formed `{schemaVersion:1, roots:[]}` initialization case as a runtime empty state, retaining extra metadata as usual. This is explicitly not publish-valid and does not amend that schema. Every nonempty catalog follows the complete canonical restrictions; empty hub children remain invalid. Zero-leaf hub arithmetic is defensive pure-function behavior only. This reconciles the spec's empty UI with its existing-schema dependency.

## 2. Static deployment and route grammar

**Decision:** Deliver root `index.html`, `styles.css`, `app.js`, and empty `.nojekyll`; use local ES modules without a bundle. Resolve resources from `new URL('./', import.meta.url)` in root `app.js`, passed to supporting modules. Use literal relative resource paths and hash-only content links, never an origin-root `/topics` request.

**Rationale:** Repository Pages sites have a repository prefix, while fragments are browser-side and are not sent as part of HTTP resource requests. No custom 404 page or route rewrite is required. `.nojekyll` allows direct static publication including existing underscore-prefixed overview files. Enabling Pages itself remains a repository setting outside the feature.

**Alternatives considered:** Path routing needs a host fallback; a hard-coded repository prefix fails root/custom-domain deployments; using the fixture's `../../` base is wrong for root `app.js`.

**Sources:** [GitHub Pages overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [Creating a Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site), [URI fragments](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment).

## 3. CSS delivery and lesson vocabulary

**Decision:** Use authoring-only Tailwind CSS 3.4.17 CLI to generate committed root `styles.css` from `assets/styles/shell.css` and `tailwind.config.cjs`. No installation or build runs when browsing or deploying. Define semantic lesson classes as ordinary CSS outside purgeable utility layers, not utilities that must be discovered again for each lesson.

**Rationale:** This meets constitutional Tailwind and zero-config static delivery together. Official Play CDN guidance labels that runtime development-only. Shared semantic CSS makes future contract-compliant partials work without core CSS/JS changes.

**Integration:** Style `.kb-topic`, `.kb-hub`, `.kb-card`, all four `.kb-callout--*` variants, `.kb-table-wrap`, `.kb-diagram`, `.kb-question`, `.kb-references`, and hub `[data-child-links]`. Scope typography and disclosure rules to articles so application dialogs and navigation do not inherit lesson-card layout. Preserve native `details > summary`; ratings are outside summaries.

**Alternatives considered:** Runtime Play CDN introduces a production dependency for styling; handwritten CSS alone omits the constitutional stack; converting every partial to utilities forces content rewrites.

**Sources:** [Tailwind v3 CLI and static output](https://v3.tailwindcss.com/docs/installation), [3.4.17 tagged package](https://raw.githubusercontent.com/tailwindlabs/tailwindcss/v3.4.17/package.json), [Play CDN limitation](https://tailwindcss.com/docs/installation/play-cdn).

## 4. Diagram and code lifecycle

**Decision:** Retain fixture-compatible Mermaid 12.3.0 browser ESM and Highlight.js 11.11.1 browser asset pins. Mount validated complete prose before awaiting either library. Load the enhancements independently, retry failed dependency loads, and report partial enhancement failures truthfully.

**Lifecycle:** A single renderer owns Mermaid configuration, source snapshots, and a serialized enhancement queue. Initialize with `startOnLoad:false` and `securityLevel:'strict'`; reconfigure deliberately when theme changes. Rebuild diagrams from decoded source and await `mermaid.run({nodes})`. Check route/theme generations before and after async work. Highlight only mounted `pre:not(.mermaid) > code` once with `highlightElement`.

**Rationale:** The sample includes nested diagrams and native disclosures that must remain usable even when a CDN fails. Theme changes must not remount the article or reset answers/focus. Serializing global Mermaid work prevents concurrent route/theme configuration races.

**Alternatives considered:** Waiting for libraries before mounting strands readers on failure. Reprocessing SVG loses source. Copying fixture theme behavior would remount all content unnecessarily.

**Version caveat:** Mermaid's npm package declares Node >=22.12.0. Use its browser distribution, not its Node package, on the repository's Node 20.19.4. Tailwind authoring CLI and browser smoke checks are separate implementation validations.

**Sources:** [Mermaid usage](https://mermaid.js.org/config/usage.html), [Mermaid themes](https://mermaid.js.org/config/theming.html), [Mermaid tagged metadata](https://raw.githubusercontent.com/mermaid-js/mermaid/mermaid@12.3.0/packages/mermaid/package.json), [Highlight.js API](https://highlightjs.readthedocs.io/en/latest/api.html), [Highlight.js tagged metadata](https://raw.githubusercontent.com/highlightjs/highlight.js/11.11.1/package.json).

## 5. Persistent state and reviews

**Decision:** Store one versioned localStorage document keyed by immutable topic IDs, with question confidence keyed by stable recall keys. Persist explicit statuses, last visits, review cycles/history/session tokens, and theme preference. Derive paths, percentages, Continue Learning, and next due timestamps.

**Rationale:** Catalog moves preserve progress. One serialization avoids partially replaced records. A recorded review-session token makes completion idempotent even after reload. Explicit Start Review followed by Complete Review distinguishes intentional review from merely reading.

**Scheduling:** Intervals are [3,7,14,30] elapsed 24-hour days. First mastery begins cycle 1/index 0. Each explicit completion advances the index capped at 3; demotion retains history but excludes the topic; remastery begins the next cycle at index 0. Confidence never advances the topic schedule.

**Recovery:** Ordinary edits may remain in a clearly unsaved session if storage fails. Corrupt existing storage stays untouched and automatic writes stop. Import validates and previews first, confirms replacement, attempts one storage write, then publishes the new state. A failed import write preserves both current memory and prior stored data. Unknown IDs/questions round-trip unchanged.

**Alternatives considered:** Route-keyed records break on moves; storing percentages or next-due timestamps duplicates derived facts; implicit completion from views conflicts with the constitution; a confidence-driven scheduler is not specified.

## 6. Navigation, search, and overlays

**Decision:** Use ordinary recursive lists, links, and separate expansion buttons, not an ARIA tree widget. Keep one sidebar DOM tree and move it between desktop mount and mobile modal dialog. Use native modal dialogs for search and import preview too, with one modal open at a time.

**Search:** Flatten manifest metadata in preorder; normalize case and whitespace; rank exact title, exact title/path word or substring matches, then edit-distance-one title/token matches for queries of at least four characters. Final tie-break is manifest order. No extra fuzzy-search library.

**Rationale:** Native links preserve modified clicks/history, native dialogs provide modality, and local metadata matching meets the current scale without another runtime dependency. Explicitly manage opener focus, backdrop/Escape dismissal, resize, and route-change focus.

**Alternatives considered:** Duplicate mobile/desktop trees cause duplicate IDs and state drift. ARIA tree semantics impose additional keyboard behavior with no learning benefit. A search service would violate the lightweight local design.

**Source:** [HTML dialog behavior](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog).

## 7. Printing and evidence

**Decision:** Synchronously snapshot and open article disclosures in `beforeprint`, restore in `afterprint`, and use explicit light print tokens. Override dark SVG text/shapes/lines/markers and `foreignObject` descendants; never depend on asynchronous rerendering during print preparation.

**Rationale:** Earlier fixture PDFs revealed that HTML diagram labels also need dark-on-light overrides. Actual PDFs must prove hidden prose/answers are present; media emulation alone does not exercise the full lifecycle.

**Validation boundary:** Reuse existing content validator/tests as regressions, then test the actual root shell at both base paths. Unit-test state/route/search boundaries and use browser scenarios for real controls, focus, persistence, races, theme, and PDF output. Historical fixture passes are supporting evidence only.

**Source:** [beforeprint event](https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeprint_event).

## Research completion

Three focused research agents checked content integration, state design, and official platform/library documentation. Primary documentation was checked during this planning session; chosen versions are compatibility pins, not claims to be the newest releases. No unresolved clarification or constitutional exception remains.
