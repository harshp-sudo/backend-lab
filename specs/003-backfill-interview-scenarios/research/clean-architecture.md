# Final Research: Clean Architecture

State: reviewed. Separate editorial/source pass completed 2026-11-17 for all six permanent scenario keys. Exact interview frequency remains unverified; adaptations are disclosed. Browser/print acceptance is recorded separately.

The JSON map records actual planning queries, implementation source checks (or explicit limitations), final selection/technical mappings and all eight per-card editorial dispositions. Vendor-specific sources are examples, not universal architectural guarantees.

```json
{
  "topicId": "d257fdd8-8532-4138-839b-7295ae2e2994",
  "title": "Clean Architecture",
  "path": "topics/system-design/backend-architecture/code-and-domain-organization/clean-architecture.html",
  "constitutionVersion": "1.2.0",
  "researchedOn": "2026-11-17",
  "state": "reviewed",
  "searches": [
    {
      "query": "site.blog.cleancoder.com clean architecture database interface framework",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "\"clean architecture\" \"interview\" database transactions",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Robert C. Martin: The Clean Architecture",
      "url": "https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S2",
      "title": "Microsoft: Common web application architectures",
      "url": "https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S3",
      "title": "Microsoft: EF Core transactions (implementation-specific example)",
      "url": "https://learn.microsoft.com/en-us/ef/core/saving/transactions",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S4",
      "title": "AWS: Making retries safe with idempotent APIs",
      "url": "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Caller operation identity and owning-side deduplication distinguish retries of one intent from a new effect."
    }
  ],
  "scenarios": [
    {
      "key": "interview-framework-context-in-domain-tests",
      "theme": "Domain tests need a live HTTP request. How will you remove the framework dependency?",
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
          "rationale": "Clean Architecture: Domain tests need a live HTTP request. How will you remove the framework dependency?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Domain tests need a live HTTP request. How will you remove the framework dependency? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A recipe should be testable without opening the restaurant. Discount policy reads the current HTTP user and request headers directly, so unit tests must boot the web framework. A scheduled job now needs the same policy. What boundary will you change and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Pass application-owned values such as actor identity and requested operation into the use case, rather than letting inner policy read a framework context. Let the HTTP adapter authenticate the request and translate trusted claims into that input. Put business authorization checks in the responsible use case/domain policy so a job cannot bypass them accidentally.\n\nUse dependency tests or module rules to keep framework imports out of the inner policy. Add fast tests that construct ordinary inputs and exercise both allowed and denied cases. Test the HTTP adapter separately for trustworthy translation; removing a dependency must not mean trusting arbitrary client-supplied identities."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain framework-independent policy and reusable entry points, but maintain explicit input and adapter mapping. Keeping framework-aware logic is a simpler alternative for transport-only behavior such as header parsing; it should remain outside the business core.\n\nFollow-up trap: replacing HttpRequest with a giant RequestContext that exposes everything retains the same coupling. If the new job acts under a service identity, define its permissions explicitly rather than impersonating an end user or disabling authorization to make reuse convenient."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain framework-independent policy and reusable entry points, but maintain explicit input and adapter mapping. Keeping framework-aware logic is a simpler alternative for transport-only behavior such as header parsing; it should remain outside the business core.\n\nFollow-up trap: replacing HttpRequest with a giant RequestContext that exposes everything retains the same coupling. If the new job acts under a service identity, define its permissions explicitly rather than impersonating an end user or disabling authorization to make reuse convenient."
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
      "key": "interview-orm-types-in-inner-port",
      "theme": "An inner repository interface returns ORM queries and provider errors. Is dependency inversion working?",
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
          "rationale": "Clean Architecture: An inner repository interface returns ORM queries and provider errors. Is dependency inversion working?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: An inner repository interface returns ORM queries and provider errors. Is dependency inversion working? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A plug is not universal if it still exposes one machine's wiring. The application defines a repository interface, but its methods return provider query objects and throw database-specific exceptions. A provider upgrade breaks the core. What will you change?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Redesign the inner contract around the use case's required behavior, returning application-owned results or explicitly shaped read projections. Keep query translation, transaction objects and provider exceptions inside the outer adapter. Map infrastructure failures to meaningful outcomes without erasing useful distinctions such as conflict versus unavailable.\n\nPlace the interface where policy defines its needs and implement it in infrastructure. Add adapter contract tests and compile-time dependency checks so the inner project cannot import the ORM. Do not promise arbitrary provider interchangeability: query capabilities and consistency requirements still need real integration verification."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You localize provider coupling and simplify policy tests, but write translation and purpose-specific query methods. A dedicated read-model adapter is an alternative for complex reporting; a generic repository need not conceal every query language feature.\n\nFollow-up trap: returning a provider object as object or dynamic only hides the dependency from the compiler. If a use case fundamentally needs a vendor-specific capability, isolate and name that capability explicitly, or accept a documented infrastructure dependency rather than advertise a portability guarantee you cannot support."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You localize provider coupling and simplify policy tests, but write translation and purpose-specific query methods. A dedicated read-model adapter is an alternative for complex reporting; a generic repository need not conceal every query language feature.\n\nFollow-up trap: returning a provider object as object or dynamic only hides the dependency from the compiler. If a use case fundamentally needs a vendor-specific capability, isolate and name that capability explicitly, or accept a documented infrastructure dependency rather than advertise a portability guarantee you cannot support."
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
      "key": "interview-atomic-use-case-without-orm-import",
      "theme": "A use case needs two atomic writes but cannot import the ORM. How do you express the transaction?",
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
          "rationale": "Clean Architecture: A use case needs two atomic writes but cannot import the ORM. How do you express the transaction?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A use case needs two atomic writes but cannot import the ORM. How do you express the transaction? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A manager can demand one completed sale without choosing the ledger's locking syntax. A use case must save an order and local reservation atomically, yet clean dependency rules keep ORM APIs outside the core. Both writes use one database. What contract will you use and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Express the required atomic operation through an application-owned unit-of-work boundary or a coarse repository operation whose contract states all-or-nothing behavior. Let the infrastructure adapter implement that boundary with the actual database transaction and enlist all required writes. The use case chooses the business boundary; infrastructure supplies the mechanism.\n\nTest rollback after the first write, commit failure and concurrent attempts against the real provider. Keep remote effects outside a claimed local transaction, and map conflicts to explicit application outcomes. Dependency inversion moves source dependencies; it does not create atomicity by itself."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You preserve policy independence and an explicit commit guarantee, but design and test a transaction abstraction carefully. Putting the whole invariant in one aggregate/repository operation is a viable simpler alternative when it fits the domain.\n\nFollow-up trap: an interface named Transaction cannot make independent remote stores atomic. If a write moves into another service, use a supported distributed coordination mechanism or an explicit durable workflow with changed consistency semantics. Do not keep the old contract while silently weakening its guarantee."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You preserve policy independence and an explicit commit guarantee, but design and test a transaction abstraction carefully. Putting the whole invariant in one aggregate/repository operation is a viable simpler alternative when it fits the domain.\n\nFollow-up trap: an interface named Transaction cannot make independent remote stores atomic. If a write moves into another service, use a supported distributed coordination mechanism or an explicit durable workflow with changed consistency semantics. Do not keep the old contract while silently weakening its guarantee."
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
      "key": "interview-outward-execution-inward-source-dependency",
      "theme": "The use case calls a database adapter at runtime. Does that violate the inward dependency rule?",
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
          "rationale": "Clean Architecture: The use case calls a database adapter at runtime. Does that violate the inward dependency rule?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: The use case calls a database adapter at runtime. Does that violate the inward dependency rule? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A wall switch can operate a replaceable lamp without the switch being designed around that lamp model. A reviewer sees a use case invoking a repository implementation at runtime and claims all execution must flow inward. The interface is owned by the application. What will you inspect and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Distinguish control flow from source dependency. The use case may invoke an application-owned interface; an outer adapter implements it and a composition root wires the instance. Inspect imports and data types: the core should depend on its abstraction, while infrastructure depends on that contract, even when runtime execution reaches the database.\n\nKeep wiring at the edge and avoid a service locator that lets policy look up arbitrary infrastructure. Verify that the application can run with a test adapter without importing the production framework. Draw both the runtime call and source dependency explicitly when explaining the design."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You allow replaceable mechanisms without forbidding useful I/O, at the cost of explicit composition and abstraction boundaries. Direct infrastructure calls are an alternative in a deliberately simpler application, but then accept that dependency rather than claiming the same isolation.\n\nFollow-up trap: moving an interface into infrastructure while the core imports it still points the source dependency outward. If a stable external standard genuinely belongs in a public contract, decide that explicitly and keep provider-specific details from leaking through it; folder names alone do not establish the dependency rule."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You allow replaceable mechanisms without forbidding useful I/O, at the cost of explicit composition and abstraction boundaries. Direct infrastructure calls are an alternative in a deliberately simpler application, but then accept that dependency rather than claiming the same isolation.\n\nFollow-up trap: moving an interface into infrastructure while the core imports it still points the source dependency outward. If a stable external standard genuinely belongs in a public contract, decide that explicitly and keep provider-specific details from leaking through it; folder names alone do not establish the dependency rule."
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
      "key": "interview-crud-abstraction-ceremony",
      "theme": "A one-screen CRUD feature now requires ten projects and an interface per class. Should you keep adding boundaries?",
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
          "rationale": "Clean Architecture: A one-screen CRUD feature now requires ten projects and an interface per class. Should you keep adding boundaries?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A one-screen CRUD feature now requires ten projects and an interface per class. Should you keep adding boundaries? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A small cupboard does not need the logistics system of a warehouse. A one-screen internal editor with little policy takes days because every change requires duplicate models, pass-through services and interfaces. The team has a short deadline and no predicted provider change. What will you simplify?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Keep the stable boundary that protects actual policy and remove pass-through abstractions with no independent responsibility. A use case can be a small function/module; clean architecture does not require a fixed number of projects or one interface per class. Prefer a direct, clear implementation behind an adapter boundary over speculative layers.\n\nMeasure change effort and test whether the simplified feature still keeps business rules independent of transport and persistence details that matter. Preserve authorization, validation and useful integration tests. Record the trigger for adding a new abstraction when real variation or policy complexity appears."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain delivery speed and clearer code while accepting some local coupling and possible later refactoring. A more elaborate boundary is a viable alternative when multiple implementations or a complex domain already require it.\n\nFollow-up trap: simplicity is not permission to move pricing or security policy into controllers. If the feature evolves into a regulated approval workflow, introduce explicit policy/use-case boundaries and audit requirements then. Design for the demonstrated responsibility rather than treating either maximum ceremony or zero abstraction as universally correct."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain delivery speed and clearer code while accepting some local coupling and possible later refactoring. A more elaborate boundary is a viable alternative when multiple implementations or a complex domain already require it.\n\nFollow-up trap: simplicity is not permission to move pricing or security policy into controllers. If the feature evolves into a regulated approval workflow, introduce explicit policy/use-case boundaries and audit requirements then. Design for the demonstrated responsibility rather than treating either maximum ceremony or zero abstraction as universally correct."
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
      "key": "interview-http-and-job-shared-policy",
      "theme": "A nightly job and HTTP endpoint implement different eligibility rules. How should they share a use case?",
      "basis": "adapted-production",
      "selectionSources": [
        "S1",
        "S2",
        "S4"
      ],
      "technicalSources": [
        "S1",
        "S2",
        "S4"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Clean Architecture: A nightly job and HTTP endpoint implement different eligibility rules. How should they share a use case?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A nightly job and HTTP endpoint implement different eligibility rules. How should they share a use case? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Two doors into the same building should not lead to different admission rules. An endpoint and a nightly job both renew subscriptions but duplicate eligibility checks and error handling. They now disagree on expired accounts. What shared boundary will you establish?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Create one policy-bearing application use case with application-owned inputs and explicit outcomes. Each entry adapter handles its transport concerns: HTTP status mapping for the endpoint, scheduling and batch progress for the job. Both invoke the same eligibility policy with an authorized actor and stable operation identity where retries can repeat effects.\n\nTest the policy independently and add one adapter integration test for each entry path. Keep batch-specific chunking and recovery outside the domain rule, while ensuring a restarted job does not renew the same subscription twice. Shared reuse should preserve semantics, not just eliminate similar-looking lines."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain consistent decisions and reusable tests, but require a clear result contract and careful batch retry handling. Separate use cases that share a smaller domain policy are an alternative when interactive and bulk workflows have genuinely different guarantees.\n\nFollow-up trap: reusing an HTTP controller from the scheduler drags framework behavior inward. If a bulk operation is intentionally allowed to bypass a user-facing limit, model that authorized difference explicitly instead of adding hidden transport checks inside the shared policy."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain consistent decisions and reusable tests, but require a clear result contract and careful batch retry handling. Separate use cases that share a smaller domain policy are an alternative when interactive and bulk workflows have genuinely different guarantees.\n\nFollow-up trap: reusing an HTTP controller from the scheduler drags framework behavior inward. If a bulk operation is intentionally allowed to bypass a user-facing limit, model that authorized difference explicitly instead of adding hidden transport checks inside the shared policy."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S1, S2, S4 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
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
    "https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html",
    "https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures",
    "https://learn.microsoft.com/en-us/ef/core/saving/transactions",
    "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/"
  ],
  "editorialReviewedOn": "2026-11-17"
}
```
