# Research and Editorial Evidence Contract

**Governs**: FR-005–009/016/022
**Planning seeds**: [15 concept records](../research/topic-sources.md)
**Purpose**: Make source honesty and answer quality independently reviewable for every lesson.

## Final per-lesson research records

During implementation, create `specs/003-backfill-interview-scenarios/research/<topic-slug>.md` for each of the 15 existing lessons. The filename uses the existing leaf slug; identity inside the record is the immutable topic ID, not the filename.

Each record must contain these sections and fields:

| Section | Required content |
| --- | --- |
| Identity and state | Exact topic ID/title/path, constitution version 1.2.0, researched-on ISO date, and record state `draft` or `reviewed`. |
| Searches | Actual concept-specific query strings, dates, result/failure status, and the distinction between successful searching and insufficient interview-frequency evidence. |
| Sources | Local source ID, descriptive title, HTTPS URL, role `technical-primary` and/or `interview-evidence`, checked-on date (or an explicit unverified/unavailable limitation), and what the source supports. |
| Scenario mapping | One row per selected stable recall key, theme/constraint, basis, selection-source IDs, technical-source IDs, exact supported frequency/company claim or `none`, and any source/assumption limitation. |
| Public disclosure | The actual learner-facing adaptation/research-limitation wording and the source-note URLs that will appear in the lesson. |
| Editorial acceptance | One reviewed row per card covering all criteria below, with pass/fail and a concrete rationale or corrective finding. |

Source IDs are unique within a record and every referenced source ID must resolve. Five to seven scenario rows must correspond exactly to the lesson's new keys; no approved row may describe a missing card or vice versa.

All current planning seeds use `adapted-production` and no verified frequency/company claim. A future finding can justify another basis only if documented. Numeric budgets and organization details invented for a scenario are explicitly author assumptions, never attributed as observed company facts.

Technical documentation may also support why a production situation is useful practice. That is selection rationale, not proof of hiring frequency. A named-company engineering article describes that company's production practice unless it explicitly establishes the interview claim.

## Failure and insufficient-evidence rules

- Record actual availability: this planning pass used web search for all 15 concepts. Do not claim it was unavailable.
- If interview recurrence cannot be established, disclose that gap and label adaptations. Continue to verify answer mechanics against primary sources.
- If a later search/revalidation attempt truly fails, record the attempted query/date/failure and what could not be refreshed. Previously checked sources retain their real check date; do not fabricate a new one.
- Missing/failed research never permits fewer than five complete scenarios, empty answers, invented citations, or unsupported frequency/ranking claims.
- A final record cannot reach `reviewed` while unresolved technical correctness, editorial completeness or source honesty failures remain.

## Per-card editorial review

Each selected scenario must receive an explicit disposition for:

1. Concept specificity: the decision tests this topic's actual responsibility/boundary.
2. Distinctness: a material production constraint or failure differs from other cards and from merely reworded foundational questions.
3. Production prompt: assumptions and constraint/failure are concrete; it asks what to do and why.
4. Direct answer: recommended action and steps are explained, not deferred to an external source or an unqualified "it depends".
5. Decision costs: gains, costs and at least one viable alternative are explained under the stated constraints.
6. Follow-up: at least one meaningful trap and changed-assumption response are complete.
7. Evidence: source roles and public claims are accurate; unsupported company/frequency claims fail.
8. Full delivery: all three labeled answer parts, applicable diagrams and complete prose exist.

Structural tooling can enforce roles, counts, labels, links, key uniqueness and nonempty prose. It must not claim to prove these semantic judgments automatically. Unsupported-claim/definition-only/duplicate-theme negative review cases must be rejected through editorial review even when their HTML is structurally valid.

## Per-lesson completion inventory

Implementation produces `evidence/lesson-completion.json` with `schemaVersion:1`, the referenced preservation-baseline digest, and exactly 15 lesson entries. Each entry records:

- `topicId`, `path`, original foundational keys and new scenario keys; counts derive from the key arrays.
- `researchRecord` and its approved scenario/source mapping.
- `preservation`, `structure`, `editorial`, `browser`, `print` dispositions: `pending`, `pass`, or `fail`, with evidence references/findings.
- Overall `status`: `pending`, `pass`, or `fail`. It is pass only when all five required dispositions pass for that lesson.

Preservation must compare original source reconstruction, not only IDs/counts. Browser proof includes both hosting bases and the new questions' rating/backup behavior; print proof includes both themes. Aggregate reports cannot stand in for absent per-lesson entries.

## Historical records

Keep earlier feature 001/002 acceptance reports unchanged as historical results. Their prior 61-question/22-diagram totals describe that earlier delivery. New evidence establishes the expanded state and does not rewrite earlier results as if the migration had already existed.
