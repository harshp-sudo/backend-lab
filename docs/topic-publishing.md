# Topic publishing

Ordinary topic requests use the existing dashboard and one end-to-end content pass.
Full Spec Kit remains appropriate for application behavior, storage/schema changes,
new learning requirements, or an explicitly requested migration/full feature cycle.
The constitution is authoritative; this workflow changes overhead, not lesson depth.
The markup/recall profile remains `constitution-1.2` because v1.3.0 changes workflow, not
the lesson schema. For explicitly staged requests, keep one compact
`docs/topic-requests/<request-slug>.md` checklist across stages: placement, one row per
lesson, research notes and shared acceptance checks. Reuse it instead of generating
separate spec/plan/data-model/contracts documents; create no request file unless needed.

## Authoring and delivery

1. Read the constitution, current `manifest.json`, and one relevant lesson and hub.
   Capture the pre-edit manifest outside the publication tree, for example:
   `cp manifest.json /tmp/backend-lab-manifest-before.json`. Keep that snapshot for reruns.
2. Audit taxonomy, reuse aligned categories, choose kebab-case paths, allocate UUIDv4 IDs
   only for new nodes. Preserve existing IDs/recall keys. Create every missing parent
   `_overview.html`; update affected child lists and meaningful roadmap diagrams.
3. Research each exact concept in batches of independent searches. Verify technical
   decisions with primary sources; disclose when question frequency is unverified or
   search is unavailable. Reuse a credible source across scenarios where it actually
   supports their decisions. Do not repeat identical searches across planning/authoring.
4. Author every lesson in full: ELI5 first; six story modules; explained Mermaid diagram;
   collapsible mechanics; decision matrix; concrete failure stories; Feynman prompt;
   3–5 foundational cards; 5–7 distinct production interview scenarios with all three
   constitutional answer parts. Use the existing `.kb-*` vocabulary and host controls.
   Every process/system needs appropriate visual coverage, but several scenarios may
   reference the same explained diagram. Add another diagram when it teaches a different
   relationship or failure path; repeated generic four-box charts add no quality.
5. Review content for correctness, narrative, assumptions, distinct decisions, costs and
   follow-up traps. Keep one complete authoring task per lesson for a batch and a compact
   per-lesson result. Do not copy complete answers into research/review evidence files.
6. Run the checks below; fix failures and rerun affected checks. Deliver the placement
   justification, applied manifest snippet and links to complete lesson/hub partials,
   plus verification results and any explicit limitations. Repository file links may
   carry complete HTML instead of repeating the same file contents in chat.

## Supported partial contract

The current executable contract is `tools/validate_content.py` plus the constitution.
The base envelope/style vocabulary is described in
`specs/001-backend-architecture/contracts/content-contract.md`; its statement that the
production dashboard is absent is historical. Inspect a current lesson for final markup.

- One `<article class="kb-topic" data-node-id="UUID">`, exact manifest-title `<h1>`.
- Six direct `<section data-section="KEY" id="node-UUID-KEY">` modules, in the order
  `hook-eli5`, `big-picture`, `mechanics`, `trade-offs`, `pitfalls`, `mastery`.
- Mastery contains a direct nested `<section data-interview-scenarios
  aria-labelledby="node-UUID-interview-scenarios">` with matching `<h3 id="...">`
  titled `Tricky & Most-Asked Interview Scenarios`.
- Each scenario is a direct `<details class="kb-question" data-recall-kind="interview"
  data-recall-id="interview-STABLE-KEBAB-KEY" data-scenario-basis="adapted-production">`.
  Use lowercase stable keys and an accurate basis (`reported-recurring`,
  `adapted-production`, `knowledge-based`). Never set `open` or a shared `name`.
- After the scenario `<summary>`, use three direct `<div data-scenario-part="...">`
  elements: `scenario`, `decision`, `trade-offs`. Each starts with `<p><strong>LABEL</strong></p>`
  followed by complete explanatory paragraphs. Labels are exactly `The Scenario & Constraint`,
  `The Direct Answer & Architectural Decision`, `Key Trade-Offs & Follow-Up Traps`.
- One visible `<aside data-interview-research>` outside the scenario cards contains a
  disclosure paragraph and named HTTPS source links. New lessons need no migration markers.
- Hubs use `.kb-hub`, matching identity/title, ELI5 orientation, Mermaid roadmap, reading
  guidance and `[data-child-links]` with every immediate child in manifest order.
- No embedded scripts/styles/storage, inline handlers, extra document shell or host controls.

## Compact research records

New/revised lessons keep one `research/topics/<immutable-topic-id>.json` file. The current
`tests/content/publishing.json` maps existing lessons to their already reviewed historical
records; new topics use the default directory without adding another registry entry.
Do not alter those historical records for an unrelated topic addition. When revising a
legacy lesson, write a fresh stable-ID record and change only its `researchRecords` mapping.

The record follows `check_research` in `tools/validate_content.py`. Required fields:

- `topicId`, exact `title`, repository-relative `path`, `constitutionVersion` (`1.3.0`
  for new records), ISO `researchedOn`, `state: "reviewed"` after review.
- `searches`: actual `{query, date, result}` rows, including failures/limitations.
- `sources`: `{id, title, url, roles, checkedOn, supportRationale}`; roles are
  `technical-primary` and/or `interview-evidence`; record limitations where applicable.
- `scenarios`: one ordered row per interview key with `key`, `theme`, `basis`,
  `selectionSources`, `technicalSources`, `supportedInterviewClaim` (`"none"` for
  adaptations), `assumptions`, `limitations`, and `editorial`.
- `editorial`: eight criteria (`concept-specificity`, `distinctness`, `production-prompt`,
  `direct-answer`, `decision-costs`, `follow-up`, `evidence`, `full-delivery`), each
  `{status: "pass"|"fail", rationale: "brief concrete finding"}`. Reviewed records have
  no failed findings. State why the criterion holds; do not duplicate the lesson prose.
- `publicDisclosure`: exact first paragraph text of the public research note;
  `sourceNoteUrls`: note URLs in order, covering the recorded sources.

For `reported-recurring`, identify the precise claim the interview evidence supports.
Technical documentation alone cannot prove interview frequency. Existing records provide
schema examples, not a required word count. A validator pass checks structure/consistency;
substantive source and editorial review still belong to the author/reviewer.

## Verification commands

Whole catalog, cheap static validation (includes sources/research shape and hub links):

```sh
python3 tools/validate_content.py --report /tmp/content-static.json
python3 -m unittest discover -s tests/content -q
node --experimental-default-type=module tests/dashboard/test_catalog.mjs
node --experimental-default-type=module tests/dashboard/test_learning_state.mjs
```

For one content request, use the pre-edit manifest and the actual changed paths:

```sh
python3 tools/check_topics.py \
  --baseline /tmp/backend-lab-manifest-before.json \
  --paths manifest.json topics/system-design/backend-architecture/communication-and-routing/new-topic.html
```

The runner selects new/renamed/moved entries and hubs whose child trees changed by comparing
manifest snapshots. Explicit lesson/research paths select that lesson and ancestor hubs.
A manifest change without a baseline conservatively selects the whole catalog and reports
history as pending. `--changed` includes staged, unstaged **and untracked** files; if the
checkout has no clean Git baseline, use explicit paths with the pre-edit manifest to avoid
classifying all existing untracked application files as newly changed runtime.
`--all` selects the catalog. Deleted/unregistered HTML fails static validation.

The runner starts and stops its own HTTP server with an OS-assigned port and serves the
real app at `/` and `/backend-lab/`. Isolated browser contexts check route reloads, identity,
all diagrams, independent keyboard disclosure and every card's confidence persistence,
mastery, mobile light/dark layouts, theme rerendering and hub-child navigation. Each selected
partial produces actual light/dark PDFs with full text/diagram-label comparison, hidden
controls and disclosure-state restoration. Review layout when new content introduces a
new visual pattern; text completeness is not a substitute for visual review.

Install pinned development tooling once (the published site still needs no build):

```sh
python3 -m venv .venv
.venv/bin/pip install -r tests/dashboard/requirements.txt
.venv/bin/python -m playwright install --with-deps chromium
# pdftotext must also be installed (Debian/Ubuntu: poppler-utils).
.venv/bin/python tools/check_topics.py --all
```

Reports/PDFs live in ignored `.cache/topic-checks/`. Atomic checkpoints preserve completed
node results if interrupted; unfinished checks remain pending. Successful complete reports
can reuse a node only when its content, relevant manifest entry/ancestors, research record,
runtime, constitution, tools, browser and pinned dependencies match and both PDF hashes
remain valid. `--no-cache` forces fresh browser/PDF checks. An unrelated manifest entry
does not invalidate unchanged lesson rendering. Cheap catalog checks always rerun.
`--static-only` explicitly reports browser/print as pending; it is not publication acceptance.

## When to broaden verification

| Change | Required additional scope |
| --- | --- |
| Only lesson/research/taxonomy/hubs | Whole-catalog static + affected lesson/hub browser and both-theme print checks; concise editorial review. |
| Shared renderer, layout CSS, libraries | Entire catalog render/mobile/theme/PDF regression + affected dashboard behavior. |
| Router, progress, backups, review state | Full relevant application regression; print when output changes. |
| Manifest schema or learning standard | Full Spec Kit assessment, validator alignment and explicitly scoped migration if needed. |

`tests/dashboard/check_dashboard.py` retains the original dashboard/backfill acceptance
stories and fixtures. They retain original named lessons and backup fixtures; they are platform/historical
regression tools, not the default topic publishing gate. Counts derive from the current manifest. Select appropriate stories for
platform changes and update those application expectations deliberately when behavior or
fixtures change. Do not weaken or regenerate migration preservation evidence.

The original backfill remains explicitly verifiable while its frozen inputs are unchanged:

```sh
python3 tools/validate_content.py --expect tests/content/backend-architecture.json
```

Its repository-bound integration tests are also explicit (they are excluded from general
content test discovery):

```sh
python3 -m unittest discover -s tests/migrations -p 'check_*.py' -q
```

After intentional catalog growth, that frozen migration audit is expected to reject the
new catalog. The publishing profile must pass instead. Never refresh a preservation
snapshot merely to make new content appear part of the old migration.
