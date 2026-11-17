# Preservation and Validation Contract

**Governs**: FR-001/003/011–024
**Baseline**: [preservation-baseline.json](preservation-baseline.json)
**Content grammar**: [scenario-content.md](scenario-content.md)

## Production and legacy entry points

Planned Python interface: `check_article(item, source, index, *, recall_profile="constitution-1.2")`. Supported profiles are current `constitution-1.2` and explicit `legacy-1.1` for historical unit fixtures. Hubs retain their existing rules.

The repository `validate(...)` and CLI run the current profile for published topics. The current expectation file `tests/content/backend-architecture.json` explicitly records `recallProfile: constitution-1.2`; a legacy value is rejected rather than passed to production checks. Omitting the marker does not infer legacy mode. There is no new legacy CLI flag.

Convert normal positive test factories to complete current content. Retain any genuinely historical samples through an explicit legacy keyword and prove the same sample fails current checks. Expected fixtures are not editorial approval of synthetic question content.

The existing CLI remains available with `--repo-root`, `--expect`, `--baseline` and `--report`. The catalog-history `--baseline` still means a previous manifest, not the preservation audit; do not overload it with a different document shape.

Add optional `--lesson <repo-relative-HTML-path>` for independent authoring checks. It accepts only a known in-scope baseline lesson and uses the same current-profile structure/preservation rules. The report must identify `scope: lesson`, the selected target and any pending editorial/browser/print evidence; it cannot claim batch completion or silently count unselected lessons as passing. Omit the flag for full-repository checks. This is a scoped check, not a legacy-profile bypass.

Current reports identify `scope: batch|lesson`, `recallProfile: constitution-1.2`, role-specific per-lesson/batch counts and source diagram counts. An intrinsic pass is not an editorial/browser/print pass; keep those dispositions explicit. An older report without the current profile/count evidence is historical, not proof of this migration.

## Current expectation references

During implementation, extend the current test expectation with these evidence references, while retaining its root/parent/groups and order:

| Field | Value |
| --- | --- |
| `recallProfile` | `constitution-1.2` |
| `preservationBaseline` | `specs/003-backfill-interview-scenarios/contracts/preservation-baseline.json` |
| `scenarioResearchDirectory` | `specs/003-backfill-interview-scenarios/research` |
| `completionRecord` | `specs/003-backfill-interview-scenarios/evidence/lesson-completion.json` |
| `deliveryRecord` | `specs/003-backfill-interview-scenarios/delivery.md` |

Validate referenced paths inside the repository, reject missing/malformed required evidence, and avoid fetching research files at runtime. The new delivery record links every updated lesson, final research record and acceptance result. Older delivery/evidence files stay historical.

## Preservation rules

For each baseline lesson:

1. Require the same catalog ID, kind, title, slug, route and file path.
2. Require exactly one complete marker pair containing exactly the new scenario subsection.
3. Remove the inclusive marker span and compare the complete remaining source to the original SHA-256 digest, without trimming or normalization.
4. Also compare original direct section identities, the first five raw section hashes, foundational key order/raw hashes, and original diagram sources for precise diagnostics.
5. Require the manifest and all six hub files to match their complete baseline hashes.
6. Check runtime hashes to confirm the expected no-shell-change design. Any narrow host compatibility fix requires an explicit recorded reason and affected browser regression; it must not silently be treated as untouched.

A repeated authoring pass must replace the same inserted block and retain existing scenario keys. New allocated keys become part of that lesson's final research/completion mapping. No baseline is regenerated after a failure.

### Implemented shared rendering compatibility review

Actual PDF checks exposed clipped labels in an original overview diagram. The expected
`runtimeCompatibilityRecord` now points to
`specs/003-backfill-interview-scenarios/evidence/renderer-compatibility.json`. This is
the narrow compatibility path anticipated by rule 6, not a refreshed preservation baseline.

The record must have schema version 1, reviewed status, the exact frozen baseline digest,
a concrete rationale and primary documentation reference. Its file list must cover exactly
the observed changed runtime paths, each with the original baseline hash, reviewed output
hash and reason. Any additional or different bytes fail. The CSS source and test fixture
also record their supporting changes. The current fix moves Mermaid's deprecated nested
`htmlLabels` option to its supported root position and bounds print diagram height/fragmentation.

Final completion requires passing host and print regression reports containing the actual
reviewed runtime hashes. A pending regression disposition cannot support completed lessons.
The manifest, hubs, lesson-byte reconstruction and all learning-state/identity checks remain
mandatory. Five runtime files remain unchanged; the shared renderer and deployed stylesheet
are the two explicit reviewed exceptions.

## Structural current-profile checks

Require the six original direct story modules plus one correctly nested scenario section. Count group roles separately, require 3–5 foundations and 5–7 interviews, and check preservation against the actual four/five-card original inventories.

Reject all of the following:

- Missing, duplicate or incorrectly placed scenario subsection/title.
- Missing, out-of-range or double-counted group; unknown role; unmarked card inside interview section; interview card outside it.
- Missing/duplicate stable key, original-key collision, malformed new key, or a rerun that regenerates assigned identities.
- Empty/multiple summary, initially open card, exclusive name, or nested recall card.
- Missing, duplicate, out-of-order or empty answer part; absent/mismatched visible constitutional labels.
- Missing source note, broken record/source mapping, invalid source URL, unsupported public evidence classification or false research-unavailable statement.
- Edited protected source, changed catalog/hubs, missing final research/completion/delivery evidence.

Structural checks verify presence/shape/resolving references. Real-source credibility, technical correctness, scenario distinctness and unsupported-frequency claims require the explicit editorial dispositions from [research-and-review.md](research-and-review.md). Tooling must not mark those judgments passed merely because HTML labels exist.

## Browser inventories and confidence

Derive per-lesson source inventories using the same group semantics before comparing DOM results. Remove fixed current totals of 61 questions/22 diagrams from `tests/dashboard/check_dashboard.py`; instead assert:

- The original 61 foundational identities remain represented.
- Every migrated lesson has its independently valid 5–7 scenario keys.
- Actual total questions equal the two groups' sum, within 136–166 for this batch.
- Every source diagram, including new nested diagrams, has a rendered result.
- Every new question gets one existing host confidence group and no fabricated rating.

Update `tests/fixtures/content-host.js` to check the two counts/parts explicitly. It remains a test-only non-persistent reading fixture, not a substitute for actual host evidence. The production app is expected to work unchanged through its current question hooks.

Seed valid old learning records, compare status/review/original confidence across migrated loading, and permit only normal visit timestamp updates. Rate/reload/export/import all new keys through real controls. Verify old backups leave new keys absent and unknown keys continue to round-trip. Revealing or rating never advances review state.

## UI, hosting and print

Use the real root shell at both root and repository-prefix URLs. Click/reload all 21 routes, check all 20 original hub-child edges, existing section links, console/page errors and diagram outcomes. Exercise new cards independently by pointer and keyboard, in both themes and at 360px.

Produce actual PDFs of all 15 migrated lessons from both themes (30 required). Existing all-article printing may yield 42 outputs including hub regressions. Extract/compare source paragraphs including the scenario labels and complete answers; also verify summary/title text, diagram/table legibility, hidden host controls and disclosure-state restoration. Keep bulk PDFs/screenshots outside the source tree.

## Evidence ownership

Implementation creates focused source/validator negative tests and per-lesson completion records. Final verification writes a feature-specific structural report, actual-host report, learning-preservation report and print results under this feature's evidence directory. Existing test suites remain meaningful; do not weaken assertions or rewrite old evidence to manufacture a pass.

Missing dependencies or unexecuted required gates are explicitly unexecuted/failing, never silently skipped as passing. Mark a lesson migrated only after preservation, structure, editorial, browser and print checks pass for that lesson.
