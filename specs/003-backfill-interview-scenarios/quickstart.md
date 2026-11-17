# Quickstart: Interview Scenario Backfill Validation

**Feature**: [spec.md](spec.md) | **Date**: 2026-11-17

The migration is implemented and verified. All 15 lessons contain six complete production scenarios each, alongside 61 preserved foundational questions. Current-profile tooling, 15 reviewed research records and all five per-lesson acceptance gates pass. See [delivery.md](delivery.md) and [final acceptance](evidence/final-acceptance.json).

## Prerequisites and setup

Run commands from the repository root. The site itself still needs only a static HTTP(S) host and a browser; no new package/build step is introduced.

Validation uses Python 3.10+, Node 20+, the existing pinned browser requirements, Chromium and Poppler tools `pdftotext`/`pdftoppm`. A working Linux browser installation needs its normal shared libraries.

```sh
python3 -m venv /tmp/backend-interviews-venv
/tmp/backend-interviews-venv/bin/python -m pip install -r tests/dashboard/requirements.txt
/tmp/backend-interviews-venv/bin/python -m playwright install chromium
```

These development tools are outside deployment assets. Existing compatible tool environments may be reused.

## 1. Verify the frozen pre-migration inputs

Read [preservation-baseline.json](contracts/preservation-baseline.json) and confirm its original 15 lessons, six hubs, 61 foundational keys and manifest/runtime hashes match the checkout before authoring. Keep an external snapshot for rollback. Do not regenerate the baseline after editing.

Run the current checks:

```sh
python3 -m unittest discover -s tests/content -p 'test_*.py' -v
node --experimental-default-type=module --test tests/dashboard/test_*.mjs
python3 tools/validate_content.py --repo-root . --expect tests/content/backend-architecture.json --report /tmp/backend-interview-current.json
```

These commands now enforce constitution v1.2.0. Expected: 61 content tests, both Node test files, and a current-profile report with 61 foundations plus 90 scenarios, 151 total cards and 112 source diagrams. The immutable baseline still contains the original 61/22 counts; it is never regenerated to match output.

## 2. Author and check one complete lesson

Each of the 15 lesson tasks owns its complete five-to-seven-card insertion and final `research/<topic-slug>.md` record. Use [concept-specific seeds](research/topic-sources.md), then finalize source/claim verification and all three answer parts under [the content contract](contracts/scenario-content.md). Sources checked during planning do not preapprove unverified wording or invented frequency claims.

The optional `--lesson` flag checks one exact baseline lesson and reports a partial authoring scope:

```sh
python3 tools/validate_content.py --repo-root . --expect tests/content/backend-architecture.json --lesson topics/system-design/backend-architecture/code-and-domain-organization/clean-architecture.html --report /tmp/clean-architecture-interview-check.json
```

Expected: `scope: lesson`, current `recallProfile`, four preserved foundational keys for this example, five to seven complete interviews, one correctly nested subsection, original-source reconstruction, and matching final research keys/source note. The other 14 lessons are not falsely marked passed. The report exposes each gate's actual status; an authoring-only pass never substitutes for editorial, browser or print evidence.

The marker span must be the only inserted bytes. Remove it and compare the original full-file digest; also compare the original card/section hashes for diagnostics. Rerun authoring on that same lesson and confirm one subsection/key set, not duplicates.

## 3. Structural and editorial negative cases

Run:

```sh
python3 -m unittest discover -s tests/content -p 'test_*.py' -v
```

Required current-profile cases include:

- Positive foundation/interview counts at both bounds; preserve DDD's fifth original card.
- Missing/duplicate/misplaced subsection/title; generic nine-card total without separate groups.
- Too few/many interview or foundational cards; unknown role, role/wrapper mismatch.
- Missing/empty/out-of-order answer part; missing visible constitutional label.
- Duplicate original/new key, invalid prefix, changed allocated key, duplicate rerun block.
- Open/exclusive/nested recall cards; forbidden partial wrappers/scripts/styles remain rejected.
- Edited protected module/card/footer, changed manifest/hub, or an attempted baseline refresh.
- Missing/mismatched research/source/completion references and a legacy-profile waiver on production validation.
- Explicit historical fixture accepted only under its named legacy unit-test mode and rejected by current mode.
- Scope/path abuse or a target outside the fixed migration inventory for `--lesson`.

Use editorial negative review cases for a definition-only card, generic copied theme, unsupported frequency/company claim, missing decision/alternative/trap, and falsely claimed research failure. Structurally valid HTML must not automatically pass these semantic cases.

## 4. Validate all migrated content and evidence

For complete batch acceptance:

```sh
python3 tools/validate_content.py --repo-root . --expect tests/content/backend-architecture.json --report /tmp/backend-interview-structure.json
node --experimental-default-type=module --test tests/dashboard/test_*.mjs
```

Expected current report:

- `scope: batch` and `recallProfile: constitution-1.2`.
- Fifteen independently valid lessons and six unchanged hubs.
- All 61 original foundational cards plus the actual 75–105 scenarios (136–166 total).
- Every original/new diagram counted from source; no fixed new total of 22.
- Manifest, hubs, original reconstructed lesson bytes/keys and old learning model preserved; the two shared rendering exceptions must exactly match their explicit reviewed hashes.
- Final per-lesson source mappings and delivery/evidence references resolve.
- Intrinsic results remain separate from any not-yet-executed browser/print/editorial gates.

The final research record for each topic must use actual dates/queries, primary technical evidence, explicit adapted/reported basis and an honest public note. All current planning seeds have unverified exact interview frequency.

## 5. Run the real dashboard at both hosting bases

Terminal A:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Terminal B, also from the repository root:

```sh
python3 -m http.server 8001 --bind 127.0.0.1 --directory ..
```

The two views are `http://127.0.0.1:8000/` and `http://127.0.0.1:8001/backend-lab/`. Run the updated actual-host suite without a story filter:

```sh
/tmp/backend-interviews-venv/bin/python tests/dashboard/check_dashboard.py --base-url http://127.0.0.1:8000/ --project-url http://127.0.0.1:8001/backend-lab/ --report /tmp/backend-interview-browser.json --pdf-dir /tmp/backend-interview-pdfs
```

The existing harness's US1–US6 filters refer to dashboard scenario groups; they are not a replacement for this feature's full migration acceptance. Run all groups plus the new migration cases for final evidence.

Expected outcomes:

- Click/direct-refresh all 21 destinations and the 20 existing hub-child edges at both bases; existing mastery section links still work.
- No unexpected console/page/Mermaid errors with healthy dependencies; every source diagram renders, including new diagrams inside closed cards.
- All new questions start closed; open two by keyboard, close one independently and verify the other remains open.
- Every new key receives one Hard/Good/Easy group and no initial fabricated rating.
- Rate/reload/export/import the expanded keys through real controls and retain both foundational/scenario ratings.
- Seed old statuses/review history/confidence, including a Mastered topic and an old backup. Loading may update ordinary visit time; revealing/rating must not change status, review state or the 15-topic denominator.
- Both themes and a 360px viewport preserve readability, local table/diagram overflow, native keyboard/focus behavior and source notes.
- Repeated route/theme/rerun operations do not duplicate cards/controls or allocate different keys.

A test-only fixture pass is supporting evidence, not a substitute for these real-host results. Its role-aware `checkRecall` must also work without writing learning state.

## 6. Real PDFs and per-lesson completion

Verify real PDFs from both themes for every migrated lesson: 30 required outputs. The reused all-content harness may produce 42 including unchanged hub regressions.

Compare full source prose, scenario summaries/labels/answer parts and source notes against extracted PDF text. Inspect diagrams and comparison tables in both themes, confirm controls are absent and saved disclosure states restore. Do not rely only on print-media emulation. Bulk PDFs/review sheets remain in `/tmp`.

Complete `evidence/lesson-completion.json` with exactly 15 entries. Each needs passing preservation, structure, editorial, browser and print evidence before overall pass; link the record from the [delivery.md](delivery.md). Capture new reports under this feature, leaving older 001/002 evidence historical.

## Verified environment and current results

The completed run used Python 3.12.11, Node 20.19.4, Playwright 1.56.0, jsonschema 4.25.1, Chromium 141.0.7390.37 and Poppler. The 13-scenario unfiltered run covered both bases, every new key and all 42 PDFs. Inspection sheets for all 30 required lesson PDFs are recorded in the per-lesson print evidence. Normalized text checks ignore whitespace, soft hyphens and decorative leading heading emoji only; both reading-order and layout extraction protect wrapped table cells.

The pinned test packages were reused from temporary directories in this workspace. Its actual command (after starting dedicated servers on 8020 and 8021) was:

```sh
PYTHONPATH=/tmp/backend-browser-check:/tmp/backend-lab-plan-schema-check \
PLAYWRIGHT_BROWSERS_PATH=/tmp/backend-playwright \
LD_LIBRARY_PATH=/tmp/backend-browser-libs/usr/lib/x86_64-linux-gnu \
python3.12 tests/dashboard/check_dashboard.py \
  --base-url http://127.0.0.1:8020/ \
  --project-url http://127.0.0.1:8021/backend-lab/ \
  --report /tmp/backend-interview-final-browser.json \
  --pdf-dir /tmp/backend-interview-pdfs
```

Use the normal virtual-environment commands above on another machine. No `/tmp` tooling is a site runtime dependency. Browser contexts disable animated document scrolling for deterministic controls while retaining actual DOM, layout, diagram and print behavior. The harness atomically checkpoints each completed scenario; only `executionStatus: complete` plus `result: pass` is whole-suite acceptance.

The [runtime compatibility record](evidence/renderer-compatibility.json) documents the narrowly verified SVG-label/print fix; [the validation contract](contracts/preservation-and-validation.md#implemented-shared-rendering-compatibility-review) defines exact before/after hash checks. Unknown runtime changes remain rejected. The existing `--baseline` CLI option continues to mean a prior manifest, not this migration's preservation audit.

All 15 completion entries pass preservation, structure, editorial, browser and print independently. Exact interview-frequency/ranking/company claims remain unverified and are disclosed as production adaptations. One supplementary PDF recheck failed and is not used for technical acceptance. Earlier planning and feature 001/002 reports remain historical.
