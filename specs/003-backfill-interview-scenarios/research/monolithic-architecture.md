# Final Research: Monolithic Architecture

State: reviewed. Separate editorial/source pass completed 2026-11-17 for all six permanent scenario keys. Exact interview frequency remains unverified; adaptations are disclosed. Browser/print acceptance is recorded separately.

The JSON map records actual planning queries, implementation source checks (or explicit limitations), final selection/technical mappings and all eight per-card editorial dispositions. Vendor-specific sources are examples, not universal architectural guarantees.

```json
{
  "topicId": "1901acc7-9225-428a-9397-072cff3d36d0",
  "title": "Monolithic Architecture",
  "path": "topics/system-design/backend-architecture/core-system-topologies/monolithic-architecture.html",
  "constitutionVersion": "1.2.0",
  "researchedOn": "2026-11-17",
  "state": "reviewed",
  "searches": [
    {
      "query": "monolithic architecture production architecture tradeoffs official AWS Microsoft",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "monolithic architecture scale horizontally database shared deployment site:learn.microsoft.com",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "Monolithic Architecture interview scaling deployment tradeoffs official interview guidance",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Microsoft: Common web application architectures",
      "url": "https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S2",
      "title": "Google Cloud engineering: Making your monolith more reliable",
      "url": "https://cloud.google.com/blog/products/management-tools/sre-for-single-tiered-software-applications",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S3",
      "title": "AWS: Strangler fig pattern",
      "url": "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    }
  ],
  "scenarios": [
    {
      "key": "interview-small-team-launch-boundary",
      "theme": "Four engineers have two weeks to launch. Should you begin with independently deployed services?",
      "basis": "adapted-production",
      "selectionSources": [
        "S1"
      ],
      "technicalSources": [
        "S1"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Monolithic Architecture: Four engineers have two weeks to launch. Should you begin with independently deployed services?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Four engineers have two weeks to launch. Should you begin with independently deployed services? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Think of one workshop with labeled benches instead of renting a building for each tool. Four engineers must deliver ordering, billing and support in two weeks, with no dedicated operations team. Load is modest and most changes cross these capabilities. What deployment topology will you choose and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Start with a single deployable application and clear internal responsibility boundaries. Keep order and billing rules in named modules, use explicit interfaces and a transaction-capable data store where needed, and build one repeatable deployment with health checks, backups and rollback. The deadline favors fewer operational moving parts.\n\nWrite down the conditions that would justify extraction later: a measured scaling hotspot, a durable independent ownership boundary or a regulatory isolation requirement. Add observability by capability now so future choices have evidence. A single deployment need not mean every class can access every table."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain fast local development, simpler transactions and one operational path; you accept shared resource and release boundaries. A small number of services is a viable alternative if an existing platform team already makes deployment, tracing and recovery routine.\n\nFollow-up trap: saying a monolith cannot scale confuses deployment topology with capacity. If one capability must run in a separately controlled environment from day one, that isolation requirement outweighs the launch convenience. Keep the remaining cohesive work together rather than automatically splitting every noun into a service."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain fast local development, simpler transactions and one operational path; you accept shared resource and release boundaries. A small number of services is a viable alternative if an existing platform team already makes deployment, tracing and recovery routine.\n\nFollow-up trap: saying a monolith cannot scale confuses deployment topology with capacity. If one capability must run in a separately controlled environment from day one, that isolation requirement outweighs the launch convenience. Keep the remaining cohesive work together rather than automatically splitting every noun into a service."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S1 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-same-rps-expensive-writes",
      "theme": "Request count is flat, yet latency doubled after a write-heavy release. Do you add more application replicas?",
      "basis": "adapted-production",
      "selectionSources": [
        "S1",
        "S2"
      ],
      "technicalSources": [
        "S1",
        "S2"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Monolithic Architecture: Request count is flat, yet latency doubled after a write-heavy release. Do you add more application replicas?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Request count is flat, yet latency doubled after a write-heavy release. Do you add more application replicas? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A restaurant serving the same number of customers can still slow down if every order becomes elaborate. Your monolith handles the same requests per second, but a release replaces cached reads with transactional writes. Database waits and p99 latency jump. The release has a 300ms response target. What will you investigate first and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Compare work per request before scaling the application. Trace changed endpoints, query plans, lock waits, transaction duration and connection-pool queues; segment read and write latency rather than relying on average CPU. Reproduce the new write mix under a realistic load test and roll back the release if its regression is clearly responsible.\n\nShorten transactions, remove redundant queries and index the actual access path before adding replicas that compete for the same database. Bound database connections across the whole fleet. Recheck correctness after batching or caching changes: neither should bypass the business rule that made the write necessary."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You target the constrained resource and avoid buying idle application CPU, but diagnosis takes measurement and a rollback may delay functionality. Additional application replicas are an alternative when profiling shows application CPU is the bottleneck and the data tier has headroom.\n\nFollow-up trap: unchanged request count does not imply unchanged workload. If the database remains healthy while encryption or serialization now dominates CPU, scale or optimize the application instead. Make the decision from resource demand and tail latency, not from the word monolith."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You target the constrained resource and avoid buying idle application CPU, but diagnosis takes measurement and a rollback may delay functionality. Additional application replicas are an alternative when profiling shows application CPU is the bottleneck and the data tier has headroom.\n\nFollow-up trap: unchanged request count does not imply unchanged workload. If the database remains healthy while encryption or serialization now dominates CPU, scale or optimize the application instead. Make the decision from resource demand and tail latency, not from the word monolith."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S1, S2 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-reporting-exhausts-checkout",
      "theme": "A reporting feature consumes all worker threads and checkout fails. How do you contain it inside a monolith?",
      "basis": "adapted-production",
      "selectionSources": [
        "S2"
      ],
      "technicalSources": [
        "S2"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Monolithic Architecture: A reporting feature consumes all worker threads and checkout fails. How do you contain it inside a monolith?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A reporting feature consumes all worker threads and checkout fails. How do you contain it inside a monolith? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "One noisy room can consume a shared building's electricity. An export endpoint launches long reports in the same process and connection pool as checkout. During business hours, checkout times out even though its own code has not changed. You need a same-day containment fix. What will you do and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Disable or throttle the expensive feature immediately, then assign it bounded concurrency, time limits and a bounded queue separate from latency-sensitive requests. Reserve sufficient database and worker capacity for checkout, cancel abandoned work where supported, and reject additional exports predictably instead of retaining unlimited jobs.\n\nMove truly long reports to a controlled background worker using a durable job identity, and expose job status rather than holding an HTTP request open. Observe queues and database contention separately; thread isolation alone does not isolate a shared disk or database. Load-test export traffic alongside checkout."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You restore priority isolation quickly without a system rewrite, but users wait for exports and share some remaining failure domains. Extracting reporting into a separately scaled process is an alternative when sustained demand or crash isolation justifies the operational cost.\n\nFollow-up trap: putting work on an unbounded in-memory queue merely moves the overload. If reports must read a consistent historical snapshot, choose a reporting replica or snapshot pipeline with explicit freshness semantics instead of letting arbitrary analytical queries compete with transactional writes."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You restore priority isolation quickly without a system rewrite, but users wait for exports and share some remaining failure domains. Extracting reporting into a separately scaled process is an alternative when sustained demand or crash isolation justifies the operational cost.\n\nFollow-up trap: putting work on an unbounded in-memory queue merely moves the overload. If reports must read a consistent historical snapshot, choose a reporting replica or snapshot pipeline with explicit freshness semantics instead of letting arbitrary analytical queries compete with transactional writes."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S2 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-shared-artifact-safe-releases",
      "theme": "Five teams ship one artifact. How do you release and roll back without disabling every team's work?",
      "basis": "adapted-production",
      "selectionSources": [
        "S1",
        "S2"
      ],
      "technicalSources": [
        "S1",
        "S2"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Monolithic Architecture: Five teams ship one artifact. How do you release and roll back without disabling every team's work?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Five teams ship one artifact. How do you release and roll back without disabling every team's work? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A shared train can still have a timetable and guarded boarding. Five teams change one monolith, and a bad billing release causes a whole-application rollback that also removes a working support feature. You must improve release safety this month without creating five services. What will you change and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Keep a reproducible artifact, require capability ownership and targeted plus integration checks, and deploy incrementally with observable health gates. Use independently controlled feature flags for risky behavior so a feature can be disabled without immediately reverting unrelated code. Exercise the old and new paths before release.\n\nDesign database changes with an expand-and-contract sequence: add compatible structures first, transition readers/writers, and remove old structures only after the rollback window closes. Record which artifact and flags are active. Test rollback against the deployed schema rather than assuming reverting application code reverses data migration."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You reduce blast radius and coordinate releases without immediate service extraction, but own flag lifecycle, compatibility tests and a shared deployment train. Separate deployables are an alternative when teams have genuinely independent contracts and persistent release contention.\n\nFollow-up trap: a feature flag cannot safely undo a destructive schema change or an external payment effect. If a data migration is irreversible, plan a forward repair and reconciliation path before rollout. If regulatory change control requires independent artifacts, internal flags alone do not satisfy that requirement."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You reduce blast radius and coordinate releases without immediate service extraction, but own flag lifecycle, compatibility tests and a shared deployment train. Separate deployables are an alternative when teams have genuinely independent contracts and persistent release contention.\n\nFollow-up trap: a feature flag cannot safely undo a destructive schema change or an external payment effect. If a data migration is irreversible, plan a forward repair and reconciliation path before rollout. If regulatory change control requires independent artifacts, internal flags alone do not satisfy that requirement."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S1, S2 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-replicas-do-not-fix-database",
      "theme": "You doubled monolith replicas but throughput stayed flat. Why is the database getting worse?",
      "basis": "adapted-production",
      "selectionSources": [
        "S1",
        "S2"
      ],
      "technicalSources": [
        "S1",
        "S2"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Monolithic Architecture: You doubled monolith replicas but throughput stayed flat. Why is the database getting worse?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: You doubled monolith replicas but throughput stayed flat. Why is the database getting worse? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "More cashiers do not help when there is only one slow stock ledger. Application replicas grow from four to eight, but the database is saturated, lock waits rise and total connections double. Checkout throughput barely moves. What architecture or capacity change will you make and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Stop increasing callers until you identify the data-tier limit. Measure transaction contention, query cost, I/O and connection waits. Apply a fleet-wide connection/concurrency budget, optimize hot queries and reduce unnecessarily broad transactions. Check whether a single hot row serializes the real business operation.\n\nSeparate read and write demand: cache safe reads or route them to replicas only where stale data is acceptable, while authoritative writes still enforce invariants. Consider partitioning data along a real access boundary only after a simpler indexing, vertical-capacity or workload-isolation fix is evaluated. Retest with the expected request mix."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You improve useful database capacity and protect recovery, but introduce cache freshness or operational partitioning costs if those measures are selected. Vertical database scaling is a viable near-term alternative when the workload fits its limits and cost is acceptable.\n\nFollow-up trap: turning code into microservices while retaining the same contended tables does not remove the bottleneck. If profiling instead shows a stateless CPU-heavy image transformation, a separately scaled worker may isolate it cleanly. Choose a boundary that owns the constrained work, not a distribution exercise around the same ledger."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You improve useful database capacity and protect recovery, but introduce cache freshness or operational partitioning costs if those measures are selected. Vertical database scaling is a viable near-term alternative when the workload fits its limits and cost is acceptable.\n\nFollow-up trap: turning code into microservices while retaining the same contended tables does not remove the bottleneck. If profiling instead shows a stateless CPU-heavy image transformation, a separately scaled worker may isolate it cleanly. Choose a boundary that owns the constrained work, not a distribution exercise around the same ledger."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S1, S2 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-extract-one-capability-gradually",
      "theme": "Only image processing needs independent scaling. How do you extract it without rewriting the whole monolith?",
      "basis": "adapted-production",
      "selectionSources": [
        "S3"
      ],
      "technicalSources": [
        "S3"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Monolithic Architecture: Only image processing needs independent scaling. How do you extract it without rewriting the whole monolith?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Only image processing needs independent scaling. How do you extract it without rewriting the whole monolith? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "You can open a specialist workshop while the original shop keeps serving customers. Image conversion consumes bursty CPU, while ordering and billing remain cohesive. A full rewrite would take a year and cannot interrupt existing clients. What migration sequence will you choose and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Use an incremental strangler boundary around image processing. Define an explicit request/job contract, place routing or an adapter at the old entry point, and move conversion behind that contract while the monolith continues handling other work. Start with a small traffic slice and compare outputs, latency and failure behavior.\n\nGive jobs stable identities and make duplicate processing safe before retrying across the new network boundary. Decide who owns image metadata and avoid uncontrolled dual writes. Retain a rollback route during the transition, observe both paths and remove the old implementation only when the new path proves operationally independent."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain independent scaling and incremental risk control at the cost of routing, compatibility and a temporary two-path system. Keeping conversion as a separate worker of the same application is a viable cheaper alternative if independent business ownership is unnecessary.\n\nFollow-up trap: a network wrapper around a function that still writes private shared tables is not full ownership isolation. If the dependency graph reveals that conversion cannot be separated without many synchronous callbacks, first simplify the internal boundary. A measured extraction can pause without forcing a rewrite of the working core."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain independent scaling and incremental risk control at the cost of routing, compatibility and a temporary two-path system. Keeping conversion as a separate worker of the same application is a viable cheaper alternative if independent business ownership is unnecessary.\n\nFollow-up trap: a network wrapper around a function that still writes private shared tables is not full ownership isolation. If the dependency graph reveals that conversion cannot be separated without many synchronous callbacks, first simplify the internal boundary. A measured extraction can pause without forcing a rewrite of the working core."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S3 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    }
  ],
  "publicDisclosure": "Researched 2026-11-17. These scenarios adapt documented production problems and architectural guidance. Interview frequency, rankings and company provenance for these exact prompts were not independently verified. Numeric budgets and organization details are author-created assumptions. Web search was available and used for this concept; primary sources support the technical reasoning, not a claim that these prompts recur in interviews.",
  "sourceNoteUrls": [
    "https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures",
    "https://cloud.google.com/blog/products/management-tools/sre-for-single-tiered-software-applications",
    "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html"
  ],
  "editorialReviewedOn": "2026-11-17"
}
```
