# Final Research: Backend for Frontend (BFF)

State: reviewed. Separate editorial/source pass completed 2026-11-17 for all six permanent scenario keys. Exact interview frequency remains unverified; adaptations are disclosed. Browser/print acceptance is recorded separately.

The JSON map records actual planning queries, implementation source checks (or explicit limitations), final selection/technical mappings and all eight per-card editorial dispositions. Vendor-specific sources are examples, not universal architectural guarantees.

```json
{
  "topicId": "1be329da-9367-4c1c-a4c8-0eff6ec862e1",
  "title": "Backend for Frontend (BFF)",
  "path": "topics/system-design/backend-architecture/communication-and-routing/backend-for-frontend.html",
  "constitutionVersion": "1.2.0",
  "researchedOn": "2026-11-17",
  "state": "reviewed",
  "searches": [
    {
      "query": "\"Backend for Frontend\" interview questions scenario",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "\"Backend for Frontend\" interview \"scenario\" mobile web",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    },
    {
      "query": "site.samnewman.io patterns architectural bff backends for frontends",
      "date": "2026-11-17",
      "result": "success; concept-specific planning research found technical guidance; exact prompt recurrence unverified"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Sam Newman: Backends For Frontends",
      "url": "https://samnewman.io/patterns/architectural/bff/",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    },
    {
      "id": "S2",
      "title": "Microsoft: Backends for Frontends",
      "url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends",
      "roles": [
        "technical-primary"
      ],
      "checkedOn": "2026-11-17",
      "supportRationale": "Primary architectural or product guidance used for the specifically mapped decisions; not evidence of hiring frequency."
    }
  ],
  "scenarios": [
    {
      "key": "interview-mobile-web-conflicting-payloads",
      "theme": "Mobile needs a tiny payload while desktop needs a rich dashboard. Should both keep one general API?",
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
          "rationale": "Backend for Frontend (BFF): Mobile needs a tiny payload while desktop needs a rich dashboard. Should both keep one general API?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Mobile needs a tiny payload while desktop needs a rich dashboard. Should both keep one general API? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A takeaway counter and a banquet hall need different serving arrangements from the same kitchen. Desktop requests rich reports, while mobile has limited bandwidth and needs a small combined summary. One general endpoint has growing conditionals and conflicting release demands. What boundary will you choose?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Introduce experience-specific backends when the difference is sustained enough to justify ownership: a mobile BFF can aggregate and shape a small response while the web BFF serves its richer composition. Keep authoritative pricing, permissions and inventory decisions in shared domain services, not copied into each experience backend.\n\nMeasure payload, round trips and team release friction before splitting. Give each BFF an owner, bounded downstream deadlines and contract tests with its frontend. It may sit behind a shared gateway that handles common edge concerns. Tailoring presentation does not require creating a new business-data authority."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain client-focused contracts and more independent UI delivery, but maintain additional deployables, composition and compatibility checks. A single API with explicit projections is a viable alternative when differences are small and team coordination remains easy.\n\nFollow-up trap: copying all backend logic into each BFF creates divergent business rules. If mobile and web converge on the same experience and ownership, reconsider whether two BFFs still pay their cost rather than retaining the split solely because the device labels differ."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain client-focused contracts and more independent UI delivery, but maintain additional deployables, composition and compatibility checks. A single API with explicit projections is a viable alternative when differences are small and team coordination remains easy.\n\nFollow-up trap: copying all backend logic into each BFF creates divergent business rules. If mobile and web converge on the same experience and ownership, reconsider whether two BFFs still pay their cost rather than retaining the split solely because the device labels differ."
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
      "key": "interview-ios-android-ownership-boundary",
      "theme": "iOS and Android need nearly identical data but have separate teams. One mobile BFF or two?",
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
          "rationale": "Backend for Frontend (BFF): iOS and Android need nearly identical data but have separate teams. One mobile BFF or two?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: iOS and Android need nearly identical data but have separate teams. One mobile BFF or two? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Two counters serving the same meal may share a kitchen, unless independent menus keep colliding. iOS and Android currently need the same composition, but release separately and have different team ownership. A blanket one-BFF-per-device rule would create immediate duplication. What will you choose and why?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Start by evaluating experience and ownership coupling rather than counting device types. Use one mobile BFF if contracts and changes remain genuinely aligned with a clear ownership agreement. Split when incompatible release needs, composition or accountability repeatedly block one another, not merely because both platforms exist.\n\nTrack which changes require coordination and agree on compatibility support for old app versions. Shared business services remain common regardless of the BFF count. If teams choose separate BFFs, let each own its experience contract and avoid a shared runtime dependency that forces their releases back together."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "A shared BFF reduces duplicate operations and composition but requires coordinated governance. Separate BFFs provide autonomy at the cost of repeated presentation code and additional operations; both are legitimate under different change patterns.\n\nFollow-up trap: two repositories backed by one mandatory shared-release library may retain lockstep coupling. If Android introduces an offline-specific synchronization model that iOS does not need, reevaluate the boundary. If only branding differs, separate deployments may offer little benefit."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "A shared BFF reduces duplicate operations and composition but requires coordinated governance. Separate BFFs provide autonomy at the cost of repeated presentation code and additional operations; both are legitimate under different change patterns.\n\nFollow-up trap: two repositories backed by one mandatory shared-release library may retain lockstep coupling. If Android introduces an offline-specific synchronization model that iOS does not need, reevaluate the boundary. If only branding differs, separate deployments may offer little benefit."
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
      "key": "interview-shared-library-release-coupling",
      "theme": "Two BFFs duplicate aggregation code. Should you force both onto one shared library?",
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
          "rationale": "Backend for Frontend (BFF): Two BFFs duplicate aggregation code. Should you force both onto one shared library?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Two BFFs duplicate aggregation code. Should you force both onto one shared library? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Sharing a recipe helps until every restaurant must change its menu whenever the recipe changes. Web and mobile BFFs duplicate a little aggregation, and a proposed common library would require coordinated upgrades for every screen change. What will you share?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Separate stable technical helpers from experience-specific composition and authoritative business rules. Share low-volatility utilities only when their versioning and ownership do not erase independent releases. Keep changing screen orchestration local, accepting modest duplication where its meanings may diverge.\n\nMove genuine business policy to its domain owner behind a contract rather than copying it into a common BFF library. Track dependency upgrades and compare the cost of duplication with the cost of coordination. Extract a library after stable common behavior emerges, not just because two code blocks initially look similar."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You preserve frontend autonomy but may maintain some duplicated presentation code. A versioned shared library is a viable alternative for truly stable common functionality with independent adoption, and a shared service can fit a cohesive runtime capability with a clear availability budget.\n\nFollow-up trap: a shared service for every helper adds network coupling without creating useful ownership. If duplicated code controls financial eligibility, it is not harmless presentation duplication; centralize the authoritative rule and keep both BFFs as consumers."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You preserve frontend autonomy but may maintain some duplicated presentation code. A versioned shared library is a viable alternative for truly stable common functionality with independent adoption, and a shared service can fit a cohesive runtime capability with a clear availability budget.\n\nFollow-up trap: a shared service for every helper adds network coupling without creating useful ownership. If duplicated code controls financial eligibility, it is not harmless presentation duplication; centralize the authoritative rule and keep both BFFs as consumers."
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
      "key": "interview-business-rule-drift-between-bffs",
      "theme": "Web and mobile calculate different discounts. Which backend is authoritative?",
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
          "rationale": "Backend for Frontend (BFF): Web and mobile calculate different discounts. Which backend is authoritative?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: Web and mobile calculate different discounts. Which backend is authoritative? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "Two waiters should not invent different prices for the same order. Web and mobile BFFs independently calculate customer discounts, and releases have diverged. The business needs one auditable decision while screens remain different. What will you change?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Move discount eligibility and calculation to the pricing/order domain owner, with explicit inputs and an authoritative result. Both BFFs request that decision and shape its presentation without reimplementing the rule. Reconcile existing divergent behavior using agreed business examples and preserve quote/version identity where a later purchase must match an earlier price.\n\nAdd contract/integration checks for both BFFs and ensure object/tenant authorization remains enforced. Display-only formatting can stay local; rounding that changes the payable amount belongs in the authoritative financial decision, not in a device-specific formatter."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You gain consistent policy and auditability, but depend on a shared domain capability and must budget its latency/availability. A locally cached quote can be a viable alternative when its version, expiry and acceptance semantics are explicitly supported.\n\nFollow-up trap: returning a raw discount percentage and letting each BFF reconstruct the final amount may retain divergence. If regional rules genuinely differ, pass the relevant jurisdiction/context to the authority and model that difference explicitly rather than treating one BFF's divergent implementation as accidental customization."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You gain consistent policy and auditability, but depend on a shared domain capability and must budget its latency/availability. A locally cached quote can be a viable alternative when its version, expiry and acceptance semantics are explicitly supported.\n\nFollow-up trap: returning a raw discount percentage and letting each BFF reconstruct the final amount may retain divergence. If regional rules genuinely differ, pass the relevant jurisdiction/context to the authority and model that difference explicitly rather than treating one BFF's divergent implementation as accidental customization."
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
      "key": "interview-old-mobile-client-compatibility",
      "theme": "A mobile app version must keep working for six months. How will the BFF evolve safely?",
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
          "rationale": "Backend for Frontend (BFF): A mobile app version must keep working for six months. How will the BFF evolve safely?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: A mobile app version must keep working for six months. How will the BFF evolve safely? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A printed menu cannot update as quickly as the kitchen software. An installed mobile app may remain active for six months, while backend services change weekly. The BFF must support the old app contract without freezing the whole backend. What will you implement?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Treat the BFF as a compatibility boundary: evolve its public contract additively where safe and translate changing domain-service contracts behind it. Keep meaningful old behavior during a documented support window, with versioned endpoints or negotiated capabilities when semantics cannot remain compatible. Test representative supported app contracts against current composition.\n\nMeasure active versions and infrequent usage before retirement. Keep authorization and critical business rules current at the domain owner; old client support does not justify accepting an insecure operation. Communicate minimum-version and sunset policy explicitly, including what a user sees when support ends."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You decouple domain releases from installed-client timing, but maintain adapters, old contract tests and support windows. A forced client upgrade is a viable alternative for a tightly managed internal app where availability and deployment policy permit it.\n\nFollow-up trap: schema compatibility does not preserve behavior if a default or unit changes. If an urgent security issue makes an old operation unsafe, revoke or narrow that capability and provide a controlled upgrade/error path rather than promising unlimited backward compatibility at the expense of security."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You decouple domain releases from installed-client timing, but maintain adapters, old contract tests and support windows. A forced client upgrade is a viable alternative for a tightly managed internal app where availability and deployment policy permit it.\n\nFollow-up trap: schema compatibility does not preserve behavior if a default or unit changes. If an urgent security issue makes an old operation unsafe, revoke or narrow that capability and provide a controlled upgrade/error path rather than promising unlimited backward compatibility at the expense of security."
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
      "key": "interview-single-frontend-extra-hop",
      "theme": "One simple frontend already has a suitable API. Does adding a BFF solve a real problem?",
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
          "rationale": "Backend for Frontend (BFF): One simple frontend already has a suitable API. Does adding a BFF solve a real problem?"
        },
        "distinctness": {
          "status": "pass",
          "rationale": "Separate pass compared all six prompts in this lesson: One simple frontend already has a suitable API. Does adding a BFF solve a real problem? tests its own boundary/failure, with a distinct changed-assumption response; it is not counted as a definition or a renamed foundational prompt."
        },
        "production-prompt": {
          "status": "pass",
          "rationale": "A small shop may not need a receptionist between the customer and the only counter. A single frontend uses two stable backend operations with acceptable latency and payload. A proposed BFF would forward both unchanged and introduce another deployment. What will you recommend?"
        },
        "direct-answer": {
          "status": "pass",
          "rationale": "Keep the simpler path until there is a concrete experience or ownership problem for a BFF to solve. Measure round trips, payload mismatch, security responsibilities and release friction. A reverse proxy or shared gateway may already handle the required edge behavior without another application composition service.\n\nKeep frontend/backend contracts clear and tests representative so later evolution remains possible. If future screens require substantial composition or a second experience creates conflicting demands, introduce the BFF at that evidence-backed boundary. Avoid turning the absence of a BFF into permission for frontend code to own business invariants."
        },
        "decision-costs": {
          "status": "pass",
          "rationale": "You avoid an extra network hop and operational owner, while accepting that the client may coordinate the current small set of calls. A BFF is a viable alternative when server-side token handling, significant aggregation or frontend-team autonomy provides a concrete benefit.\n\nFollow-up trap: a new security requirement may justify a server-side boundary even with one UI. If credentials or trust policy now require that component, reevaluate the decision and design its responsibilities explicitly. The right answer follows actual constraints, not a mandatory count of architectural boxes."
        },
        "follow-up": {
          "status": "pass",
          "rationale": "You avoid an extra network hop and operational owner, while accepting that the client may coordinate the current small set of calls. A BFF is a viable alternative when server-side token handling, significant aggregation or frontend-team autonomy provides a concrete benefit.\n\nFollow-up trap: a new security requirement may justify a server-side boundary even with one UI. If credentials or trust policy now require that component, reevaluate the decision and design its responsibilities explicitly. The right answer follows actual constraints, not a mandatory count of architectural boxes."
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
    }
  ],
  "publicDisclosure": "Researched 2026-11-17. These scenarios adapt documented production problems and architectural guidance. Interview frequency, rankings and company provenance for these exact prompts were not independently verified. Numeric budgets and organization details are author-created assumptions. Web search was available and used for this concept; primary sources support the technical reasoning, not a claim that these prompts recur in interviews.",
  "sourceNoteUrls": [
    "https://samnewman.io/patterns/architectural/bff/",
    "https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends"
  ],
  "editorialReviewedOn": "2026-11-17"
}
```
