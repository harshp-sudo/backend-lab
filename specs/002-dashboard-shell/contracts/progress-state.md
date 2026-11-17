# Progress State and Backup Contract

**Version**: 1 | **Scope**: FR-019–029
**Schema**: [progress-backup.schema.json](progress-backup.schema.json)
**Example**: [progress-backup.example.json](progress-backup.example.json)

## Storage and export

Store one JSON workspace under `backend-lab.learning.v1`. Its shape is schema `$defs.state`; exported files use the schema root envelope. Export names may use `backend-lab-progress-<UTC-date>.json`, MIME `application/json`. The backup's `exportedAt` is not restored as the workspace's `updatedAt`.

Missing state means empty topics, null theme preference, and a current valid initial `updatedAt`; creating that default need not write storage until a real mutation occurs. No migration from `tests/fixtures/content-host.js` is needed because that fixture deliberately saved no learning state.

All timestamps use canonical UTC `YYYY-MM-DDTHH:mm:ss.sssZ`. Validate actual calendar/time values as well as string syntax. Future timestamps are not inherently invalid: a backup may come from another device/clock. Review arithmetic uses integer milliseconds and 86,400,000 ms per day, not local calendar-day mutation.

## Validation beyond JSON Schema

Validate every record, including unmatched IDs, before preview or restoration:

1. Require the exact supported format/version and complete field shapes. Reject unknown structural properties rather than silently discarding data from a potentially incompatible future format.
2. Treat topic IDs as opaque nonempty whitespace-free strings; do not impose UUID policy on catalog identities. Recall keys remain kebab-case. Use own-key/Map semantics, not assignment/merge into application prototypes.
3. A mastered topic requires a non-null review record. A never-mastered topic may have null review; a demoted topic may retain its prior record.
4. Review history starts at cycle 1 with a `mastered` event/index 0. Within a cycle, only `review` events follow, advancing index by exactly one capped at 3. A new cycle increments by one and starts with a mastery event/index 0.
5. `review.cycle`, `lastReviewed`, and `intervalIndex` must equal the last history event's values. Mastery events have null session IDs; review events have unique non-null session UUIDs within the topic.
6. A non-null session must belong to the latest cycle and a mastered topic. An unfinished session ID must not already appear in history. A completed session must correspond to exactly one review event in its cycle, with matching completion time; it must be the latest completed review event.
7. Session completion cannot precede its start. Clearing a session during demotion does not remove historical completion events. Starting another review replaces the session record but leaves its earlier history event.
8. Review state is historical when status is unfinished: ignore its schedule for due views. Remastery derives the next cycle from the retained record, never from a route or a question confidence value.

Schema checks alone cannot enforce these sequences or compare timestamps. The application implements these explicit semantic rules, and focused tests exercise invalid histories rather than duplicating every schema property test.

## Review operations

`Start Review` is available on mastered lessons. It creates a session only on deliberate activation. If a session is already unfinished, preserve its token and show Resume Review/Complete Review rather than creating another.

`Complete Review` receives the topic ID and current session token. Require a mastered topic, matching latest cycle, and matching unfinished session. Append one review event with next index `min(index+1,3)`, update `lastReviewed`, and persist the completed session. A repeated token is a no-op; a stale token cannot affect a new cycle or session.

After completion, disable/remove that completion action and show an explicit Start Another Review control. Reloading or revisiting retains the completed token. Early review is allowed only through the same explicit start/complete flow.

First mastery creates a review at index 0. Repeated Mark as Mastered on an already-mastered topic does not change timestamps, history, session, or `updatedAt`. Demotion clears the session but preserves history. Remastery starts the next cycle and a fresh 3-day interval.

## Safe import transaction

1. Read the selected file without mutating storage, in-memory state, theme, or progress controls.
2. Parse, structurally validate, then semantically validate the whole backup. Invalid files expose a useful reason and retain existing state.
3. Preview replacement: backup timestamp, matched current topic records, unmatched IDs, mastery counts, and any determinable unmatched question keys. Unknown records are retained; catalog/question matching does not determine structural validity.
4. Cancel, Escape, selecting a different import, or opening another modal discards the candidate without changes.
5. On Confirm Replacement, serialize the candidate workspace once and attempt a single `localStorage.setItem`. Do not clear storage or write topic records one by one.
6. If the write fails, leave the existing memory and stored value unchanged, report restoration failure, and retain the candidate only for retry/cancel.
7. Only after a successful write, publish the restored document, refresh all current views and theme, and close the preview with a success message. Do not stamp a fresh visit merely because import repaints the mounted lesson; that would alter restored values.

The portable record is replaced, not merged. Unknown IDs/questions in the incoming record survive; records absent from the incoming snapshot are removed only after this explicit confirmation.

## Ordinary persistence failures

Normal learning changes update the current session and attempt a whole-document write. On success, announce saved state where appropriate. On failure, keep that session record, show a persistent unsaved warning, and offer JSON export. Do not claim a save succeeded.

If initial storage is corrupt or an unsupported version, preserve its raw stored value and block automatic writes. Use an empty warned in-memory session for reading and explicit edits. A valid confirmed import is the replacement/recovery path. If storage access itself is unavailable, reading and export still work; import cannot claim durable restoration until its write succeeds.

No reset/clear-storage control, multi-tab conflict resolution, or remote synchronization is introduced by this feature.

## Example acceptance meaning

The example contains one currently known mastered topic (Clean Architecture) and one unmatched topic. At 2026-11-17T06:00:00.000Z:

- Current global mastery is 1/15, rounded to 7%; the unmatched In Progress record is excluded.
- Clean Architecture has `good` confidence for `dependency-direction`.
- Its completed cycle-1 review at 2026-11-04T09:05:00.000Z uses index 1 (7 days); its due instant is 2026-11-11T09:05:00.000Z.
- Replaying its recorded completed session cannot advance to index 2.
- Export/import preserves both topic records and all values, including its explicit dark preference, without creating a new visit.
