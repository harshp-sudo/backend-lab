# Validation and Delivery Contract v1

**Scope**: FR-001–FR-006, FR-019, FR-021–FR-022, and all success criteria.
The following tool and fixture interfaces are planned for implementation, not created by
the planning command. Production deployment still requires only static content assets.

## Intrinsic Validator Interface

Planned entry point: `tools/validate_content.py`, using Python 3.10-compatible standard
library APIs. It reads the catalog and files; it never rewrites them or accesses learning
storage. Invocation from the repository root:

```bash
python3 tools/validate_content.py --repo-root . \
  --expect tests/content/backend-architecture.json \
  --report /tmp/backend-architecture-static.json
```

| Argument | Meaning |
| --- | --- |
| `--repo-root` | Repository location; manifest defaults to `manifest.json` below it. |
| `--expect` | Test-only expected batch inventory, derived from the exact request. |
| `--baseline` | Optional previous manifest for identity-preservation comparison. |
| `--report` | Optional JSON report destination; create parent directories when needed. |

The expectation fixture contains the profile name, System Design and Backend Architecture
titles/slugs, the four requested category titles/slugs, and each requested topic title/slug
in order. Optional `deliveryRecord` names a repository-relative required delivery document;
the implemented batch profile uses `specs/001-backend-architecture/delivery.md`. It does not contain permanent IDs or serve the application. It verifies request
coverage rather than becoming a second runtime content index. Unrelated catalog nodes are
permitted and preserved; batch counts refer to the 15 requested leaves and their six hubs.

Exit `0` means all required intrinsic checks passed. Exit `1` means content or catalog
validation failed. Exit `2` means invalid command arguments or an unreadable input.
An exit `0` never certifies browser rendering, teaching comprehension, or real-host integration.

## Intrinsic Checks

| Check group | Required behavior |
| --- | --- |
| JSON and shape | Reject malformed JSON, repeated object keys, missing core fields, unsupported schema version, non-hub roots, empty hubs, or children on a topic. |
| Identity | Check globally unique IDs; new nodes use canonical UUIDv4. With a baseline, preserve all previous IDs and node kinds; no automatic identity reassignment. |
| Taxonomy | Require the exact batch membership, labels, ordering, four groups and 5/4/3/3 distribution. Synonym alignment also needs editorial review. |
| Locations | Derive unique routes and files; reject duplicate sibling slugs and destinations escaping the resolved content root, including symlinks. |
| Article identity | One correct article, matching title and node ID, expected topic/hub class, no forbidden document wrapper or executable/style markup. |
| Topic structure | Six ordered module keys; prose in every module; diagram block; mechanics details; comparison table; failure-story labels; Feynman prompt; three to five recall items. |
| Recall structure | Unique stable local keys, meaningful summary and answer text, no initial open attribute and no shared disclosure group name. |
| Hub coverage | Roadmap source, introductory/reading guidance content, and the exact immediate-child link list in manifest order. |
| Links | Every authored content route and requested section exists; reject malformed internal links and duplicate DOM IDs. Source URLs must use the allowed external-link form. |
| Completeness | Reject explicit unfinished-content markers, empty instructional sections, missing files, and missing required bundle artifacts. |

The validator checks this project's known contract directly; it is not a general JSON
Schema engine or HTML conformance checker. The formal [schema](manifest.schema.json)
can additionally be used by editors or a development-time schema validator. Syntactic
structure checks cannot establish analogy fidelity, diagram validity, or conceptual accuracy.
Historical IDs cannot be certified from one manifest alone; without a baseline, report that
comparison as pending while checking new-ID format for this initial empty-catalog batch.

## Report Format and Acceptance Tiers

A JSON report records `profile`, `phase`, `result`, `counts`, `checks`, and
`integrationStatus`. Each check includes `name`, `status`, `artifact`, and `message`.
Check status is `pass`, `fail`, `pending`, or `not-applicable`. Counts distinguish total
catalog nodes from requested batch nodes. Intrinsic reports use `phase: "intrinsic"` and
`integrationStatus: "pending"` until a separate actual-host review supplies evidence.

| Tier | Evidence | Initial planned status |
| --- | --- | --- |
| Intrinsic | Manifest, cross-file validator, focused validator tests, and editorial review | Pending implementation |
| Browser fixture | Render all 21 partials, syntax/render errors, disclosures, themes, 360px width, A4 print lifecycle | Pending implementation |
| Actual dashboard | Route/breadcrumb flow, global status/confidence, reload persistence, reviews, rename/move state preservation | Pending host integration |
| Learner comprehension | Five novice opening trials spanning all four groups; at least four meet the 30-second goal | Pending human review |

Any failed required check prevents acceptance at its tier. Pending tiers must remain visible
in delivery reporting. The batch may be described as content-complete with pending integration
only when its intrinsic and browser-fixture evidence support that narrower claim; it may not
be described as fully integrated or as having passed learner trials without those checks.

## Browser Fixture Interface

Planned fixture: `tests/fixtures/content-host.html`, with adjacent JavaScript and CSS. It
mounts production partials and the shared [content contract](content-contract.md), loading
only pinned renderer assets. It has a reading canvas and test controls, not product features.

The fixture exposes `contentFixture.checkAll()` and `contentFixture.mount(route)` for
repeatable console-driven checks. `checkAll()` returns and displays a report for all expected
21 nodes, fails on network/render errors, and records browser/library versions. Mounting a
route exposes normal links, details, reading themes, and print preparation for manual review.
Loading indicators and missing-asset errors must be visible; a missing renderer is not a pass.

The fixture must not persist progress, implement search or a review queue, or masquerade as
the application's learning engine. Native recall behavior and article identity can be tested
there; actual learning-state preservation is checked only with the real host.

## Focused Negative Fixtures and Historical Checks

Use `unittest` temporary fixtures for duplicate JSON keys, duplicate IDs, slug/file collisions,
missing partials, wrong article IDs, missing story modules, invalid recall counts, broken hub
links, and baseline ID replacement. Include a positive rename/move fixture that retains ID
and repairs its affected links. These validate the checker, not the unseen dashboard.

Reapply the authoring workflow against the delivered tree and compare the result against a
baseline: zero new identities/nodes and no unrelated changes. Concept alignment is reviewed
by the author. With a real host, record status, reviews, and confidence for a sample topic,
rename/move it while retaining its ID, then reload and compare the exact saved state.

## Delivery Bundle

The implementation creates `specs/001-backend-architecture/delivery.md` with the audit result,
15 one-line placement justifications, artifact paths, source-review notes, and tiered validation
results. Include a paste-ready manifest snapshot: the whole file for this initial catalog,
or a contextual update if the implementation-time audit finds existing content. Label this
as a dated delivery snapshot; `manifest.json` remains the runtime authority.

Deliver all 15 complete topic files and six hubs, or reuse/update aligned hubs if the current
tree has changed. No lesson bodies are replaced by documentation links or placeholder text.
Record any conflict resolutions and every pending integration or learner check explicitly.
