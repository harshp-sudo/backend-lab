# Final Research: Hexagonal Architecture

State: reviewed. Separate editorial/source pass completed 2026-11-17 for all six permanent scenario keys. Exact interview frequency remains unverified; adaptations are disclosed. Browser/print acceptance is recorded separately.

The JSON map records actual planning queries, implementation source checks (or explicit limitations), final selection/technical mappings and all eight per-card editorial dispositions. Vendor-specific sources are examples, not universal architectural guarantees.

```json
{
  "topicId": "7db3e3c3-10aa-4709-bf33-63848952d81f",
  "title": "Hexagonal Architecture",
  "path": "topics/system-design/backend-architecture/code-and-domain-organization/hexagonal-architecture.html",
  "constitutionVersion": "1.2.0",
  "researchedOn": "2026-11-17",
  "state": "reviewed",
  "searches": [
    {
      "query": "site.alistair.cockburn.us hexagonal architecture ports adapters",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "\"hexagonal architecture\" \"interview\" testing adapters",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Alistair Cockburn: Hexagonal Architecture",
      "url": "https://alistair.cockburn.us/hexagonal-architecture",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S2",
      "title": "Alistair Cockburn: Component + Strategy / Ports and Adapters revisited",
      "url": "https://alistaircockburn.com/Component%20plus%20strategy.pdf",
      "limitation": "Implementation recheck on 2026-11-17 timed out; this supplementary PDF is not relied on for accepted technical claims.",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": null,
      "supportRationale": "Supplementary reference only; unavailable during this recheck and not mapped as technical support for any accepted scenario."
    },
    {
      "id": "S3",
      "title": "AWS: Making retries safe with idempotent APIs",
      "url": "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S4",
      "title": "Microsoft: Choosing a testing strategy",
      "url": "https://learn.microsoft.com/en-us/ef/core/testing/choosing-a-testing-strategy",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Test doubles can differ from real databases; real-adapter checks are needed for provider semantics and transaction behavior."
    }
  ],
  "scenarios": [
    {
      "key": "interview-rest-csv-same-application-port",
      "theme": "REST and nightly CSV imports disagree on order validation. Which port should they share?",
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
          "rationale": "Hexagonal Architecture: REST and nightly CSV imports disagree on order validation. Which port should they share?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: REST and nightly CSV imports disagree on order validation. Which port should they share? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Different plugs should power the same appliance behavior. A REST adapter rejects invalid orders, while a CSV importer writes directly to storage and accepts them. The business rule must hold regardless of entry channel. What port and adapters will you define?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Expose an application operation such as PlaceOrder with application-owned inputs and outcomes. Make REST and CSV separate driving adapters that translate transport data into that operation. Put the authoritative validation and invariant inside the application/domain rather than trusting either adapter's preliminary checks.\n\nKeep HTTP status codes, CSV row errors and file parsing at the edges. Test the operation without either transport, then test each adapter's mapping of valid and invalid input. Give batch rows stable operation identities if retries can repeat a purchase. An adapter should translate entry mechanics, not supply an alternate business implementation."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain consistent behavior and isolated testing but maintain two translation paths. Separate use cases sharing a smaller domain policy are a viable alternative when bulk import and interactive ordering have different authorized semantics.\n\nFollow-up trap: calling the REST endpoint from the importer adds network and authentication failure without necessarily improving the boundary. If the import must cross a process or trust boundary, a remote API may be appropriate, but keep its contract explicit and handle retries and partial batch completion deliberately."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain consistent behavior and isolated testing but maintain two translation paths. Separate use cases sharing a smaller domain policy are a viable alternative when bulk import and interactive ordering have different authorized semantics.\n\nFollow-up trap: calling the REST endpoint from the importer adds network and authentication failure without necessarily improving the boundary. If the import must cross a process or trust boundary, a remote API may be appropriate, but keep its contract explicit and handle retries and partial batch completion deliberately."
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
      "key": "interview-outbound-timeout-port-semantics",
      "theme": "A payment adapter times out after a possible effect. What should the outbound port return?",
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
          "rationale": "Hexagonal Architecture: A payment adapter times out after a possible effect. What should the outbound port return?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A payment adapter times out after a possible effect. What should the outbound port return? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A courier can lose the reply after delivering the parcel. A payment adapter catches every timeout and returns payment-failed. The application retries with a new charge and customers sometimes pay twice. What should the port's contract express and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Model confirmed success, definitive rejection and unknown outcome separately in the application-owned port. Pass one stable operation key to the adapter and require it to preserve that identity across safe retries. Persist the application's pending intent and use provider lookup or reconciliation to resolve ambiguity rather than treating a transport exception as a business rejection.\n\nKeep provider response codes and SDK exception classes inside the adapter, but do not erase uncertainty during translation. Contract-test a lost reply after a committed charge and verify that retries reuse the same identity. The business use case decides whether to wait, return pending or request manual resolution."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain honest failure semantics and safer recovery at the cost of more application states and durable reconciliation. A provider with a synchronous, queryable idempotent operation can simplify recovery; it still requires the application to distinguish unknown from rejected.\n\nFollow-up trap: an adapter cannot guarantee exactly-once effects from an external system that offers neither deduplication nor outcome lookup. If that assumption changes, stop blind automatic retries and introduce reconciliation or a different provider contract. Renaming the exception does not remove the original distributed uncertainty."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain honest failure semantics and safer recovery at the cost of more application states and durable reconciliation. A provider with a synchronous, queryable idempotent operation can simplify recovery; it still requires the application to distinguish unknown from rejected.\n\nFollow-up trap: an adapter cannot guarantee exactly-once effects from an external system that offers neither deduplication nor outcome lookup. If that assumption changes, stop blind automatic retries and introduce reconciliation or a different provider contract. Renaming the exception does not remove the original distributed uncertainty."
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
      "key": "interview-in-memory-adapter-contract-gap",
      "theme": "The in-memory adapter passes, but real storage violates uniqueness and rollback. How do you test the port?",
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
          "rationale": "Hexagonal Architecture: The in-memory adapter passes, but real storage violates uniqueness and rollback. How do you test the port?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: The in-memory adapter passes, but real storage violates uniqueness and rollback. How do you test the port? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A toy socket that always works cannot certify the building's wiring. Unit tests use an in-memory repository whose behavior differs from production under concurrent inserts and transaction failures. The port promises one reservation per seat. What tests will establish that promise?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Write a shared behavioral contract for the port's required semantics, then run it against the real adapter with the production database engine/configuration. Include duplicate-key races, failed writes, transaction rollback and error mapping. Keep the in-memory adapter for fast policy tests, but make its documented simplifications explicit.\n\nExercise the invariant with concurrent callers through the application and verify the database constraint or concurrency mechanism actually enforces it. Avoid implementing a second database inside the fake. A passing fake shows how policy reacts to assumed outcomes; it does not prove infrastructure can produce those outcomes correctly."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain realistic adapter guarantees while paying for integration setup and slower tests. A lightweight substitute provider is a useful alternative for some feedback, but cannot validate locking or SQL semantics it does not share.\n\nFollow-up trap: asserting that Save was called once says nothing about two concurrent requests. If the selected store cannot meet the port's atomic reservation contract, change the implementation or explicitly redesign the guarantee; do not quietly weaken the contract to match the fake."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain realistic adapter guarantees while paying for integration setup and slower tests. A lightweight substitute provider is a useful alternative for some feedback, but cannot validate locking or SQL semantics it does not share.\n\nFollow-up trap: asserting that Save was called once says nothing about two concurrent requests. If the selected store cannot meet the port's atomic reservation contract, change the implementation or explicitly redesign the guarantee; do not quietly weaken the contract to match the fake."
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
      "key": "interview-provider-sdk-model-leak",
      "theme": "A vendor SDK upgrade breaks the core. Where should its models and exceptions stop?",
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
          "rationale": "Hexagonal Architecture: A vendor SDK upgrade breaks the core. Where should its models and exceptions stop?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A vendor SDK upgrade breaks the core. Where should its models and exceptions stop? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Replacing a phone charger should not require rewiring every room. An outbound shipping adapter exposes SDK address objects and vendor exceptions through an application port. A provider upgrade now breaks use cases and tests. What will you change and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Make the port accept and return application-owned concepts such as ShipmentRequest, ShipmentReference and explicit outcomes. Translate vendor models, authentication and error details inside the shipping adapter. Preserve useful semantics such as invalid address, temporarily unavailable and unknown outcome without leaking SDK types.\n\nCreate focused mapping tests and adapter contract tests for the upgraded provider. Wire the implementation at the composition root so the core need not import or instantiate the SDK. Review serialization and units as well as type names; an address or weight conversion can be syntactically valid and still wrong."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You localize provider churn and simplify application tests, but maintain a mapping layer and may expose fewer provider-specific capabilities. A deliberately vendor-specific boundary is a viable alternative when the application depends fundamentally on unique features and accepts that coupling.\n\nFollow-up trap: copying every SDK field into an identically shaped internal object preserves semantic coupling. If a new capability is actually required, add an intentional application contract for it rather than a generic provider escape hatch that bypasses the boundary."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You localize provider churn and simplify application tests, but maintain a mapping layer and may expose fewer provider-specific capabilities. A deliberately vendor-specific boundary is a viable alternative when the application depends fundamentally on unique features and accepts that coupling.\n\nFollow-up trap: copying every SDK field into an identically shaped internal object preserves semantic coupling. If a new capability is actually required, add an intentional application contract for it rather than a generic provider escape hatch that bypasses the boundary."
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
      "key": "interview-port-per-class-ceremony",
      "theme": "An interface per class produces dozens of meaningless ports. What deserves a real port?",
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
          "rationale": "Hexagonal Architecture: An interface per class produces dozens of meaningless ports. What deserves a real port?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: An interface per class produces dozens of meaningless ports. What deserves a real port? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A building does not need a new entrance for every cupboard. A team creates a port and adapter for each helper class, so a small feature requires many pass-through files. There is only one external storage dependency and little domain complexity. What will you simplify?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Define ports at meaningful application conversations or external capability boundaries, not mechanically at every class. Keep internal collaboration ordinary when it does not cross a dependency boundary or need replacement. Consolidate pass-through abstractions while preserving the actual driving use case and outbound storage contract.\n\nExplain each remaining port in business or application terms: what does the application need, and what behavior must an adapter satisfy? Test through those stable conversations. Hexagonal architecture describes inside/outside separation; the drawing's six sides do not prescribe a number of ports or layers."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You reduce ceremony and improve navigation while accepting ordinary internal coupling that may later need refactoring. More granular ports are a viable alternative when capabilities vary independently or require distinct failure/security contracts.\n\nFollow-up trap: one enormous generic port can be as harmful as dozens of trivial ones because it exposes unrelated capabilities. If a helper becomes a third-party boundary with its own timeout or authorization behavior, introduce a deliberate port then rather than retaining a simplicity rule after its assumptions change."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You reduce ceremony and improve navigation while accepting ordinary internal coupling that may later need refactoring. More granular ports are a viable alternative when capabilities vary independently or require distinct failure/security contracts.\n\nFollow-up trap: one enormous generic port can be as harmful as dozens of trivial ones because it exposes unrelated capabilities. If a helper becomes a third-party boundary with its own timeout or authorization behavior, introduce a deliberate port then rather than retaining a simplicity rule after its assumptions change."
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
      "key": "interview-compatible-module-direct-port-call",
      "theme": "Two in-process modules already share a compatible application contract. Is another adapter necessary?",
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
          "rationale": "Hexagonal Architecture: Two in-process modules already share a compatible application contract. Is another adapter necessary?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Two in-process modules already share a compatible application contract. Is another adapter necessary? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Two matching plugs do not need a converter just to look architectural. A reporting module can call an application-owned query interface implemented by Orders in the same process. A reviewer demands an extra pass-through adapter on principle. No translation or policy difference exists. What will you recommend?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Allow direct collaboration through the explicit compatible contract when dependency direction and ownership are correct. An adapter earns its place by translating a protocol/model, enforcing an edge policy or adapting a real mismatch; it need not exist as an empty forwarding class. Keep private storage and domain internals behind the contract.\n\nAdd contract tests for the observable query behavior and document its consistency and authorization expectations. Wire the implementation outside the consuming policy. If the modules later separate physically, introduce a remote adapter that preserves the application-facing contract while making latency and failure behavior explicit."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You keep local code simple and avoid meaningless wrappers, but depend on a stable agreed interface. A real anti-corruption adapter is a viable alternative when the modules use different meanings or when isolation from provider change is needed.\n\nFollow-up trap: direct access to another module's tables is not equivalent to direct use of its public port. If a remote move introduces unknown outcomes or partial availability, revisit the contract; retaining a synchronous-looking method name must not conceal a materially different failure model."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You keep local code simple and avoid meaningless wrappers, but depend on a stable agreed interface. A real anti-corruption adapter is a viable alternative when the modules use different meanings or when isolation from provider change is needed.\n\nFollow-up trap: direct access to another module's tables is not equivalent to direct use of its public port. If a remote move introduces unknown outcomes or partial availability, revisit the contract; retaining a synchronous-looking method name must not conceal a materially different failure model."
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
  "publicDisclosure": "Researched 2026-11-17. These scenarios adapt documented production problems and architectural guidance. Interview frequency, rankings and company provenance for these exact prompts were not independently verified. Numeric budgets and organization details are author-created assumptions. Web search was available and used for this concept; primary sources support the technical reasoning, not a claim that these prompts recur in interviews. A supplementary Ports and Adapters PDF timed out during rechecking and is not relied on for these answers.",
  "sourceNoteUrls": [
    "https://alistair.cockburn.us/hexagonal-architecture",
    "https://alistaircockburn.com/Component%20plus%20strategy.pdf",
    "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/",
    "https://learn.microsoft.com/en-us/ef/core/testing/choosing-a-testing-strategy"
  ],
  "editorialReviewedOn": "2026-11-17"
}
```
