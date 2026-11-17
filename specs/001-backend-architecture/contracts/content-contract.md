# Content and Host Contract v1

**Consumers**: A compatible static dashboard and the test-only reading fixture.
**Producers**: The manifest and topic/hub authoring workflow.
**Scope**: FR-004–FR-018 and FR-020. The real dashboard is currently absent.

## Partial Envelope

Each UTF-8 HTML partial has exactly one root `<article>`, a matching manifest `data-node-id`,
and one `<h1>` with the manifest title. Topic articles use `.kb-topic`; hub articles use
`.kb-hub`. Outside the article, permit only whitespace and author comments.

Do not include `doctype`, `html`, `head`, `body`, `script`, `style`, stylesheet links,
inline event handlers, inline style attributes, application chrome, or storage operations.
This is an authoring contract for trusted repository content, not a general-purpose HTML
sanitizer or a way to import arbitrary untrusted HTML.

The host loads one article into its reading canvas. It owns shared styles, libraries,
navigation, themes, print preparation, confidence/status controls, and persistence.

## Topic Section Contract

Each topic contains these direct child `section[data-section]` elements, in order, after
its title and optional short introduction. Each section has its own descriptive `<h2>`.

| Section key | Required content |
| --- | --- |
| `hook-eli5` | Problem, why it matters, intuitive model and everyday analogy before jargon. |
| `big-picture` | At least one Mermaid diagram, explained in surrounding prose. |
| `mechanics` | Complete step-by-step mechanics in native details cards connected to the analogy. |
| `trade-offs` | Decision table with alternatives/conditions, gains, costs, and choice guidance. |
| `pitfalls` | Topic-specific Symptom → Root Cause → Fix/Prevention stories and practical impact. |
| `mastery` | Feynman prompt, three to five foundational recall questions, a nested five-to-seven-card interview subsection, real-world takeaway. |

Section IDs use `node-<node-id>-<section-key>` so they remain unique and stable. The router
accepts the section key rather than requiring the long DOM ID in authored links.
Supporting source links may appear alongside the relevant explanation or in a references
footer after the six modules. They do not substitute for complete lesson prose.

Recall items are `<details class="kb-question" data-recall-id="<stable-local-key>">` with
a meaningful `<summary>` question and a complete answer body. No recall disclosure has an
initial `open` attribute or a shared `name`. Closing/opening one question must not change
another question. Code and diagram examples must encode HTML-special characters as text.

## Hub Contract

Each hub contains a short ELI5 introduction, a Mermaid roadmap, suggested reading guidance,
and a visible child-link list marked `data-child-links`. This list has exactly one labeled
link per immediate manifest child in child order, preserving unrelated children. Related
or recommended reading links may exist outside that list.

Roadmap diagram labels describe the same immediate children as the list; explanatory prose
and human review verify conceptual accuracy. Navigation must not depend on clicking diagram
nodes. Hubs are complete lightweight orientation pages, not incomplete topic lessons.

## Navigation Grammar

| Purpose | Authored form | Host behavior |
| --- | --- | --- |
| Topic or hub | `#/<ancestor-slugs>/<node-slug>` | Resolve the exact known manifest route and mount its derived content. |
| Lesson section | `#/<ancestor-slugs>/<topic-slug>?section=mechanics` | Mount/retain the lesson, open containing disclosure if needed, scroll to the section. |
| External source | Absolute `https:` URL | Follow as an external reference; do not treat as a content route. |

Content routes have no trailing slash and permit no query except one recognized section
key. Do not use bare `#mechanics`, since it would replace the hash route. Content anchors
remain ordinary accessible `<a>` elements. The host preserves modified-click behavior and
browser back/forward navigation. Unknown routes/sections produce a visible error without
claiming the requested content loaded.

Requests for `manifest.json` and derived `topics/...` resources resolve against the host's
application base URL. A deployment under `/backend-lab/` must not fetch from the origin's
`/topics/` directory. The same partials must work under either base without editing them.

## Rendering Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant Host
    participant Manifest
    participant Canvas
    User->>Host: Follow known content route
    Host->>Manifest: Resolve permanent ID and derived resource
    Host->>Canvas: Mount matching article
    Host->>Canvas: Render diagrams and code; attach host controls
    Host->>Canvas: Update context and optional section scroll
    Canvas-->>User: Complete lesson or visible rendering error
```

The host initializes Mermaid once with `startOnLoad: false` and `securityLevel: "strict"`,
then awaits `mermaid.run({ nodes: mountedDiagramNodes })` after each mount. It retains original
diagram source before rendering so theme changes can reconstruct and rerender blocks.
Rendering errors fail the browser check; do not suppress them and report success.
[Mermaid usage](https://mermaid.js.org/config/usage.html)

Mermaid blocks use `<pre class="mermaid">`. Include `accTitle` / `accDescr` where supported,
with an adjacent prose explanation in every case. Code uses `<pre><code class="language-…">`
and the host highlights newly mounted code elements with `hljs.highlightElement`; exclude
Mermaid blocks. Use plaintext where no supported language grammar applies.
[Mermaid accessibility](https://mermaid.js.org/config/accessibility.html),
[Highlight.js API](https://highlightjs.readthedocs.io/en/latest/api.html)

The browser-fixture baseline uses exact versioned browser assets: Mermaid `12.3.0` ESM and
Highlight.js `11.11.1`. No npm runtime or build is required. The fixture records asset URLs,
versions, browser version, and errors in its report; missing assets fail rather than silently
skip diagram checks. The production host may select another compatible, tested version.

## Shared Presentation and Controls

Host styles support `.kb-card`, `.kb-callout--structure` (blue), `.kb-callout--insight`
(yellow), `.kb-callout--impact` (green), `.kb-callout--pitfall` (pink/red), `.kb-table-wrap`,
and `.kb-diagram`. Shared typography follows the constitution. Tables have semantic headers
and captions/context; wide content can scroll within its wrapper on mobile. At 360-pixel
width the page itself must not overflow because of a table or diagram.

The host implements this common style vocabulary once, using its constitutional Tailwind
setup; the test fixture supplies a small reference stylesheet, not a production design
system. Native headings, links, summaries, and lists preserve readable structure without CSS.

The host identifies the current topic through the article's stable ID and recall questions
through `data-recall-id`. It supplies its existing status and confidence controls. Partials
do not include empty control placeholders, nonfunctional buttons, or a second state engine.
Opening a lesson or answer never implies mastery.

## Print Lifecycle

Before printing, save disclosure open states and open all mechanics and recall details.
Shared print CSS hides dashboard/control chrome, preserves all prose and answers, and fits
diagrams and tables to the printable width. After printing, restore disclosure states.
Check actual print preview/PDF, not only print-media emulation.
[MDN printing guide](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Printing)

## Acceptance Boundary

The browser fixture demonstrates this proposed contract on all 21 partials, including
mount/unmount, diagrams, keyboard disclosures, themes, mobile width, and print restoration.
It must not implement a dashboard sidebar, search, persistent learning engine, review queue,
or backup UI. Passing the fixture is not evidence that a real dashboard conforms. That
integration remains separately pending until tested against an actual host.

## Current scenario profile — constitution v1.2.0

Published lessons use `constitution-1.2`: retain three to five foundational cards and add exactly one nested mastery subsection titled **Tricky & Most-Asked Interview Scenarios** with five to seven independent native scenario cards. The original six direct modules remain. Each new card has a permanent `interview-` key, `data-recall-kind="interview"`, an honest research basis, and three ordered labeled answer parts with complete constrained decisions, alternatives and follow-up traps.

The normative [scenario grammar](../../003-backfill-interview-scenarios/contracts/scenario-content.md), [research/editorial evidence](../../003-backfill-interview-scenarios/contracts/research-and-review.md) and [preservation/validation contract](../../003-backfill-interview-scenarios/contracts/preservation-and-validation.md) define the exact current markup and acceptance. Missing kind still means foundational. Existing host controls provide confidence, keyboard/native disclosure and print behavior without per-lesson scripts/styles.

Only explicit historical unit fixtures may request `legacy-1.1`; production validation never infers or accepts a legacy waiver. Feature 001/002 reports remain historical results rather than evidence of this migration.
