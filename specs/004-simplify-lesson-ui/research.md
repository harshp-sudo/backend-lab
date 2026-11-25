# Research: Simplify Lesson UI

**Implementation follow-through:** Completed and validated; see [delivery.md](delivery.md). The design-stage statements below record their original stage.

**Date:** 2026-11-25. **Stage:** Planning only. All decisions below are design decisions;
no website or governance migration has been performed.

## 1. Scope and measured baseline

**Decision:** Treat this as one shared UI/content-presentation feature. Use a deterministic
copy migration and existing learning APIs; do not reauthor 135 lessons or create 135
authoring tasks for a presentation-only change.

**Evidence:** Current manifest has 181 nodes, 135 lessons, 46 hubs and nine branches.
Intrinsic inventory contains 273 diagrams, 541 foundational cards and 810 interview cards.
All 135 lessons have a dated generic research paragraph. Seven exact wording variants
occur with frequencies 1, 14, 15, 15, 15, 30 and 45. The related-decision preamble occurs
in 120 lessons. Manifest SHA256 at planning:
`99114903e942e037c66a9442ac58f4fc6aabb66b54580e5cde95faac28334a16`.

**Rationale:** One audited transformation can preserve complete teaching content more
reliably than manual rewrites. Re-audit the actual manifest before implementation.

**Alternatives considered:** Latest-batch-only cleanup misses older variants; broad deletion
of paragraphs mentioning dates/research can destroy meaningful explanation; CSS hiding
leaves unwanted text in source, assistive output or print.

## 2. Canonical copy and footer migration

**Decision:** Keep `aside[data-interview-research]` outside closed questions. Replace only
its audited first generic paragraph with a small `h4` titled Sources; retain the exact
ordered named links. Replace the exact related intro with a Related topics label in
actual internal-link groups and style those lists to wrap compactly.

**Evidence:** The original 15 Backend Architecture footers say Sources and further reading
and contain external references. They are not related-topic groups. Container Orchestration
has meaningful discovery/mesh prose before the removable preamble; retain that prose.
`tools/validate_content.py` already checks link identity and source mapping.

**Rationale:** Preserve the existing integration hook, link meaning and educational content.
Use parsed element positions plus exact original substrings, not whole-document reserialization.

**Alternatives considered:** Relabeling every footer misclassifies external references;
removing complete asides deletes provenance links; changing only rendered HTML leaves
future authoring and direct partial content inconsistent.

## 3. Presentation validation without a recall-schema migration

**Decision:** Keep `recallProfile: constitution-1.2`. Add explicit
`researchPresentation: sources-only-v1` to current publishing expectations. Preserve
strict `disclosure-v1` behavior for explicit historical expectations/fixtures.
Current `topic-publishing` configurations missing the new setting must fail; unknown
settings must fail. Thread the selected presentation through article, interview and
research validation rather than introducing a skip flag.

**Evidence:** `tools/validate_content.py` currently requires a visible note, matches its
first paragraph to `publicDisclosure`, and requires adaptation/frequency wording. Its
recall profile also governs unchanged question roles/counts. `tests/content/publishing.json`
maps the first 15 lessons to historical Markdown research; the rest use UUID JSON records.

**Rationale:** This changes public research presentation, not recall structure. Keep
research files and mappings byte-identical. Existing `publicDisclosure` fields become
archived provenance in current mode; new records can omit them. Maintain source roles,
dates, basis/claim consistency, actual searches, assumptions and all eight editorial checks.
Do not infer presentation policy from a record's historic constitution version.

**Alternatives considered:** Bumping the recall profile conflates independent contracts;
making all checks optional weakens source validation; rewriting historical research invents
new provenance; an omitted current setting must not silently fall back to old behavior.

## 4. Governance alignment

**Decision:** During implementation, amend the constitution's public-disclosure mandate
and align the active publishing guide/skill. Target constitution 2.0.0 under its own
MAJOR rule because this removes an incompatible mandatory presentation requirement.
Preserve ratification date; set amendment date to the actual implementation date.
No learning-content, research-honesty or stable-identity principle is removed.

**Rationale:** The user's explicit request and FR-016 authorize this change. It is a
planned amendment with named dependents, not a silent constitutional exception. Current
research records can retain 1.2.0/1.3.0 provenance; accept 2.0.0 for new records after adoption.

**Alternatives considered:** Leaving governance unchanged causes future publishers to
restore the paragraph; removing research obligations would exceed the request. Generic
Spec Kit templates contain no hard-coded disclaimer and need no cosmetic rewrite.

## 5. Native compact progress and unchanged state

**Decision:** Keep one native `#topic-status` select with a visible Progress label, followed
by a conditional review group. Retain existing Start review / Complete review / Start
another review labels. Remove `#mastery-actions`, `.mastery-footer` construction/copy and
the obsolete `master-topic` button handler. Keep confidence controls untouched.

**Evidence:** `app.js` learningControls/refreshLearningControls and delegated status handler;
`assets/js/learning-state.js` markStatus/startReview/completeReview. Selecting Mastered
already performs the required explicit mastery transition. The native select is a labeled
selection control; a custom combobox is unnecessary. See [MDN select](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/select).

**Rationale:** No new dependency, custom control, storage schema or status model is needed.
Storage key stays `backend-lab.learning.v1`; backup/state versions stay 1. Existing review
intervals stay 3/7/14/30 days, including no-op/replay and remastery behavior.

**Alternatives considered:** A two-state toggle cannot express all statuses; three large
buttons compete with review actions; a second bottom widget violates the single-area spec.

## 6. Layout and focus

**Decision:** Keep the select node stable and update only the dependent review group.
Desktop uses a single inline row; 360px layout has one status row and one review row,
with 44px minimum control targets and at most 8px row gap. Review date text uses a short
visible format with an unambiguous full accessible date. Measure actual dimensions;
do not shrink targets or silently truncate actions to meet bounds.

On review start/completion, move focus to the corresponding replacement review button
only if focus was in the replaced group. Otherwise preserve focus, including confidence
cards. If a focused control disappears, use the remaining status selector. Use
`focus({preventScroll:true})` for this local replacement where appropriate; its scroll
behavior is documented in [MDN focus](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus).

**Evidence:** Existing refresh replaces a footer and focuses its heading; that heading
will no longer exist. Refreshes can run after unrelated confidence/store updates.

**Alternatives considered:** Rebuilding the whole row loses native select focus; focusing
the title on every update interrupts self-testing; hiding overflowing controls fails usability.

## 7. Cache and print boundaries

**Decision:** Migrate canonical partials and request lesson HTML with `cache: no-cache`
while retaining AbortSignal and relative URL construction in `loadArticle`. This allows
HTTP revalidation without per-navigation random URLs or a new caching subsystem.
Do not promise an already open old application tab updates itself without reload.
[MDN Request.cache](https://developer.mozilla.org/en-US/docs/Web/API/Request/cache)
documents conditional revalidation for cached responses in this mode.

Keep `data-host-controls` on the compact area and retain print open/restore behavior in
`assets/js/content-renderer.js`. Printed source links and educational content remain.

**Alternatives considered:** `no-store` unnecessarily discards reusable responses;
renderer text-stripping creates a second migration mechanism; a service worker adds
unrequested lifecycle complexity. The current application has no service worker or stored
lesson-body cache.

## 8. Proportional but complete verification

**Decision:** Run current whole-catalog intrinsic validation, general content/catalog/state
suites, then whole-catalog render/print plus current application and new compact-UI checks.
Expected catalog scope today is 543 browser cases and 362 PDFs; derive it at runtime.

Use existing checkpoint/fingerprint reuse after affected fixes. Include the new presentation
config in renderer evidence fingerprints so a policy change cannot reuse stale results.
Explicitly enumerate current dashboard scenarios US1–US6; historical MIGRATION is not a
current acceptance suite. Do not rewrite its frozen evidence to accommodate intended changes.

**Evidence:** `tools/check_topics.py` treats explicit runtime paths as broader regression,
but `--all` alone does not set that flag. Its report deliberately remains pending when
shared runtime paths are provided until application regression is established separately.
`tests/dashboard/check_dashboard.py` defaults include named historical migration work.

**Alternatives considered:** Fifteen-lesson sampling misses a shared change; accepting a
static-only/pending report overstates completion; rerunning unrelated historical migrations
or every unchanged successful check after a local fix adds overhead without evidence value.

## Research completion

Local read-only UI/state and content/governance investigations were delegated as required
by the planning skill, then reconciled against the files named above. Browser platform
references were checked on 2026-11-25. No design questions remain unresolved. These
findings do not claim the proposed UI, migration or tests have been implemented.
