# Final Research: API Gateway Pattern

State: reviewed. Separate editorial/source pass completed 2026-11-17 for all six permanent scenario keys. Exact interview frequency remains unverified; adaptations are disclosed. Browser/print acceptance is recorded separately.

The JSON map records actual planning queries, implementation source checks (or explicit limitations), final selection/technical mappings and all eight per-card editorial dispositions. Vendor-specific sources are examples, not universal architectural guarantees.

```json
{
  "topicId": "a5b7beee-bdbd-4987-9a41-8e16471b0a32",
  "title": "API Gateway Pattern",
  "path": "topics/system-design/backend-architecture/communication-and-routing/api-gateway-pattern.html",
  "constitutionVersion": "1.2.0",
  "researchedOn": "2026-11-17",
  "state": "reviewed",
  "searches": [
    {
      "query": "\"API Gateway\" interview production scenario system design trade offs",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "site.learn.microsoft.com azure architecture api gateway pattern aggregation gateway failure throttling",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Microsoft: API gateways",
      "url": "https://learn.microsoft.com/en-us/azure/architecture/microservices/design/gateway",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S2",
      "title": "Microsoft: Gateway aggregation",
      "url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S3",
      "title": "OWASP: Broken Object Level Authorization",
      "url": "https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Authenticated identity does not authorize arbitrary referenced objects; resource access checks must cover each operation."
    },
    {
      "id": "S4",
      "title": "Redis: INCR and rate-limiter examples",
      "url": "https://redis.io/docs/latest/commands/incr/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Atomic shared counters and expiry race considerations illustrate why a distributed quota needs an explicit coordinated mechanism; this is not a universal gateway default."
    }
  ],
  "scenarios": [
    {
      "key": "interview-mobile-screen-fanout-budget",
      "theme": "A mobile screen needs six backend calls within 400ms. What should the gateway aggregate?",
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
          "rationale": "API Gateway Pattern: A mobile screen needs six backend calls within 400ms. What should the gateway aggregate?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A mobile screen needs six backend calls within 400ms. What should the gateway aggregate? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A receptionist can gather several answers while a visitor makes one trip. A mobile screen spends much of its time on cellular round trips to six backend services. Some backend reads are independent, but one expensive dependency dominates. You have a 400ms response budget. What will you aggregate and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Provide a screen-appropriate aggregate operation when it removes costly client round trips without hiding domain decisions. Execute independent downstream reads concurrently with bounded fan-out, one overall deadline and smaller dependency budgets. Return only the fields the screen needs, and keep authoritative business rules in their owning services.\n\nTrace aggregation latency and payload size. Give optional data an explicit omission or stale-data policy, and avoid chaining an aggregator to another aggregator repeatedly. If the screen needs substantial presentation-specific orchestration, a BFF behind the shared edge may be a clearer owner than a growing universal gateway policy."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You reduce mobile chattiness and simplify clients, but add server-side work, failure composition and a scaling hotspot. Direct parallel client requests are a viable alternative for a small number of fast independent services when network conditions permit them.\n\nFollow-up trap: aggregation does not make a slow essential dependency fast. If all six results must be fresh and complete, the slowest required path still bounds the response. Change the read model, underlying performance or response promise rather than claiming fan-out alone guarantees 400ms."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You reduce mobile chattiness and simplify clients, but add server-side work, failure composition and a scaling hotspot. Direct parallel client requests are a viable alternative for a small number of fast independent services when network conditions permit them.\n\nFollow-up trap: aggregation does not make a slow essential dependency fast. If all six results must be fresh and complete, the slowest required path still bounds the response. Change the read model, underlying performance or response promise rather than claiming fan-out alone guarantees 400ms."
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
      "key": "interview-optional-dependency-partial-response",
      "theme": "Order data succeeds but recommendations times out. Should the gateway fail the whole response?",
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
          "rationale": "API Gateway Pattern: Order data succeeds but recommendations times out. Should the gateway fail the whole response?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Order data succeeds but recommendations times out. Should the gateway fail the whole response? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A missing brochure should not prevent handing over a paid ticket. A gateway aggregates essential order status and optional recommendations. Recommendations stalls, and the gateway returns a generic 500 despite valid order data. What response and timeout policy will you choose?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Classify required and optional components in the API contract. Bound recommendation work separately, cancel or stop waiting when its budget expires, and return essential order data with an explicit partial/degraded indicator or an approved cached recommendation. Do not substitute invented order or payment state.\n\nIsolate optional fan-out concurrency and observe timeout/fallback rates so degradation remains visible. Test slow responses, failures and cancellation under load. Preserve meaningful upstream status rather than translating every outcome into one error. The client must know whether missing data is optional or the operation itself failed."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You improve useful availability but require clients to understand partial results and cache freshness. Failing the whole response is a viable alternative when the contract requires complete consistent data and partial information would be misleading.\n\nFollow-up trap: treating fraud authorization as optional because it is slow changes correctness. If recommendations become required to meet a contractual pricing decision, either wait within a redesigned budget or return a truthful pending/error outcome; do not keep the optional fallback after the guarantee changes."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You improve useful availability but require clients to understand partial results and cache freshness. Failing the whole response is a viable alternative when the contract requires complete consistent data and partial information would be misleading.\n\nFollow-up trap: treating fraud authorization as optional because it is slow changes correctness. If recommendations become required to meet a contractual pricing decision, either wait within a redesigned budget or return a truthful pending/error outcome; do not keep the optional fallback after the guarantee changes."
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
      "key": "interview-shared-quota-multiple-replicas",
      "theme": "Each gateway replica enforces a local limit, but a client exceeds the global quota. How will you coordinate?",
      "basis": "adapted-production",
      "selectionSources": [
        "S1",
        "S4"
      ],
      "technicalSources": [
        "S1",
        "S4"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "API Gateway Pattern: Each gateway replica enforces a local limit, but a client exceeds the global quota. How will you coordinate?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Each gateway replica enforces a local limit, but a client exceeds the global quota. How will you coordinate? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Five entrances each counting visitors independently cannot enforce one building-wide limit. Five gateway replicas each allow 100 requests per minute for the same client. The product promises one shared quota, but a central counter may add latency and become unavailable. What will you design?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Define the quota key, time window, burst policy and acceptable enforcement error before choosing storage. For a strict shared quota, use an appropriate atomic shared limiter or coordinated allocation with explicit failure behavior. For a soft protective limit, local budgets or leased tokens can reduce coordination while allowing a documented bounded overshoot.\n\nAuthenticate the quota identity instead of trusting an arbitrary header. Instrument allowed, rejected and unavailable decisions, test concurrent requests across replicas, and choose fail-open or fail-closed behavior by endpoint risk. A gateway product's rate-limit feature needs its actual distributed semantics checked."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "Shared enforcement improves fairness but adds coordination, latency and a failure dependency. Local limits are a viable alternative for approximate overload protection, provided callers are not promised a strict aggregate quota.\n\nFollow-up trap: scaling replicas silently multiplies an uncoordinated local allowance. If this becomes a hard billing or financial entitlement, a best-effort edge limiter is insufficient; enforce the authoritative entitlement in the responsible domain as well, and preserve its exact accounting semantics."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "Shared enforcement improves fairness but adds coordination, latency and a failure dependency. Local limits are a viable alternative for approximate overload protection, provided callers are not promised a strict aggregate quota.\n\nFollow-up trap: scaling replicas silently multiplies an uncoordinated local allowance. If this becomes a hard billing or financial entitlement, a best-effort edge limiter is insufficient; enforce the authoritative entitlement in the responsible domain as well, and preserve its exact accounting semantics."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S1, S4 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-authentication-versus-object-authorization",
      "theme": "The gateway validates a token. Can backend services trust every requested order ID?",
      "basis": "adapted-production",
      "selectionSources": [
        "S1",
        "S3"
      ],
      "technicalSources": [
        "S1",
        "S3"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "API Gateway Pattern: The gateway validates a token. Can backend services trust every requested order ID?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: The gateway validates a token. Can backend services trust every requested order ID? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A valid building pass does not grant access to every locker. The gateway authenticates a user, but an attacker changes an order ID and reaches another customer's record. Internal service traffic can also bypass the public gateway. Where will authorization be enforced?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Keep edge authentication and coarse request filtering, then enforce object/action authorization at the service that owns the order. Propagate identity through a trusted, integrity-protected mechanism and prevent clients from forging internal identity headers. Backend services must verify the identity/context and check access to the specific resource.\n\nTest cross-user, cross-tenant and direct internal access attempts. Distinguish user identity from gateway workload identity; a trusted proxy is not automatically the business owner of the data. Log safe correlation and denied actions without leaking secrets or sensitive records."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain consistent resource protection across entry paths but perform checks in more than one layer and manage trusted identity propagation. Centralized policy evaluation is a viable alternative for shared policy decisions, while resource ownership/context still needs reliable enforcement.\n\nFollow-up trap: putting every object permission in gateway routing configuration couples the edge to changing domain state. If a single trusted internal batch actor needs broader access, grant a scoped explicit capability rather than dropping service-level checks for all internal traffic."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain consistent resource protection across entry paths but perform checks in more than one layer and manage trusted identity propagation. Centralized policy evaluation is a viable alternative for shared policy decisions, while resource ownership/context still needs reliable enforcement.\n\nFollow-up trap: putting every object permission in gateway routing configuration couples the edge to changing domain state. If a single trusted internal batch actor needs broader access, grant a scoped explicit capability rather than dropping service-level checks for all internal traffic."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S1, S3 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-gateway-domain-orchestration-growth",
      "theme": "Refund, tax and inventory workflows now live in gateway configuration. What should move out?",
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
          "rationale": "API Gateway Pattern: Refund, tax and inventory workflows now live in gateway configuration. What should move out?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Refund, tax and inventory workflows now live in gateway configuration. What should move out? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A receptionist should route requests rather than become every department's manager. Gateway policies now calculate tax, orchestrate refunds and update stock. Releases need several domain teams, and failures are difficult to test. What boundary will you restore?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Keep the gateway focused on shared edge responsibilities such as routing, authentication, quotas and simple aggregation. Move authoritative business policy and durable workflows into cohesive application/domain services with explicit contracts and owners. Characterize existing behavior before migrating so external APIs remain compatible.\n\nUse the gateway to route gradually to the new owner, trace end-to-end outcomes and retain a rollback plan. A screen-specific BFF may own presentation composition, but it also should not duplicate financial or inventory authority. Separate transport convenience from business correctness."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain testable policy ownership and a smaller edge blast radius, but add or clarify service interactions and compatibility work. Keeping a small deterministic response transformation in the gateway is a viable alternative when it has no hidden domain state or workflow responsibility.\n\nFollow-up trap: moving all policies into one generic orchestration service can recreate the same central coupling. If the operation requires one immediate invariant, place that decision under a coherent owner; if it spans independent owners, use explicit durable workflow semantics rather than a sequence of unrecorded gateway calls."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain testable policy ownership and a smaller edge blast radius, but add or clarify service interactions and compatibility work. Keeping a small deterministic response transformation in the gateway is a viable alternative when it has no hidden domain state or workflow responsibility.\n\nFollow-up trap: moving all policies into one generic orchestration service can recreate the same central coupling. If the operation requires one immediate invariant, place that decision under a coherent owner; if it spans independent owners, use explicit durable workflow semantics rather than a sequence of unrecorded gateway calls."
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
      "key": "interview-edge-release-shared-blast-radius",
      "theme": "A gateway rollout breaks every backend route. How will you reduce the shared entry-point risk?",
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
          "rationale": "API Gateway Pattern: A gateway rollout breaks every backend route. How will you reduce the shared entry-point risk?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A gateway rollout breaks every backend route. How will you reduce the shared entry-point risk? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A faulty front door can block access to otherwise healthy rooms. A routing-policy release sends all clients to an invalid destination, while backend services remain healthy. You need fast recovery and safer future changes. What will you do?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Roll back or disable the faulty policy through a tested recovery path, then verify representative routes and identities end to end. Keep gateway instances redundant and configuration changes versioned, validated and gradually rolled out. Use synthetic probes for critical paths rather than treating process health as proof of correct routing.\n\nPartition policy ownership or gateway deployments where distinct clients/security domains justify smaller blast radii. Apply timeout and resource controls so one bad route cannot exhaust all edge capacity. Exercise both instance failure and logically valid but wrong configuration in deployment tests."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You reduce configuration blast radius and improve recovery at the cost of rollout complexity and possibly multiple gateways. One shared highly available gateway remains a viable alternative when change discipline and isolation meet the risk budget.\n\nFollow-up trap: multiple replicas loaded with the same bad configuration are all wrong together. If a proposal bypasses the gateway for emergency access, it must preserve authentication, authorization and operational control; an undocumented unprotected backend endpoint is not a safe rollback strategy."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You reduce configuration blast radius and improve recovery at the cost of rollout complexity and possibly multiple gateways. One shared highly available gateway remains a viable alternative when change discipline and isolation meet the risk budget.\n\nFollow-up trap: multiple replicas loaded with the same bad configuration are all wrong together. If a proposal bypasses the gateway for emergency access, it must preserve authentication, authorization and operational control; an undocumented unprotected backend endpoint is not a safe rollback strategy."
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
    }
  ],
  "publicDisclosure": "Researched 2026-11-17. These scenarios adapt documented production problems and architectural guidance. Interview frequency, rankings and company provenance for these exact prompts were not independently verified. Numeric budgets and organization details are author-created assumptions. Web search was available and used for this concept; primary sources support the technical reasoning, not a claim that these prompts recur in interviews.",
  "sourceNoteUrls": [
    "https://learn.microsoft.com/en-us/azure/architecture/microservices/design/gateway",
    "https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation",
    "https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/",
    "https://redis.io/docs/latest/commands/incr/"
  ],
  "editorialReviewedOn": "2026-11-17"
}
```
