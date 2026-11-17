# Research: Backend Architecture Interview Scenario Backfill

**Feature**: [spec.md](spec.md) | **Date**: 2026-11-17
**Status**: Phase 0 complete. These are design/research findings; no lesson migration or application change has been executed.

## 1. Actual content, host and validation boundaries

**Decision:** Keep all current lesson content and identities, and insert one additional scenario subsection inside each existing mastery module. Use the same native question class and stable key mechanism that the host already handles.

**Evidence:** Read the current constitution v1.2.0, manifest, complete Clean Architecture lesson, original content/host contract, Python validator and unit fixtures, browser reading fixture, actual dashboard question/control code, browser harness and prior backup model. The inventory is 15 topic leaves, six hubs, 61 foundational cards and 22 diagrams. Clean Architecture includes a diagram inside a closed mechanics disclosure, already supported by descendant rendering.

**Rationale:** The real host discovers `details.kb-question[data-recall-id]` and supplies independent confidence controls. New card kinds do not need another state engine, selectors in the application, a storage-version bump, or per-lesson shell edits.

**Alternatives considered:** A new flashcard widget duplicates existing behavior. Moving old questions or changing their keys loses evidence of preservation. Adding cards as a seventh direct article section violates the blueprint.

## 2. Separate groups with a backward-compatible marker

**Decision:** Keep original questions byte-for-byte, with missing `data-recall-kind` meaning foundational. New cards retain `class="kb-question"` and add `data-recall-kind="interview"`, with stable `interview-<semantic-kebab-key>` recall IDs. Put them inside exactly one nested `section[data-interview-scenarios]` with the required h3 title.

Each interview answer has three ordered `div[data-scenario-part]` blocks: `scenario`, `decision`, `trade-offs`, using the exact three constitutional labels in strong paragraphs. A source note inside the subsection exposes the research basis and limitation.

**Rationale:** This distinguishes the 3–5 foundational and 5–7 interview counts without modifying old question markup or the host. Strong paragraph labels render with existing CSS and are already included by PDF paragraph extraction.

**Alternatives considered:** Widening one total count permits incomplete groups. Requiring a new foundational marker changes old bytes unnecessarily. An interview-only class would bypass existing confidence attachment. Extra route/section-query values are unnecessary.

## 3. Preservation and repeatability

**Decision:** Freeze a planning-time [preservation baseline](contracts/preservation-baseline.json), including manifest/node metadata, all six hub hashes, all 15 complete source hashes, direct-section identities/hashes, original card keys/raw hashes, diagram-source hashes and runtime file hashes. Insert a single contiguous, comment-delimited scenario block immediately before the existing mastery takeaway.

Removing exactly that block must reconstruct the original complete lesson hash. A rerun replaces the existing block and reuses its keys/research mapping rather than appending another one. Implementation also snapshots original files outside the checkout before editing.

**Rationale:** Full-source reconstruction proves more than a word-count or ID-only check: it protects the first five modules, Feynman text, all original answers, references, diagrams and takeaway bytes. It works even when initial repository content has not yet been committed.

**Alternatives considered:** Only comparing total counts misses rewritten explanations. Only comparing first-five sections misses changed foundational answers and footers. Regenerating the baseline after authoring would make preservation claims meaningless.

## 4. Research performed for all exact concepts

**Decision:** Use the 39 concept-specific searches and 90 candidate production themes in [topic-sources.md](research/topic-sources.md) as initial authoring material. There are six candidate themes for each of the 15 lessons, with primary technical sources. Final authoring may retain five to seven well-supported distinct scenarios per lesson; six is a working target, not a requirement to fill weak cards.

**Finding:** Searches found applicable production/architecture guidance and interview preparation material, but did not independently establish recurrence, rankings or company provenance for these exact prompts. All current seeds are therefore **adapted production variants**, with that evidence gap disclosed. Browsing was available and used; do not describe this as unavailable research.

**Rationale:** Technical primary sources support correct architectural reasoning but cannot prove interview frequency. Official [Amazon preparation guidance](https://www.amazon.jobs/content/en/how-we-hire/interview-prep/software-development-topics) confirms broad preparation areas, not a verified list of these questions. Author interviews are also not hiring-frequency evidence.

**Alternatives considered:** Claiming the exact questions are industry-ranked from a generic preparation article would misrepresent evidence. A generic search for all architecture topics violates FR-006. Claiming sources are unavailable would contradict this research pass.

**Handoff:** Write one final research record per lesson with actual selected keys, claim-specific references, query/date record, selection basis and editorial outcome. Recheck version-sensitive vendor guidance when writing answers. Full prompts/answers and final per-card approvals belong to implementation, not this plan.

## 5. Current contract and explicit legacy isolation

**Decision:** Extend the Python article checker with a keyword-only recall profile: current default `constitution-1.2`, explicit `legacy-1.1` for retained historical unit fixtures only. Repository/CLI validation must require the current profile for the migrated batch and reject any expectation attempting to waive it. Mark the current inventory expectation explicitly as `constitution-1.2`.

Update the original content/host contract to describe the two groups and link to the supplement designed here. Convert normal positive fixtures to current-conforming examples. Keep any old-only tests explicit and prove they fail current-profile validation.

**Rationale:** Old unit samples and historical reports can remain useful without weakening acceptance for newly migrated lessons. The current validator simply counts every question together and must change. No manifest or runtime-content schema change is needed.

**Alternatives considered:** Defaulting to legacy mode lets migrations pass without scenarios. Inferring profile from marker presence rewards missing markers. A global legacy CLI bypass would undermine batch acceptance.

## 6. Counts, browser coverage and unchanged state

**Decision:** Derive active per-lesson counts and diagram counts from current source, and validate group semantics separately. Retain 61 original cards as a preservation assertion, add 75–105 interview cards, and verify actual totals (136–166). Update both the test-only fixture and actual browser harness; fixed totals of 61 questions or 22 diagrams must not remain the sole current checks.

Use existing browser controls and unchanged JSON backups to prove old/new ratings coexist. Loading a lesson may update its ordinary last visit; migration and answer/rating actions must not change status or review history/schedule.

**Rationale:** The host already keys confidence by topic ID plus recall key. No new topic/mastery denominator, automatic demotion, storage migration, or review policy is justified.

**Alternatives considered:** Hard-coding a total of 151 assumes every author must use six cards. Clearing progress to simplify testing violates the migration. Historical fixture passes are not current host acceptance.

## 7. Print and editorial acceptance

**Decision:** Use existing shared styles, source-preserving diagram rendering and synchronous print disclosures. Test all 21 routes at both hosting bases, all new cards by keyboard, both themes at 360px, backup restoration, and real PDFs of every migrated lesson from both themes (30 required outputs). Existing all-content print checks may also produce six-hub PDFs as regression extras.

Require structured validation plus human/editorial review for real constraints, decision quality, alternatives, traps and honest evidence. New cards and any diagrams must remain self-contained when references are offline.

**Rationale:** Count/label checks cannot prove that an architectural answer is correct or an interview claim is supported. Existing print hooks cover all details descendants, but expanded content must still be verified in real PDFs.

**Alternatives considered:** A bare total-count pass or fake frequency assertion is not quality evidence. Print-media emulation does not establish disclosure restoration or full printed answers.

## Resolved decisions and limits

No implementation clarification or constitutional exception remains. Planning research was delegated to three focused agents, each covering five exact concepts with independent queries and primary sources; repository integration was audited locally. Pinned runtime/test dependencies remain those of the existing dashboard. No new framework, build step, backend, hosting change or account operation is introduced.
