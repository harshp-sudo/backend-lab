# Concept-Specific Research Seeds

**Researched**: 2026-11-17 | **Scope**: all 15 existing lessons

Web search was available and used separately for every concept below. These are six candidate production themes per lesson (90 planning seeds), not authored questions, complete answers, or final card identities. Implementation must select five to seven distinct scenarios per lesson, assign stable keys once, map individual claims to the relevant sources, and recheck version-sensitive guidance when writing the answers.

**Evidence classification for every seed below: adapted production variant. Interview frequency, rankings, and company-specific provenance for the exact prompts were not independently verified.** Search found technical guidance and preparation material, but those are not evidence that an exact prompt recurs in hiring interviews. Limited interview evidence must be disclosed in each lesson's associated research note. No browsing-unavailable claim is appropriate for this research pass.

[Amazon's official preparation guidance](https://www.amazon.jobs/content/en/how-we-hire/interview-prep/software-development-topics) supports applied system-design/distributed-computing preparation broadly; it does not validate a ranked list of these prompts. Expert/author discussions encountered during searches likewise do not establish hiring-interview recurrence.

The query strings below record searches actually performed by the three planning research agents. Source links are primary technical references. Original company engineering accounts describe production experience, not verified hiring questions. Vendor-specific APIs, defaults and transaction mechanisms must remain labeled as examples rather than universal architectural properties.

## Distributed System Fundamentals

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `distributed systems system design interview production retries idempotency timeouts Amazon Builders Library`
- `Distributed System Fundamentals interview consistency partition idempotency site:amazon.jobs`
- `Distributed System Fundamentals partition replication consistency site:allthingsdistributed.com Dynamo`

**Primary technical sources**:

1. [AWS: Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
2. [AWS: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
3. [Original Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

**Candidate constraints/decisions**:

1. Payment timeout after an uncertain commit; prevent a second charge.
2. Retries at three dependency layers amplify an overload; protect recovery.
3. A regional partition separates cart updates from strict stock allocation.
4. An immediate post-update read sees stale profile data; choose its guarantee.
5. Disconnected clients edit the same record; define conflict assumptions.
6. A slow replica appears failed; distinguish suspicion from certainty.

## Monolithic Architecture

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `monolithic architecture production architecture tradeoffs official AWS Microsoft`
- `monolithic architecture scale horizontally database shared deployment site:learn.microsoft.com`
- `Monolithic Architecture interview scaling deployment tradeoffs official interview guidance`

**Primary technical sources**:

1. [Microsoft: Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)
2. [Google Cloud engineering: Making your monolith more reliable](https://cloud.google.com/blog/products/management-tools/sre-for-single-tiered-software-applications)
3. [AWS: Strangler fig pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html)

**Candidate constraints/decisions**:

1. A small team has a two-week launch deadline and limited operations capacity.
2. Request volume is unchanged but expensive writes replace cheap reads.
3. A low-priority feature exhausts shared threads and harms checkout.
4. Several teams share one artifact and need safe release/rollback ownership.
5. Application replicas increase but the database remains saturated.
6. One capability needs independent release/scaling; extract incrementally.

## Modular Monolith

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `modular monolith architecture production boundaries Shopify engineering`
- `modular monolith Spring Modulith verifying module boundaries events site:docs.spring.io`
- `Modular Monolith interview module boundaries transactions production site:spring.io`

**Primary technical sources**:

1. [Shopify: Deconstructing the Monolith](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity)
2. [Shopify: Under Deconstruction](https://shopify.engineering/shopify-monolith)
3. [Spring Modulith: Verifying Application Module Structure](https://docs.spring.io/spring-modulith/reference/verification.html)
4. [Spring Modulith: Working with Application Events](https://docs.spring.io/spring-modulith/reference/events.html)

**Candidate constraints/decisions**:

1. Developers bypass module APIs and read private internals.
2. Order, billing and inventory responsibilities form a dependency cycle.
3. Two modules must uphold one immediate business invariant.
4. A noncritical event listener fails after the main transaction commits.
5. A shared common package collects business rules owned by every team.
6. A module is considered for extraction despite hidden data coupling.

## Service-Oriented Architecture (SOA)

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `service oriented architecture SOA enterprise service bus orchestration tradeoffs site:aws.amazon.com`
- `Service Oriented Architecture SOA interview enterprise service bus versioning site:aws.amazon.com`
- `Service Oriented Architecture SOA enterprise integration contracts versioning site:docs.oasis-open.org soa`

**Primary technical sources**:

1. [OASIS: SOA Reference Model 1.0](https://docs.oasis-open.org/soa-rm/v1.0/soa-rm.html)
2. [AWS: What is SOA?](https://aws.amazon.com/what-is/service-oriented-architecture/)
3. [AWS: What is an enterprise service bus?](https://aws.amazon.com/what-is/enterprise-service-bus/)
4. [AWS: Saga orchestration pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-orchestration.html)

**Candidate constraints/decisions**:

1. ERP, CRM and shipping systems expose incompatible contracts.
2. A central integration bus becomes a bottleneck and outage amplifier.
3. Consumers cannot upgrade together when a shared service changes.
4. An independently owned workflow includes long human delays.
5. Business rules accumulate in orchestration/transformation middleware.
6. A canonical enterprise model forces coordinated changes across teams.

## Microservices Architecture

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `microservices architecture service boundaries distributed transactions testing tradeoffs site:learn.microsoft.com`
- `Microservices Architecture interview design service boundaries consistency failures site:amazon.jobs`

**Primary technical sources**:

1. [Microsoft: Microservices architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices)
2. [Microsoft: Identify microservice boundaries](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/microservice-boundaries)
3. [Microsoft: Design patterns for microservices](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/patterns)
4. [AWS: Saga orchestration pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-orchestration.html)

**Candidate constraints/decisions**:

1. Two services require coordinated releases for every ordinary change.
2. Checkout crosses synchronous dependencies and exceeds its latency budget.
3. Order, payment and stock commit independently; recover from partial success.
4. Teams share writable database tables to simplify reporting.
5. A failed downstream service exhausts upstream resources.
6. Service count outgrows a small operations team's capacity.

## Layered Architecture

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `site.learn.microsoft.com architecture n-tier architecture style bypass middle tier latency`
- `"layered architecture" "interview" production constraints`

**Primary technical sources**:

1. [Microsoft: N-tier architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier)
2. [Microsoft: Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)
3. [Microsoft: EF Core transactions (implementation-specific example)](https://learn.microsoft.com/en-us/ef/core/saving/transactions)

**Candidate constraints/decisions**:

1. Mostly pass-through layers add six network hops to simple CRUD.
2. A direct-database endpoint bypasses pricing validation used by batch jobs.
3. The team mistakes logical layers for mandatory separate servers.
4. Upper layers depend on query builders during a storage migration.
5. Two repository writes partially succeed; decide transaction ownership.
6. Fake-based tests pass while actual infrastructure violates assumptions.

## Clean Architecture

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `site.blog.cleancoder.com clean architecture database interface framework`
- `"clean architecture" "interview" database transactions`

**Primary technical sources**:

1. [Robert C. Martin: The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
2. [Microsoft: Common web application architectures](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)
3. [Microsoft: EF Core transactions (implementation-specific example)](https://learn.microsoft.com/en-us/ef/core/saving/transactions)

**Candidate constraints/decisions**:

1. Domain tests require a real web request/framework context.
2. An inner storage interface exposes ORM types and provider exceptions.
3. A use case requires atomic multi-write behavior without infrastructure imports.
4. Runtime execution goes outward while source dependencies must point inward.
5. A short-deadline CRUD change acquires mandatory projects/interfaces everywhere.
6. HTTP and scheduled jobs must reuse one policy-bearing use case.

## Hexagonal Architecture

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `site.alistair.cockburn.us hexagonal architecture ports adapters`
- `"hexagonal architecture" "interview" testing adapters`

**Primary technical sources**:

1. [Alistair Cockburn: Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture)
2. [Alistair Cockburn: Component + Strategy / Ports and Adapters revisited](https://alistaircockburn.com/Component%20plus%20strategy.pdf)

**Candidate constraints/decisions**:

1. REST and nightly CSV entry points must apply identical rules.
2. A third-party call times out after a possible committed effect.
3. An in-memory adapter passes while real storage breaks its contract.
4. An SDK upgrade changes provider models and exception types.
5. A proposed port-per-class design grows abstraction ceremony.
6. Two compatible application modules might not need an extra adapter.

## Domain-Driven Design (DDD)

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `site.martinfowler.com bounded context domain driven design`
- `"domain driven design" "interview" aggregates consistency`
- `site.learn.microsoft.com domain driven design aggregates transaction bounded contexts`

**Primary technical sources**:

1. [Martin Fowler: Bounded Context](https://martinfowler.com/bliki/BoundedContext.html)
2. [Microsoft: Design a microservice domain model](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model)
3. [Microsoft: Domain analysis](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis)
4. [Microsoft: Anti-Corruption Layer](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer)

**Candidate constraints/decisions**:

1. Billing and Support use incompatible meanings for Customer.
2. Concurrent purchases oversell the final available unit.
3. A giant aggregate causes unnecessary contention.
4. A workflow crosses independently owned aggregate/service boundaries.
5. A legacy ERP model contaminates the new domain vocabulary.
6. Simple CRUD is burdened with elaborate tactical DDD patterns.

## Event-Driven Architecture

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `"event driven architecture" interview duplicate messages ordering constraints`
- `site.learn.microsoft.com event driven architecture style event ordering idempotent`

**Primary technical sources**:

1. [Microsoft: Event-driven architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven)
2. [Martin Fowler: What do you mean by Event-Driven?](https://martinfowler.com/articles/201701-event-driven.html)
3. [AWS: Transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

**Candidate constraints/decisions**:

1. A database commit succeeds but event publication fails.
2. Duplicate delivery repeats an externally visible side effect.
3. Events for one entity arrive out of order.
4. Consumer lag makes a user-facing projection stale.
5. ID-only notifications require expensive callbacks to the producer.
6. An apparent event secretly commands another service's workflow.

## API Gateway Pattern

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `"API Gateway" interview production scenario system design trade offs`
- `site.learn.microsoft.com azure architecture api gateway pattern aggregation gateway failure throttling`

**Primary technical sources**:

1. [Microsoft: API gateways](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/gateway)
2. [Microsoft: Gateway aggregation](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation)

**Candidate constraints/decisions**:

1. A mobile screen needs several services within a tight latency budget.
2. An optional dependency times out while essential order data succeeds.
3. Gateway replicas need a shared quota without excessive coordination.
4. Edge authentication succeeds but object authorization belongs downstream.
5. Domain orchestration accumulates inside gateway policy configuration.
6. An edge deployment affects otherwise healthy backend capabilities.

## Backend for Frontend (BFF)

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `"Backend for Frontend" interview questions scenario`
- `"Backend for Frontend" interview "scenario" mobile web`
- `site.samnewman.io patterns architectural bff backends for frontends`

**Primary technical sources**:

1. [Sam Newman: Backends For Frontends](https://samnewman.io/patterns/architectural/bff/)
2. [Microsoft: Backends for Frontends](https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends)

**Candidate constraints/decisions**:

1. Mobile bandwidth and desktop functionality require different experiences.
2. Android/iOS share behavior but have different team ownership.
3. Duplicated aggregation competes with shared-library release coupling.
4. Authoritative business rules drift between experience backends.
5. An old mobile client must keep its contract for several months.
6. A simple single frontend might not justify another deployment boundary.

## Service Discovery

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `site.kubernetes.io service discovery dns service endpoints distributed service discovery`
- `"Service Discovery" interview stale DNS health checks scenario`
- `site.kubernetes.io docs dns pods services readiness terminating endpoints`
- `site.consul.io docs discovery health checks DNS caching stale reads service discovery`

**Primary technical sources**:

1. [Kubernetes: Service](https://kubernetes.io/docs/concepts/services-networking/service/)
2. [Kubernetes: Pod and endpoint termination flow](https://kubernetes.io/docs/tutorials/services/pods-and-endpoint-termination-flow/)
3. [HashiCorp: Configure Consul DNS behavior](https://developer.hashicorp.com/consul/docs/discover/dns/configure)

**Candidate constraints/decisions**:

1. Requests reach terminating instances during deployment.
2. A registered service remains unavailable because of negative DNS caching.
3. Available registry reads are stale during a control-plane disruption.
4. A headless service returns addresses without choosing an endpoint.
5. The same service name resolves differently across namespaces.
6. A VM client must discover services without adopting a discovery SDK.

## Service Mesh

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `"Service Mesh" interview production mTLS retries sidecar`
- `site.istio.io latest docs concepts traffic management retries security mutual TLS`

**Primary technical sources**:

1. [Istio: Traffic management](https://istio.io/latest/docs/concepts/traffic-management/)
2. [Istio: Security](https://istio.io/latest/docs/concepts/security/)
3. [Istio: Sidecar or ambient?](https://istio.io/latest/docs/overview/dataplane-modes/)

**Candidate constraints/decisions**:

1. Proxy and application retries multiply downstream load.
2. Strict mutual TLS breaks legacy callers during migration.
3. Encrypted authenticated traffic still reaches unauthorized operations.
4. Latency/memory budgets constrain the choice of data-plane mode.
5. A small canary receives unexpected traffic.
6. Mesh resilience cannot supply the application's business fallback.

## Multi-Tenant Architecture

**Selection basis**: adapted production; exact interview frequency not independently verified.

**Queries performed**:

- `"Multi-Tenant Architecture" interview production tenant isolation noisy neighbor`
- `site.learn.microsoft.com azure architecture multitenant noisy neighbor isolation tenancy models`
- `site.learn.microsoft.com multitenant noisy neighbor antipattern tenant migration database`

**Primary technical sources**:

1. [Microsoft: Tenancy models](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models)
2. [Microsoft: Multitenant storage/data approaches](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data)
3. [Microsoft: Multitenancy and Azure SQL Database](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/sql-database)
4. [Microsoft: Noisy Neighbor antipattern](https://learn.microsoft.com/en-gb/azure/architecture/antipatterns/noisy-neighbor/noisy-neighbor)

**Candidate constraints/decisions**:

1. One tenant degrades everyone else's latency.
2. An enterprise customer needs stronger resource isolation.
3. A query/cache omits the tenant identity.
4. A tenant needs independent restore or regional data placement.
5. A large tenant must move with minimal interruption.
6. Per-tenant customizations multiply storage/operational complexity.

## Authoring handoff

For each lesson, create its final research record using [the evidence contract](../contracts/research-and-review.md). Preserve the distinction between scenario-selection support and technical-correctness support. Fresh numeric budgets or organizational constraints are author-created scenario assumptions unless a cited original source establishes them. No new lesson content or interview-frequency claim is approved merely by this seed list.
