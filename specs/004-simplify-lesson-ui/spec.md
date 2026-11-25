# Feature Specification: Simplify Lesson UI

**Feature Branch**: `main` (no branch hook configured)
**Created**: 2026-11-25
**Status**: Implemented and validated; see [delivery.md](delivery.md).
**Input**: Remove the repeated dated research/adaptation disclaimer everywhere on the website, remove “Continue by comparing the related decisions:”, remove the “MAKE IT YOURS” section, and provide an intuitive progress control that takes little space.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read without repeated administrative copy (Priority: P1)

As a learner moving between lessons, I want the page to focus on the subject instead of repeating how its interview questions were researched.

**Why this priority**: The requested cleanup applies throughout the catalog and directly reduces reading clutter.

**Independent Test**: Read lessons from every existing branch, including older and newer wording variants, and inspect their printed versions. The unwanted boilerplate is absent, while sources and complete teaching material remain available.

**Acceptance Scenarios**:

1. **Given** any existing lesson with a paragraph beginning “Researched” followed by a date and research/adaptation/frequency disclaimers, **When** I read or print it, **Then** that paragraph is absent in full.
2. **Given** a lesson using an older equivalent disclosure, **When** I read it, **Then** the equivalent administrative paragraph is also absent; cleanup is not limited to the exact latest wording or date.
3. **Given** scenario source references, **When** the paragraph is removed, **Then** the named source links remain accessible in a compact “Sources” group without replacement boilerplate.
4. **Given** hypothetical numbers or product-dependent behavior in an answer, **When** I read it, **Then** the specific assumptions needed to understand that answer remain beside the explanation.

---

### User Story 2 - Track learning with one compact control (Priority: P1)

As a learner, I want an obvious, small progress control instead of duplicate controls and a large motivational card.

**Why this priority**: The screenshot shows a large repeated end-of-lesson card; progress must remain easy to use after removing it.

**Independent Test**: On a lesson with each supported status, change progress, reload, navigate away and return, and verify the same status and appropriate review actions without the old banner.

**Acceptance Scenarios**:

1. **Given** any lesson, **When** it opens, **Then** one compact row near the title shows “Progress” and a selector for Not Started, In Progress and Mastered. There is no large bottom progress card or second progress selector.
2. **Given** a lesson not yet mastered, **When** I explicitly select Mastered, **Then** the lesson is mastered, the shared progress indicators update, and the normal review schedule begins.
3. **Given** an already mastered lesson, **When** I open it, **Then** its next review date and a Start review action are available in the compact progress area.
4. **Given** an active review, **When** I reveal or rate answers, **Then** the review remains active until I explicitly choose Complete review. Completing it retains the established scheduling behavior.
5. **Given** stored progress or a backup, **When** I reload or restore it, **Then** statuses, confidence, review history and unknown imported records remain intact.
6. **Given** a keyboard or touch interface in either theme, **When** I use progress or review controls, **Then** their labels, focus and selected state remain clear and usable.

---

### User Story 3 - Follow related lessons without filler (Priority: P2)

As a learner finishing a topic, I want the useful related links without a repetitive instructional sentence.

**Why this priority**: Related topics aid learning; their repeated preamble adds no useful information.

**Independent Test**: Visit a lesson with related links, follow each destination, and verify that the introductory sentence and large mastery card are absent.

**Acceptance Scenarios**:

1. **Given** related lessons, **When** I reach them, **Then** “Continue by comparing the related decisions:” is absent and the existing destinations remain in a compact, clearly labeled related-topics group.
2. **Given** a lesson without related links, **When** it opens, **Then** no empty related-topics heading or container is shown.
3. **Given** a newly added lesson following the updated publishing rules, **When** it is published, **Then** it follows the same clean presentation without regenerating the removed boilerplate.

### Edge Cases

- Older lessons have different dated research paragraphs; all equivalent variants are in scope.
- Other source notes or educational paragraphs may contain dates or the word “research”; they must not be indiscriminately deleted.
- Reading, expanding answers, rating confidence and switching theme must never implicitly master a lesson or complete a review.
- Moving a mastered topic to another status must retain the existing reset/remastery semantics; this feature does not invent a new review policy.
- An active review must remain usable after route reload, theme switching or backup restoration according to existing behavior.
- A failed save/import must remain visible and truthful; the compact control must not falsely imply durable success.
- Long titles, long related-link labels and review dates must fit at a 360-pixel viewport without overlap or horizontal page scrolling.
- Keyboard focus must remain usable after status/review actions change the available controls.
- Hubs have no individual lesson status; they must not gain a misleading progress selector.
- Print output must omit interactive progress/review controls and removed boilerplate while retaining sources, diagrams, comparisons, Feynman prompts and all answers.
- Future catalog growth and an old cached lesson must not permanently reintroduce the removed presentation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Remove the entire generic dated research paragraph from every current lesson, covering every wording/date variant of research method, adapted scenarios, unverified interview frequency/company/ranking and generic hypothetical-number/runtime disclaimers. Do not relocate this paragraph into another website page, tooltip, collapsed panel or print-only area.
- **FR-002**: Retain useful named source links in a concise Sources group. Do not replace the removed paragraph with synonymous administrative boilerplate or remove the supporting references.
- **FR-003**: Preserve substantive context-specific assumptions, qualifications, evidence limitations and technical trade-offs inside the explanations where they affect the answer.
- **FR-004**: Remove “Continue by comparing the related decisions:” wherever it appears in the website. Preserve related destinations, their identities and keyboard access; present them as a compact Related topics group that wraps on narrow screens.
- **FR-005**: Remove the entire large MAKE IT YOURS callout, including its motivational heading, explanatory text and the equivalent mastered-state promotional copy. No empty banner or replacement marketing section may remain.
- **FR-006**: Provide exactly one lesson-level progress area near the title: the concise label Progress and a three-status selector. Remove the duplicate status/motivational helper text and avoid a second persistent progress area at the bottom.
- **FR-007**: The learner must be able to select any supported status with no more than two deliberate interactions. Labels must include text rather than rely on color or an unexplained icon.
- **FR-008**: Mastered topics must expose the next scheduled review date and the currently relevant explicit review action within the compact progress area. Inactive and active review states must be distinguishable without the removed card.
- **FR-009**: Retain the existing explicit status, mastery, review-start and review-completion semantics. Opening content, revealing answers and rating confidence must not substitute for those actions.
- **FR-010**: Preserve topic identities, recall identities, existing statuses, confidence, visit history, review history/sessions and backup compatibility. Status changes must update sidebar, ancestors, overall mastery, Continue Learning and review queue consistently.
- **FR-011**: Progress must persist across normal reloads and backup export/import. Existing storage/import failure feedback must remain accurate and accessible.
- **FR-012**: At ordinary text size, the lesson progress area must occupy at most one row and 56 pixels of height at desktop widths of 1024 pixels or more, and at most two rows and 112 pixels at a 360-pixel viewport, including the mastered/active-review variants. These bounds exclude temporary error messages and an opened selector menu. Controls must have touch targets of at least 44 by 44 pixels.
- **FR-013**: All changed controls and link groups must support keyboard navigation, visible focus, understandable accessible names and readable light/dark contrast. Focus must remain on a meaningful surviving control after a state change.
- **FR-014**: Preserve all six learning modules, complete explanations, diagrams, mechanics, comparisons, pitfalls, Feynman practice, foundational cards and scenario questions/answers. Removing the host's promotional mastery card must not remove the lesson's actual Feynman or mastery-check content.
- **FR-015**: Retain research dates, provenance, adaptation/frequency limitations, actual searches and technical source mappings in maintainer research records. Do not turn removal of public boilerplate into new unsupported interview-frequency claims.
- **FR-016**: Align the current authoring/governance and acceptance requirements with this request so future lessons are accepted without the public disclaimer paragraph. Requirements that currently mandate visible frequency/adaptation boilerplate or an exact match to a public paragraph must be deliberately revised; retain the underlying research, source, honesty and lesson-depth requirements. Frozen historical acceptance evidence must remain historical.
- **FR-017**: Apply the presentation rules to all current lessons and future topic generation, not only the latest DevOps batch. Derive coverage from the current catalog.
- **FR-018**: Preserve dashboard navigation, search/shortcuts, themes, source and related links, home progress/review behavior and deployment under both the site root and a repository subdirectory.
- **FR-019**: Printed lessons must exclude removed copy and interactive controls while retaining complete educational material and source references without blank replacement panels.
- **FR-020**: Provide catalog-wide acceptance of the shared presentation changes, including mobile, both themes, printable content and progress/review/backup regression. Existing validators must be aligned with the intended presentation change, not bypassed or replaced with fixed inventory assumptions.

### Key Entities *(include if feature involves data)*

- **Lesson**: Existing identity, title, ordered learning modules, questions and related destinations; teaching content remains complete.
- **Learning record**: Existing lesson status, confidence ratings, visits and review state; presentation changes do not replace this record.
- **Review session**: Existing explicit start/completion state and scheduled next review; surfaced through the compact progress area.
- **Source group**: Named references available to the reader without generic process commentary.
- **Maintainer research record**: Traceable research date, queries, sources, provenance and limitations retained outside the reading interface.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every current lesson has zero occurrences of the unwanted research paragraph or equivalent boilerplate, the related-decision introductory sentence, and the MAKE IT YOURS card in normal reading and print output.
- **SC-002**: A learner can see and change status in no more than two deliberate interactions using the single Progress area; the desktop/mobile size bounds in FR-012 hold for all status/review variants.
- **SC-003**: In every tested status, confidence, mastery, review and backup journey, existing records remain intact and every progress/review display agrees after reload or restoration.
- **SC-004**: All existing source and related-topic destinations remain reachable. Every lesson retains its complete six-module teaching content and the same question identities and answers.
- **SC-005**: All current lesson and hub pages remain readable in both themes at desktop and 360-pixel widths, with no new horizontal page overflow or obscured controls, and complete printable learning content.
- **SC-006**: A subsequent lesson produced under the updated publishing requirements is accepted without reintroducing boilerplate or the large mastery card, while retaining source links and complete research records.

## Assumptions

- The original specification invocation was planning only. Subsequent authorized implementation and governance alignment are complete; acceptance is recorded in [delivery.md](delivery.md).
- This is a shared presentation and learning-presentation requirement change, so the full feature specification applies rather than the routine topic-addition profile.
- “Not needed anywhere” refers to website presentation, including print; existing maintainer research evidence remains in the repository.
- All equivalent repetitive research-note variants are included, not only the exact sentence quoted by the user. The audit found 135 such paragraphs with seven distinct wordings.
- Related links are valuable and remain. The instruction removes their filler introduction, not their destinations.
- MAKE IT YOURS identifies the host's large progress callout, not the constitutional in-lesson Feynman exercise.
- One compact Progress row near the title is the chosen default; the review date/action appears there only when relevant. No design-choice clarification is necessary to make this specification actionable.
- The audit baseline is 181 nodes: 135 lessons and 46 hubs across nine branches. The related-decision sentence occurs in 120 lessons. Acceptance must use the actual catalog if it grows.
- Current governance and checks require a visible research note and public frequency disclosure. The user's request changes that presentation requirement; implementation must align those rules explicitly while retaining honest research records and contextual technical assumptions.
- This feature adds no lessons, hierarchy changes or new progress model. Shared presentation and acceptance work may touch all lessons; it does not authorize reauthoring their explanations or regenerating topic/question identities.
- Historical evidence and unrelated project documents remain intact. Commit, push and deployment are outside this specification-stage request.
