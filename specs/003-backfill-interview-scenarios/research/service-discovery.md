# Final Research: Service Discovery

State: reviewed. Separate editorial/source pass completed 2026-11-17 for all six permanent scenario keys. Exact interview frequency remains unverified; adaptations are disclosed. Browser/print acceptance is recorded separately.

The JSON map records actual planning queries, implementation source checks (or explicit limitations), final selection/technical mappings and all eight per-card editorial dispositions. Vendor-specific sources are examples, not universal architectural guarantees.

```json
{
  "topicId": "5522e024-f6dd-471e-a3e4-41d0a60a5d2f",
  "title": "Service Discovery",
  "path": "topics/system-design/backend-architecture/infrastructure-and-multi-tenancy/service-discovery.html",
  "constitutionVersion": "1.2.0",
  "researchedOn": "2026-11-17",
  "state": "reviewed",
  "searches": [
    {
      "query": "site.kubernetes.io service discovery dns service endpoints distributed service discovery",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "\"Service Discovery\" interview stale DNS health checks scenario",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "site.kubernetes.io docs dns pods services readiness terminating endpoints",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "site.consul.io docs discovery health checks DNS caching stale reads service discovery",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Kubernetes: Service",
      "url": "https://kubernetes.io/docs/concepts/services-networking/service/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S2",
      "title": "Kubernetes: Pod and endpoint termination flow",
      "url": "https://kubernetes.io/docs/tutorials/services/pods-and-endpoint-termination-flow/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S3",
      "title": "HashiCorp: Configure Consul DNS behavior",
      "url": "https://developer.hashicorp.com/consul/docs/discover/dns/configure",
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
    }
  ],
  "scenarios": [
    {
      "key": "interview-terminating-endpoints-drain",
      "theme": "Deployments still send requests to terminating instances. What does service discovery need besides registration?",
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
          "rationale": "Service Discovery: Deployments still send requests to terminating instances. What does service discovery need besides registration?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Deployments still send requests to terminating instances. What does service discovery need besides registration? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Removing a shop from the directory does not stop a customer already walking through its door. During rolling deployment, requests hit terminating instances and fail. Endpoint updates and existing connections do not disappear instantly. What shutdown and readiness sequence will you verify?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Inspect the actual endpoint conditions, readiness changes, load-balancer propagation and open connection behavior. Stop accepting new work through the platform's supported readiness/drain mechanism, allow in-flight requests to finish within a bounded grace period, and ensure the process handles termination signals correctly. Tune the sequence from measured propagation rather than assuming deregistration is instantaneous.\n\nFor Kubernetes, verify the deployed version's EndpointSlice terminating/ready/serving behavior and the data plane's interpretation. Test long-lived connections, keep-alive clients and termination under load. Make retries safe where they are allowed, because a lost reply during shutdown can still hide a completed effect."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "Graceful draining reduces rollout errors but takes time and temporarily retains old capacity. Immediate termination is a viable alternative for disposable idempotent work whose interruption/retry semantics are acceptable; it is not a default for every request.\n\nFollow-up trap: passing a liveness check does not mean an instance should receive new traffic. If a hard node failure prevents draining, rely on bounded deadlines, safe retries and recovery rather than claiming the graceful path covers every outage. Registration, readiness and active-connection lifecycle are separate concerns."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "Graceful draining reduces rollout errors but takes time and temporarily retains old capacity. Immediate termination is a viable alternative for disposable idempotent work whose interruption/retry semantics are acceptable; it is not a default for every request.\n\nFollow-up trap: passing a liveness check does not mean an instance should receive new traffic. If a hard node failure prevents draining, rely on bounded deadlines, safe retries and recovery rather than claiming the graceful path covers every outage. Registration, readiness and active-connection lifecycle are separate concerns."
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
      "key": "interview-negative-dns-cache-new-service",
      "theme": "A new service is registered, yet clients keep receiving name-not-found. Where will you look?",
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
          "rationale": "Service Discovery: A new service is registered, yet clients keep receiving name-not-found. Where will you look?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A new service is registered, yet clients keep receiving name-not-found. Where will you look? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A visitor keeps using yesterday's note saying the shop does not exist. The registry contains a newly deployed service, but some clients still fail DNS resolution. A direct registry query succeeds. What will you inspect before restarting every client?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Trace the complete resolution path: client/runtime cache, local resolver, forwarding DNS cache and registry answer. Check negative caching as well as positive TTLs, and compare fully qualified queries from the failing environment. A registry update cannot invalidate every downstream cache automatically.\n\nUse the platform's documented DNS behavior and configure suitable cache lifetimes and retry/backoff for transient discovery misses. Observe actual answers and TTLs at each layer. Ensure the service is healthy and in the expected namespace/domain before blaming caching; an answer can be correctly negative for a wrongly qualified name."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You avoid unnecessary restarts and make rollout discovery predictable, but manage a trade-off between freshness and DNS load. A controlled readiness gate that waits for expected resolution is a viable alternative for deployment sequencing; it does not replace ongoing failure handling.\n\nFollow-up trap: setting every TTL to zero does not force all client libraries to behave identically and can overload resolvers. If the application maintains long-lived resolved connections, refreshing DNS alone may not rotate them. Verify the client's connection lifecycle as well as the DNS cache."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You avoid unnecessary restarts and make rollout discovery predictable, but manage a trade-off between freshness and DNS load. A controlled readiness gate that waits for expected resolution is a viable alternative for deployment sequencing; it does not replace ongoing failure handling.\n\nFollow-up trap: setting every TTL to zero does not force all client libraries to behave identically and can overload resolvers. If the application maintains long-lived resolved connections, refreshing DNS alone may not rotate them. Verify the client's connection lifecycle as well as the DNS cache."
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
      "key": "interview-stale-registry-during-outage",
      "theme": "The discovery control plane is unavailable. May clients keep using cached endpoints?",
      "basis": "adapted-production",
      "selectionSources": [
        "S3",
        "S4"
      ],
      "technicalSources": [
        "S3",
        "S4"
      ],
      "supportedInterviewClaim": "none",
      "assumptions": "Scenario organization, numbers, deadlines and proposed implementation details are author-created; sources support underlying mechanics, not an observed company incident or exact interview prompt.",
      "limitations": "Exact recurrence/rank/company provenance unverified; vendor examples do not imply universal defaults.",
      "editorial": {
        "concept-specificity": {
          "status": "pass",
          "rationale": "Service Discovery: The discovery control plane is unavailable. May clients keep using cached endpoints?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: The discovery control plane is unavailable. May clients keep using cached endpoints? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "An old address book may be more useful than none, but some shops may have closed. A registry disruption prevents fresh reads while existing service instances still run. Read traffic can tolerate some stale endpoint information; a sensitive writer endpoint cannot be guessed safely. What policy will you choose?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Separate discovery availability from endpoint authority. Permit bounded last-known-good endpoint use for operations whose risk allows it, with connection deadlines, health observations and a maximum staleness policy. Retain an explicit failure path when no usable target remains. Do not infer that a cached endpoint still holds exclusive write authority.\n\nCheck the discovery product's consistency/stale-read settings and caching chain, including how quickly unhealthy or removed instances disappear. Exercise a control-plane outage while data-plane traffic continues. Report degraded freshness so operators can distinguish resilient cached operation from a healthy registry."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You keep some traffic working during a control-plane incident but may contact stale or unhealthy targets. Failing closed on fresh discovery is a viable alternative where stale routing threatens correctness or security.\n\nFollow-up trap: successful TCP connection is not proof that the server is the current leader. If an endpoint performs exclusive writes, enforce authority with the service's real leadership/fencing protocol or an authoritative proxy. Service discovery locates candidates; it does not supply the business consistency guarantee."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You keep some traffic working during a control-plane incident but may contact stale or unhealthy targets. Failing closed on fresh discovery is a viable alternative where stale routing threatens correctness or security.\n\nFollow-up trap: successful TCP connection is not proof that the server is the current leader. If an endpoint performs exclusive writes, enforce authority with the service's real leadership/fencing protocol or an authoritative proxy. Service discovery locates candidates; it does not supply the business consistency guarantee."
        },
        "evidence": {
          "status": "pass",
          "rationale": "Separate pass checked mapped primary sources S3, S4 against this decision and its limits. All budgets/organizations are author assumptions; no exact interview-frequency/company claim is made."
        },
        "full-delivery": {
          "status": "pass",
          "rationale": "Three complete prose parts plus a valid decision-path diagram; native closed card uses existing shared controls."
        }
      }
    },
    {
      "key": "interview-headless-service-client-balancing",
      "theme": "A headless service returns several addresses. Who chooses one and handles failure?",
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
          "rationale": "Service Discovery: A headless service returns several addresses. Who chooses one and handles failure?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A headless service returns several addresses. Who chooses one and handles failure? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A directory gives you several shop addresses instead of one receptionist. A Kubernetes headless Service resolves to multiple endpoints, and the application repeatedly chooses the first address. Traffic is uneven and a failed endpoint causes repeated errors. What responsibilities moved to the client?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Treat the returned addresses as candidates rather than a complete load-balancing policy. Use a client or proxy that refreshes discovery, selects endpoints appropriately, bounds connection attempts and handles target failure without unsafe retrying of effects. Verify how the actual protocol/client consumes multiple DNS records and reuses connections.\n\nChoose headless discovery deliberately when direct endpoint identity is needed, such as a stateful protocol. If ordinary service-level balancing is sufficient, a normal virtual service address may provide a simpler abstraction. Check endpoint readiness and topology rather than assuming every returned address is equally suitable."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain direct instance visibility and protocol-specific control but take on balancing, caching and failure behavior. A standard ClusterIP Service or supported proxy is a viable alternative when clients should not manage individual instances.\n\nFollow-up trap: DNS round-robin is not per-request fair balancing, especially with connection pools. If the protocol requires a specific shard or leader, random selection is wrong; route using that protocol's authoritative membership/role information rather than treating every discovered instance as interchangeable."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain direct instance visibility and protocol-specific control but take on balancing, caching and failure behavior. A standard ClusterIP Service or supported proxy is a viable alternative when clients should not manage individual instances.\n\nFollow-up trap: DNS round-robin is not per-request fair balancing, especially with connection pools. If the protocol requires a specific shard or leader, random selection is wrong; route using that protocol's authoritative membership/role information rather than treating every discovered instance as interchangeable."
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
      "key": "interview-namespace-name-resolution",
      "theme": "The same short service name reaches different backends in two environments. How will you debug it?",
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
          "rationale": "Service Discovery: The same short service name reaches different backends in two environments. How will you debug it?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: The same short service name reaches different backends in two environments. How will you debug it? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Two towns can each have a Main Street. A client calling inventory works in one namespace but reaches a different service or fails in another. The application config uses only the short name. What will you inspect and make explicit?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Inspect the client's namespace, resolver search domains, cluster/domain configuration and the actual fully qualified answer. Compare the intended target with the resolved endpoint set from inside each workload's network context. Use the correct qualified service name for cross-namespace communication instead of assuming a short name has global meaning.\n\nKeep environment-specific names in controlled configuration and validate them during deployment. Verify network policy, ports and service selectors after name resolution succeeds; a correct DNS answer does not prove connectivity or authorization. Add a diagnostic that reports the resolved target safely without leaking credentials."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain predictable routing and clearer diagnostics, but maintain explicit environment configuration. Short names remain a viable convenient alternative for intentionally local same-namespace dependencies when that scope is documented.\n\nFollow-up trap: hard-coding instance IPs bypasses discovery and breaks when instances change. If the intended boundary is cross-cluster rather than cross-namespace, a local service FQDN is insufficient; use the platform's supported cross-cluster discovery/routing design and its security model."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain predictable routing and clearer diagnostics, but maintain explicit environment configuration. Short names remain a viable convenient alternative for intentionally local same-namespace dependencies when that scope is documented.\n\nFollow-up trap: hard-coding instance IPs bypasses discovery and breaks when instances change. If the intended boundary is cross-cluster rather than cross-namespace, a local service FQDN is insufficient; use the platform's supported cross-cluster discovery/routing design and its security model."
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
      "key": "interview-vm-without-discovery-sdk",
      "theme": "A VM client needs changing service endpoints without a discovery SDK. Which integration fits?",
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
          "rationale": "Service Discovery: A VM client needs changing service endpoints without a discovery SDK. Which integration fits?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A VM client needs changing service endpoints without a discovery SDK. Which integration fits? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A visitor can use an ordinary phone directory without learning the registry's private filing system. A legacy VM application must call changing service instances, but its release process cannot adopt a discovery SDK. It can use standard DNS and a configured proxy. What will you choose?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Use a supported discovery-facing DNS interface or a local/server-side proxy that resolves membership for the legacy client. Choose based on the client's DNS refresh, connection reuse and protocol behavior. Keep service identity stable while the discovery/proxy layer tracks changing endpoints, and verify authentication and network access from the VM.\n\nTest endpoint removal, DNS failure and a proxy restart under real connection pooling. Document health filtering and cache staleness rather than assuming a DNS answer is a live-health guarantee. An SDK is one integration option, not the definition of service discovery."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You avoid invasive legacy code changes and centralize discovery mechanics, but rely on DNS caching behavior or an additional proxy hop/failure domain. An SDK is a viable alternative when fine-grained metadata, watch semantics or protocol-specific routing justify the client change.\n\nFollow-up trap: a very long-lived connection can keep using a removed instance after a DNS refresh. If the application needs immediate revocation or strict per-instance authorization, use a suitable enforced proxy/security boundary and explicit connection draining rather than relying on TTL alone."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You avoid invasive legacy code changes and centralize discovery mechanics, but rely on DNS caching behavior or an additional proxy hop/failure domain. An SDK is a viable alternative when fine-grained metadata, watch semantics or protocol-specific routing justify the client change.\n\nFollow-up trap: a very long-lived connection can keep using a removed instance after a DNS refresh. If the application needs immediate revocation or strict per-instance authorization, use a suitable enforced proxy/security boundary and explicit connection draining rather than relying on TTL alone."
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
    "https://kubernetes.io/docs/concepts/services-networking/service/",
    "https://kubernetes.io/docs/tutorials/services/pods-and-endpoint-termination-flow/",
    "https://developer.hashicorp.com/consul/docs/discover/dns/configure",
    "https://docs.hazelcast.com/hazelcast/5.7/data-structures/fencedlock"
  ],
  "editorialReviewedOn": "2026-11-17"
}
```
