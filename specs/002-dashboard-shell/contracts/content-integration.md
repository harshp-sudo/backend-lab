# Dashboard Content Integration Contract

**Version**: 1 | **Scope**: FR-003/004/017–020/030–034
**Authority**: This adds host obligations to the existing [Content and Host Contract v1](../../001-backend-architecture/contracts/content-contract.md), without changing partials.

## Inspected input and unchanged identities

The exact catalog and all derived resources are captured in [manifest-audit.json](manifest-audit.json). The complete sample read during planning is:

`topics/system-design/backend-architecture/code-and-domain-organization/clean-architecture.html`

Its node ID is `d257fdd8-8532-4138-839b-7295ae2e2994`. It contains six mechanics details, four recall details, and two diagrams, including a sequence diagram inside a mechanics disclosure. Its stable question keys are `dependency-direction`, `four-circles`, `adapter-tests`, and `error-semantics`. Integration must discover all descendants, not just top-level diagrams.

Also inspected `topics/system-design/backend-architecture/_overview.html`; it uses native `[data-child-links]` list items as the four subcategory roadmap cards. The shell must style those existing items, not replace the overview with a second hand-maintained catalog.

## Envelope and lifecycle

1. Parse fetched text off-canvas. Require exactly one article with the selected node ID, matching `.kb-topic` or `.kb-hub`, and the expected title. Reject invalid envelopes before mounting.
2. Preserve the complete article and all authored headings, sections, links, code, and answer text. No scripts, style overrides, storage operations, or application chrome belong in partial files.
3. Mount prose and native disclosures immediately after validation. Add host-owned controls in memory, then load diagram/highlighting dependencies independently.
4. Announce content availability separately from enhancement success/failure. A missing library must not prevent reading.
5. Capture each diagram's decoded `textContent` before rendering. Maintain sources in renderer-owned node records, not a second modified content file.
6. On navigation, invalidate/abort prior fetch work and guard every async stage with the active route generation. On a theme change, use a theme generation too. Serialize Mermaid configuration/render calls, and discard disconnected/stale jobs.
7. On a same-topic section change, retain the mounted article and controls, open necessary containing details, and scroll to the requested section. Do not refetch or reset answer visibility merely to scroll.

The six section keys remain `hook-eli5`, `big-picture`, `mechanics`, `trade-offs`, `pitfalls`, and `mastery`. IDs remain `node-<node-id>-<section-key>`.

## CSS selector mapping

| Existing selector | Shell style/behavior |
| --- | --- |
| `.kb-topic, .kb-hub` | Readable centered article width (approximately 78ch); generous spacing; responsive h1–h3; preserve heading hierarchy. |
| Article `section[data-section]` | Consistent spacing and header-aware anchor offset; respect reduced motion. |
| `.kb-card` | Neutral bordered surface and rounded corners, supported even though the current batch does not use this class. |
| `.kb-callout--structure` | Blue semantic surface for structure. |
| `.kb-callout--insight` | Yellow semantic surface for ELI5/WHY. |
| `.kb-callout--impact` | Green semantic surface for outcomes. |
| `.kb-callout--pitfall` | Pink/red semantic surface for failure stories. |
| Article `details, summary` | Native disclosure, clear focus/marker, bordered cards, spacing when open; never globally force answers visible on screen. |
| `details.kb-question[data-recall-id]` | Independent native recall disclosure; host rating group after answer content, outside summary. |
| `.kb-diagram, pre.mermaid` | Diagram surface, local overflow, visible source fallback on error, responsive SVG. |
| `.kb-table-wrap` | Local horizontal scroll; table header/caption/border styles; no page overflow. |
| `pre:not(.mermaid) > code` | Highlight applicable language-* code; monospace; scrolling on screen, wrapping in print. |
| `.kb-hub [data-child-links]` | Responsive grid of immediate-child cards; retain existing labels, order, links, and explanatory paragraphs. |
| `.kb-references` | Muted readable source footer and wrapping long URLs. |

Scope prose/table/disclosure rules to the canvas articles. Keep application navigation lists, modal headings, and search results independent.

### Tokens and typography

Use Inter with system sans-serif fallback, and JetBrains Mono with system monospace fallback. Remote fonts are optional enhancements. Light base `#FAFAFA`; paper `#FFFFFF`; body text `#202B38`; muted text `#596675`; border `#DCE3E9`. Semantic light surfaces begin from fixture colors blue `#EDF4FF`, yellow `#FFF8DD`, green `#EDF8EF`, pink `#FFF0F2`.

Dark base `#151B23`; paper `#1C2530`; body `#E6EDF5`; muted `#B6C1CD`; border `#3C4B5D`. Semantic dark surfaces begin from blue `#202F48`, yellow `#3B3420`, green `#20382C`, pink `#412832`. Verify body/link/control contrast rather than treating these initial tokens as proof of accessibility.

Keep all supported semantic selectors outside Tailwind's removable utility/component layers. Scan `index.html`, `app.js`, `assets/js/**/*.js`, and `topics/**/*.html` for utility classes; shared partials require no new utility classes to render. Committed `styles.css` is the runtime stylesheet; source is `assets/styles/shell.css`.

## Native recall and learning controls

- A fresh article mount starts each `details.kb-question` closed. Never add a shared `name` attribute.
- Leave the native summary as the question toggle. Pointer, Enter, and Space retain native behavior.
- Append exactly one labeled confidence group per question, using buttons with `aria-pressed` for Hard, Good, and Easy. Its state is keyed by article ID + recall key, not index or text.
- Rating controls are outside `summary` and inside the disclosed answer area. They must not toggle the details element.
- Opening/closing an answer is transient and does not write mastery or review completion. Saved confidence remains when an article remounts.
- Add a host status control and footer to topic articles only. The footer includes Mark as Mastered, or already-mastered state plus Start Review/Complete Review and explicit status change.
- Start Review is a deliberate action that creates/preserves a session; opening a due topic does not do so. After completion, show a completed state and explicit Start Another Review action.
- Mark all added control containers with host-owned data attributes so repeated rendering cannot duplicate them. The disk partial remains unchanged.

## Diagram and code assets

| Dependency | Exact browser asset |
| --- | --- |
| Mermaid 12.3.0 | `https://cdn.jsdelivr.net/npm/mermaid@12.3.0/dist/mermaid.esm.min.mjs` |
| Highlight.js 11.11.1 | `https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.11.1/highlight.min.js` |

A single renderer owns Mermaid initialization with `startOnLoad:false`, `securityLevel:'strict'`, and theme-aware configuration. Initial configuration is shared; only explicit theme changes reconfigure it. Use saved sources to replace diagram nodes, then await rendering; do not remount the whole article for a theme change. Preserve native disclosure states, rating controls, and focus.

Highlight only unprocessed code nodes. Known current explicit languages are JSON and SQL; unsupported languages remain plain readable text. A failure in either library must not block the other's enhancement. Clear rejected dependency promises so Retry actually retries.

## Print contract

Synchronously snapshot all article details and open them before printing; restore their individual states after printing, idempotently. Hide header/sidebar/overlays and every host learning control. Use light paper/body/code tokens, wrap code and tables, and fit diagrams to page width.

Set high-contrast print styles for SVG text/tspan, shapes, paths/lines, markers, and `foreignObject` descendant text/backgrounds. Do not wait for asynchronous theme rendering in `beforeprint`. Print controls may await any active enhancement job before invoking printing; native browser print must still expose complete prose synchronously.

Acceptance requires actual PDFs for all 21 articles in both themes, checking hidden answers and prose, visual legibility, and post-print restoration. The earlier fixture's success does not establish dashboard compliance.
