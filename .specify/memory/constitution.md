<!--
Sync Impact Report
Version change: 2.0.0 -> 3.0.0 (MAJOR: teaching and interactive-visual contract)
Rationale: mandatory project-anchored storytelling, section signposts, and per-lesson
interactive visuals redefine lesson acceptance and require a managed widget lifecycle.
Modified principles:
- I. ELI5-First Narrative Learning -> I. Friendly, Concept-First Narrative Learning
- II. Visual-First, Frictionless Navigation -> II. Purposeful Visuals and Frictionless Navigation
- III. The Standard Topic Story Blueprint -> III. The Six-Act Story and Progressive Disclosure
- V. Lightweight Static Architecture and Incremental Growth (widget asset integration)
- VI. Complete, Mobile- and Print-Friendly Delivery (visual accessibility and fallbacks)
Added sections:
- Standardized Project Lens and Objective Engineering
- Interactive and Animated Visuals Contract
- Teaching Standard Adoption and Widget Rollout
Expanded: lesson review gates, scenario anchoring, and governance amendment history.
Removed sections: None. Superseded temporary sync comments consolidated here.
Deferred placeholders: None.
Follow-up work, not executed by this constitution-only command:
- Specify the LabVisuals registry and app.js mount/cleanup integration, shared asset loading,
  safe SVG/Canvas support, and index.html library loading where required.
- Align publishing skills/guides, templates when needed, validators, and browser/print checks
  after assessing the new contract; preserve frozen historical evidence.
- Scope and verify existing-lesson migration; prior UI migration acceptance remains separate.
This report is temporary review material; remove it before committing the amendment.
-->
# Personal Learning Knowledge Base Constitution

## Core Principles

### I. Friendly, Concept-First Narrative Learning

The project MUST be a single-page, static HTML/JavaScript/CSS living knowledge base for
deep, frictionless personal learning across diverse topics. Every topic MUST tell a
cohesive story in the order Context → Core Concept → Deep Dive → Real-World Impact.
Disconnected fact dumps MUST NOT substitute for that narrative.

Lessons MUST sound like a thoughtful, technically sharp friend explaining an idea over
coffee or at a whiteboard: warm, direct, conversational, and respectful. They MUST avoid
textbook stiffness, lecturer-like monologues, unexplained jargon, and patronizing language.
Authors MUST keep the explanation engaging with relevant analogies, brief "aha!" callouts,
and natural transitions such as "Imagine this..." or "Here's the catch..." where they help
the reader connect ideas. Light, relevant humor MAY add personality; forced jokes, slang,
and repeated catchphrases MUST NOT distract from understanding or technical precision.

ELI5-first clarity is the highest-priority learning requirement. Every concept MUST begin
with an intuitive mental model and a simple, real-world analogy before introducing jargon,
formal definitions, or complex mechanics. The opening MUST explain what problem the
concept solves and why it matters, aiming to make the core idea click within 30 seconds.
Necessary depth MUST remain available after this intuitive introduction.

The primary teaching goal MUST be understanding a universal concept and its general
trade-offs. The standardized project MUST provide a familiar lens, never an excuse to
teach undocumented implementation quirks or defend a sub-optimal design. Examples and
analogies MUST state relevant limits and MUST NOT sacrifice accuracy for entertainment.

Rationale: a friendly voice and familiar mental model make precise ideas easier to follow
without reducing their depth.

### II. Purposeful Visuals and Frictionless Navigation

Lessons MUST combine narrative with diagrams, flowcharts, comparison tables, or interactive
visual aids wherever the concept benefits from them. Walls of text MUST NOT be the sole
teaching mechanism. Explanations of a process, hierarchy, timeline, or system MUST include
valid Mermaid syntax using an appropriate supported diagram type, such as `graph TD`,
`sequenceDiagram`, `mindmap`, or `pie`. A relevant, explained diagram MAY cover multiple
scenarios when their relationship to it is clear. There is no per-scenario diagram quota.
New diagrams MUST teach a distinct relationship, sequence, constraint or failure path;
repeated generic diagrams MUST NOT substitute for meaningful visual explanation.

Every lesson MUST also include at least one purposeful interactive visual or animated
diagram that makes motion, a state transition, or a trade-off over time visible. It MUST
augment or enhance Mermaid rather than remove the required big-picture diagram. The
visual MUST connect to the concept and an anchor-system workflow, with a clear action,
observable consequence, and explanation of what the learner can infer. Examples include
request flow, traffic splitting, queue backpressure, cache expiry, and changing latency.
Decorative motion and unrelated charts MUST NOT count toward this requirement. One visual
MAY support multiple mechanics or scenarios; there is no per-card animation quota.

The interface MUST use a clean, modern documentation-dashboard layout with a recursive
left sidebar, top-bar learning controls, and a main reading canvas. Navigation MUST support
arbitrarily deep nesting without a hard-coded depth limit, starting with Domain → Category
→ Topic → Subtopic. Every navigation node MUST display a completion badge or progress
ring; container nodes MUST reflect their descendant topics' progress.

Rationale: visible relationships and predictable navigation reduce the effort required to
understand a concept and return to it later.

### III. The Six-Act Story and Progressive Disclosure

Every lesson MUST tell a connected Why -> What -> How -> So What story through the six
modules below, in order. A topic is incomplete if any module is missing or contains an
unexplained placeholder. Preserve the existing six section identities and recall keys;
the act names describe teaching purpose, not a new routing or storage schema.

Every teaching section, including each module and nested explanatory section, MUST begin
with one friendly sentence explaining why the detail matters and how it connects to the
larger story. This signpost MUST be specific to the section and MAY be its first narrative
sentence; repeated generic introductions MUST NOT replace useful orientation. Paragraphs
MUST develop one idea at a time, with short transitions that connect cause and consequence.
Dense walls of text, disconnected fact lists, and unexplained jumps in abstraction MUST
be rewritten. Progressive disclosure MUST move depth out of the initial reading path
without omitting essential reasoning or leaving the open narrative incomprehensible.

1. **🎯 The Hook & ELI5 (Why):** Introduce a universal problem through a relatable situation
   in the standardized project domain. Explain why it matters and give a simple analogy
   before technical terms, targeting intuitive understanding within 30 seconds.
2. **🗺️ High-Level Big Picture (What):** Explain the industry-standard solution with a
   valid Mermaid diagram and an interactive or animated visual within a familiar domain
   workflow. Show the relationship or behavior the visual helps the learner understand.
3. **🔍 Step-by-Step Mechanics (How):** Explain behavior in a logical sequence, connecting
   each step to the opening mental model. Keep the main narrative light; use native
   `<details>` accordions for deep mechanics, code walkthroughs, and optional derivations.
   Use recognizable examples from the anchor tech stack where suitable; explain unfamiliar
   syntax and keep implementation details subordinate to the concept.
4. **⚖️ Comparisons & Trade-Offs (When and Why):** Include a crisp comparison table of
   alternatives, gains, costs, and the conditions that change the decision. Discuss better
   tools or patterns when appropriate even when they are outside the anchor stack.
   When comparing approaches is not meaningful, compare applicable choices or conditions
   and explain the scope explicitly instead of inventing alternatives.
5. **⚠️ Common Pitfalls, Bugs & "What-If" Scenarios (What Breaks):** Cover misconceptions,
   edge cases, and failure modes using Symptom → Root Cause → Fix/Prevention. Explain consequences
   in practical or real-world terms.
6. **🧠 Active Recall & Mastery Check (So What):** Include the Feynman prompt
   "Summarize this in your own words" and three to five foundational active-recall
   flashcards or what-if questions with hidden or collapsible answers. In addition,
   include a dedicated subsection titled **Tricky & Most-Asked Interview Scenarios**
   containing five to seven distinct, real-world scenario-based interview questions.
   Each MUST ask what the learner would do and why under explicit production
   constraints, and MUST use the structured interactive answer format defined in the
   research standard below. Use concrete prompts such as "Imagine this feature's traffic
   doubles... what will you do and why?" within the standardized domain; changing names
   alone MUST NOT count as distinct reasoning. This subsection belongs inside module six;
   it MUST NOT replace foundational recall cards or introduce a seventh top-level story module.
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

Interactive visuals MUST use declarative lesson markup and registered, reusable static
JavaScript assets through the visual-widget contract below. Optional visual libraries
MUST be loaded by the host, not through executable scripts embedded in lesson partials.

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

Widgets MUST mount and clean up through the shared lifecycle, remain understandable with
reduced motion, and provide keyboard-accessible controls and a textual explanation. Their
layout and semantic colors MUST follow host CSS variables in both themes and fit mobile
screens without clipping controls or essential visual content.

The recursive sidebar MUST collapse into a usable drawer on mobile. Reading, navigation,
self-testing, and theme controls MUST remain usable on small screens. Print styles MUST
produce clean PDF output, preserving lesson content, diagrams, and readable comparisons
while removing obstructive navigation and controls. Content hidden by interactive reading
controls MUST remain available in the printed lesson.

Animated, SVG, and Canvas visuals MUST provide a readable print representation and the
explanations needed to understand their important states. A blank canvas, missing chart,
or arbitrary animation frame MUST NOT stand in for the complete printed explanation.

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

### Interactive and Animated Visuals Contract

Each lesson MUST provide the purposeful visual required by Principle II and explain its
inputs, visible behavior, and takeaway. An interactive visual MUST expose a meaningful
learner action and observable result; an animated demonstration MUST provide playback
control. Merely revealing prose or running decorative motion MUST NOT count as a visual.

- **Declarative hook:** Each widget root MUST expose
  `data-visual-widget="<widget-name>"`, using a stable kebab-case widget name. HTML, SVG,
  Canvas elements, explanatory text, and validated configuration MAY live in the partial.
  Executable scripts, inline event handlers, and arbitrary executable configuration MUST
  NOT be embedded in lesson partials or evaluated from their content.
- **Registration:** Shared static assets MUST register both `setup(root, context)` and
  `cleanup(root)` under `window.LabVisuals[widgetName]` before mounting. These functions
  MUST keep state scoped to the widget instance, support multiple instances without
  collisions, and tolerate repeated setup/cleanup without duplicate work or errors.
- **Host lifecycle:** `app.js` MUST mount registered widgets after lesson insertion and
  clean them up before route replacement or removal. Theme rerenders that replace a root
  MUST follow the same cleanup/remount lifecycle. Adding a lesson with an existing widget
  MUST NOT require a route-specific branch or manual core-shell change.
- **Cleanup:** `cleanup(root)` MUST cancel owned requestAnimationFrame loops, timers, and
  cancellable work; remove listeners; disconnect observers and subscriptions; dispose of
  workers and chart instances; and release retained DOM references. Noncancelable async
  callbacks MUST ignore unmounted instances. A failed setup MUST clean up partial
  resources, show an explanatory fallback, and leave other lesson features usable.
- **Lightweight assets:** Widgets SHOULD use zero-build HTML/SVG, animated SVG, or HTML5
  Canvas to keep the static application lightweight and avoid unnecessary dependencies.
  Rough.js and Chart.js MAY be used when they improve the explanation; shared CDN
  dependencies MUST be version-pinned and loaded once through `index.html`. Pre-rendered
  `.svg` charts and reproducible Python generation scripts MUST live in `/assets/visuals/`.
  Static charts MAY complement a widget but MUST NOT alone satisfy the interactive or
  animated visual requirement. Library failure MUST retain a useful text/static fallback.
- **Accessible interaction:** Controls MUST have clear labels, keyboard operation, and
  visible focus. Visuals MUST provide pause, restart, or step controls appropriate to the
  demonstration and honor `prefers-reduced-motion` with manual steps or nonanimated state
  changes that retain learning value. They MUST pause ongoing work while hidden or
  off-screen and MUST NOT require flashing, timing-dependent reading, or color alone to
  convey meaning.
- **Responsive themes:** Visuals MUST use host Light/Dark CSS variables, semantic colors,
  readable contrast, and responsive sizing. SVG view boxes and Canvas/chart resizing MUST preserve
  labels and controls on mobile; theme changes MUST update visuals without duplicate
  instances or losing independent learning state.
- **Print and fallback:** Visuals MUST provide a static diagram/chart or annotated sequence of relevant
  states and a textual takeaway for print, unavailable libraries, and unsupported graphics.
  Canvas output MUST have an intentional print representation. Print MUST show the full
  teaching content without requiring playback or interaction.

Rationale: a shared, explicit lifecycle makes dynamic explanations reusable without
leaking resources or making learning depend on motion, a particular theme, or a mouse.

## Content Workflow and Quality Gates

### Standardized Project Lens and Objective Engineering

Before authoring or substantively revising a lesson, authors MUST read
`.specify/memory/anchor-system.md`. Its clean domain, component names, entities, workflows,
and illustrative scale assumptions MUST be the canonical backdrop for ELI5 examples,
Mermaid diagrams, widget demonstrations, code snippets, and interview scenarios. Use
names such as Transaction Service, Quote Service, Aggregation Service, and Pricing Service
consistently. Authors MUST NOT introduce obscure internal aliases or expose private project
detail.

Lessons MUST teach the universal concept first, using the project to make it relatable.
They MUST NOT audit raw legacy shortcuts, teach organization-specific trivia, or justify
a weak design merely because it appears in a project or fits the familiar stack. When
an analogy is not a literal application, authors MUST explain its boundary instead of
inventing project capabilities or distorting the concept. This preserves accurate
teaching for disciplines beyond the example application's architecture.

Authors MUST use the anchor's TypeScript/Node.js, Python/FastAPI, and database tools when
they clarify the mechanism. They MUST compare industry-standard alternatives objectively and
recommend a better-suited tool or pattern when constraints warrant it, including options
outside that stack and state the relevant benefits, costs, and conditions. Authors MUST NOT
present any tool or pattern as universally best. The anchor stack guides example syntax,
not the dashboard runtime constraints in Principle V.

Anchor workload figures MUST remain illustrative assumptions, with the scope and units
needed to reason about them. Authors MUST NOT turn them into production measurements,
performance guarantees, or unsupported business claims. Lessons MUST remain self-contained
and MUST NOT require readers to inspect raw project documentation to understand an example.

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

### Teaching Standard Adoption and Widget Rollout

Version 3.0.0 governs all new and substantively revised lessons. The required voice,
section signposts, six-act progression, standard project naming, and meaningful visual
behavior MUST be reviewed together; adding a widget MUST NOT substitute for complete
explanations, recall, or researched interview answers.

The LabVisuals registry, `app.js` lifecycle, shared asset loading, safe SVG/Canvas support,
and any `index.html` library integration are required platform work, not capabilities
delivered by this amendment. They MUST be specified, implemented, and verified through
the full Spec Kit workflow before a dependent lesson is accepted. Authors MUST NOT work
around missing host support with embedded scripts or report pending gates as passed.

An implementation assessment MUST align the publishing workflow, relevant skills and
templates, supported partial contract, validators, and browser/print checks. This
constitution-only amendment does not modify those artifacts. Structural validation alone
MUST NOT be represented as proof of friendly prose, technical accuracy, or teaching quality.

Existing unchanged lessons retain their recorded acceptance baseline until explicitly
migrated. A migration MUST define its inventory and preserve topic IDs, recall keys,
progress, review history, confidence, sources, and research evidence. Neither this
amendment nor an earlier presentation migration establishes v3.0.0 conformance. Frozen
historical baselines MUST remain unchanged; adoption and verification remain pending
until the relevant lessons and platform changes are delivered and reviewed.

### Interview Scenario Research and Answer Standard

For every new or substantively revised topic lesson, the AI MUST research and author
five to seven distinct questions for its **Tricky & Most-Asked Interview Scenarios**
subsection. Each question MUST concern the exact concept being taught and present a
real production situation, an explicit constraint or failure, and a decision prompt:
"What will you do and why?" Definition-only questions, vocabulary checks, and superficial
rewrites of the same scenario MUST NOT count toward these five to seven questions.

Scenario sets MUST use the anchor's standard domain and names, with engaging prompts
that test the concept under concrete scale, latency, consistency, reliability, or budget
constraints. They MUST test universal decisions rather than recall of private project
behavior. Where an industry-standard alternative fits better than the anchor stack, the
answer MUST explain and defend that alternative.

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

Editorial review MUST also verify a friendly conversational voice, purposeful analogies
and transitions, one-sentence signposts for every teaching section, connected story flow,
progressive disclosure, and accurate use of the standardized project lens. It MUST reject
forced humor, dense fact dumps, legacy-design rationalizations, invented capabilities,
and examples whose familiarity obscures the universal trade-off.

Visual acceptance MUST verify the explained Mermaid diagram and at least one meaningful
interactive or animated demonstration per lesson. Browser checks MUST exercise controls,
keyboard access, reduced motion, mobile layout, both themes, repeated navigation, hidden
visual pausing, and cleanup after route replacement, including setup-failure handling.
They MUST confirm that callbacks, listeners, instances, and retained resources do not
accumulate across repeated mounts. Print review MUST verify static visual states and full
answers. Shared lifecycle/library/style changes require catalog-wide regression as above.

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

Version 3.0.0 establishes friendly conversational teaching, six-act progressive disclosure,
purpose-driven signposts, the standardized anchor-system lens, and mandatory purposeful
interactive visuals with a managed LabVisuals lifecycle. This is a MAJOR amendment because
the visual requirement changes lesson acceptance and requires a new host integration
contract. It preserves six modules, foundational recall, researched interview scenarios,
named Sources, immutable identities, and learning state. Runtime integration, workflow
alignment, and scoped lesson migration require subsequent implementation and acceptance;
the amendment itself delivers governance only.

**Version**: 3.0.0 | **Ratified**: 2026-11-17 | **Last Amended**: 2026-11-25
