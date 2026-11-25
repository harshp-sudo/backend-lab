# Implementation Plan: Simplify Lesson UI

**Branch:** `main` | **Date:** 2026-11-25 | **Spec:** [spec.md](spec.md)
**Feature directory:** `specs/004-simplify-lesson-ui`
**Status:** Research, design and implementation complete; validated results are in [delivery.md](delivery.md).
**Resolution note:** setup-plan reports logical feature key `004-simplify-lesson-ui`;
the actual Git branch is `main`. No hook created or switched a branch.

## Summary

Remove the generic research paragraph from all lessons, remove the related-decision
preamble and large host mastery banner, and use one compact Progress/status/review row.
Preserve complete teaching material, source and related links, all stable identities and
existing learning state. Migrate canonical partials once; align publishing policy so new
lessons remain clean. Research presentation changes independently of the recall contract.

This is a shared application/presentation change using the full feature workflow. It is
not a new topic batch. The current 135 lessons do not need reauthoring, new question
research or separate authoring tasks merely to remove audited boilerplate.

## Technical Context

**Language/Version:** Existing HTML5, CSS and browser ES6+ modules; Python 3.11+ tooling.
**Primary Dependencies:** Reuse Mermaid 12.3.0, Highlight.js 11.11.1 and existing Tailwind
3.4.17 build setup. Add no runtime dependency and no framework.
**Storage:** Existing `backend-lab.learning.v1` localStorage state, backup/state version 1;
existing Markdown/JSON research records. No schema/data migration for progress.
**Testing:** Python unittest, Node catalog/state suites, Playwright 1.56.0 +
jsonschema 4.25.1, Chromium and Poppler PDF extraction; reuse installed tools.
**Target Platform:** Static GitHub Pages and local HTTP; root and repository subdirectory,
desktop and 360px mobile, keyboard/touch, light/dark, A4 print.
**Project Type:** Single-page static application and content-publishing toolchain.
**Performance Goals:** Preserve lazy topic fetch/enhancement and instant local status
updates. Progress fits ≤56px/one row at ≥1024px and ≤112px/two rows at 360px, with ≥44px
control targets. No additional network request for research records during reading.
**Constraints:** Preserve complete modules, question answers/keys, diagrams, source order,
related destinations, review semantics and unknown backup records. No hidden replacement
disclaimers. No real deployment, commits or push under this stage.
**Scale/Scope:** 181 nodes = 135 lessons + 46 hubs, nine branches; seven paragraph variants,
120 related preambles. Expected unchanged 273 diagrams and 1,351 recall cards.
**Baseline:** Manifest SHA256
`99114903e942e037c66a9442ac58f4fc6aabb66b54580e5cde95faac28334a16`.
Re-audit before edits and derive all verification inventories from that working tree.

## Constitution Check

Pre-research review: **PASS for this explicitly authorized design scope.** The user's
request supersedes the existing public-disclosure presentation mandate; FR-016 identifies
the required amendment and preserves the underlying evidence obligations. Implementation
must adopt and align that amendment before accepting migrated lessons.

| Gate | Design disposition |
| --- | --- |
| ELI5, narrative and six complete modules | Preserved byte-for-byte outside the narrowly allowed source/footer edits; Feynman practice remains. |
| Research and honest claims | Existing evidence stays intact; current readers retain named sources; no unsupported frequency claims are introduced. |
| Public disclosure mandate | Explicit authorized amendment planned to constitution 2.0.0, preserving ratification date and recording actual amendment date/sync impacts. No silent exception. |
| Persistent explicit learning | Existing APIs, key, versions, intervals and replay protection remain unchanged. |
| Static architecture and taxonomy | No hierarchy, manifest, ID, routing or dependency change. HTTP revalidation stays relative. |
| Mobile, keyboard, themes and print | Measured layout/focus checks plus whole-catalog rendering and full-answer PDFs. |
| Proportional publishing | One deterministic migration; no topic re-research or frozen-baseline regeneration. Shared changes justify catalog-wide acceptance. |

Post-design review: **PASS.** All dependencies and policy changes are resolved in the
design contracts. Production delivery remains gated on actually implementing the amendment,
migration, controls and checks; this plan does not claim those gates passed.

## Project Structure

### Documentation (this feature)

```text
specs/004-simplify-lesson-ui/
├── spec.md
├── checklists/requirements.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   ├── lesson-presentation.md
│   └── progress-controls.md
└── quickstart.md
```

`tasks.md` belongs to the subsequent tasks stage and is not generated here. Execution
reports, local snapshots, PDFs and screenshots use ignored `.cache/lesson-ui/`; do not
copy complete lesson answers into new documentation/evidence ledgers.

### Source code and active contracts (planned changes)

```text
app.js                                      # One stable progress row; remove host banner
styles.css                                  # Compact responsive row and wrapping links
assets/js/content-renderer.js               # Conditional lesson HTTP revalidation only
assets/js/learning-state.js                 # Reuse unchanged
manifest.json                              # Preserve unchanged
topics/**/*.html                            # Narrow migration in 135 lessons; hubs unchanged
research/topics/                            # Preserve existing records unchanged
specs/003-.../research/                      # Preserve original Markdown records unchanged
.specify/memory/constitution.md              # Explicit presentation amendment
.agents/skills/topic-publish/SKILL.md         # Future authorship follows amended contract
docs/topic-publishing.md                     # Current Sources/presentation rules
tools/validate_content.py                   # Explicit presentation modes and invariants
tools/check_topics.py                       # Select mastery via status; fingerprint policy
tools/migrate_lesson_presentation.py         # New deterministic dry-run/apply/verifier
tests/content/publishing.json               # Current sources-only-v1 presentation mode
tests/content/test_*.py                      # Legacy/current cases and migration safety
tests/dashboard/check_dashboard.py          # Current source/status/print expectations
tests/dashboard/check_lesson_ui.py           # New owned-server UI/application acceptance
tests/dashboard/test_catalog.mjs            # Reuse current suite
tests/dashboard/test_learning_state.mjs     # Reuse current suite
```

**Structure Decision:** Extend the existing shell and verification tools in place. No
new application layer or standalone state module. Preserve older specs/contracts/evidence
as historical artifacts; current defaults and explicit historical-mode checks stay distinct.

## Phase 0 — Research decisions

[research.md](research.md) records the audit, evidence and alternatives. Decisions:

1. Keep the native `#topic-status` select, relabel it Progress and retain existing review
actions. Remove footer-only DOM and obsolete master-topic action.
2. Maintain the select node across refreshes; update the dependent review region and
transfer focus only when its focused control is replaced.
3. Keep the recall profile `constitution-1.2`; add explicit current
`researchPresentation: sources-only-v1`. Historical `disclosure-v1` remains strict.
4. Preserve research files byte-for-byte, including archived publicDisclosure strings;
new records need not include a public paragraph field.
5. Use parser-guided exact substring edits rather than hiding text or reserializing
lessons. Distinguish source footers from actual related-topic groups.
6. Use conditional HTTP revalidation for lesson fetches, with no service worker or custom
lesson cache.
7. Run shared catalog/render/print and current application behavior acceptance once for
the final inputs; rerun only affected failed/changed inputs through verified fingerprints.

## Phase 1 — Design and contracts

### A. Snapshot and policy alignment

Capture the pre-edit manifest, relevant source bytes, paragraph variants, ordered source/
related links, topic/card identities, diagram hashes and all research/historical evidence
hashes under `.cache/lesson-ui/`. Do not overwrite the original snapshot on resume.

Amend the constitution and active publishing skill/guide together during implementation.
The amendment is limited to public source presentation and compact progress, with full
research honesty/depth retained. Current configuration must explicitly require sources-only-v1.
Allow existing recorded constitution versions 1.2.0/1.3.0 and new 2.0.0 research without
rewriting original provenance. No historical record mapping change.

### B. Validation contract before migration

Thread research presentation through `check_interviews`, `check_article`, `check_research`,
registered topic checkers and `validate`. Do not update only one direct-call path.
Current topic-publishing configs missing/using an unknown presentation must fail closed;
named historical migration expectations can infer disclosure-v1. Direct legacy fixture
tests use that mode explicitly. Learning structure validation remains common and strict.

See [lesson-presentation.md](contracts/lesson-presentation.md) for current/legacy positive
and negative cases, exact source-link mapping and migration allowances. New current
fixtures prove future publishing acceptance without creating a live lesson or new IDs.

### C. Canonical migration

The migration utility defaults to dry-run, derives all targets from the manifest and
checks every note against the captured variant/element shape. An apply is idempotent and
writes only approved paragraph/heading/related-group changes. An unexpected shape stops
with the path and reason rather than guessing.

Verify the resulting bytes equal the allowlisted transformation of each original source.
All question bodies/keys, first-five-module teaching, diagrams, URLs/link order and
meaningful footer prose must be preserved. Keep all 46 hubs and the manifest unchanged.
Preserve external Sources and further reading footers. Do not rewrite full answers or
re-run historical question research.

### D. Shared controls and layout

Implement [progress-controls.md](contracts/progress-controls.md) in app.js/styles.css.
Retain `#topic-status` and `data-host-controls`; remove the footer and extra helper text.
The conditional review region displays one relevant action and a short next-review date.
Use one desktop row; two bounded mobile rows. Keep all text/actions accessible.

Use the existing `markStatus`, `rateQuestion`, `startReview` and `completeReview`
transitions. No learning-state/schema changes are planned. Preserve storage-failure notices,
backup replacement, unknown records and all dashboard rollups.

### E. Loading, print and freshness

In loadArticle, preserve relative URL/AbortSignal behavior and request conditional
revalidation. Do not text-strip an old body in the renderer as a second cleanup mechanism.
Normal reload/navigation must fetch or validate current canonical partials.

Keep existing beforeprint/afterprint open/restore logic and control-hiding hooks. Extend
print acceptance to check removed copy/control text absence alongside complete source
references, answers and diagram labels. Review actual output; extracted text alone cannot
prove contrast or wrapping.

## Verification strategy and execution order

1. Add meaningful unit/fixture cases for both presentation modes, deterministic migration,
missing sources/config, reintroduced boilerplate and unchanged evidence. Preserve strict
legacy negative tests instead of deleting them.
2. Run current whole-catalog intrinsic validation and existing Python/Node suites.
3. Run the owned-server whole-catalog runner with explicit shared-runtime paths and the
pre-edit manifest. Current expected scope: 181 partials, 543 browser cases, 362 PDFs.
Runtime/style/contract changes invalidate prior feature cache; subsequent reuse requires
matching fingerprints and valid PDF hashes. Include publishing.json in the fingerprint.
4. Run `tests/dashboard/check_lesson_ui.py` to execute current US1–US6 application journeys
and the feature-specific control/source/link/cache/backup checks at both bases. It owns
server startup/cleanup and isolated contexts, explicitly excluding historical MIGRATION
and redundant repeated full-catalog print work.
5. Verify compact row state matrix at 1024/1440px and 360px in both themes: not-started,
in-progress, mastered, active review and completed review. Measure targets, row count and
height, not screenshots alone. Exercise focus, two-interaction selection and temporary errors.
6. Compare baseline protected hashes, teaching/identity/link inventory and research bytes.
Visually inspect all diagram/theme output at contact-sheet scale, all seven migrated note
variants and representative long tables/code/scenario pages; zoom anomalous output.
Full-answer/label extraction remains mandatory for every PDF.
7. Record a combined acceptance result only when catalog and current application reports
pass with the final input fingerprints. The catalog runner intentionally leaves shared
application regression pending; do not relabel that report as a standalone full pass.
Use a final feature summary that references both passing components and any fixes.

Commands and expected results are in [quickstart.md](quickstart.md). Missing browser/PDF
tools, failed checks or static-only execution leave implementation acceptance pending.

## Requirement traceability

| Requirements | Design owner | Acceptance |
| --- | --- | --- |
| FR-001–004 | Exact copy/source/footer migration | All variants absent; ordered links and contextual prose preserved |
| FR-005–008, FR-012–013 | Single compact status/review area | Layout, keyboard, focus, target size and all review variants |
| FR-009–011 | Existing learning-state APIs | Current application + state suite, seeded records, reload/backup |
| FR-014–015 | Baseline inventory and unchanged research | Educational hashes, full PDFs, same IDs/keys and evidence bytes |
| FR-016–017 | Explicit amendment and presentation mode | Strict legacy/current fixtures and fresh publishing fixture |
| FR-018–020 | Shared app/catalog acceptance | Root/project navigation, themes/mobile/print, final input hashes |

## Complexity Tracking

No new runtime architecture, storage migration or unapproved exception. The only
incompatible contract change is the explicitly requested public-presentation amendment.
Two small feature tools are justified by 135-file deterministic preservation and real
browser acceptance; no new migration ledger or external service is introduced.

## Planning completion

Research and design are complete; no unresolved clarification markers or extension hooks.
The application, content, research and constitution were unchanged during planning.
Task generation and implementation subsequently completed; see [tasks.md](tasks.md) and [delivery.md](delivery.md).
