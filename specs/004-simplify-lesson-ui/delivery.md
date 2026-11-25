# Delivery: Simplify Lesson UI

**Status:** Implemented and validated; all 31 tasks complete.
**Date:** 2026-11-25. **Working branch:** `main`.

All 135 lessons now show named Sources without the repeated research-process paragraph.
The 120 related-decision preambles are replaced with compact Related topics groups.
Original external-reference footers and meaningful Container Orchestration guidance remain.

The large host mastery card is removed. One native Progress selector follows each lesson
heading, with a short next-review date and the relevant explicit review action when mastered.
Desktop controls occupy one row; mobile uses at most two at ordinary text size. Controls
remain at least 44 × 44px and wrap at enlarged text sizes. Review replacements preserve
keyboard focus, while confidence ratings preserve the focused card/button.

The conditional partial fetch revalidates cached HTML. Current publishing now explicitly
uses `sources-only-v1`; constitution 2.0.0, the publishing guide and topic-publish skill
require concise Sources and maintainer evidence for future topics. Research depth, honest
limitations, scenario counts and contextual assumptions remain mandatory. Strict historical
`disclosure-v1` fixtures remain supported without rewriting frozen evidence.

## Acceptance evidence

Local reports and visual artifacts are intentionally ignored under `.cache/lesson-ui/`.
Final results below were reconciled against the actual reports, current input fingerprints
and all 362 PDF hashes.

| Check | Result |
| --- | --- |
| Intrinsic catalog and source/research contract | Pass: 181 nodes, 135 lessons, 46 hubs |
| Python content fixtures | Pass: 90 tests |
| Node catalog and learning-state suites | Pass: 14 tests |
| Deterministic migration/preservation | Pass: 135 lessons, 352 protected files unchanged |
| Catalog browser cases and light/dark PDFs | Component pass: 181 pages, 543 browser cases, 362 PDFs |
| Current dashboard and feature acceptance | Pass: all 10 current journeys; 72 progress/layout cases; 20 Sources cases; cache, state, backup and related-link checks |
| Visual review and final evidence reconciliation | Pass: 546 diagram/theme captures across 23 contact sheets, seven Sources variants, control states, reading examples and selected PDF pages |
| Final working-tree whitespace/hooks | Pass; no implementation extension hooks configured |

The catalog runner deliberately retains its top-level pending result/exit 1 for shared
runtime changes. Its 181 node results are complete and passed. The feature runner verified
every final fingerprint and PDF hash, then composed that component with all current
dashboard journeys into a **pass** in `application.json`. The original catalog report was
not rewritten as a standalone full pass. Its SHA-256 is
`ec87f80fc04f54652e8b737cd1e99f1673f09b4d4c3cbbd5fe8ead7be1fffda0`.

Local evidence: [combined application](../../.cache/lesson-ui/application.json),
[catalog component](../../.cache/lesson-ui/catalog-component.json),
[preservation](../../.cache/lesson-ui/final-copy-verify.json),
[visual review](../../.cache/lesson-ui/review.json),
[progress states](../../.cache/lesson-ui/visual/progress-states-contact.jpg).
All diagram/theme contact sheets were reviewed, with five refreshed captures inspected
at full size. PDF visual review sampled 60 opening pages and 25 detailed pages across the
nine branches; automated text/answer/diagram-label and print-restoration checks covered
every PDF. Warm-cache checks proved canonical revalidation from an actually cached old
partial. The large-text check exposed and fixed a mobile overflow before final acceptance.
The standalone content-host fixture also passed all 181 partials with zero learning-state writes.

## Preserved contracts

The manifest, all 46 hubs, research records/mappings and learning-state module remain
unchanged. All 273 diagram sources, 541 foundational cards and 810 interview scenarios,
including their stable identities and full answers, remain intact. Storage key/version,
backup format, confidence, review history/session/replay protection and unknown imported
records use the existing model. No learner-data migration is introduced.

Canonical changes are restricted to the audited source paragraphs and related labels;
the migration helper rejects unexpected shapes or unrelated content drift and supports
safe dry-run, scoped application, verification and idempotent resumption.

## Scope and limits

This feature changes presentation and current publishing acceptance. It does not re-research
or re-author lessons. Browser verification uses the installed pinned Chromium headless
shell at both root and project base paths. No new dependency, site build or production
backend is required. Commit, push and deployment are outside this implementation request.
Unrelated private project reference files remain local and unchanged.
