# Final Research: Distributed System Fundamentals

State: reviewed. Separate editorial/source pass completed 2026-11-17 for all six permanent scenario keys. Exact interview frequency remains unverified; adaptations are disclosed. Browser/print acceptance is recorded separately.

The JSON map records actual planning queries, implementation source checks (or explicit limitations), final selection/technical mappings and all eight per-card editorial dispositions. Vendor-specific sources are examples, not universal architectural guarantees.

```json
{
  "topicId": "a1cef6f2-5f76-4376-980d-64af99310ec8",
  "title": "Distributed System Fundamentals",
  "path": "topics/system-design/backend-architecture/core-system-topologies/distributed-system-fundamentals.html",
  "constitutionVersion": "1.2.0",
  "researchedOn": "2026-11-17",
  "state": "reviewed",
  "searches": [
    {
      "query": "distributed systems system design interview production retries idempotency timeouts Amazon Builders Library",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "Distributed System Fundamentals interview consistency partition idempotency site:amazon.jobs",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "Distributed System Fundamentals partition replication consistency site:allthingsdistributed.com Dynamo",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "AWS: Timeouts, retries, and backoff with jitter",
      "url": "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S2",
      "title": "AWS: Making retries safe with idempotent APIs",
      "url": "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S3",
      "title": "Original Dynamo paper",
      "url": "https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S4",
      "title": "Hazelcast: Fencing tokens and uncertain lock ownership",
      "url": "https://docs.hazelcast.com/hazelcast/5.7/data-structures/fencedlock",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Monotonic fencing tokens must be checked by the effect owner; timeout/lease expiry does not stop a paused former owner."
    },
    {
      "id": "S5",
      "title": "Microsoft: Cosmos DB consistency levels (session example)",
      "url": "https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Session/read-your-writes consistency is distinct from a global latest-value guarantee; application proposals require supported version/freshness mechanisms."
    }
  ],
  "scenarios": [
    {
      "key": "interview-payment-timeout-unknown-outcome",
      "theme": "A payment times out after a possible charge. How do you retry without charging twice?",
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
          "rationale": "Distributed System Fundamentals: A payment times out after a possible charge. How do you retry without charging twice?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A payment times out after a possible charge. How do you retry without charging twice? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Think of losing a receipt after paying: no receipt does not mean no payment. A checkout waits two seconds for a charge, times out, and the customer immediately retries. The provider may already have committed. You must avoid a second charge while still letting the customer discover the outcome. What will you do and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Treat the timeout as unknown, not rejected. Persist a purchase operation with one stable idempotency key before contacting the provider, and reuse that key for retries of the same amount, currency and customer. The effect owner must atomically bind the key to the effect; a caller-side check alone cannot prevent concurrent duplicate charges.\n\nReturn a pending operation reference when the outcome is uncertain. Query the provider by that identity or reconcile its authoritative callbacks, then publish a confirmed or rejected result. Bound retries and retain deduplication records for the documented retry window; reject reuse of the key with different purchase data."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain recoverable outcomes and duplicate protection at the cost of durable operation state, reconciliation and delayed confirmation. An alternative is a synchronous-only checkout that stops accepting work on timeout, but it still needs a way to reconcile a charge that already happened.\n\nFollow-up trap: generating a new key on each attempt creates new purchases. If the provider has no idempotency or lookup capability, do not claim exactly-once charging: stop automatic ambiguous retries, retain the unresolved operation and reconcile before allowing a fresh charge. A later genuine purchase needs a new identity."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain recoverable outcomes and duplicate protection at the cost of durable operation state, reconciliation and delayed confirmation. An alternative is a synchronous-only checkout that stops accepting work on timeout, but it still needs a way to reconcile a charge that already happened.\n\nFollow-up trap: generating a new key on each attempt creates new purchases. If the provider has no idempotency or lookup capability, do not claim exactly-once charging: stop automatic ambiguous retries, retain the unresolved operation and reconcile before allowing a fresh charge. A later genuine purchase needs a new identity."
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
      "key": "interview-retry-storm-overload",
      "theme": "Three dependency layers retry during overload. How do you stop the recovery traffic becoming an outage?",
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
          "rationale": "Distributed System Fundamentals: Three dependency layers retry during overload. How do you stop the recovery traffic becoming an outage?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Three dependency layers retry during overload. How do you stop the recovery traffic becoming an outage? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Imagine everyone repeatedly redialing a busy shop. Three layers each permit up to three attempts, so one original call can produce 27 downstream attempts. Latency is rising and callers have a one-second overall deadline. Extra attempts consume the capacity the dependency needs to recover. What will you change first and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Measure downstream attempt volume separately from user traffic, shed excess load and temporarily reduce retries. Choose one deliberate retry owner for the operation rather than multiplying independent policies. Retry only eligible transient failures when the remaining deadline and retry budget permit it; back off with jitter so clients do not wake together.\n\nPropagate the end-to-end deadline, cap concurrency and queues, and require safe repetition for mutating operations. Test a degraded dependency under load, watching successful work, saturation and recovery time rather than celebrating a lower error count produced by more attempts."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You preserve recovery capacity and predictable latency, while some requests fail earlier instead of receiving extra chances. A small bounded queue or cached read is a viable alternative for selected workloads; it is not a replacement for controlling overload.\n\nFollow-up trap: increasing every timeout holds scarce connections longer and can worsen saturation. If traffic is an asynchronous job stream with a long completion window, move retries into a durable worker schedule with controlled concurrency rather than applying the interactive one-second policy unchanged. The deadline belongs to the user operation, not independently to each hop."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You preserve recovery capacity and predictable latency, while some requests fail earlier instead of receiving extra chances. A small bounded queue or cached read is a viable alternative for selected workloads; it is not a replacement for controlling overload.\n\nFollow-up trap: increasing every timeout holds scarce connections longer and can worsen saturation. If traffic is an asynchronous job stream with a long completion window, move retries into a durable worker schedule with controlled concurrency rather than applying the interactive one-second policy unchanged. The deadline belongs to the user operation, not independently to each hop."
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
      "key": "interview-partition-cart-versus-stock",
      "theme": "A region is partitioned. Can cart edits stay available while the final stock unit remains safe?",
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
          "rationale": "Distributed System Fundamentals: A region is partitioned. Can cart edits stay available while the final stock unit remains safe?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A region is partitioned. Can cart edits stay available while the final stock unit remains safe? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Two disconnected shops may write wish lists, but they cannot both promise the same last item without an allocation rule. A regional network partition interrupts coordination. Customers should still edit carts, yet confirmed purchases must never oversell a unique ticket. What do you allow in each region and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Separate cart intent from authoritative allocation. Accept reversible cart changes locally with version metadata and a defined merge policy. Confirm the ticket only through an owner or coordination mechanism that can enforce the single-unit invariant; a region unable to reach that authority must return pending or temporarily unavailable for purchase.\n\nMake the distinction visible: adding an item is not a reservation. After connectivity returns, merge permitted cart changes, revalidate stock and resolve pending operations using stable identities. If you preallocate disjoint regional stock rights, enforce those rights locally rather than letting both regions sell the full inventory."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "Cart availability improves while strict purchase availability is deliberately reduced. Preallocated quotas are an alternative that preserves local sales within each region's rights, but can strand unused capacity and complicate rebalancing.\n\nFollow-up trap: eventual reconciliation cannot undo the fact that two customers were promised the same unique seat. If the item becomes replenishable stock and the business explicitly accepts backorders, you may allow provisional orders with compensation and clear customer terms. That is a changed business guarantee, not evidence that a strict invariant was preserved during the partition."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "Cart availability improves while strict purchase availability is deliberately reduced. Preallocated quotas are an alternative that preserves local sales within each region's rights, but can strand unused capacity and complicate rebalancing.\n\nFollow-up trap: eventual reconciliation cannot undo the fact that two customers were promised the same unique seat. If the item becomes replenishable stock and the business explicitly accepts backorders, you may allow provisional orders with compensation and clear customer terms. That is a changed business guarantee, not evidence that a strict invariant was preserved during the partition."
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
      "key": "interview-read-after-profile-update",
      "theme": "A successful profile update is followed by an old value. Which read guarantee will you add?",
      "basis": "adapted-production",
      "selectionSources": [
        "S3",
        "S5"
      ],
      "technicalSources": [
        "S3",
        "S5"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Distributed System Fundamentals: A successful profile update is followed by an old value. Which read guarantee will you add?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A successful profile update is followed by an old value. Which read guarantee will you add? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "You change a name at one desk, then ask another desk whose notebook has not caught up. A profile API acknowledges a committed update, but the next read hits a lagging replica and shows the old name. Browsing other people's profiles can be slightly stale; seeing your own edit revert is unacceptable. What will you do and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Provide read-your-writes behavior for the editing session instead of making every read globally synchronous. Return an authoritative version with the update. Route the subsequent session read to a source known to include that version, or wait up to a bounded budget for a replica to reach it before falling back to the authority.\n\nTrace cache versions as well as database replication: a fresh database read can still be hidden by an old response cache. Invalidate or version the relevant cache entry, and test a delayed replica, region failover and session movement. Do not acknowledge a write before its required durability condition is satisfied."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You improve the editing experience with less coordination than a universal latest-value guarantee, but carry session/version metadata and may increase authority load or latency. Reading all profile traffic from the writer is a simpler alternative when its capacity is adequate.\n\nFollow-up trap: a fixed sleep only guesses replication delay. If a legal-name decision must be current for every observer, session consistency is insufficient; move that decision to an authoritative, appropriately coordinated read and accept its availability/latency cost. Define what happens when the required version cannot be reached within the budget."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You improve the editing experience with less coordination than a universal latest-value guarantee, but carry session/version metadata and may increase authority load or latency. Reading all profile traffic from the writer is a simpler alternative when its capacity is adequate.\n\nFollow-up trap: a fixed sleep only guesses replication delay. If a legal-name decision must be current for every observer, session consistency is insufficient; move that decision to an authoritative, appropriately coordinated read and accept its availability/latency cost. Define what happens when the required version cannot be reached within the budget."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S3, S5 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-offline-conflict-business-meaning",
      "theme": "Two offline devices edit the same record. Will last-write-wins preserve what the user intended?",
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
          "rationale": "Distributed System Fundamentals: Two offline devices edit the same record. Will last-write-wins preserve what the user intended?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Two offline devices edit the same record. Will last-write-wins preserve what the user intended? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Two children alter copies of the same shopping list while apart. One adds milk; the other removes bread. A server later receives both snapshots, and device clocks may be wrong. You must preserve meaningful changes without silently resurrecting a deliberate deletion. What conflict rule will you choose and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Model the operations and their business meaning before choosing a merge. Attach version information so the server can detect concurrent edits rather than pretending arrival order represents causality. For a cart, consider item-level add/remove operations with explicit deletion semantics; for a sensitive address change, surface a conflict or require an authoritative choice.\n\nPersist enough causal or revision information to distinguish a retry from a new edit, and make merges deterministic and testable. Explain any conflict to the user when intent cannot be inferred safely. The original Dynamo design is evidence for application-assisted reconciliation, not a universal recipe for every data type."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "Semantic merging preserves more intent than overwriting whole snapshots, but increases metadata, testing and domain-specific rules. Last-write-wins is a viable cheaper alternative for replaceable preferences when the business accepts lost concurrent updates and understands clock/ordering limitations.\n\nFollow-up trap: unioning every list makes removals disappear. If the record is a bank balance or exclusive allocation rather than a shopping list, merging arbitrary edits may violate an invariant. Send authoritative commands with concurrency checks or serialize those decisions instead of transferring a cart merge policy to money."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "Semantic merging preserves more intent than overwriting whole snapshots, but increases metadata, testing and domain-specific rules. Last-write-wins is a viable cheaper alternative for replaceable preferences when the business accepts lost concurrent updates and understands clock/ordering limitations.\n\nFollow-up trap: unioning every list makes removals disappear. If the record is a bank balance or exclusive allocation rather than a shopping list, merging arbitrary edits may violate an invariant. Send authoritative commands with concurrency checks or serialize those decisions instead of transferring a cart merge policy to money."
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
      "key": "interview-slow-replica-failure-suspicion",
      "theme": "A replica misses heartbeats but may still be alive. When is failover safe?",
      "basis": "adapted-production",
      "selectionSources": [
        "S1",
        "S3",
        "S4"
      ],
      "technicalSources": [
        "S1",
        "S3",
        "S4"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Distributed System Fundamentals: A replica misses heartbeats but may still be alive. When is failover safe?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A replica misses heartbeats but may still be alive. When is failover safe? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A friend who does not answer may be busy, not gone. A replica stops responding during a network slowdown, while some clients can still reach it. An operator wants to promote another writer immediately. The system must not allow conflicting authoritative writes. What will you check and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Treat timeout-based failure detection as suspicion. Investigate network reachability, process health and replication progress separately, while enforcing a bounded client deadline. If a single-writer design fails over, promotion must follow its authority protocol, such as quorum-backed leadership with fencing tokens that the storage layer checks.\n\nStop or fence the old writer's authority before relying on the new one; merely removing it from one load balancer is insufficient when old connections remain. Monitor lag and explicitly choose the permitted recovery point. Exercise a partition where the old process is alive, not only a clean process crash."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "Conservative promotion protects consistency but can lengthen unavailability. A multi-writer, conflict-resolving design is an alternative for data whose operations can be merged; it changes semantics and does not remove coordination requirements for strict invariants.\n\nFollow-up trap: aggressive heartbeats improve detection speed but do not prove death. If the workload is read-only and stale reads are acceptable, you can reroute reads sooner without granting new write authority. If the old writer cannot be fenced and a strict single-writer guarantee is mandatory, stop writes rather than silently create split brain."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "Conservative promotion protects consistency but can lengthen unavailability. A multi-writer, conflict-resolving design is an alternative for data whose operations can be merged; it changes semantics and does not remove coordination requirements for strict invariants.\n\nFollow-up trap: aggressive heartbeats improve detection speed but do not prove death. If the workload is read-only and stale reads are acceptable, you can reroute reads sooner without granting new write authority. If the old writer cannot be fenced and a strict single-writer guarantee is mandatory, stop writes rather than silently create split brain."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S1, S3, S4 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
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
    "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/",
    "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/",
    "https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf",
    "https://docs.hazelcast.com/hazelcast/5.7/data-structures/fencedlock",
    "https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels"
  ],
  "editorialReviewedOn": "2026-11-17"
}
```
