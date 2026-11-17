# Project workflow

Read `.specify/memory/constitution.md` before changing lessons or application behavior.

## Route requests by scope

- **Add or revise topic content** using the existing manifest/partial contract: read
  `.agents/skills/topic-publish/SKILL.md` and execute its lightweight publishing workflow.
  This includes batches, taxonomy placement and missing parent hubs. One ordinary request
  authorizes research, complete authoring, integration and verification; do not require
  the user to invoke specify → plan → tasks → implement separately.
- **Dashboard behavior, routing, persistence, manifest schema or learning-standard changes**:
  use the appropriate full Spec Kit workflow. A historical migration is an explicit scope,
  not the default validation profile for future topics.
- Honor an explicit request for planning only, a particular skill/stage, or a full Spec Kit
  cycle. The content profile in the Spec Kit skills keeps those stages compact; it must
  not turn a planning request into implementation or silently resume an older feature.

For routine content, inherit the constitution and supported markup. Do not create fresh
spec/data-model/contracts/evidence ledgers or change the shell unless the scope needs them.
Keep one complete authoring item per lesson in a batch. Never shorten lessons to save time.
Use `docs/topic-publishing.md` for commands, research records and verification scope.

Run `python3 tools/check_topics.py` with explicit paths plus a pre-edit manifest snapshot,
or with `--changed` (includes untracked files). Whole-catalog intrinsic validation is always
required; browser/PDF checks target the changed lessons and affected hubs. Broaden checks
for shared runtime/style/state changes as documented. A pending or failed gate is not done.
Never rewrite frozen migration baselines to make a new topic pass. Preserve existing node
IDs, recall keys, progress and unrelated work. Commit/push only when requested.
