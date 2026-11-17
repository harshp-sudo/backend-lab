# Research: Backend Architecture Learning Batch

**Date**: 2026-11-17
**Scope**: Resolve the Technical Context questions in [plan.md](plan.md). Research is
complete; the absent dashboard is a known integration dependency, not an undecided design.

## 1. Content Scope and Host Readiness

**Decision**: Deliver one manifest, 15 complete lesson partials, six hub partials, and focused
validation tooling during implementation. Define the host interface now; do not build the
dashboard, persistence engine, or deployment in this feature.

**Rationale**: Repository inspection found no manifest, topics, dashboard, or package manifest.
The [specification](spec.md) explicitly limits this batch to content and integration contracts.
A small test-only canvas can demonstrate the contract without claiming dashboard acceptance.

**Alternatives considered**: Building the entire application would expand scope. Pretending
the missing dashboard already works would misrepresent acceptance. Waiting for it would
unnecessarily prevent content authoring and intrinsic validation.

## 2. Recursive Manifest and Derived Locations

**Decision**: Use `{schemaVersion: 1, roots: [...]}`. Nodes contain `id`, `kind`, `title`,
`slug`, and hub-only `children`. Derive route, breadcrumb ancestry, and content location
from the same tree; do not store a second route index or redundant parent/path fields.
Child array order is navigation order. Hubs must contain at least one child when published.

**Rationale**: One recursive structure prevents navigation and filesystem maps from drifting.
JSON Schema 2020-12 supports recursive definitions through `$defs` and `$ref`.
[JSON Schema Core](https://json-schema.org/draft/2020-12/json-schema-core#section-8.2.4)

**Alternatives considered**: Separate indexes, fixed-depth models, and stored `parentId` plus
`route` plus `contentPath` introduce avoidable synchronization work. Empty published hubs
would be unfinished roadmap placeholders. Unknown optional metadata remains permitted and
must be preserved when merging an existing catalog.

## 3. Permanent Identity and Safe Merges

**Decision**: Mint a lowercase UUIDv4 once for each newly created node. Preserve existing
identities, including legacy opaque IDs encountered in a later audit. Keep the manifest as
the durable identity registry; never derive IDs from a mutable name or path.

**Rationale**: Python's `uuid4()` produces random UUIDs independent of taxonomy. Reusing IDs
allows host-owned progress to survive a rename or move.
[Python UUID documentation](https://docs.python.org/3.10/library/uuid.html)

**Alternatives considered**: Slug IDs and path-derived UUIDv5 values couple identity to
placement. A separate registry duplicates the catalog. A strict UUID-only schema would
encourage replacing legitimate existing IDs, so the schema accepts nonempty opaque IDs;
new-ID format and historical preservation are additional traversal checks.

Read the entire existing tree, align by permanent identity and conceptual meaning, and
preserve unrelated children and optional metadata. Synonyms require author judgment; string
matching alone cannot prove conceptual identity. Resolve occupied paths before writing.

## 4. Script-Free Partials and Native Disclosures

**Decision**: Use one semantic article per partial, stable node/recall identifiers, six
ordered lesson sections, and native `<details>` for mechanics and recall answers. Keep
scripts, stylesheets, routing, and storage outside lesson files. Hubs are lightweight
orientation articles and do not require the six lesson modules.

**Rationale**: Native disclosures provide useful interaction without per-topic JavaScript.
Recall answers omit `open` and shared `name` attributes: `open` is a Boolean attribute, and
named disclosure groups can force exclusive opening.
[HTML Standard: details](https://html.spec.whatwg.org/multipage/interactive-elements.html#the-details-element)

**Alternatives considered**: Custom card-flipping scripts, Alpine instances per lesson, and
embedded CSS would increase authoring and integration work. Native details satisfy the
specification's reveal-or-flip requirement with fewer dependencies.

## 5. Rendering, Themes, and Printing

**Decision**: The host renders newly mounted Mermaid blocks with `mermaid.run`, highlights
code through `hljs.highlightElement`, and owns shared semantic CSS. The test-only browser
profile pins Mermaid **12.3.0** and Highlight.js **11.11.1**; partials import neither.
These are verified release baselines, not floating latest-version requirements.
[Mermaid release](https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.3.0),
[Highlight.js release](https://github.com/highlightjs/highlight.js/releases/tag/11.11.1)

**Rationale**: Dynamic mounting requires explicit rendering after insertion. Keep original
diagram text for theme rerenders, use strict Mermaid security, and place ordinary navigation
links outside diagrams. The selected browser profile requires no local Node runtime; Mermaid's
current npm tooling requires Node 22.12+, whereas this workspace has Node 20.19.4.
[Mermaid usage](https://mermaid.js.org/config/usage.html),
[Highlight.js API](https://highlightjs.readthedocs.io/en/latest/api.html)

Before printing, the host opens disclosures and records their previous state; afterward it
restores them. Print-media CSS alone is not evidence that this lifecycle ran.
[MDN printing guide](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Printing)

**Alternatives considered**: Automatic page-load-only rendering misses injected lessons.
Per-partial library imports and floating CDN versions make behavior harder to reproduce.
Relying on closed disclosures to print consistently is insufficient for complete PDFs.

## 6. Location Grammar and Hosting Base

**Decision**: Derive logical routes as `/` plus ancestor slugs with no trailing slash.
Use `#/system-design/...` links for content navigation and a `?section=` suffix for
within-lesson anchors. Resolve manifest and content requests relative to the configured
application base, including when hosted below `/backend-lab/`.

**Rationale**: Both root and project-subpath hosting can use identical partials. A single
hash-route grammar avoids collisions between content navigation and local section links.
The host uses the platform URL API for resolution.
[MDN URL constructor](https://developer.mozilla.org/en-US/docs/Web/API/URL/URL)

**Alternatives considered**: Hard-coded origin-root fetches break project-subpath hosting.
Plain `#section` anchors would replace the content route unless given a separate grammar.
History-based routes would require server fallback behavior outside this static batch.

## 7. Validation Without a Production Build

**Decision**: Plan a Python 3.10-compatible standard-library validator and focused negative
fixture tests. Use a browser-only mount fixture for rendered diagrams and reading layouts.
Keep actual dashboard acceptance and human comprehension trials separately reported.

**Rationale**: JSON, UUID, paths, and HTML structure are inspectable without production
dependencies. Reject repeated JSON keys; check resolved filesystem containment rather than
string prefixes. `HTMLParser` is a parser, not a standards-conformance or teaching-quality
validator; browser and editorial reviews remain necessary.
[Python JSON decoder](https://docs.python.org/3.10/library/json.html#repeated-names-within-an-object),
[Path resolution](https://docs.python.org/3.10/library/pathlib.html#pathlib.Path.resolve),
[HTMLParser](https://docs.python.org/3.10/library/html.parser.html)

The formal JSON Schema documents interface shape; the validator implements this small
contract directly rather than attempting to implement a general schema engine. Global ID
uniqueness, cross-file links, and immutability against a baseline require traversal beyond
ordinary array validation.
[JSON Schema Validation](https://json-schema.org/draft/2020-12/json-schema-validation)

**Alternatives considered**: A frontend build and browser-download requirement would add
unnecessary setup. Static token checks cannot prove diagram rendering or analogy fidelity.
A fixture cannot prove the real dashboard's persistence or navigation implementation.

## 8. Primary Sources for Lesson Authoring

**Decision**: Teach definitions from original authors, standards, or first-party architecture
documentation. Label vendor implementations as examples and recheck changing product claims
during implementation. The table is an authoring source map, not finished lesson content.

**Rationale**: The categories describe complementary learning dimensions, not a universal
architecture maturity ladder. Each lesson needs contextual comparisons and accurate failure
stories. **Alternatives considered**: Generic comparison blogs or framework tutorials alone
are insufficient as the definition of an architectural concept.

| Topic | Primary source | Editorial focus |
| --- | --- | --- |
| Distributed System Fundamentals | [AWS Builders' Library](https://aws.amazon.com/builders-library/challenges-with-distributed-systems/) | Partial failures, uncertain outcomes, and latency; distribution is not automatic resilience. |
| Monolithic Architecture | [Fowler: Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) | Deployment boundary and contextual costs; avoid universal prescriptions. |
| Modular Monolith | [Spring Modulith fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html) | Module APIs and dependency boundaries; Spring is an example. |
| Service-Oriented Architecture (SOA) | [OASIS reference model](https://docs.oasis-open.org/soa-rm/v1.0/soa-rm.html) | Contracts and capabilities; avoid defining SOA as mandatory SOAP or an ESB. |
| Microservices Architecture | [Lewis and Fowler](https://martinfowler.com/articles/microservices.html) | Independent deployment, capabilities, and operational costs; size alone is insufficient. |
| Layered Architecture | [Microsoft N-tier guidance](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier) | Distinguish logical layers from physical tiers. |
| Clean Architecture | [Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) | Dependency direction versus runtime control flow. |
| Hexagonal Architecture | [Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture) | Ports, adapters, and inside/outside boundaries; not six mandatory ports. |
| Domain-Driven Design (DDD) | [Microsoft domain analysis](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis), [Evans reference](https://www.domainlanguage.com/ddd/reference/) | Strategic modeling before tactical patterns; DDD does not require distribution. |
| Event-Driven Architecture | [Microsoft architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven) | Events versus commands, duplicates, ordering, and consistency conditions. |
| API Gateway Pattern | [Richardson's pattern](https://microservices.io/patterns/apigateway.html) | Routing/composition benefits and an added operational dependency. |
| Backend for Frontend (BFF) | [Sam Newman](https://samnewman.io/patterns/architectural/bff/) | Client-specific needs and ownership versus maintenance costs. |
| Service Discovery | [Richardson's pattern](https://microservices.io/patterns/client-side-discovery.html), [Kubernetes DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) | Resolution versus instance selection; Kubernetes is an example. |
| Service Mesh | [Istio overview](https://istio.io/latest/docs/overview/what-is-istio/), [data-plane modes](https://istio.io/latest/docs/overview/dataplane-modes/) | Control/data planes; meshes need not always use per-service sidecars. |
| Multi-Tenant Architecture | [Microsoft guidance](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/overview) | Tenant/user distinction, isolation choices, and noisy neighbors. |

The Evans page was discoverable but returned HTTP 403 during research; use the accessible
first-party alternative and do not claim to have inspected inaccessible full text. Cross-topic
review must avoid treating deployment shape, code organization, communication, and operational
infrastructure as mutually exclusive alternatives.

## Research Closure

All Technical Context questions are resolved by decisions 1–8. No clarification marker
remains. Dashboard readiness is explicitly **pending integration**; browser rendering and
learner trials are future acceptance work, not results of this planning phase.
