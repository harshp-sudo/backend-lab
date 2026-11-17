# Quickstart and Validation Guide

This is the run guide for the implemented content batch described in [plan.md](plan.md).
The manifest, 15 complete lessons, six hubs, intrinsic validator, expectation fixture, and
reference browser canvas are available. Production dashboard/learning-state integration
and actual novice comprehension trials remain separate pending acceptance tiers. See
[delivery.md](delivery.md) and its evidence reports for executed results.

Run shell commands from the repository root. See the [data model](data-model.md) for the
exact inventory and [validation contract](contracts/validation-contract.md) for command
semantics and reporting boundaries.

## 1. Prerequisites

- Python with the standard-library APIs used by Python 3.10 or newer; no pip dependencies
  are required for the validator. This workspace provides Python 3.10.12.
- A current desktop browser and a mobile viewport emulator or device.
- Network access for the fixture's exact pinned Mermaid and Highlight.js browser assets,
  or locally hosted equivalents recorded with the same versions. No Node install is needed.
- Required repository files: `manifest.json`, all 21 partials, `tools/validate_content.py`,
  `tests/content/`, and `tests/fixtures/content-host.html` with its shared fixture assets.

Inspect the formal interface schema as JSON:

```bash
python3 -m json.tool specs/001-backend-architecture/contracts/manifest.schema.json
```

Expected: formatted schema output and exit `0`. This command checks JSON syntax only;
it does not validate a catalog or prove lesson completeness.

## 2. Validate Files and the Requested Inventory

Run the intrinsic checks:

```bash
python3 tools/validate_content.py --repo-root . \
  --expect tests/content/backend-architecture.json \
  --report /tmp/backend-architecture-static.json
python3 -m unittest discover -s tests/content -p 'test_*.py' -v
```

Expected for this initial delivery:

- The requested batch contains 15 topic leaves, six hubs, and category counts 5 / 4 / 3 / 3.
- Every derived file exists, every article identity matches, all six lesson modules are
  present, and all immediate-child links match the catalog.
- There are 45–75 recall items in total, three to five per lesson, with closed answers.
- Required intrinsic checks pass; known rendering, comprehension, and host integration
  checks remain unclaimed. Validator-negative-fixture tests all pass.
- A validation failure identifies the artifact and cause and exits nonzero. Deliberately
  missing files, duplicate IDs, wrong modules, and broken links must not be accepted.

The test-only expected inventory checks this request; it does not become a runtime index.
If the implementation-time audit finds unrelated content, preserve it and report total
catalog counts separately from the requested batch counts.

## 3. Serve the Test Reading Canvas

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory .
```

Open `http://127.0.0.1:8000/tests/fixtures/content-host.html`. This fixture is a test canvas;
there is no assumption that a production `index.html` exists. Stop the server with Ctrl+C
when finished. The standard-library server is for local validation.
[Python http.server](https://docs.python.org/3.10/library/http.server.html)

In browser developer tools, run:

```javascript
await contentFixture.checkAll()
```

Expected: all 21 expected partials are loaded and checked, each has at least one rendered
diagram, and no fetch, parse, or render errors are suppressed. The report records exact
renderer and browser versions. Missing libraries or a failed diagram produce a failed
browser check rather than a skipped success.

To inspect a representative lesson:

```javascript
await contentFixture.mount('/system-design/backend-architecture/core-system-topologies/distributed-system-fundamentals')
```

Verify keyboard access to every summary and link. Reveal two recall answers at once; both
must remain open independently. Mount another lesson and return; the fixture must not mark
anything Mastered or write learning state. Verify every roadmap child link and context label.
Repeat the link walkthrough when serving the fixture beneath a project URL prefix to confirm
that base-relative manifest/content loading works without editing partials.

## 4. Check Themes, Mobile Reading, and Real Print Preview

For all 15 lessons and six hubs:

1. Inspect both fixture reading themes. Text, semantic accent cards, code examples, and
   diagram labels remain legible. Theme rerenders use the original diagram source.
2. Set the viewport to 360 CSS pixels. Prose fits the page; wide tables or diagrams remain
   available in their own scrolling areas without making the whole page overflow.
3. Close mechanics and recall disclosures, note a mixed sample of open/closed states, and
   open the browser's print dialog. Select A4 and inspect/save a PDF.
4. Confirm all mechanics, answers, diagrams, and comparison entries appear in the PDF and
   test controls do not obscure learning content. Return from printing and confirm the
   prior disclosure states are restored.

Record the browser version and observed evidence. A print-media screenshot alone does not
establish that `beforeprint`/`afterprint` preparation and restoration worked.

## 5. Check Repeat Delivery and Identity Preservation

Save a manifest baseline outside the production content tree:

```bash
cp manifest.json /tmp/backend-architecture-before.json
```

Reapply the same authoring request on a disposable copy of the delivered content. Expect
zero additional nodes or identities and no unrelated changes. Validate that candidate using
its repository location and the saved baseline:

```bash
python3 tools/validate_content.py --repo-root . \
  --expect tests/content/backend-architecture.json \
  --baseline /tmp/backend-architecture-before.json \
  --report /tmp/backend-architecture-repeat.json
```

Run that command from the candidate copy's root, or set `--repo-root` to its absolute path.
Comparing a file to itself without reapplying the authoring workflow does not prove repeat
delivery. The focused unit fixtures additionally cover a valid rename/move with unchanged
identity and a rejected ID replacement. They prove validator behavior, not real persistence.

## 6. Actual Dashboard Integration — When a Host Is Available

Record this tier as **pending host integration** while no compatible dashboard exists.
Once available, use the actual dashboard rather than the fixture:

1. Enter through System Design and follow all roadmap paths to the 15 lessons. Confirm
   correct breadcrumbs and content without full-page reloads; verify browser back/forward.
2. Confirm new topics are Not Started and that opening lessons/revealing answers does not
   change mastery. Explicitly set sample statuses and Hard/Good/Easy confidence ratings.
3. Reload and verify the saved state, progress aggregation, and review history by topic ID.
4. On a disposable catalog/host instance, rename and move a sample topic while retaining
   its ID and recall keys. Repair affected links and reload. Compare all saved state with
   its pre-move snapshot; hub progress must still count descendant topics exactly once.
5. Exercise global controls, both themes, mobile navigation, and printing with these partials
   and confirm no per-topic manual edits to shared dashboard CSS or JavaScript were needed.

Do not create a substitute progress engine inside the fixture to turn this tier green.

## 7. Editorial Review and Opening Comprehension

Review every lesson against the six modules and [primary source map](research.md#8-primary-sources-for-lesson-authoring).
Check the analogy's accuracy, concept-by-concept ELI5 ordering, coherent narrative, meaningful
trade-offs, complete failure stories, real-world impact, and explanatory recall answers.
Structural validation cannot determine those qualities.

Conduct five novice opening-reading trials, covering all four categories. Give each trial
at most 30 seconds on the opening, then ask the learner to state the problem and explain
the analogy in their own words. At least four trials must satisfy both parts. Record topic,
time, and outcome; do not claim this result from word counts or author self-certification.

## 8. Report the Delivery Honestly

The [delivery record](delivery.md) contains the audit, 15 placement justifications,
paste-ready manifest snapshot, all content paths, conflicts resolved, and validation evidence
by tier. Report failures and pending dependencies explicitly. Content-complete with pending
host integration is a narrower result than fully integrated dashboard acceptance.

## Executed Validation Evidence

The initial implementation passed 39 focused unit tests, all 21 partials through intrinsic
checks, both root/project-prefix navigation, 22 rendered diagrams, 61 keyboard-operable
recall answers, 360px page overflow checks, and actual A4 PDF generation with hidden
mechanics/answers included and disclosure state restored. Reapply and rename/move tests
used independent disposable content copies; no production IDs were regenerated.

Reports are in `specs/001-backend-architecture/evidence/`. Browser tooling was installed
only under `/tmp/` for this execution; it is not needed to serve the static fixture in a
normal browser. The CLI's optional `deliveryRecord` expectation points to the required
delivery document. If validating a catalog that reuses non-UUID legacy IDs, supply the
audit baseline through `--baseline`; do not replace those identities to satisfy new-ID rules.

Actual host persistence/review/global-UI behavior and SC-004 novice results are still
pending, as explicitly reported in the delivery record. The reference fixture never writes
learning state or claims to be the production knowledge-base dashboard.
