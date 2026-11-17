# Scenario Content Contract v1

**Governs**: FR-002–005/010–017/019–024
**Extends**: [existing Content and Host Contract v1](../../001-backend-architecture/contracts/content-contract.md).
**Current profile**: `constitution-1.2`. This design supplement becomes normative for migrated content during implementation.

## Existing envelope and unchanged host

Keep one `article.kb-topic[data-node-id]` with its exact h1, six direct child story sections and original stable section IDs. Hubs and the manifest remain byte-identical to the baseline.

Keep all original `details.kb-question[data-recall-id]` elements byte-identical. Missing `data-recall-kind` means foundational. Explicit `foundational` is permitted for future newly authored content, but this backfill must not add it to the protected old cards.

New questions keep `kb-question` so current `app.js`, shared CSS, source rendering, print preparation and confidence attachment continue to work without a new widget or per-lesson shell edits. The storage key/backup schema and 15-topic mastery denominator do not change.

## One nested subsection

Within the existing `section[data-section="mastery"]`, insert exactly one new `section[data-interview-scenarios]` immediately before the existing real-world-impact/takeaway element. Its `aria-labelledby` references its h3 ID, `node-<topic-id>-interview-scenarios`, whose text is exactly:

**Tricky & Most-Asked Interview Scenarios**

This nested section is not a seventh direct article section. Existing router section keys remain unchanged; links to mastery still work. New internal bare hash links are not introduced.

The subsection contains five to seven interview-card children and a clearly associated research/source note. A short orientation paragraph may precede the cards. Every card is a direct child of the subsection; do not nest one recall card inside another.

## Card grammar

| Element/attribute | Required value or behavior |
| --- | --- |
| `details.kb-question` | Exactly one independent recall disclosure per scenario. |
| `data-recall-kind` | Exactly `interview` for a new scenario. |
| `data-recall-id` | `interview-` plus a meaningful kebab-case key allocated once. Unique across all recall keys within the topic. |
| `data-scenario-basis` | `adapted-production`, `reported-recurring`, or `knowledge-based`, matching its final research record and public disclosure. |
| Direct `summary` | Exactly one, nonempty; identifies the production constraint/decision. |
| `open`, `name` | Both absent. Fresh mounts start closed and opening another answer does not close this one. |
| Three direct answer-part `div` blocks | Exactly the parts below, in order, with complete prose and required visible labels. |
| Scripts/styles/handlers/controls | None in the partial; host supplies shared confidence/status controls. |

Stable keys describe scenarios, not their ordinal positions or current wording. Preserve them when reordering/rewording a scenario and on reruns. All original keys remain reserved. Unknown roles, unmarked cards inside the interview subsection, and interview cards outside that subsection are invalid.

### Ordered answer parts

| `data-scenario-part` | Visible label in a `p > strong` | Required substance |
| --- | --- | --- |
| `scenario` | The Scenario & Constraint | Complete production situation, assumptions, concrete constraint/failure, and what-will-you-do/why prompt. |
| `decision` | The Direct Answer & Architectural Decision | Recommended action, reasoning and actionable architectural/debugging steps; scope of assumptions. |
| `trade-offs` | Key Trade-Offs & Follow-Up Traps | Gains/costs, viable alternative, interviewer-style follow-up trap, and changed-assumption response. |

Each part contains at least one further nonempty explanatory paragraph after its label. Labels alone or vague one-line substitutes do not establish completeness; editorial review is mandatory. Strong paragraph labels intentionally reuse existing article styles and PDF paragraph extraction.

Use figures/diagrams where the constitutional visualization rule applies, with adjacent explanation. Existing diagrams remain intact, and the renderer must find new diagrams even inside closed scenario cards. Syntax/code examples retain the existing escaping/highlighting contract.

## Research note and sources

Include one visible `[data-interview-research]` note within the new subsection. It identifies the research date, evidence classification/limitation and relevant named HTTPS source links. Card data and the final research record map individual scenarios to the applicable sources; the note may group common links rather than repeat every URL.

Current planning seeds all require an adaptation disclosure, such as: "These scenarios adapt documented production problems and architectural guidance. Interview frequency for these exact prompts was not independently verified." A source's company affiliation is not evidence that the company asks the question.

A card marked `reported-recurring` needs explicit interview evidence in its record and an accurate visible claim. Knowledge-based fallback needs a documented actual search failure/unavailability and visible limitation. Existing successful planning research must not be relabeled as unavailable.

## Exact preservation and reruns

The entire new subsection, including its source note, is the only inserted block. Surround it with exactly these literal markers:

```html
<!-- kb-interview-scenarios:start -->
<!-- kb-interview-scenarios:end -->
```

The actual subsection belongs between those markers; the two-marker illustration is grammar, not a deliverable lesson.

No added bytes may sit outside the delimited block. Removing the inclusive marker span must reproduce the original complete source hash in [preservation-baseline.json](preservation-baseline.json), without whitespace normalization. This also protects original module-six material and footer references.

Exactly one marker pair and one subsection are allowed. A rerun replaces that block using the already assigned keys; it never appends another one or regenerates identities. Malformed/multiple markers fail rather than guessing a repair.

## Separate counting and current profile

- Foundational: all mastery recall cards with missing kind or explicit `foundational`, outside the interview subsection; require 3–5 and the exact baseline keys/raw markup for each migrated lesson.
- Interview: subsection cards with kind `interview`; require 5–7 and the complete grammar above.
- Total: sum both groups; current migration baseline 61 foundations plus 75–105 scenarios = 136–166 questions.
- A lesson with nine generic cards but no interview group is invalid; a lesson with six interviews but no foundation group is invalid.
- The production repository validator uses `constitution-1.2`. An explicit `legacy-1.1` keyword is reserved for historical unit fixtures only. Missing markers must never imply a legacy waiver, and production expectation/CLI validation must reject that waiver.

## Host acceptance

All new questions receive the existing independent Hard/Good/Easy controls, absent prior confidence, persistent ratings, and normal backup behavior. Revealing/rating does not alter mastery or review timestamps. Both question groups share one stable topic/question namespace.

Verify both themes, keyboard operation, 360px layout, all 21 routes at both bases, every diagram, and real PDFs of all 15 migrated lessons per theme. Printing opens all answer details and restores their prior states. Shared host code/styles are expected to remain unchanged; any proven compatibility fix must be narrowly justified and receive affected regression checks.
