# Feature Specification: Backfill Backend Architecture Interview Scenarios

**Feature Branch**: `main` (no branch hook configured; feature identity is `003-backfill-interview-scenarios`)

**Created**: 2026-11-17

**Status**: Implemented and verified — all 15 lessons pass constitution v1.2.0 migration acceptance

**Input**: User description: "Backfill all 15 existing lesson HTML files under topics/system-design/backend-architecture/ to match our updated constitution."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Practice production decisions in every existing lesson (Priority: P1)

As a learner, I can finish any existing Backend Architecture lesson and practice realistic interview decisions about that exact concept, with complete answers that explain the reasoning and its limits.

**Why this priority**: The requested migration is complete only when every existing lesson offers the expanded mastery practice required by constitution v1.2.0.

**Independent Test**: Review any migrated lesson in isolation. Its original learning story and foundational recall remain intact, followed within the mastery module by five to seven complete scenario cards with the required title, prompts, and answer parts.

**Acceptance Scenarios**:

1. **Given** any of the 15 in-scope lessons, **When** I reach Active Recall & Mastery Check, **Then** the Feynman prompt and original foundational questions remain and a dedicated "Tricky & Most-Asked Interview Scenarios" subsection contains five to seven additional questions.
2. **Given** a scenario card, **When** I reveal its answer, **Then** I find the production situation and constraints, an explicit recommended architectural/debugging decision with reasoning, and the costs, alternative, follow-up traps, and changed-assumption response.
3. **Given** the full set in one lesson, **When** I compare the prompts, **Then** they test materially distinct applied decisions or failure situations about that concept, rather than definitions or superficial rewrites.
4. **Given** the full batch, **When** completion is reviewed, **Then** all 15 named files are independently accounted for and none is substituted with a summary, placeholder, or another lesson's generic scenario set.

---

### User Story 2 - Understand the evidence behind interview practice (Priority: P1)

As a learner, I can see why these scenarios were selected and distinguish reported interview patterns from informed production adaptations.

**Why this priority**: The subsection's name must not turn an unsupported claim into supposed evidence of interview frequency or technical correctness.

**Independent Test**: Audit a lesson's research record and associated source note without running the dashboard. Trace every scenario to its selection basis, verify its technical references, and check that frequency/company claims match the evidence.

**Acceptance Scenarios**:

1. **Given** web search is available, **When** a lesson's new question set is selected, **Then** concept-specific searches inform selection and the record identifies relevant sources, the research date, and how each scenario relates to the findings.
2. **Given** a scenario is adapted from a production pattern, **When** I inspect its source note, **Then** it is identified as an adaptation and is not claimed to be a verified company question or measured ranking.
3. **Given** search is unavailable, fails, or yields insufficient interview evidence, **When** the lesson is delivered, **Then** the specific limitation and inferred/adapted basis are disclosed, while the complete five-to-seven-card set is still present.
4. **Given** an answer recommends an architectural or debugging action, **When** its correctness is reviewed, **Then** applicable technical claims are checked against primary technical documentation or original architecture references, separately from evidence of interview frequency.

---

### User Story 3 - Keep my existing learning record while adding new practice (Priority: P1)

As a returning learner, I retain my existing understanding, bookmarks, review schedule, and confidence ratings after lessons gain new scenarios.

**Why this priority**: A content backfill must not reset months of learning or silently redefine completion.

**Independent Test**: Load a pre-backfill learning record against migrated content, including an older exported backup. Verify preserved topic/question identities, original confidence and review values, initially unrated new questions, and ordinary behavior after an explicit new rating.

**Acceptance Scenarios**:

1. **Given** stored topic statuses, review history and foundational confidence, **When** the migrated lessons become available, **Then** their immutable identities, routes and saved records still match; existing Mastered topics remain Mastered and the mastery denominator remains 15.
2. **Given** a newly added scenario, **When** I first open its lesson, **Then** its answer is hidden and it has no fabricated prior rating; revealing or rating it does not mark the lesson Mastered or complete a review.
3. **Given** two scenario cards, **When** I reveal both using the keyboard and close one, **Then** the other remains open and each has independent Hard/Good/Easy confidence that survives reload and backup restoration.
4. **Given** an older backup without the new question keys, **When** I restore it through the existing confirmed-replacement flow, **Then** its recorded values restore correctly and the new scenarios remain unrated until I act.

---

### User Story 4 - Read and verify the expanded lessons everywhere the dashboard works (Priority: P2)

As a learner and maintainer, I can use the full scenario sets on desktop/mobile and in printed copies, and acceptance checks identify incomplete migrations.

**Why this priority**: Complete authored answers have value only when they work in the actual host and remain protected from future omissions.

**Independent Test**: Exercise each migrated lesson through the real dashboard, run the updated content checks against conforming and intentionally incomplete cases, and print every updated lesson from both themes.

**Acceptance Scenarios**:

1. **Given** healthy hosting and rendering dependencies, **When** I navigate every hub and migrated lesson at a site root and repository subdirectory, **Then** full content and diagrams load without unexpected console/rendering errors and existing links still work.
2. **Given** a migrated lesson in either theme at a 360-pixel viewport, **When** I read, reveal answers, and rate confidence, **Then** controls remain labeled and reachable by keyboard, with no page-wide overflow.
3. **Given** an expanded lesson with closed answers, **When** I print it from either theme, **Then** all original explanations and all new scenario/decision/trade-off/trap content are included, with readable diagrams/tables and disclosure states restored afterward.
4. **Given** a lesson missing the dedicated subsection, a required answer part, or the allowed scenario count, **When** acceptance is checked, **Then** it fails explicitly; increasing a single undifferentiated recall limit does not qualify it as compliant.

### Edge Cases

- A lesson already has four or five foundational cards, including some what-if questions. Preserve all of them and add five to seven separately identified interview scenarios; existing cards do not count twice.
- An interview theme overlaps a foundational concept. The new card must introduce a materially different production constraint/decision, not merely rename the old prompt.
- Two related architecture concepts share a broad problem. Each lesson's scenarios must test that lesson's specific responsibility, boundary, or trade-off rather than reuse a generic set.
- Interview sources establish a topic pattern but not the exact production numbers or prompt. Mark invented constraints as an adaptation and support the technical reasoning separately.
- A source makes an unsupported company/frequency claim, contradicts primary documentation, or becomes unavailable. Do not repeat it as fact; find appropriate evidence or disclose the gap without dropping required content.
- A lesson originally has five foundational cards (DDD). Retain all five; do not trim it to a common four-card baseline.
- New keys collide with a foundational question or another scenario in the same lesson. Reject the duplicate before delivery.
- An older backup has no scenario ratings, or a newer backup has question keys not currently visible. Preserve existing restoration/unknown-key behavior and never invent ratings.
- A topic was Mastered before the additional practice existed. Do not reset its status, completion percentage or review schedule; new practice is available for an intentional revisit.
- Added explanations need more diagrams. Preserve existing diagrams and satisfy applicable constitutional visualization requirements without hard-coding the old global diagram count as the new total.
- A validator or browser check still treats every recall card as one three-to-five group or assumes the total is 61. Update the current acceptance contract to distinguish the two groups and count the expanded inventory correctly.
- Legacy test fixtures describe earlier content. They must be identified explicitly as legacy where retained, rather than silently exempting migrated lessons from the new standard.
- Published hub overviews are not six-module lessons. The six existing hubs remain navigation/regression targets, not additional scenario-authoring targets.

## Requirements *(mandatory)*

### Migration Scope

The exact content scope is the following 15 existing topic leaves under `topics/system-design/backend-architecture/`. File paths below are relative to that directory. The current inventory contains 61 foundational questions; these are a preservation baseline, not the post-migration total.

| Topic | Existing relative lesson path | Foundational cards to retain |
| --- | --- | ---: |
| Distributed System Fundamentals | `core-system-topologies/distributed-system-fundamentals.html` | 4 |
| Monolithic Architecture | `core-system-topologies/monolithic-architecture.html` | 4 |
| Modular Monolith | `core-system-topologies/modular-monolith.html` | 4 |
| Service-Oriented Architecture (SOA) | `core-system-topologies/service-oriented-architecture.html` | 4 |
| Microservices Architecture | `core-system-topologies/microservices-architecture.html` | 4 |
| Layered Architecture | `code-and-domain-organization/layered-architecture.html` | 4 |
| Clean Architecture | `code-and-domain-organization/clean-architecture.html` | 4 |
| Hexagonal Architecture | `code-and-domain-organization/hexagonal-architecture.html` | 4 |
| Domain-Driven Design (DDD) | `code-and-domain-organization/domain-driven-design.html` | 5 |
| Event-Driven Architecture | `communication-and-routing/event-driven-architecture.html` | 4 |
| API Gateway Pattern | `communication-and-routing/api-gateway-pattern.html` | 4 |
| Backend for Frontend (BFF) | `communication-and-routing/backend-for-frontend.html` | 4 |
| Service Discovery | `infrastructure-and-multi-tenancy/service-discovery.html` | 4 |
| Service Mesh | `infrastructure-and-multi-tenancy/service-mesh.html` | 4 |
| Multi-Tenant Architecture | `infrastructure-and-multi-tenancy/multi-tenant-architecture.html` | 4 |

### Functional Requirements

- **FR-001**: The backfill MUST migrate every lesson in the scope table and provide a per-lesson completion record. Each of the 15 lessons MUST receive its own authoring task and independent content acceptance during the subsequent task/implementation phases.
- **FR-002**: Each lesson MUST contain exactly one dedicated subsection titled **Tricky & Most-Asked Interview Scenarios** within its existing sixth mastery module, containing five to seven additional scenario questions. The six-module top-level blueprint MUST remain intact.
- **FR-003**: The existing first five modules, Feynman prompt, foundational question prompts/answers, and their stable keys MUST be retained. All 61 original foundational questions MUST remain complete; additions to mastery and associated research/source notes MUST NOT replace or summarize existing lesson content.
- **FR-004**: Every new scenario MUST be its own native `<details>` card with a descriptive `<summary>`. Its expanded answer MUST contain three clearly labeled parts using the constitutional names: **The Scenario & Constraint**, **The Direct Answer & Architectural Decision**, and **Key Trade-Offs & Follow-Up Traps**.
- **FR-005**: Each scenario MUST describe a real-world production situation and explicit constraint/failure, ask what the learner would do and why, provide a recommended action with reasoning and actionable architectural/debugging steps, and explain gains/costs, at least one viable alternative, one follow-up trap, and a changed-assumption response. Distinct cards MUST test materially distinct situations/decisions; definition-only questions and superficial paraphrases MUST NOT satisfy the count.
- **FR-006**: For each of the 15 exact concepts, authors MUST use available web search before selecting scenarios, targeting relevant system-design, debugging and architecture trade-off interview patterns. Searches and technical verification MUST address that concept; one general architecture search MUST NOT stand in for research on every lesson.
- **FR-007**: Each lesson MUST expose selection-source links next to the relevant cards or in a clearly associated source note. Applicable technical answer claims MUST be verified with primary technical documentation or original architecture references; technical correctness evidence alone MUST NOT be described as proof of interview frequency.
- **FR-008**: The research record MUST map every scenario to its selection basis and supporting sources, identify the concept and research date, and distinguish reported recurring interview patterns from adapted/inferred production variants. Frequency/ranking/company-specific claims MUST NOT exceed what the evidence establishes.
- **FR-009**: If web search is genuinely unavailable, fails, or returns insufficient interview evidence, the research record and learner-facing source note MUST disclose the specific limitation and identify the affected scenarios as knowledge-based or adapted. This MUST NOT reduce the required five-to-seven count, omit complete answers, or justify fabricated citations.
- **FR-010**: New scenario answers MUST start hidden on a fresh lesson mount and remain independently operable by pointer and keyboard. Each summary and confidence control MUST be meaningfully labeled; opening or closing one question MUST NOT force another to close.
- **FR-011**: Existing manifest IDs, titles, slugs, file paths, routes, section identities, and foundational recall keys MUST stay unchanged. Every new scenario MUST receive a stable question identity unique within its lesson and distinct from all existing keys; re-running the migration MUST NOT duplicate cards or regenerate saved identities.
- **FR-012**: Each scenario MUST participate in the existing Hard/Good/Easy self-testing model, with the latest rating retained across navigation, reload and JSON export/import. Initially absent scenario ratings MUST remain unrated. Revealing/rating an answer MUST NOT change mastery or complete a topic review.
- **FR-013**: The migration itself MUST preserve topic status, review history/schedule, recorded visits and existing confidence. Existing Mastered topics MUST NOT be demoted because new practice was added, and progress MUST still count the same 15 topic leaves. Normal user-driven visits, status changes, ratings and confirmed backup replacement retain their existing behavior.
- **FR-014**: All additions MUST render as self-contained partial content in the existing shared dashboard, using its common styles and learning controls. The migration MUST NOT require individual manual shell edits per lesson or introduce a backend, build requirement, new navigation taxonomy, or different review algorithm.
- **FR-015**: Current content acceptance MUST distinguish foundational recall (three to five, preserving the actual per-lesson baseline) from the separate interview group (five to seven). Merely widening a single total recall range MUST NOT pass a lesson missing either required group.
- **FR-016**: Acceptance MUST reject migrated content with missing/duplicate subsection headings, out-of-range group counts, missing/empty structured answer parts, duplicate/unstable question identities, or initially exposed/exclusively grouped answers. Editorial review MUST additionally verify concept specificity, source honesty, concrete decisions, viable alternatives and meaningful traps.
- **FR-017**: Current inventories and browser checks MUST account for the preserved 61 foundational cards plus the actual added scenario count, and for every existing/new diagram. Baseline numbers MUST be used as preservation checks, not mistaken for post-migration totals. Historical pre-migration evidence MUST remain identifiable as historical.
- **FR-018**: Integration verification MUST use the actual dashboard to load all 15 migrated lessons and six unchanged hubs at both root and repository-subdirectory hosting paths, exercising links/direct refresh and confirming no unexpected console or diagram-rendering errors in the healthy-dependency case.
- **FR-019**: The new subsection and all interactions MUST remain readable in light/dark themes and usable at 360-pixel viewport width without page-wide overflow. Confidence selection, disclosure operation and focus MUST work by keyboard, consistent with the existing accessibility contract.
- **FR-020**: Real print/PDF verification MUST cover every migrated lesson from both themes, including all original prose, foundational answers, new scenario/decision/trade-off/trap content, and readable diagrams/tables. Printing MUST restore the prior disclosure states afterward.
- **FR-021**: The delivery MUST align the current content/host contract, content validation, affected test fixtures and dashboard acceptance expectations with constitution v1.2.0. Any retained legacy fixture/profile MUST be explicit; migrated lessons MUST NOT receive a legacy waiver. Existing valid behavior outside this migration MUST continue to pass its relevant checks.
- **FR-022**: The completion record MUST identify each lesson, preserved foundational count/keys, added scenario count/keys, research/source evidence and editorial/integration outcome. No lesson MUST be declared migrated solely because a batch-level check passed or a placeholder subsection exists.
- **FR-023**: New explanations of processes, hierarchies, timelines or systems MUST satisfy the constitution's applicable visualization rules. Existing diagrams MUST be preserved, and every diagram included in the expanded lessons MUST render successfully in the host.
- **FR-024**: The manifest hierarchy and six existing overview hubs MUST remain unchanged. Content changes are limited to the 15 lessons' mastery additions and associated source notes, together with necessary supporting contract/validation/integration alignment; unrelated lesson rewrites, dashboard redesign, new topics and deployment changes are outside scope.

### Key Entities *(include if feature involves data)*

- **Lesson migration target**: One existing topic identity/path and its six-module content, associated with its original foundational questions and required scenario set.
- **Preservation baseline**: The original catalog/topic identities, question keys/counts and lesson material needed to demonstrate that the migration retains existing content and learning records.
- **Foundational recall card**: An original, stable-keyed question/answer retained in the foundational group; included in the existing 61-card baseline.
- **Interview scenario card**: A newly stable-keyed, concept-specific production prompt with the three required answer parts, associated research basis and independent confidence record.
- **Research evidence record**: A concept/scenario mapping to sources, research date, selection/correctness rationale, reported-versus-adapted classification and any explicit research limitation.
- **Learning record**: Existing topic status/visits/review values and per-question confidence; new question keys extend practice without replacing old records or changing topic identities.
- **Per-lesson acceptance record**: The preserved and added inventories plus structural, editorial, integration and print results establishing complete migration for that one lesson.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 15 lessons contain the dedicated interview subsection with five to seven complete new scenarios each: 75–105 new scenarios overall, alongside all 61 retained foundational questions (136–166 total learning questions).
- **SC-002**: Every added scenario passes editorial review for a concrete production constraint, explicit decision/reasoning, gains/costs, viable alternative, follow-up trap and changed-assumption response; none is accepted as a definition-only or superficial duplicate question.
- **SC-003**: All 15 lessons have concept-specific research records and source notes, and 100% of new scenarios have a traceable selection basis. Every frequency/company claim is supported or clearly replaced with an adaptation/limitation disclosure; applicable technical recommendations have verified primary-source support.
- **SC-004**: All original topic/question identities, routes, first-five-module content and 61 foundational prompts/answers are retained. A pre-migration learning record keeps its prior status/review/confidence values after content replacement, apart from normal explicit user actions.
- **SC-005**: Every new scenario can be revealed/hidden independently by keyboard, rated, revisited after reload and restored from a backup with the chosen confidence intact. Revealing/rating never changes topic mastery or the due review schedule.
- **SC-006**: All 21 existing content destinations open and refresh at both hosting locations, and every included diagram renders without unexpected console/rendering errors. The expanded lessons remain readable and operable at 360 pixels in both themes.
- **SC-007**: All 15 migrated lessons produce complete, readable printed output from each theme (30 outputs), with original and new hidden answers present and each lesson's prior disclosure states restored afterward.
- **SC-008**: Acceptance detects every intentionally introduced missing-group, invalid-count, missing-answer-part, duplicate-identity and unsupported-claim case through the appropriate structural/editorial check. Each of the 15 completion records links its own evidence rather than relying on a blanket batch approval.

## Assumptions

- The adopted standard is constitution v1.2.0. Its five-to-seven interview scenarios are additional to the three-to-five foundational cards; the current files contain four each except DDD, which contains five.
- This command specifies the migration. Scenario selection/research, lesson editing, supporting contract changes and acceptance execution occur in the subsequent plan/tasks/implementation phases; they are not claimed as completed by this document.
- The audited manifest identifies exactly the 15 lessons in the scope table. Six hubs remain unchanged. This is a content migration at existing locations, so no new placement, manifest entries or permanent node IDs are required.
- Available web search must actually be used for each concept; limited frequency evidence is not permission to invent interview provenance. The constitutional fallback applies only to a recorded unavailability/failure/evidence gap.
- Five to seven scenarios may vary by lesson according to distinct researched decisions; there is no requirement to choose a uniform six or to assert a numerical frequency ranking.
- Existing lesson modules one through five already meet their recorded learning baseline. This feature preserves them and expands module six/source notes without reopening unrelated content or dashboard design work.
- Existing shared styling, disclosure, confidence, storage and backup behavior are dependencies. Supporting alignment is limited to what is necessary for complete scenario integration and accurate validation; future planning selects the exact representation.
- Existing mastery statuses remain the learner's explicit choices. New scenarios do not require an automatic progress reset or a storage-format change.
- Existing source references can support technical reasoning but must not be relabeled as interview-frequency evidence without support.
- Original acceptance reports remain historical evidence. New per-lesson and integration results must establish the migrated state without rewriting earlier claims into fictitious past passes.
- No branch hook or branch override is configured; the working branch remains `main` and the feature is selected through `specs/003-backfill-interview-scenarios`.
