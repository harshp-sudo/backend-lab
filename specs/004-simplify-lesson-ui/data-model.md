# Data Model: Simplify Lesson UI

**Implementation follow-through:** Completed and validated; see [delivery.md](delivery.md). The design-stage statements below record their original stage.

**Status:** Design only. Reuse the current learning model; no stored-state or backup migration.

## Lesson and question identity

The recursive manifest retains schemaVersion 1 and all existing `id`, `kind`, `title`,
`slug` and hub `children` values. Topic routes/paths remain derived from ancestry.
All `data-node-id`, `data-recall-id`, question ordering and scenario-basis values remain.
No title, slug or route becomes a persistence key.

The lesson's six story sections, diagrams and complete questions remain authoritative.
Only the generic source paragraph, the exact related preamble and permitted group labels
change in canonical partials. Hubs are not lesson-status records.

## Learning record (unchanged)

Use `assets/js/learning-state.js` and its existing validation as the exact authority.
The root state retains its current version, update time and topic map. A topic record
retains status, lastVisitedAt, stable-key confidence and review; the storage key remains
`backend-lab.learning.v1`. Backup envelope/version remain unchanged.

| Record component | Existing meaning | Preservation rule |
| --- | --- | --- |
| status | not-started, in-progress or mastered | Change only through the existing explicit transition |
| lastVisitedAt | Most recent recorded visit | Ordinary visits may update it; a copy/UI migration does not rewrite it |
| confidence | Recall key to rating and ratedAt | Hard/Good/Easy affect confidence only |
| review.cycle | Mastery cycle identity | Preserve monotonic remastery behavior |
| review.lastReviewed | Last accepted mastery/review time | Never infer a new review from reading or rating |
| review.intervalIndex | Index into 3/7/14/30-day schedule | Preserve current bounds and advancement |
| review.history | Existing mastery/review event log | Do not drop, duplicate or fabricate events |
| review.session | Current/recent explicit review session | Preserve identity, cycle and completion/replay protection |
| Unknown topic records | Imported records absent from current catalog | Preserve in backups/storage; exclude from known-topic progress denominator |

### State transitions to expose, not reimplement

| User action | Existing transition | Compact UI outcome |
| --- | --- | --- |
| Choose the same status | No-op | Selection and review remain stable |
| Choose In Progress or Not Started | Existing markStatus transition; leaving mastery clears active session while retaining prescribed history | Only the status group remains |
| Choose Mastered from another status | New mastery cycle/event, index 0, lastReviewed set, session cleared | Next date and Start review appear |
| Rate a question | Confidence change only | Selected rating updates; focus stays in the card |
| Start review | Existing session creation or active-session no-op | Complete review action appears |
| Complete current active review | One accepted event and capped interval advancement | Start another review plus next date |
| Repeat/stale completion | Existing no-op | No duplicate history or interval advancement |
| Confirm valid backup import | Existing whole-state replacement on successful persistence | Render imported status/session without starting a new cycle |

## Source group and research records

Reader presentation keeps one `aside[data-interview-research]` with a Sources label and
named HTTPS references outside closed scenario cards. The label is not a seventh module
or a question. Source labels, URLs and order remain stable.

Maintainer records stay at their existing mapped paths: the original 15 Markdown records
and the current UUID JSON records. Retain `topicId`, title/path, constitutionVersion,
researchedOn, searches, sources with roles/support/check dates, scenario basis/claim/source
mappings, assumptions/limitations, editorial findings and `sourceNoteUrls`.

Existing `publicDisclosure` values remain byte-for-byte historical evidence. In the current
sources-only presentation they do not describe rendered text and are not copied into it.
New sources-only records may omit that field. Historic constitutionVersion values are
provenance, not a request to render an old paragraph.

## Publishing expectation (new field, no learner-data impact)

| Setting | Current publishing | Historical explicit checks |
| --- | --- | --- |
| recallProfile | constitution-1.2 | constitution-1.2 |
| researchPresentation | sources-only-v1; mandatory explicit value | disclosure-v1; named historical expectation may infer it |

Unknown values fail. A missing setting in current topic-publishing configuration fails.
Do not use presence/absence of `publicDisclosure` to choose a looser mode.

## Ephemeral UI state

The selected option and review action derive from the existing learning record. DOM focus,
row layout and expanded recall answers remain interaction/presentation state, not new
stored fields. No UI migration writes to saved progress merely to establish the new layout.
