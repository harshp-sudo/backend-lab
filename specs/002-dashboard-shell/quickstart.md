# Quickstart and Validation Guide: Dashboard Shell

**Feature**: [spec.md](spec.md) | **Date**: 2026-11-17

The dashboard and all validation tools below are implemented. The final acceptance run passed all ten browser scenario groups at root and repository-prefix URLs, 14 dashboard logic tests, 39 existing content tests, and 42 PDF outputs. See [acceptance summary](evidence/acceptance-summary.md) and [full browser evidence](evidence/final-acceptance.json).

## Prerequisites

- For normal use/deployment: committed static files, an HTTP(S) static host, and an evergreen browser. No Node, package installation, application server, or build.
- For validation: Python 3.10+, Node 20+, and browser test tooling. Linux may require the shared libraries documented by Playwright's browser installation.
- Optional CSS maintenance: Node/npm and network access for pinned Tailwind CLI. Generated root CSS is committed; deploying never invokes this step.
- Run commands below from the repository root. Browser/PDF dependencies belong in an external virtual environment and are not deployed.

## 1. Existing content regression (available now)

```sh
python3 -m unittest discover -s tests/content -p 'test_*.py' -v
python3 tools/validate_content.py --repo-root . --expect tests/content/backend-architecture.json --report /tmp/backend-architecture-content.json
```

Expected: existing 39 tests pass; content validation succeeds. The audit baseline remains six hubs, 15 topics, 22 diagrams, 61 recall items, all IDs unchanged. Current content/fixture evidence is not evidence that the new dashboard works.

## 2. Optional CSS authoring (maintainer only)

```sh
npx --yes tailwindcss@3.4.17 -c ./tailwind.config.cjs -i ./assets/styles/shell.css -o ./styles.css --minify
```

Expected: root `styles.css` is generated with all shared semantic selectors intact. Confirm `.kb-card`, each callout variant, hub child cards, native article details, diagram/table wrappers, and print/foreignObject rules survive generation. Validate the CLI on available Node 20.19.4. Do not install Mermaid's Node package for this browser-only application.

## 3. Pure logic tests

```sh
node --experimental-default-type=module --test tests/dashboard/test_*.mjs
```

Expected test groups:

- Catalog: exact schema restrictions, duplicate IDs/routes, preserved metadata/order, root hubs, nonempty child rules, explicit runtime empty-root sentinel, and six-level recursion.
- Routes: topic/hub/home and six allowed section keys; reject unknown nodes, queries, duplicates, trailing slashes, encoded separators, dot segments, and normalization tricks.
- Search: title/path/case, insertion/deletion/substitution, bucket ranking and manifest-order ties.
- State: 0/15, 3/15=20%, 15/15, hub and unknown-record exclusion, empty guards, and every Continue Learning fallback.
- Review: all due intervals at -1ms/exact/+1ms, inclusive comparisons, final repeating 30 days, explicit session replay/reload, demotion/remastery, and timezone-independent elapsed days.
- Restore: populated roundtrip with unknown IDs/keys; invalid format/version/enums/calendar times/history; cancelled import and failed write preserve memory/storage; corrupt initial storage blocks automatic writes.
- Identity: move/rename a node without changing its ID and retain status, visits, reviews, and question ratings.

These checks verify behavior and failure boundaries. The direct per-file commands below also display all 14 named logic tests:

```sh
node --experimental-default-type=module tests/dashboard/test_catalog.mjs
node --experimental-default-type=module tests/dashboard/test_learning_state.mjs
```

## 4. Preview root and repository-path deployment

In terminal A:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

In terminal B, still starting from the repository root:

```sh
python3 -m http.server 8001 --bind 127.0.0.1 --directory ..
```

Open these two views of the same assets:

- Root: `http://127.0.0.1:8000/`
- Repository path: `http://127.0.0.1:8001/backend-lab/`

For both, directly open and refresh:

`#/system-design/backend-architecture/code-and-domain-organization/clean-architecture`

Also open its `?section=mechanics` hash query. Expected: correct article, active ancestors, full breadcrumbs, two diagrams (one inside mechanics), and no request to an incorrect origin-root topics directory. Browser back/forward must retain valid routing; clicking a hub must load its overview.

Confirm an empty root `.nojekyll` exists. Deploy the repository's static root through GitHub Pages without a package/build step or path edits. Enabling Pages in repository settings is a separate publishing prerequisite, not performed by this guide.

## 5. Browser harness setup and contract

Development requirements: `playwright==1.56.0` and `jsonschema==4.25.1` in `tests/dashboard/requirements.txt`.

The harness must explicitly check canonical UTC calendar values (or register a date-time format checker). A minimal jsonschema installation may omit optional date-time validators, so passing its structural validation alone does not prove a date such as February 30 is rejected.

```sh
python3 -m venv /tmp/backend-lab-dashboard-venv
/tmp/backend-lab-dashboard-venv/bin/python -m pip install -r tests/dashboard/requirements.txt
/tmp/backend-lab-dashboard-venv/bin/python -m playwright install chromium
```

Run the full browser suite:

```sh
/tmp/backend-lab-dashboard-venv/bin/python tests/dashboard/check_dashboard.py --base-url http://127.0.0.1:8000/ --project-url http://127.0.0.1:8001/backend-lab/ --report /tmp/dashboard-browser.json --pdf-dir /tmp/dashboard-pdfs
```

For an incremental check, append `--story US1` (or US2–US6); omitting it runs all six stories. US6/full runs require `--pdf-dir` to satisfy the print gate.

Harness interface: both URLs are required and refer to the same catalog; `--report` writes structured acceptance results and `--pdf-dir` enables all-article print checks. A failed required scenario exits nonzero. Missing libraries/browser/PDF tooling must fail or identify an unexecuted gate, never count as a pass.

Report browser/OS/reference-device details, viewport/theme/base URL, dependency pins, unexpected console/page/request errors, checked routes/IDs, search latency samples, scenario outcomes, and print artifacts. Test expected fault-injection errors separately from unexpected failures.

## 6. Actual-shell acceptance scenarios

### Catalog, home, and navigation

- Open/reload all 21 destinations at both base URLs; follow all 20 hub-child edges; exercise breadcrumbs, native modified clicks, history, and section links.
- Start from empty progress: home shows 0/15, a catalog-derived Backend Architecture category card, a first-lesson shortcut, and an empty review queue. Its overview has the four existing subcategory cards.
- Seed exactly three current mastered records: home/header show 20%, matching subtree badges and counts.
- Exercise last-visited unfinished, no-visit fallback, hub-only visits, all-mastered due/next, runtime empty-root initialization, and synthetic six-level navigation.
- Intercept a missing/invalid manifest, missing partial, mismatched article identity, and slow earlier request. Show recoverable errors and ensure only the latest request owns the canvas/context.

### Rendering and learning

- Verify all 22 diagrams and language-tagged JSON/SQL code across all articles. Process nested diagrams, not only direct children.
- Reveal/hide all 61 answers independently by keyboard. Rate a question and verify only its chosen confidence persists after navigation/reload.
- Reading/revealing never changes Not Started or a due schedule. Status changes update home/sidebar/header consistently; repeated mastery clicks are idempotent.
- Block Mermaid alone and Highlight.js alone, then retry. Complete prose and native controls remain usable; failed enhancements are visibly identified.
- Change theme rapidly during navigation; check no duplicate diagrams/controls, preserved disclosure/focus state, and no stale rendering ownership.
- Rename/move a manifest node in an isolated intercepted catalog with its ID retained and equivalent partial response; verify saved status/review/question records follow the ID.

### Reviews and persistence

- Use a controlled reference clock for each interval boundary at -1ms, exact time, and +1ms.
- Open a due topic without completing it: it remains due. Start Review explicitly and Complete Review once: it leaves the queue. Repeated completion/reload cannot advance again.
- Start another review explicitly to test early review; test demotion/remastery and final repeating 30-day intervals.
- Return home/refocus and cross a due instant while home stays open; verify queue refresh without manual reload.
- Simulate corrupt storage and a throwing/quota-limited write. Reading/session edits/export remain usable with an unsaved warning; original corrupt bytes remain untouched.
- Simulate an import write failure: unlike an ordinary unsaved edit, restoration leaves both current memory and stored state unchanged.

### Backup interface

- Validate [the example](contracts/progress-backup.example.json) against the [schema](contracts/progress-backup.schema.json), then the semantic [state rules](contracts/progress-state.md).
- Import through the real preview/confirmation UI. At its reference time the known Clean Architecture record contributes 1/15 (7%) and is due; the unmatched topic is retained and excluded.
- Export and restore into a fresh browser context, comparing the complete saved workspace values. Restoration repaint must not stamp a new visit.
- Exercise invalid version/status/timestamp/history, cancellation/Escape, matched/unmatched ID counts, explicit theme, and unknown recall keys. All invalid/cancelled cases preserve the prior record.

### Mobile, keyboard, and print

- At 360px and desktop width: open/close drawer, traverse deep branches, resize with drawer open, choose a route, and verify focus. No page-wide horizontal overflow; table/diagram local scrolling is allowed.
- Use only keyboard for search, rating, status, theme, export, import preview, and drawer. Confirm modal focus containment, Escape/backdrop behavior, selected search result, and opener/content focus restoration.
- Check body-text contrast >=4.5:1, visible focus, non-color-only status, reduced motion, and font fallback in both themes.
- Generate actual PDFs of all 21 articles from each theme (42 outputs). Verify all source prose and hidden answers are present, controls are absent, diagrams/tables remain readable, dark SVG/foreignObject text is legible, and disclosure states restore.
- Compare decoded source paragraph/answer text with normalized extracted PDF text; visually inspect diagrams/tables in every PDF. Media emulation alone is insufficient. Document the PDF engine and available extraction/rendering tools.

## Acceptance completion

The checked-in [final report](evidence/final-acceptance.json) records passing results for SC-001–SC-010 and FR-001–FR-034. Chromium 141.0.7390.37 / Playwright 1.56.0 performed the browser checks; Node 20.19.4 performed logic checks. Body/muted-text token contrast passed all 24 tested combinations (minimum 5.30:1). All 42 PDFs preserved the complete 630 source paragraphs per theme (1,260 comparisons) and restored disclosure states.

Generated PDFs, rendered review sheets and screenshots remain under `/tmp/backend-dashboard-pdfs` and `/tmp/backend-dashboard-print-review`; their paths are local run artifacts, not deployment prerequisites. The local run used the existing external Playwright/Python tool directories; a fresh environment can use the pinned requirements and browser installation commands above. No GitHub settings were changed and no deployment was performed.
