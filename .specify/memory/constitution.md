<!-- Sync impact: 1.3.0 -> 2.0.0. User-authorized presentation amendment, 2026-11-25.
Align current publishing guide/skill and sources-only-v1 validation; retain recall profile
constitution-1.2, complete evidence and frozen historical records. Migration acceptance pending. -->
<!--
Sync Impact Report
Version change: 1.2.0 -> 1.3.0 (MINOR: incremental content-publishing workflow)
Rationale: routine lesson requests inherit stable contracts; repeated platform planning,
migration-specific validation and redundant evidence must not block catalog growth.
Modified principles: II and VI clarify purposeful visual coverage without per-card quotas.
Added section: Incremental Topic Publishing and Verification, preserving all learning gates.
Aligned: root AGENTS.md, topic-publish skill, four Spec Kit content-profile entrypoints,
spec/plan/tasks templates, docs/topic-publishing.md, generic validator profile and scoped runner.
Existing content: no rewrite required; all six modules, recall/scenario counts, source
honesty, immutable identities, mobile and print requirements remain in force.
Historical backfill snapshots/evidence remain frozen and explicitly scoped.
Deferred placeholders: None.
-->
# Personal Learning Knowledge Base Constitution

## Core Principles

### I. ELI5-First Narrative Learning

The project MUST be a single-page, static HTML/JavaScript/CSS living knowledge base for
deep, frictionless personal learning across diverse topics. Every topic MUST tell a
cohesive story in the order Context → Core Concept → Deep Dive → Real-World Impact.
Disconnected fact dumps MUST NOT substitute for that narrative.

ELI5-first clarity is the highest-priority learning requirement. Every concept MUST begin
with an intuitive mental model and a simple, real-world analogy before introducing jargon,
formal definitions, or complex mechanics. The opening MUST explain what problem the
concept solves and why it matters, aiming to make the core idea click within 30 seconds.
Necessary depth MUST remain available after this intuitive introduction.

Rationale: learners need a familiar mental model before they can connect technical detail
to a meaningful understanding.

### II. Visual-First, Frictionless Navigation

Lessons MUST combine narrative with diagrams, flowcharts, comparison tables, or interactive
visual aids wherever the concept benefits from them. Walls of text MUST NOT be the sole
teaching mechanism. Explanations of a process, hierarchy, timeline, or system MUST include
valid Mermaid syntax using an appropriate supported diagram type, such as `graph TD`,
`sequenceDiagram`, `mindmap`, or `pie`. A relevant, explained diagram MAY cover multiple
scenarios when their relationship to it is clear. There is no per-scenario diagram quota.
New diagrams MUST teach a distinct relationship, sequence, constraint or failure path;
repeated generic diagrams MUST NOT substitute for meaningful visual explanation.

The interface MUST use a clean, modern documentation-dashboard layout with a recursive
left sidebar, top-bar learning controls, and a main reading canvas. Navigation MUST support
arbitrarily deep nesting without a hard-coded depth limit, starting with Domain → Category
→ Topic → Subtopic. Every navigation node MUST display a completion badge or progress
ring; container nodes MUST reflect their descendant topics' progress.

Rationale: visible relationships and predictable navigation reduce the effort required to
understand a concept and return to it later.

### III. The Standard Topic Story Blueprint

Every topic document MUST contain the following six modules in this order. A topic is
incomplete if any module is missing or contains an unexplained placeholder.

1. **🎯 The Hook & ELI5 (Context):** State the problem and why it matters. Introduce a
   simple real-world analogy before technical terminology, targeting intuitive understanding
   within 30 seconds.
2. **🗺️ High-Level Big Picture (Visual Diagram):** Embed a valid Mermaid flowchart, mind
   map, architecture diagram, or other appropriate Mermaid diagram showing how the pieces
   fit together.
3. **🔍 Step-by-Step Mechanics (Low-Level Deep Dive):** Explain internal behavior in a
   logical sequence using collapsible `<details>` cards or tabbed views to reveal depth
   progressively. Connect each step to the opening mental model.
4. **⚖️ Comparisons & Trade-Offs (Decision Matrix):** Include a structured comparison
   table explaining why to choose the approach, the alternatives, the gains, and the costs.
   When comparing approaches is not meaningful, compare applicable choices or conditions
   and explain the scope explicitly instead of inventing alternatives.
5. **⚠️ Common Pitfalls, Bugs & "What-If" Scenarios:** Cover misconceptions, edge cases,
   and failure modes using Symptom → Root Cause → Fix/Prevention. Explain consequences
   in practical or real-world terms.
6. **🧠 Active Recall & Mastery Check (Learning Engine):** Include the Feynman prompt
   "Summarize this in your own words" and three to five foundational active-recall
   flashcards or what-if questions with hidden or collapsible answers. In addition,
   include a dedicated subsection titled **Tricky & Most-Asked Interview Scenarios**
   containing five to seven distinct, real-world scenario-based interview questions.
   Each MUST ask what the learner would do and why under explicit production
   constraints, and MUST use the structured interactive answer format defined in the
   research standard below. This subsection belongs inside module six; it MUST NOT
   replace the foundational recall cards or introduce a seventh top-level story module.
   End by connecting the lesson to real-world impact and useful takeaways.

Rationale: a consistent story structure lets learners focus on the subject while combining
intuition, mechanics, decisions, failure analysis, and retrieval practice.

### IV. Persistent Learning and Active Recall

The learning engine MUST run client-side and persist learning state in `localStorage`.
It MUST provide JSON export and import controls for backing up and restoring that state.
Core learning and progress tracking MUST NOT require a backend service.

Each topic MUST support the statuses **Not Started**, **In Progress**, and **Mastered**
(Completed). The sidebar and global mastery indicator MUST derive their displayed progress
from the same topic state. Completion MUST NOT be inferred solely from opening a lesson
or revealing an answer.

Completed topics MUST record a `lastReviewed` timestamp. A spaced-repetition queue MUST
automatically highlight topics due for refresh on the dashboard home screen, using an
explicit review schedule with 3, 7, 14, and 30 days as the default interval sequence. The
engine MUST retain sufficient review state to determine the next due review consistently.

Self-testing MUST let learners flip or reveal Q&A cards and rate their confidence as
**Hard**, **Good**, or **Easy**. Confidence ratings MUST be persisted as learning state
so they can support continued review.

The interview scenarios required by Principle III MUST be independently collapsible
`<details>` cards with descriptive `<summary>` prompts and stable recall identities.
They MUST participate in the shared self-testing and confidence model without changing
existing topic IDs or recall keys. Revealing an interview answer or rating confidence
MUST NOT imply mastery or complete a topic review.

Rationale: explicit progress, retrieval practice, and scheduled revisits turn a reference
collection into a durable personal learning system.

### V. Lightweight Static Architecture and Incremental Growth

The application MUST remain deployable as static assets, with no required application
server or heavy backend. Use HTML5, Tailwind CSS through a CDN or lightweight build,
Vanilla ES6+ JavaScript or Alpine.js, Mermaid.js for diagrams, and Prism.js or Highlight.js
for syntax-highlighted code and formulas where applicable. The architecture MUST remain
zero-build or use only a lightweight build consistent with these constraints.

One navigation manifest, `manifest.json`, MUST be the source of truth for the recursive
content hierarchy. Individual lessons MUST live in modular HTML partials, such as
`/topics/computer-science/distributed-systems/consistent-hashing.html`. The renderer MAY
also support Markdown lessons through the same lightweight static architecture, but every
future AI-generated topic delivery MUST include a complete HTML partial. Selecting a
lesson MUST dynamically load it into the main canvas without a full-page reload.

Before creating any topic artifacts, the AI MUST audit `manifest.json` and determine the
logical Domain (Root) → Category (Parent) → Sub-Category, when needed → Topic (Leaf) path.
It MUST reuse conceptually aligned nodes and automatically create genuinely missing roots
or parents. Each newly created root or parent MUST receive an `_overview.html` hub that
explains its big picture and links to its children. These lightweight Overview / Roadmap
Cards are navigation hubs, distinct from the six-module topic lessons in Principle III.

URL routes and directory paths MUST use strict `kebab-case` slugs and mirror the sidebar
hierarchy one-to-one beneath the common topic-content base directory. `_overview.html` is
the reserved hub filename and the explicit exception to kebab-case naming. Every manifest
node MUST have a unique, immutable `id`. Topic progress in `localStorage` MUST be keyed by
the stable topic ID rather than its title, slug, or path so renames and moves preserve it.

Adding a topic MUST deliver its complete lesson file, the matching manifest changes, and
any newly required parent hubs. Routine topic additions MUST NOT require changing the
navigation renderer, hard-coding another nesting level, or redesigning the application
shell. Existing lessons and progress MUST remain usable as the collection grows. The
four-step placement and delivery protocol below governs every future topic request.

Rationale: content-driven routing and small static modules keep long-term expansion fast
and maintainable for personal use.

### VI. Complete, Mobile- and Print-Friendly Delivery

AI-generated lessons and implementation changes MUST be complete within their requested
scope. Explanations MUST be self-contained and MUST NOT be truncated or replaced by
`TODO`, "add explanation here," empty sections, or equivalent filler. Delivered HTML,
JavaScript, and CSS MUST contain the working behavior required by that scope.

AI authors MUST automatically supply valid Mermaid diagrams whenever explaining processes,
hierarchies, timelines, or systems, and MUST follow the six-module story blueprint for every
new topic. Diagram source alone MUST NOT replace the surrounding explanation. Shared
visual coverage follows Principle II; authors MUST NOT generate redundant per-card diagrams
merely to inflate diagram counts.

Strict taxonomy hygiene is mandatory: AI authors MUST reuse and extend conceptually aligned
parent nodes and MUST NOT create duplicate categories with slightly different names, such
as `databases` and `database-systems`. Unrelated topics MUST NOT be placed directly at the
root level for convenience.

Every generated topic file, modal, or hub partial MUST render cleanly inside the existing
main dashboard canvas using its supported content contract. A topic delivery MUST NOT
require manual CSS or JavaScript edits to the core shell. Its diagrams, code highlighting,
collapsible content, and recall interactions MUST work through the shell's existing
integration points without disrupting other lessons or dashboard behavior.

The recursive sidebar MUST collapse into a usable drawer on mobile. Reading, navigation,
self-testing, and theme controls MUST remain usable on small screens. Print styles MUST
produce clean PDF output, preserving lesson content, diagrams, and readable comparisons
while removing obstructive navigation and controls. Content hidden by interactive reading
controls MUST remain available in the printed lesson.

Rationale: complete explanations and adaptable presentation preserve the knowledge base's
usefulness across devices and exported copies.

## Interface and Presentation Contract

Lessons MUST use one compact Progress status selector near the title. Preserve all three
statuses and explicit mastery/review transitions; show the relevant review action/date
in the same compact area. Do not add a second large promotional mastery card. Actual
Feynman practice and the complete mastery-check module remain required.


- **Left sidebar:** Provide a collapsible recursive tree for Domain → Category → Topic →
  Subtopic and deeper levels, with a visible completion badge or progress ring at every node.
  On mobile, expose this navigation through a collapsible drawer.
- **Top bar:** Provide breadcrumbs, instant fuzzy search opened by `Cmd+K` or `Ctrl+K`,
  a global progress bar labeled with the percentage mastered, and a Dark/Light theme toggle.
- **Main canvas:** Provide a clean, wide-margin reading area with card-based grids,
  callout boxes, and smooth anchor scrolling. Responsive layouts MUST preserve readable
  content and access to comparison tables and diagrams.
- **Palette:** The light theme MUST use a warm-neutral base such as `#FAFAFA` or `#F8FAFC`.
  Soft pastel accents MUST communicate meaning consistently: blue for architecture and
  structure, yellow for key insights and WHY, green for impact and takeaways, and pink/red
  for pitfalls and edge cases. The dark theme MUST preserve these semantic distinctions
  and readable text contrast.
- **Typography:** Use Inter or Plus Jakarta Sans for interface and body text, and JetBrains
  Mono for code and formulas, with suitable fallback fonts. Code blocks MUST use syntax
  highlighting through the selected highlighting library.
- **Reference interpretation:** The written dashboard requirements in this constitution
  govern implementation. A reference deck, if later supplied, MAY refine visual details
  without removing these requirements.

## Content Workflow and Quality Gates

**Automated Taxonomy & Incremental Placement Protocol**

For every future topic request, the AI MUST act as a Knowledge Architect and execute these
four steps in order:

1. **Taxonomy Audit & Placement:** Inspect the existing recursive tree in `manifest.json`
   before creating anything. Determine the most logical Domain (Root) → Category (Parent)
   → Sub-Category, when needed → Topic (Leaf) path. Reuse existing conceptually aligned
   parents; do not create synonymous categories. Keep depth balanced, preferring two to
   four levels including the topic leaf. Any deeper placement MUST have a conceptual
   justification; this preference MUST NOT impose a hard depth limit on the renderer.
   Unrelated topics MUST NOT be dumped at the root level.
2. **Auto-Creation of Missing Parents/Roots:** Automatically scaffold missing root and
   parent nodes in `manifest.json` when a topic introduces a new discipline or branch.
   For example, Quantum Computing can require a new discipline when only Web Development
   exists. Every newly created root or parent MUST also receive a lightweight
   `_overview.html` Overview / Roadmap Card in its matching directory. Each hub MUST
   explain the domain or branch's big picture and link to its children; when those children
   are topics, the links MUST open the corresponding lessons. Adding children to an
   existing hub MUST keep its roadmap links consistent with the manifest.
3. **Standardized Naming & Folder Mirroring:** Use strict `kebab-case` slugs for routes
   and directories, mirroring the sidebar tree one-to-one beneath the content base, for
   example `computer-science/distributed-systems/consistent-hashing.html`. Preserve the
   reserved `_overview.html` hub filename. Assign a unique, immutable `id` to every new
   manifest node and preserve all existing IDs. Renaming or moving a topic MUST retain
   its ID, `localStorage` progress, review history, and confidence ratings.
4. **Complete Delivery Bundle:** Apply the topic and manifest updates together and output
   a bundle containing all of the following:
   - A one-line **Placement Justification** showing the chosen path, for example
     `Root: AI & ML > Parent: LLM Architecture > Topic: Attention Mechanism`, with a brief
     reason for the placement and any depth exception.
   - A ready-to-paste **Updated `manifest.json` snippet** including the topic and every
     newly created root or parent, with stable IDs and enough surrounding context to
     identify where it belongs in the existing tree.
   - A **Complete Topic HTML Partial** following the six-step Story Blueprint: ELI5,
     Mermaid diagram, deep dive, trade-offs, pitfalls, and active recall.
   - Every newly required **`_overview.html` hub partial**, plus any existing hub update
     needed to keep child links accurate. The bundle MUST NOT leave implied hub work
     unfinished.

### Incremental Topic Publishing and Verification

Routine additions or revisions of lessons, taxonomy entries and hubs that preserve the
existing application contract MUST use the compact topic-publishing workflow documented
in `docs/topic-publishing.md` and selected through root `AGENTS.md`. A normal request MUST
be carried through research, full authorship, integration and verification without requiring
four separate user commands. Explicit planning-only, stage-specific or full-cycle requests
MUST retain their requested scope.

The workflow MUST inherit the constitution and supported partial contract. It MUST NOT
create new feature specifications, data models, contracts or migration evidence ledgers
by default for an unchanged shell. Batches MUST retain one complete authoring item per
lesson, with shared setup, catalog integration and verification grouped once. Research
and editorial findings MUST remain traceable but concise; copying complete answers into
multiple review records is not a quality requirement.

Before editing the catalog, authors MUST capture the prior manifest and inspect existing
taxonomy and representative partials. Validation MUST check the whole current catalog's
intrinsic contracts, links, complete hubs and research mappings. Browser, keyboard, theme,
mobile and full-answer print checks MUST cover changed lessons and affected hubs. Shared
renderer/style/library changes require catalog-wide rendering and print regression;
routing/state/backup changes require full relevant application regression. A schema or
learning-standard change requires full Spec Kit assessment and explicit migration scope.

Verification MUST derive inventory and progress expectations from the current manifest.
Frozen migration counts, hashes, and evidence MUST apply only to that named migration;
they MUST NOT become default publishing prerequisites. Baselines MUST NOT be regenerated
to conceal intentional catalog growth. Change discovery MUST include untracked files or
use explicit paths and a pre-edit manifest when no usable Git baseline exists.

The verification runner SHOULD own server startup/readiness/cleanup and isolated browser
contexts. It MAY reuse successful rendering/print results only when relevant content,
manifest identity/path/context, research, shared runtime, contract, tooling and browser
inputs remain unchanged and output artifacts are intact. Cheap catalog validation MUST
always rerun. Interrupted or unexecuted gates MUST remain pending. Source correctness and
substantive editorial review MUST NOT be inferred from a structural validator pass.

All existing learning and delivery standards remain mandatory, including ELI5-first depth,
the six modules, three to five foundational cards, five to seven complete researched
production scenarios, meaningful visuals, immutable IDs/recall keys and usable mobile/print
output. Reduced planning overhead MUST NOT reduce content quality or completeness.

### Interview Scenario Research and Answer Standard

For every new or substantively revised topic lesson, the AI MUST research and author
five to seven distinct questions for its **Tricky & Most-Asked Interview Scenarios**
subsection. Each question MUST concern the exact concept being taught and present a
real production situation, an explicit constraint or failure, and a decision prompt:
"What will you do and why?" Definition-only questions, vocabulary checks, and superficial
rewrites of the same scenario MUST NOT count toward these five to seven questions.

**Web-grounded selection:** When web search is available, the AI MUST use it before
selecting the scenario set. Searches MUST target the exact concept and its commonly
asked system-design, debugging, and architectural trade-off interview situations.
Select scenarios using recurring patterns in credible interview reports, interview
preparation sources, or published interview guidance. Verify technical answers against
primary technical documentation or original architecture references where applicable.
The AI MUST NOT present generic textbook definitions as evidence of interview frequency.

The lesson MUST retain named source links supporting technical reasoning and scenario
selection in a concise, visible Sources group outside closed question cards. It MUST NOT
repeat generic authoring dates, adaptation/frequency disclaimers or research-process prose
in the website, tooltips, hidden panels or print output. Context-specific assumptions and
technical limitations MUST remain beside the explanations they qualify.

Maintainer research records MUST preserve actual queries/dates, sources, scenario basis,
limitations and editorial review. Reported interview-frequency/company/ranking claims MUST
have supporting evidence; otherwise record the scenario as an adaptation without inventing
claims. Search failures or insufficient frequency evidence MUST be recorded in maintainer
records. Removing public boilerplate MUST NOT weaken research or reduce scenario counts.
Existing historical publicDisclosure fields remain provenance; new records need no public
paragraph field. Canonical source links MUST match their ordered research mappings.

**Structured interactive answers:** Every scenario MUST use its own native `<details>`
card. Its `<summary>` MUST identify the production problem and decision being tested;
the expanded card MUST contain these three clearly labeled parts:

1. **The Scenario & Constraint:** State the real-world situation, relevant assumptions,
   and concrete constraints such as scale, latency, consistency, reliability, ownership,
   compatibility, or budget. Ask what the learner would do and why.
2. **The Direct Answer & Architectural Decision:** Give an explicit recommended action,
   explain why it fits those constraints, and describe the critical implementation or
   debugging steps needed to act on it. State any assumptions that change the answer;
   "it depends" without a decision and reasoning is incomplete.
3. **Key Trade-Offs & Follow-Up Traps:** Explain the gains and costs, at least one viable
   alternative, and the follow-up constraints or misconceptions an interviewer could
   probe. Include how the decision changes when a relevant assumption or failure mode
   changes. Do not replace this analysis with a generic advantages/disadvantages list.

Questions MUST test applied reasoning rather than memorized definitions. The set MUST
cover materially different production constraints and include debugging/failure analysis
and architectural trade-offs where applicable to the concept. Native disclosure controls,
shared card styles, hidden answers, keyboard operation, confidence persistence, and full
printed answers MUST follow the host's supported content contract. All explanations MUST
remain self-contained even when source links are unavailable to the reader.

**Automatic consistency:** Routine content requests inherit these requirements through
the compact publishing checklist; separate specs and plans are not mandatory. When a
specification or plan is produced, every future topic specification MUST include acceptance
criteria for the dedicated subsection, five-to-seven count, production constraints,
named source links and maintainer evidence, and all three answer parts. Every future topic plan MUST
include concept-specific question research, source verification, authoring, and affected
content-contract/validation alignment. Task breakdowns and implementations MUST deliver
the complete scenario set and verify independent disclosure behavior, stable identities,
confidence integration, accessibility, and print completeness. These rules apply without
requiring the user to repeat this amendment.

Rationale: realistic decisions under constraints test whether learners can apply a mental
model, defend its costs, and respond to changing assumptions in an interview or production.

Before accepting a new or revised lesson, review MUST verify all six modules, ELI5 before
jargon for each concept, narrative continuity, valid rendered diagrams, complete trade-off
and failure analysis, three to five foundational recall questions, and the separate five
to seven complete interview scenarios. Review MUST verify the dedicated subsection,
concept-specific production constraints, named research links and recorded evidence limitations,
and all three structured answer parts in every independently collapsible scenario card.
Opening a topic through its manifest entry MUST load the intended lesson without a page
reload. Topic additions MUST preserve existing navigation and learning state.

Placement review MUST also verify the manifest audit, reuse of aligned parents, absence of
duplicate categories, justified depth, complete parent hubs with working child links,
kebab-case paths matching the sidebar, and unique IDs preserved across renames or moves.
Delivery review MUST verify the placement justification, paste-ready manifest snippet,
complete HTML lesson and hub files, and rendering inside the existing canvas without
manual shell CSS or JavaScript edits.

For changes affecting application behavior, validation MUST cover the affected requirements,
including recursive navigation, search and its shortcut, breadcrumb updates, theme switching,
progress consistency, persistence across reloads, JSON backup/restore, review due dates,
and confidence ratings as applicable. Mobile and print changes MUST be checked in their
respective layouts. Verification MAY use focused manual checks or automated tests, but
MUST establish the affected behavior rather than merely mirror implementation details.

Specifications, plans, tasks, and reviews MUST identify the constitutional requirements
relevant to their scope. Unimplemented features MUST remain explicit planned work; a
constitution update alone MUST NOT be represented as delivery of the application.

## Governance

This constitution governs project specifications, implementation plans, task breakdowns,
application changes, and topic authorship. Within the project's learning requirements,
ELI5-first clarity has highest priority; it MUST be satisfied alongside the required depth,
visuals, and complete content rather than used to omit them.

An amendment MUST record the proposed change, rationale, effect on existing content or
behavior, and any migration work. The project owner approves amendments, including through
an explicit request to update these principles. Adopted amendments MUST update this file,
its version, and its last-amended date. The original ratification date MUST be preserved.

Versioning MUST follow semantic versioning: MAJOR for incompatible governance or principle
removals or redefinitions; MINOR for new principles, sections, or materially expanded
guidance; PATCH for clarifications and other non-semantic wording changes. Version 1.0.0
records initial adoption of the project-specific constitution.

Version 1.2.0 expands mastery practice with researched, structured production-interview
scenarios while retaining the six-module blueprint and foundational recall. The new rules
govern all future topic specifications, plans, tasks, and implementations immediately.
Existing unchanged lessons retain their recorded acceptance baseline; they MUST NOT be
represented as satisfying the new scenario standard until explicitly migrated and checked.
New or substantively revised lessons MUST meet the new standard, and their work MUST
align any affected content contracts, validators, and inventory/browser expectations.
Migration MUST preserve existing topic IDs, recall keys, and saved learning state. Updating
this constitution alone does not perform or claim that migration.

Version 1.3.0 adds proportional, persistent topic-publishing governance and clarifies
purposeful diagram reuse. It requires workflow/tool alignment, not a new lesson backfill.
It does not relax the v1.2.0 learning content or source-evidence requirements.

Every relevant specification and change review MUST check compliance with these rules.
Conflicts MUST be resolved by revising the proposed work or adopting an explicit amendment;
silent exceptions are not permitted. A material amendment MUST identify affected lessons,
implementation behavior, and planning artifacts that require follow-up alignment.

Version 2.0.0 changes mandatory public research presentation to concise Sources links and
maintainer evidence, and requires compact explicit progress controls. This incompatible
presentation amendment is authorized by the project owner's Simplify Lesson UI request.
It migrates all current generic source paragraphs and shared controls; complete teaching,
research honesty, stable identities and learning state remain mandatory. Active publishing
instructions and validation must align; frozen historical evidence remains historical.

**Version**: 2.0.0 | **Ratified**: 2026-11-17 | **Last Amended**: 2026-11-25
