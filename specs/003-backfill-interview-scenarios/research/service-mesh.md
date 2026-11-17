# Final Research: Service Mesh

State: reviewed. Separate editorial/source pass completed 2026-11-17 for all six permanent scenario keys. Exact interview frequency remains unverified; adaptations are disclosed. Browser/print acceptance is recorded separately.

The JSON map records actual planning queries, implementation source checks (or explicit limitations), final selection/technical mappings and all eight per-card editorial dispositions. Vendor-specific sources are examples, not universal architectural guarantees.

```json
{
  "topicId": "84458963-012b-4a80-828a-2da27d8b509d",
  "title": "Service Mesh",
  "path": "topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/service-mesh.html",
  "constitutionVersion": "1.2.0",
  "researchedOn": "2026-11-17",
  "state": "reviewed",
  "searches": [
    {
      "query": "\"Service Mesh\" interview production mTLS retries sidecar",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "site.istio.io latest docs concepts traffic management retries security mutual TLS",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Istio: Traffic management",
      "url": "https://istio.io/latest/docs/concepts/traffic-management/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S2",
      "title": "Istio: Security",
      "url": "https://istio.io/latest/docs/concepts/security/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S3",
      "title": "Istio: Sidecar or ambient?",
      "url": "https://istio.io/latest/docs/overview/dataplane-modes/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S4",
      "title": "AWS: Timeouts, retries, and backoff with jitter",
      "url": "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Layered retries amplify attempts; deadlines, safe repetition and bounded backoff protect recovery."
    },
    {
      "id": "S5",
      "title": "AWS: Making retries safe with idempotent APIs",
      "url": "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Caller operation identity and owning-side deduplication distinguish retries of one intent from a new effect."
    },
    {
      "id": "S6",
      "title": "OWASP: Broken Object Level Authorization",
      "url": "https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Authenticated identity does not authorize arbitrary referenced objects; resource access checks must cover each operation."
    }
  ],
  "scenarios": [
    {
      "key": "interview-mesh-app-retry-multiplication",
      "theme": "Application and proxy retries multiply downstream load. Which layer should own the policy?",
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
          "rationale": "Service Mesh: Application and proxy retries multiply downstream load. Which layer should own the policy?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Application and proxy retries multiply downstream load. Which layer should own the policy? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Two assistants independently repeating the same phone call can overwhelm the recipient. An application retries payment requests and the mesh proxy also retries them, causing duplicate attempts and overload. The overall request has a strict deadline. What will you configure and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Inventory the effective retry policies at the application, SDK, gateway and mesh. Choose deliberate ownership per operation and bound the total attempts, elapsed time and concurrency. Put business-aware recovery where operation identity and uncertain outcomes are understood; keep proxy retries limited to explicitly safe failure/operation combinations.\n\nPropagate an end-to-end deadline, add jitter/backoff where supported and observe actual attempts rather than only top-level requests. Require idempotency for repeatable effects. Test a slow dependency and a lost response after commit; the mesh cannot infer whether a business effect happened merely from a transport error."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain predictable load and recovery behavior but may return failures sooner instead of spending extra attempts. Mesh-level handling is a viable alternative for suitable transport failures when it remains within the application's safety and deadline contract.\n\nFollow-up trap: enabling automatic retries globally does not make mutating requests safe. If the workload changes to asynchronous idempotent jobs with a longer completion window, move retry scheduling into controlled durable workers rather than reusing an interactive proxy policy unchanged. Do not let two independent retry budgets silently multiply."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain predictable load and recovery behavior but may return failures sooner instead of spending extra attempts. Mesh-level handling is a viable alternative for suitable transport failures when it remains within the application's safety and deadline contract.\n\nFollow-up trap: enabling automatic retries globally does not make mutating requests safe. If the workload changes to asynchronous idempotent jobs with a longer completion window, move retry scheduling into controlled durable workers rather than reusing an interactive proxy policy unchanged. Do not let two independent retry budgets silently multiply."
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
      "key": "interview-strict-mtls-legacy-migration",
      "theme": "Strict mutual TLS breaks legacy callers. How do you migrate without leaving a permanent insecure hole?",
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
          "rationale": "Service Mesh: Strict mutual TLS breaks legacy callers. How do you migrate without leaving a permanent insecure hole?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Strict mutual TLS breaks legacy callers. How do you migrate without leaving a permanent insecure hole? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Changing a building to badge-only entry can lock out legitimate visitors who have not received badges. Strict mesh mTLS is enabled before all callers participate, and legacy clients fail. You need a staged migration with a clear security endpoint. What will you do?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Inventory legitimate callers and supported data-plane paths, then migrate workload identity and certificate trust before enforcing strict mode on the affected traffic. Use a narrowly scoped transitional policy only where needed, observe remaining plaintext/legacy paths and set an owner and expiry for each exception. Validate actual policy precedence and port/protocol behavior in the deployed mesh.\n\nRoll out enforcement by workload or namespace with canaries and connectivity tests. Keep authorization policies aligned with authenticated identities, and provide a secure gateway/adapter for legacy callers that cannot join directly. Do not describe transitional plaintext acceptance as the final security guarantee."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You preserve availability while reaching enforced identity protection, but carry temporary policy complexity and risk. A coordinated cutover is a viable alternative for a small fully controlled caller set with an acceptable maintenance window.\n\nFollow-up trap: permissive mode does not mean every connection is encrypted, and encryption does not prove permission. If a workload handles data that cannot tolerate a plaintext transition, isolate it and require a secure compatible entry path before allowing access, even if some legacy calls must stop."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You preserve availability while reaching enforced identity protection, but carry temporary policy complexity and risk. A coordinated cutover is a viable alternative for a small fully controlled caller set with an acceptable maintenance window.\n\nFollow-up trap: permissive mode does not mean every connection is encrypted, and encryption does not prove permission. If a workload handles data that cannot tolerate a plaintext transition, isolate it and require a secure compatible entry path before allowing access, even if some legacy calls must stop."
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
      "key": "interview-mtls-not-object-permission",
      "theme": "All traffic uses mTLS, yet one service reads another tenant's orders. What protection is missing?",
      "basis": "adapted-production",
      "selectionSources": [
        "S2",
        "S6"
      ],
      "technicalSources": [
        "S2",
        "S6"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Service Mesh: All traffic uses mTLS, yet one service reads another tenant's orders. What protection is missing?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: All traffic uses mTLS, yet one service reads another tenant's orders. What protection is missing? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A verified employee badge does not authorize opening every customer's folder. Mesh mTLS authenticates workloads and encrypts traffic, but a service can still request an arbitrary tenant's order. What authorization checks belong in the mesh and application?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Use mesh authorization for explicit service-to-service policy at the supported protocol level, and enforce tenant/object/action permissions in the owning application using trusted identity/context. Distinguish workload identity from the end user's delegated rights. Reject forged tenant headers and prevent untrusted callers from bypassing the intended entry path.\n\nTest allowed and denied workload paths plus cross-tenant object access. Propagate only scoped identity/context and maintain auditable correlation. Verify which policy layer sees which information; a network proxy may not possess the domain state needed to decide ownership of an individual order."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You combine consistent transport identity with domain-aware access control, but manage policy at more than one boundary. Centralized policy evaluation is a viable alternative for reusable rules when the application supplies trustworthy context and still enforces the decision.\n\nFollow-up trap: a valid certificate proves an identity under the trust model, not permission for every action. If background processing legitimately needs cross-tenant access, grant an explicit narrow capability rather than disabling tenant checks for all mesh-authenticated traffic."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You combine consistent transport identity with domain-aware access control, but manage policy at more than one boundary. Centralized policy evaluation is a viable alternative for reusable rules when the application supplies trustworthy context and still enforces the decision.\n\nFollow-up trap: a valid certificate proves an identity under the trust model, not permission for every action. If background processing legitimately needs cross-tenant access, grant an explicit narrow capability rather than disabling tenant checks for all mesh-authenticated traffic."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S2, S6 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-sidecar-ambient-measured-choice",
      "theme": "Proxy memory and tail latency exceed budget. Is ambient mode automatically the answer?",
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
          "rationale": "Service Mesh: Proxy memory and tail latency exceed budget. Is ambient mode automatically the answer?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Proxy memory and tail latency exceed budget. Is ambient mode automatically the answer? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Changing the delivery arrangement can reduce per-room equipment without making transport free. A sidecar deployment consumes too much memory on small nodes and adds latency. The team proposes ambient mode without checking required traffic features or isolation. What evaluation will you run?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Measure the current data path under representative traffic, including connection patterns, policy, telemetry and failure. Compare supported sidecar and ambient designs for the exact deployed versions and required L4/L7 capabilities, including whether waypoint proxies or other components are needed. Budget total resource use and shared failure domains, not only per-pod sidecar memory.\n\nPilot a limited workload, verify identity/authorization and rollout/rollback behavior, and measure p95/p99 latency plus operational burden. Choose the simplest mode that meets the actual requirements. Avoid promising universal performance improvement from an architecture label."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "A different data plane may reduce some per-workload overhead but introduce shared components, feature constraints and migration work. Tuning existing sidecars or removing an unnecessary mesh is a viable alternative when it meets security/operations needs more cheaply.\n\nFollow-up trap: comparing a bare L4 path with a fully featured L7 sidecar is not an equivalent benchmark. If mandatory application-layer authorization requires additional proxies, include their cost and behavior. If strict workload isolation outweighs memory savings, retain the design that actually meets that constraint."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "A different data plane may reduce some per-workload overhead but introduce shared components, feature constraints and migration work. Tuning existing sidecars or removing an unnecessary mesh is a viable alternative when it meets security/operations needs more cheaply.\n\nFollow-up trap: comparing a bare L4 path with a fully featured L7 sidecar is not an equivalent benchmark. If mandatory application-layer authorization requires additional proxies, include their cost and behavior. If strict workload isolation outweighs memory savings, retain the design that actually meets that constraint."
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
    },
    {
      "key": "interview-canary-traffic-unexpected-share",
      "theme": "A 5% canary receives unexpected traffic. Which routing assumptions will you inspect?",
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
          "rationale": "Service Mesh: A 5% canary receives unexpected traffic. Which routing assumptions will you inspect?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A 5% canary receives unexpected traffic. Which routing assumptions will you inspect? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A sign saying five percent does not prove every entrance follows the same sign. A mesh canary unexpectedly serves much more traffic or the wrong clients. Some calls target a different host, and versions use long-lived connections. What will you investigate first?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Inspect the effective route configuration, host matching, subset labels, gateway/sidecar path and policy precedence from the actual clients. Verify that requests traverse the configured rule and that canary endpoints are labeled as intended. Separate weighted request distribution from session affinity, long-lived streams and low-sample randomness.\n\nCompare route metrics with application version metrics and use a controlled request set to validate behavior. Roll back the faulty rule if user impact is rising. Test the stable and canary paths independently, including any headers or identity conditions used for targeted rollout."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain evidence about the real traffic path but need end-to-end visibility across configuration and clients. Header- or identity-targeted canaries are a viable alternative when deterministic cohorts matter more than approximate percentage distribution.\n\nFollow-up trap: a 5% weight is not a promise that every group of twenty requests contains exactly one canary call. If the protocol is a long-lived connection or stream, confirm the actual routing unit before interpreting request counts. Do not compensate for a misapplied rule by guessing another percentage."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain evidence about the real traffic path but need end-to-end visibility across configuration and clients. Header- or identity-targeted canaries are a viable alternative when deterministic cohorts matter more than approximate percentage distribution.\n\nFollow-up trap: a 5% weight is not a promise that every group of twenty requests contains exactly one canary call. If the protocol is a long-lived connection or stream, confirm the actual routing unit before interpreting request counts. Do not compensate for a misapplied rule by guessing another percentage."
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
      "key": "interview-mesh-business-fallback-limit",
      "theme": "The mesh times out a payment call. Can it return a successful business fallback?",
      "basis": "adapted-production",
      "selectionSources": [
        "S1",
        "S2",
        "S5"
      ],
      "technicalSources": [
        "S1",
        "S2",
        "S5"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Service Mesh: The mesh times out a payment call. Can it return a successful business fallback?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: The mesh times out a payment call. Can it return a successful business fallback? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A courier may report delivery failure but cannot decide that a purchase was paid. A team wants the mesh to replace a payment timeout with a success-shaped response so checkout remains green. The payment outcome may be unknown. What belongs in infrastructure versus application recovery?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Let the mesh provide configured transport controls and telemetry, while the application owns business outcomes. Persist the payment operation identity, return pending or a permitted error on uncertainty, and reconcile with the authority before confirming the order. A proxy-generated HTTP success cannot establish that money moved.\n\nUse fallback only where the business permits a truthful alternative, such as cached recommendations with explicit staleness. Test transport timeout, committed-but-unacknowledged effects and dependency recovery. Make dashboards distinguish transport availability from completed business operations rather than optimizing a green status code."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You preserve correctness and honest user state at the cost of visible pending outcomes and reconciliation. Failing closed is a viable alternative for an operation that cannot safely proceed without confirmation; it still needs to discover whether a timed-out effect committed.\n\nFollow-up trap: resilience features cannot infer domain intent or compensate an external effect automatically. If the operation changes to a noncritical read with an approved cache, a mesh/application fallback may become appropriate. Reevaluate semantics per operation instead of applying one global success fallback."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You preserve correctness and honest user state at the cost of visible pending outcomes and reconciliation. Failing closed is a viable alternative for an operation that cannot safely proceed without confirmation; it still needs to discover whether a timed-out effect committed.\n\nFollow-up trap: resilience features cannot infer domain intent or compensate an external effect automatically. If the operation changes to a noncritical read with an approved cache, a mesh/application fallback may become appropriate. Reevaluate semantics per operation instead of applying one global success fallback."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S1, S2, S5 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
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
    "https://istio.io/latest/docs/concepts/traffic-management/",
    "https://istio.io/latest/docs/concepts/security/",
    "https://istio.io/latest/docs/overview/dataplane-modes/",
    "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/",
    "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/",
    "https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/"
  ],
  "editorialReviewedOn": "2026-11-17"
}
```
