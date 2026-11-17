# Backend Architecture Delivery

**Implementation date**: 2026-11-17

## Taxonomy audit (T001)

No manifest, topic directory, or production dashboard existed at implementation start.
There are no existing nodes, conflicting paths, legacy IDs, or learning state to migrate.
System Design → Backend Architecture → the four requested categories → topic is a balanced
four-level hierarchy. Initial scope: 15 complete lessons and six overview hubs.
New identities are UUIDv4 assigned once in manifest.json; there is no secondary ID registry.

## Acceptance tiers

- Intrinsic: PASS (39 tests; all 21 partials and references checked).
- Reference browser fixture: PASS (21 partials, 22 diagrams, both themes, mobile, real PDFs).
- Actual dashboard and durable learning state: pending host integration; no host exists.
- Novice comprehension: pending human review; no trials have been conducted.

## Lesson implementation and review (T011–T027)

All 15 individually authored lessons are complete: 26,836 words, 92 mechanics cards,
16 rendered diagrams, 45 topic-specific failure stories, and 61 independent recall answers.
Each lesson starts with its own familiar analogy and follows one worked business story
through the six required modules. This was author/editorial review, not novice testing.

The primary-source map was checked against original-author/first-party pages during
authoring. Platform mechanisms are labeled as examples; architecture choices are contextual,
not a maturity ranking. The Evans reference page is supplementary; accessible Microsoft
domain-analysis material was used rather than claiming access to blocked full text.

All 15 lessons passed the reference Chromium 141 browser run: actual SVG rendering,
independently openable answers, both themes, 360px page overflow checks, and real A4 PDF
generation. PDF text extraction confirmed every mechanics/answer body was included;
beforeprint opened disclosures and afterprint restored their prior states. Desktop/mobile
screenshots were visually inspected. Wide diagrams/tables scroll inside their own wrappers.

Evidence: [structure](evidence/lesson-structure.json) and
[browser lesson report](evidence/browser-lessons.json). Temporary PDFs are under
`/tmp/backend-architecture-pdfs/`; test tools/libraries are isolated under `/tmp/`, with no
production npm/Python dependencies added.

| Lesson | Words | Mechanics cards | Recall questions | Browser/print |
| --- | ---: | ---: | ---: | --- |
| Distributed System Fundamentals | 1801 | 6 | 4 | PASS |
| Monolithic Architecture | 1778 | 6 | 4 | PASS |
| Modular Monolith | 1731 | 6 | 4 | PASS |
| Service-Oriented Architecture (SOA) | 1755 | 6 | 4 | PASS |
| Microservices Architecture | 1753 | 6 | 4 | PASS |
| Layered Architecture | 1744 | 6 | 4 | PASS |
| Clean Architecture | 1831 | 6 | 4 | PASS |
| Hexagonal Architecture | 1728 | 6 | 4 | PASS |
| Domain-Driven Design (DDD) | 2035 | 7 | 5 | PASS |
| Event-Driven Architecture | 1802 | 6 | 4 | PASS |
| API Gateway Pattern | 1770 | 6 | 4 | PASS |
| Backend for Frontend (BFF) | 1733 | 6 | 4 | PASS |
| Service Discovery | 1727 | 6 | 4 | PASS |
| Service Mesh | 1697 | 6 | 4 | PASS |
| Multi-Tenant Architecture | 1951 | 7 | 4 | PASS |

## Hub and navigation verification (T030–T036)

All six hub files are complete and their ordered child lists match the manifest.
The root and project-prefix fixture runs each followed all 20 parent-child links to real
articles and checked location context plus browser back/forward. The full static content/link
check passed. Evidence: [navigation](evidence/navigation.json). This is fixture evidence,
not a claim about the absent production dashboard.

## Active recall and host controls (T037–T039)

All 61 questions have complete topic-specific explanatory answers and stable semantic local
keys. The five DDD cards cover context/service boundaries, identity/value, aggregate
invariants, publication, and modeling cost; all other lessons have four cards covering
their own failure and decision cases. No key is computed from current list position.

Chromium keyboard checks used focus plus Enter on native summaries in all 15 lessons.
Two answers remained open independently, closing one left the other open, topic/recall
identities remained unchanged, and localStorage was unchanged. Evidence:
[native recall report](evidence/recall.json).

Actual status, Hard/Good/Easy persistence, review timestamps, and global mastery behavior
are **pending host integration**. There is no production dashboard or learning engine to
exercise. No substitute status/rating controls or fake persistence were introduced in
the reference fixture. Completing this disposition is not a claim that those scenarios passed.

## Historical identity and repeat delivery (T040–T044)

The 39 focused Python tests pass, including valid baseline preservation, ID replacement/loss,
kind changes, metadata loss, missing/orphan partials, missing delivery records, CLI exits, and
a valid rename/move with repaired links.

The full requested taxonomy was re-audited and reapplied to a separate content candidate.
All 21 nodes were reused; no identities/nodes were added, and manifest/HTML hashes stayed
identical. This exercised the authoring audit/upsert/no-op workflow against another copy,
not merely a comparison of the original file with itself. [Replay evidence](evidence/repeat.json).

A second candidate moved and renamed Distributed System Fundamentals into the code/domain
category, retained its topic ID and all four recall keys, relocated its full HTML, repaired
all referencing links and affected roadmap/card lists, and validated against a temporary
updated expectation profile plus the original identity baseline. The canonical production
profile and 5/4/3/3 placement remain unchanged. [Rename/move evidence](evidence/rename-move.json).

Actual durable learning-state preservation after a move remains **pending host integration**.
No production dashboard exists on which to save status/review/confidence and reload them.
The content test proves retained references and correct navigation, not persistence behavior.

## Placement Justifications

- Root: System Design > Parent: Backend Architecture > Sub-category: Core System Topologies > Topic: Distributed System Fundamentals — explains deployment/coordination shape and its failure or ownership boundary.
- Root: System Design > Parent: Backend Architecture > Sub-category: Core System Topologies > Topic: Monolithic Architecture — explains deployment/coordination shape and its failure or ownership boundary.
- Root: System Design > Parent: Backend Architecture > Sub-category: Core System Topologies > Topic: Modular Monolith — explains deployment/coordination shape and its failure or ownership boundary.
- Root: System Design > Parent: Backend Architecture > Sub-category: Core System Topologies > Topic: Service-Oriented Architecture (SOA) — explains deployment/coordination shape and its failure or ownership boundary.
- Root: System Design > Parent: Backend Architecture > Sub-category: Core System Topologies > Topic: Microservices Architecture — explains deployment/coordination shape and its failure or ownership boundary.
- Root: System Design > Parent: Backend Architecture > Sub-category: Code & Domain Organization > Topic: Layered Architecture — explains internal responsibility, dependency, or business-model boundaries.
- Root: System Design > Parent: Backend Architecture > Sub-category: Code & Domain Organization > Topic: Clean Architecture — explains internal responsibility, dependency, or business-model boundaries.
- Root: System Design > Parent: Backend Architecture > Sub-category: Code & Domain Organization > Topic: Hexagonal Architecture — explains internal responsibility, dependency, or business-model boundaries.
- Root: System Design > Parent: Backend Architecture > Sub-category: Code & Domain Organization > Topic: Domain-Driven Design (DDD) — explains internal responsibility, dependency, or business-model boundaries.
- Root: System Design > Parent: Backend Architecture > Sub-category: Communication & Routing > Topic: Event-Driven Architecture — explains how participants exchange work or present backend interactions.
- Root: System Design > Parent: Backend Architecture > Sub-category: Communication & Routing > Topic: API Gateway Pattern — explains how participants exchange work or present backend interactions.
- Root: System Design > Parent: Backend Architecture > Sub-category: Communication & Routing > Topic: Backend for Frontend (BFF) — explains how participants exchange work or present backend interactions.
- Root: System Design > Parent: Backend Architecture > Sub-category: Infrastructure & Multi-Tenancy > Topic: Service Discovery — explains operational communication/location or customer isolation boundaries.
- Root: System Design > Parent: Backend Architecture > Sub-category: Infrastructure & Multi-Tenancy > Topic: Service Mesh — explains operational communication/location or customer isolation boundaries.
- Root: System Design > Parent: Backend Architecture > Sub-category: Infrastructure & Multi-Tenancy > Topic: Multi-Tenant Architecture — explains operational communication/location or customer isolation boundaries.

All requested leaves are four levels deep. No depth exception, synonymous category, path
conflict, or separate root was required. Parent node IDs are permanent and every missing
parent has its own complete overview.

## Complete Artifact Bundle

| Role | Full partial path |
| --- | --- |
| hub: System Design | [topics/system-design/_overview.html](../../topics/system-design/_overview.html) |
| hub: Backend Architecture | [topics/system-design/backend-architecture/_overview.html](../../topics/system-design/backend-architecture/_overview.html) |
| hub: Core System Topologies | [topics/system-design/backend-architecture/core-system-topologies/_overview.html](../../topics/system-design/backend-architecture/core-system-topologies/_overview.html) |
| topic: Distributed System Fundamentals | [topics/system-design/backend-architecture/core-system-topologies/distributed-system-fundamentals.html](../../topics/system-design/backend-architecture/core-system-topologies/distributed-system-fundamentals.html) |
| topic: Monolithic Architecture | [topics/system-design/backend-architecture/core-system-topologies/monolithic-architecture.html](../../topics/system-design/backend-architecture/core-system-topologies/monolithic-architecture.html) |
| topic: Modular Monolith | [topics/system-design/backend-architecture/core-system-topologies/modular-monolith.html](../../topics/system-design/backend-architecture/core-system-topologies/modular-monolith.html) |
| topic: Service-Oriented Architecture (SOA) | [topics/system-design/backend-architecture/core-system-topologies/service-oriented-architecture.html](../../topics/system-design/backend-architecture/core-system-topologies/service-oriented-architecture.html) |
| topic: Microservices Architecture | [topics/system-design/backend-architecture/core-system-topologies/microservices-architecture.html](../../topics/system-design/backend-architecture/core-system-topologies/microservices-architecture.html) |
| hub: Code & Domain Organization | [topics/system-design/backend-architecture/code-and-domain-organization/_overview.html](../../topics/system-design/backend-architecture/code-and-domain-organization/_overview.html) |
| topic: Layered Architecture | [topics/system-design/backend-architecture/code-and-domain-organization/layered-architecture.html](../../topics/system-design/backend-architecture/code-and-domain-organization/layered-architecture.html) |
| topic: Clean Architecture | [topics/system-design/backend-architecture/code-and-domain-organization/clean-architecture.html](../../topics/system-design/backend-architecture/code-and-domain-organization/clean-architecture.html) |
| topic: Hexagonal Architecture | [topics/system-design/backend-architecture/code-and-domain-organization/hexagonal-architecture.html](../../topics/system-design/backend-architecture/code-and-domain-organization/hexagonal-architecture.html) |
| topic: Domain-Driven Design (DDD) | [topics/system-design/backend-architecture/code-and-domain-organization/domain-driven-design.html](../../topics/system-design/backend-architecture/code-and-domain-organization/domain-driven-design.html) |
| hub: Communication & Routing | [topics/system-design/backend-architecture/communication-and-routing/_overview.html](../../topics/system-design/backend-architecture/communication-and-routing/_overview.html) |
| topic: Event-Driven Architecture | [topics/system-design/backend-architecture/communication-and-routing/event-driven-architecture.html](../../topics/system-design/backend-architecture/communication-and-routing/event-driven-architecture.html) |
| topic: API Gateway Pattern | [topics/system-design/backend-architecture/communication-and-routing/api-gateway-pattern.html](../../topics/system-design/backend-architecture/communication-and-routing/api-gateway-pattern.html) |
| topic: Backend for Frontend (BFF) | [topics/system-design/backend-architecture/communication-and-routing/backend-for-frontend.html](../../topics/system-design/backend-architecture/communication-and-routing/backend-for-frontend.html) |
| hub: Infrastructure & Multi-Tenancy | [topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/_overview.html](../../topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/_overview.html) |
| topic: Service Discovery | [topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/service-discovery.html](../../topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/service-discovery.html) |
| topic: Service Mesh | [topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/service-mesh.html](../../topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/service-mesh.html) |
| topic: Multi-Tenant Architecture | [topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/multi-tenant-architecture.html](../../topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/multi-tenant-architecture.html) |

The complete lesson bodies are in those HTML files, not replaced by this delivery record.
Word counts above are approximate source-text counts including headings, code/diagram
source, labels, and references; they are not timed-reading or comprehension evidence.

## Paste-Ready Manifest Snapshot

Snapshot date: 2026-11-17. This is the complete initial manifest, including all newly created
parents and permanent IDs. The runtime source of truth remains the root `manifest.json`.

<!-- manifest-snapshot -->
```json
{
  "schemaVersion": 1,
  "roots": [
    {
      "id": "d3825659-12c2-4fc8-b6fe-bdd050762da3",
      "kind": "hub",
      "title": "System Design",
      "slug": "system-design",
      "children": [
        {
          "id": "401502d7-77c1-438c-a663-053fc5d18ada",
          "kind": "hub",
          "title": "Backend Architecture",
          "slug": "backend-architecture",
          "children": [
            {
              "id": "782e772f-8c50-46aa-a26a-d37ff94599a2",
              "kind": "hub",
              "title": "Core System Topologies",
              "slug": "core-system-topologies",
              "children": [
                {
                  "id": "a1cef6f2-5f76-4376-980d-64af99310ec8",
                  "kind": "topic",
                  "title": "Distributed System Fundamentals",
                  "slug": "distributed-system-fundamentals"
                },
                {
                  "id": "1901acc7-9225-428a-9397-072cff3d36d0",
                  "kind": "topic",
                  "title": "Monolithic Architecture",
                  "slug": "monolithic-architecture"
                },
                {
                  "id": "ab88a9ad-48ea-4968-becb-b0641aa6321d",
                  "kind": "topic",
                  "title": "Modular Monolith",
                  "slug": "modular-monolith"
                },
                {
                  "id": "11d759b2-bda9-45ba-a34d-0a0326cabd56",
                  "kind": "topic",
                  "title": "Service-Oriented Architecture (SOA)",
                  "slug": "service-oriented-architecture"
                },
                {
                  "id": "04eae1bf-07bc-4646-8ce4-db2871fcfada",
                  "kind": "topic",
                  "title": "Microservices Architecture",
                  "slug": "microservices-architecture"
                }
              ]
            },
            {
              "id": "1dce8024-d12a-4295-ae55-afa135170fb5",
              "kind": "hub",
              "title": "Code & Domain Organization",
              "slug": "code-and-domain-organization",
              "children": [
                {
                  "id": "012a24bf-b2d7-4824-9a52-016ed4399c5e",
                  "kind": "topic",
                  "title": "Layered Architecture",
                  "slug": "layered-architecture"
                },
                {
                  "id": "d257fdd8-8532-4138-839b-7295ae2e2994",
                  "kind": "topic",
                  "title": "Clean Architecture",
                  "slug": "clean-architecture"
                },
                {
                  "id": "7db3e3c3-10aa-4709-bf33-63848952d81f",
                  "kind": "topic",
                  "title": "Hexagonal Architecture",
                  "slug": "hexagonal-architecture"
                },
                {
                  "id": "a612a2d8-260a-4e97-82e7-b2851459e0c7",
                  "kind": "topic",
                  "title": "Domain-Driven Design (DDD)",
                  "slug": "domain-driven-design"
                }
              ]
            },
            {
              "id": "a83461a8-4d18-4132-908e-dac2eab5638d",
              "kind": "hub",
              "title": "Communication & Routing",
              "slug": "communication-and-routing",
              "children": [
                {
                  "id": "0b36c2d3-9c94-47df-adce-d80bf6c3f720",
                  "kind": "topic",
                  "title": "Event-Driven Architecture",
                  "slug": "event-driven-architecture"
                },
                {
                  "id": "a5b7beee-bdbd-4987-9a41-8e16471b0a32",
                  "kind": "topic",
                  "title": "API Gateway Pattern",
                  "slug": "api-gateway-pattern"
                },
                {
                  "id": "1be329da-9367-4c1c-a4c8-0eff6ec862e1",
                  "kind": "topic",
                  "title": "Backend for Frontend (BFF)",
                  "slug": "backend-for-frontend"
                }
              ]
            },
            {
              "id": "e4b099e0-3f6c-480e-bb61-76e763a8e5e5",
              "kind": "hub",
              "title": "Infrastructure & Multi-Tenancy",
              "slug": "infrastructure-and-multi-tenancy",
              "children": [
                {
                  "id": "5522e024-f6dd-471e-a3e4-41d0a60a5d2f",
                  "kind": "topic",
                  "title": "Service Discovery",
                  "slug": "service-discovery"
                },
                {
                  "id": "84458963-012b-4a80-828a-2da27d8b509d",
                  "kind": "topic",
                  "title": "Service Mesh",
                  "slug": "service-mesh"
                },
                {
                  "id": "689dd587-de37-4e22-9412-bd42b118da79",
                  "kind": "topic",
                  "title": "Multi-Tenant Architecture",
                  "slug": "multi-tenant-architecture"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Novice comprehension disposition (T048)

SC-004 is **pending human review**. No actual novice trials were available in this execution.
Required evidence remains five opening trials spanning all four categories, at most
30 seconds per opening, with at least four trials demonstrating the ability to state the problem and
explain the analogy in their own words. Source review, AI/author review, and page word counts
do not establish this result. This pending tier is not an unfinished lesson or a missing
content file; it is a distinct acceptance dependency.

## Final Browser and Content Evidence (T046–T050)

The completed `contentFixture.checkAll()` run passed all 21 partials with 22 rendered SVG
diagrams and all 61 native recall items. All six hub layouts passed both themes, 360px
page-overflow checks, and actual A4 PDF generation with child labels retained. JSON and SQL
examples were verified as highlighted; section navigation worked. Lesson screen-layout evidence was retained; all 21 PDFs were subsequently regenerated
after final high-contrast diagram print styling, as recorded below.
[Final browser report](evidence/browser-final.json).

The final intrinsic report contains 24 passing checks over the actual manifest/content and
one explicit pending comparison because no pre-project catalog existed; separate replay and
rename/move baselines passed. The 39 focused unit tests also passed. The actual manifest validates against the
formal Draft 2020-12 schema. There are no unregistered HTML partials or regenerated
production identities. [Intrinsic report](evidence/intrinsic.json).

All four taxonomy steps are evidenced by the audit, automatic six-parent hub creation,
mirrored kebab-case paths and permanent IDs, and the complete bundle above. Every lesson
contains the full six-module story and sources; no lesson was replaced by a summary.
The fixture uses shared contract styling and does not implement a second persistence engine.

Content implementation and reference-fixture acceptance are complete. **Actual dashboard
integration and SC-004 novice comprehension remain pending**, as required by their explicit
disposition tasks. All 50 execution tasks are complete within that bounded scope; this
record does not claim the missing host or human acceptance results exist.

### Final Print Contrast Review

Visual inspection identified faint connectors when a dark-themed Mermaid diagram was
printed on a light page. Shared fixture print CSS now sets explicit dark text/connectors
and light node backgrounds for both SVG text and HTML-based Mermaid labels. All 21 PDFs
were regenerated and checked against the complete decoded source paragraphs: **630/630
paragraphs retained**, including every hidden mechanics and recall answer. Actual print
preparation/restoration was checked and test chrome is absent.
[Final print report](evidence/print-final.json).

The secondary project-prefix server was stopped after verification. The main local preview
is available at `http://127.0.0.1:8000/tests/fixtures/content-host.html`.
