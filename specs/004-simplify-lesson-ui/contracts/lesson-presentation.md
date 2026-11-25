# Contract: Lesson Copy, Sources and Publishing

**Status:** Implemented and verified; see [delivery](../delivery.md).
**Applies to:** All manifest-derived lessons and future publishing acceptance.
**Related:** [Spec](../spec.md), [research](../research.md), [data model](../data-model.md).

## Canonical lesson source

1. Retain the existing article identity/title and six direct story sections in order.
2. Keep every diagram, foundational/interview key, answer, confidence integration hook,
   scenario basis and meaningful contextual assumption.
3. In the existing source aside, remove only the audited generic first paragraph. Insert
   an `h4` Sources label and retain the named reference list/ordered URLs. Keep the source
   group visible outside all closed question cards, not behind another disclosure.
4. Remove the exact related-decision preamble from actual related-topic groups and label
   those groups Related topics. Preserve every target/order and meaningful adjacent prose.
5. Retain the original external Sources and further reading footers as external-reference
   groups. Do not relabel them as related topics or delete their references.
6. No public replacement explanation about adaptation/frequency, authoring process, dates
   or generic numeric assumptions may be put in a tooltip, hidden content, another site
   page or printed-only area. Specific assumptions inside answers remain.
7. No empty source/link group, placeholder heading or empty banner is allowed.

## Deterministic migration and preservation

`tools/migrate_lesson_presentation.py` is the proposed small migration/verifier utility.
It must support dry-run before apply and a subsequent baseline comparison. Its command
contract is defined in [quickstart](../quickstart.md); it is not implemented at planning time.

- Resolve all target paths through the manifest; never use a fixed topic count or assume
  every HTML file is a lesson.
- Capture original bytes and inventory once under the supplied ignored snapshot directory.
  Reuse that original on resume; refuse an accidental replacement of an existing baseline.
- Inventory the first source-paragraph shapes/text, named source links, footer links,
  node/recall identities, diagram source, learning sections and protected file hashes.
- Parse elements and use exact original offsets/substrings for edits. Do not use a broad
  case-insensitive delete of arbitrary paragraphs or serialize whole documents.
- Recognize audited generic-note shapes; an unexpected/multiple/nested or missing source
  shape must fail with the path/reason unless it already matches the finished contract.
- Apply only the permitted paragraph/label/group changes. Repeat application is a no-op.
- Verify each result equals its allowlisted transformation of captured original bytes.
  All cards/answers, diagrams, technical prose and original link order must compare equal.
- Hash-compare the unchanged manifest, all hubs, existing research records/mappings,
  historical acceptance evidence and unrelated files. Active publishing configuration is
  deliberately changed only to add the presentation setting; its old mappings remain equal.
- Produce a compact inventory/diff result, not a duplicate answer ledger. Unexpected edits
  fail acceptance rather than expanding the allowlist silently.

## Current versus historical validation

Current configuration in `tests/content/publishing.json` explicitly selects
`researchPresentation: sources-only-v1`, alongside the unchanged recallProfile.
Unknown/missing current presentation values fail closed. Historical named migration
expectations and legacy fixtures use `disclosure-v1`; no global disable-disclosure switch.

Thread the selected policy through `validate`, registered topic checker calls,
`check_article`, `check_interviews` and `check_research`. The report must state the applied
presentation policy. Direct-call tests must explicitly select the intended policy.

| Check | sources-only-v1 | disclosure-v1 |
| --- | --- | --- |
| Six modules, counts, identities, answer parts | Strict existing checks | Strict existing checks |
| One visible source group outside cards | Required with Sources heading and named links | Required with original visible note |
| Generic first research paragraph | Prohibited | Required by historical disclosure rules |
| publicDisclosure equality to rendered first paragraph | Not applicable; existing field is archival | Required |
| Public adaptation/frequency formula | Prohibited generic boilerplate | Existing strict rule retained |
| Source URL order and sourceNoteUrls | Exact existing mapping required | Exact existing mapping required |
| Source roles, actual queries/dates, basis, supported claims, eight editorial criteria | Required | Required |
| Bad URL, hidden/missing source, key mismatch, unsupported reported claim | Reject | Reject |

Accept documented existing research provenance versions 1.2.0/1.3.0 and new 2.0.0 in current
publishing after the amendment. Do not change original research timestamps/version fields.
Omitting a public paragraph field on a newly generated current record is valid; omitting
research evidence or reviewed status is not.

### Required meaningful fixture cases

- Current clean six-module lesson + complete record passes without `publicDisclosure`.
- Current clean lesson + an unchanged older record containing archived `publicDisclosure`
  passes with matching sources and scenario mappings.
- Reintroduced generic note, renamed boilerplate, hidden/missing sources, unexpected public
  intro paragraph or a missing/unknown current config setting fails.
- Corrupted source order/URL, false supported claim, missing research, incomplete answers,
  changed keys and invalid editorial findings fail as before.
- Explicit legacy valid note passes; removing/mismatching its disclosure still fails.
- A fresh temporary publishing fixture meets the new contract without adding a real
  catalog topic. This establishes future authoring compatibility.
- Migration preserves a non-generic dated explanation, the Container Orchestration prose,
  legacy external footers and all educational bytes outside allowed spans.

## Governance and historical boundaries

Implementation amends the active constitution to 2.0.0 for the incompatible public-display
mandate change; preserve the original ratification date and record the real amendment date,
reason, migration scope and synchronized active guide/skill/configuration. This user's
explicit request supplies authorization for that scoped change.

`docs/topic-publishing.md` and the topic-publish skill must teach the Sources-only group
and maintainer-only research limitations. Do not alter generic templates without an actual
conflicting rule, or rewrite historical specifications/evidence to assert retroactive
compliance. Historical frozen migration checks remain specific to their original snapshot;
they are not acceptance of an intentionally changed live catalog.

## Rendering and evidence

- Shared CSS renders reference/related lists compactly with wrapping readable labels.
- `loadArticle` retains relative addressing, identity guards and abort behavior; conditional
  HTTP revalidation checks for updated canonical lessons on navigation/reload.
- Do not add a renderer-only text-removal filter, service worker or new network fetch for
  research records.
- Whole-catalog browser/print and current application checks are required. Printed sources,
  complete answers and diagrams remain; removed copy and host controls are absent.
- Include current publishing configuration/presentation in evidence fingerprints; reject
  mismatching fingerprints or damaged/missing PDFs before reuse.
