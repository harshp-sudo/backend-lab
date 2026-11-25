# Validation Guide: Simplify Lesson UI

This is the implemented acceptance guide. Migration/UI-check tools below are available;
the completed execution results are recorded in [delivery.md](delivery.md). Original
pre-edit snapshots remain protected and must not be replaced when reproducing checks.

## Prerequisites

From the repository root, use Python 3.11+, Node, `pdftotext`, Chromium and the pinned
packages in `tests/dashboard/requirements.txt`: Playwright 1.56.0/jsonschema 4.25.1.
Reuse a working installation rather than downloading another browser. No site build is needed.

The audited development environment already has these reusable paths:

```sh
export PYTHONPATH=/tmp/backend-browser-check:/tmp/backend-lab-plan-schema-check
export PLAYWRIGHT_BROWSERS_PATH=/tmp/backend-playwright
export LD_LIBRARY_PATH=/tmp/backend-browser-libs/usr/lib/x86_64-linux-gnu
```

Use `/home/harsh/.local/bin/python3.12` for browser commands below when using those cached
packages. If the paths are gone, install the pinned development dependencies once into a
normal virtual environment and use that interpreter instead. Localhost sockets/Chromium
may require the environment's execution permission; do not substitute a static-only pass.

## 1. Snapshot and review the proposed copy change

Before implementation edits, capture the original working-tree baseline once:

```sh
python3 tools/migrate_lesson_presentation.py --snapshot .cache/lesson-ui/baseline
```

Default: dry-run. The optional `--scope sources|related|all` selects a story slice; default all verifies both completed transformations. Save original manifest/lesson bytes and protection inventories
only when the snapshot does not exist; report exact proposed edits and unexpected shapes.
Do not replace an existing baseline on resume. Today expect 135 source paragraphs across
seven variants and 120 related preambles; reconcile additions if the catalog has grown.

Expected: all 181 current nodes accounted for, known note shapes, all existing source/
related links captured, no write to topics during dry-run. Apply only after the active
governance and current/legacy validator design have been aligned during implementation.

```sh
python3 tools/migrate_lesson_presentation.py --snapshot .cache/lesson-ui/baseline --apply
python3 tools/migrate_lesson_presentation.py --snapshot .cache/lesson-ui/baseline --verify
```

Expected: exact allowlisted transformation, no educational/source-link/identity loss and
no research/historical-evidence edits. Repeat apply must report no further changes.

## 2. Intrinsic and general regression checks

```sh
python3 tools/validate_content.py --report .cache/lesson-ui/intrinsic.json
python3 -m unittest discover -s tests/content -q
node --experimental-default-type=module tests/dashboard/test_catalog.mjs
node --experimental-default-type=module tests/dashboard/test_learning_state.mjs
```

Expected: all current checks pass. The intrinsic report states sources-only-v1 and the
actual manifest-derived inventory. Today: 181 nodes, 135 lessons, 46 hubs, 273 diagrams,
541 foundational and 810 interview cards. Include new positive/negative presentation and
migration fixtures; no public paragraph match is required in current mode, but incomplete
research, missing sources or changed answers must still fail.

The named historical migration suite/expectation is not a current-live-catalog gate after
intentional presentation changes. Preserve its original files and strict legacy fixture
rules; do not regenerate frozen hashes or mark its past reports as new acceptance.

## 3. Whole-catalog real browser and PDF checks

```sh
/home/harsh/.local/bin/python3.12 tools/check_topics.py \
  --baseline .cache/lesson-ui/baseline/manifest.json \
  --paths app.js styles.css assets/js/content-renderer.js \
  --report .cache/lesson-ui/catalog.json \
  --pdf-dir .cache/lesson-ui/pdfs
```

The runner owns its server and serves root plus `/backend-lab/`. Page checks use bounded
concurrency (default `--jobs 2`; choose 1 on a constrained machine), with sibling cleanup
on failure and verified per-node checkpoint reuse after interruption. Explicit shared-runtime
paths select the whole catalog and truthfully flag broader application regression.
At today's inventory expect **181 passing node results, 543 browser cases and 362 PDFs**.
Check relative fetch/reload, correct identity, Mermaid/code, independent cards, confidence,
status persistence, mobile/theme state, hub navigation and zero console/layout errors.
All printed answers, source text and diagram labels must be complete; controls must be
hidden and prior disclosure state restored.

Important existing-runner behavior: after successful node checks with runtime changes,
its top-level result remains **pending** and exit status is 1 solely because broader
application regression is required. Inspect the report: any failed node, missing output,
other pending reason or incomplete execution is a real incomplete/failed gate. Do not
mask this exit or edit the report into a pass. The next step validates this component and
provides the combined application acceptance.

Publishing configuration/presentation must be included in final evidence fingerprints.
Reuse only matching successful node outputs with valid PDF hashes after subsequent fixes.
Changed shared styles/runtime require new checks across the catalog; do not keep old
reports as though they proved the new inputs.

## 4. Current dashboard and compact-UI acceptance

Planned focused owned-server runner:

```sh
/home/harsh/.local/bin/python3.12 tests/dashboard/check_lesson_ui.py \
  --catalog-report .cache/lesson-ui/catalog.json \
  --baseline .cache/lesson-ui/baseline \
  --report .cache/lesson-ui/application.json \
  --screenshots .cache/lesson-ui/visual
```

Independent application cases may run while the catalog renders; the runner waits and
keeps its result pending until catalog completion. Final composition must validate final
catalog fingerprints, every selected node/case and PDF
hash, accepting only the documented broader-regression pending state as its component
input. It must then execute the current US1–US6 application journeys from the existing
dashboard harness with the new status actions, plus feature cases below. The US6
`print_articles` subscenario is satisfied by the already validated catalog PDF results;
record that explicit reuse rather than generating all 362 PDFs twice. Do not run the
default historical MIGRATION scenario against intentionally changed source. Existing
EXPANDED layout/card coverage substantially overlaps catalog checks; current source-group
expectations still need updating in the harness for direct use.

Use isolated browser contexts and owned server cleanup at both `/` and `/backend-lab/`.
Required evidence:

- All current US1–US6 journey functions execute except the explicitly reused print step:
  navigation/errors, home rollups, every-lesson reading/status, enhancement failure/retry,
  reviews, search/shortcut, drawer/theme, backup and corrupt/quota persistence handling.
- Exactly one Progress selector per lesson, none on hubs, no footer banner/obsolete helper
  copy; Sources and true Related topics groups retain their correct semantics/destinations.
- At 1024/1440px: row height ≤56px. At 360px: ≤112px and at most two rows. Verify every
  status, no-session mastery, active and completed reviews in both themes/base paths.
  Targets ≥44px in both dimensions; no clipping or horizontal page overflow.
- Pointer status selection takes at most two interactions. Keyboard operation and visible
  focus work; unchanged select retains focus, review replacement focuses its new action,
  and rating a recall card keeps focus in the card.
- Seed complete representative learning records across all nine branches plus an unknown
  imported topic; perform reload/export/import and compare unaffected records. Exercise
  active/completed session restoration, remastery, repeated/stale completion and no-op status.
- Fixed-clock review boundaries pass immediately before and at 3/7/14/30 days. Revealing
  or rating alone does not master or complete review. Continue Learning uses a strictly
  latest visit timestamp, avoiding ties as an accidental fixture assumption.
- A warm HTTP-cache test serves an older cacheable partial, updates the canonical response
  and verifies navigation/reload revalidates to clean current content without losing abort/
  latest-route behavior or changing relative paths. Do not claim an old running tab updates
  without reloading the application.
- A fresh temporary lesson/research fixture passes current publishing without the generic
  paragraph; legacy negative cases and current rejected-copy/source cases remain meaningful.

Expected: application result pass only after every required journey and final catalog
component verifies. Save a combined summary pointing to immutable report fingerprints;
do not promote the catalog report by overwriting its broader-regression status.

## 5. Visual and preservation review

Review all diagrams in both browser themes at contact-sheet scale and inspect anomalies
at full resolution. Review migrated Sources and related groups across all seven original
wording variants, the original external-reference footer and the meaningful Container
Orchestration footer. Inspect actual mobile control states and representative printed
openings, diagrams, long tables/code, Feynman boxes and fully expanded scenario pages.
PDF text completeness is checked for every output, independent of visual sampling.

```sh
python3 tools/migrate_lesson_presentation.py --snapshot .cache/lesson-ui/baseline --verify
git diff --check
```

Verify unchanged manifest/hubs, ordered links, diagram source, all question IDs/answers,
research bytes/mappings, learning-state code and historical evidence. Active policy/validator/
shared-UI changes must be the intentional reviewed scope. Preserve unrelated `docs/project/`.

Record actual outcomes and any corrections in a concise feature delivery note only after
implementation acceptance. Stop with an honest pending/failed result if any required
gate is unexecuted. Commit, push and deployment require their applicable user instruction.
