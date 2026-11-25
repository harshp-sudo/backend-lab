# Contract: Compact Progress and Review Controls

**Status:** Implemented and verified; see [delivery](../delivery.md).
**Related:** [Spec](../spec.md), [state model](../data-model.md).

## Visible interface

Every lesson has exactly one `.lesson-toolbar[data-host-controls]` immediately after its
title. Keep one native `select#topic-status` with the visible associated label Progress
and text options Not Started, In Progress and Mastered; underlying values stay
`not-started`, `in-progress`, `mastered`.

Remove `#mastery-actions`, `.mastery-footer`, MAKE IT YOURS, both motivational headings,
associated helper prose and the old Mark as Mastered button. Remove the old Your
understanding / Progress is yours to decide text. The in-lesson mastery module, Feynman
prompt and green educational impact callouts remain.

| Learning state | Additional compact content |
| --- | --- |
| Not Started | None |
| In Progress | None |
| Mastered, no active/completed session | Next review date + Start review |
| Mastered, incomplete active session | Next review date + Complete review |
| Mastered, completed session | Next review date + Start another review |
| Hub | No lesson progress control |

The date remains readable, with a short visible Next label and an accessible complete
meaning/date. A compact visible date must not create ambiguous scheduling. Use the actual
existing lastReviewed/interval rather than a new calculation policy.

## Interaction and focus

- Status selection invokes the existing markStatus action, including explicit Mastered.
  Remove the obsolete footer-only `master-topic` handler; do not recreate its button elsewhere.
- Review actions invoke the existing start/complete functions with current session identity.
- Keep the select DOM node stable during store refreshes. Update only dependent review
  content; do not remove/recreate a focused native selector during selection.
- If Start review replaces its own focused button, focus Complete review. After completion,
  focus the new start/restart control. If a relevant focused control disappears on a status
  change, focus the status selector.
- Do not move focus when refresh was caused by confidence rating, theme, another store
  update, or import while focus is elsewhere. Preserve normal route/import-dialog focus.
- Use a local no-scroll focus restoration when replacing a control; visible keyboard focus
  must remain discernible. No focus trap or document-heading fallback tied to the removed
  footer.
- The existing persistence notice remains outside the measured compact row and truthfully
  reports unsaved session-only changes or failed import replacement.
- Repeated same-status selection and stale/replayed review events preserve existing no-op
  behavior. Reading, revealing and rating never start/complete mastery or review.

## Layout/accessibility

| Width/state | Measured requirement |
| --- | --- |
| Desktop ≥1024px, every state above | One row, bounding height ≤56px |
| 360px mobile, Not Started/In Progress | One compact status row |
| 360px mobile, every mastered/review state | At most two rows, bounding height ≤112px |
| Every status/action control | Target width and height ≥44px |

Use existing theme tokens with compact flex/grid layout. At 360px, reserve the first row
for label/select and the second for review date/action, with at most 8px gap. Permit date
text to flex rather than shrinking the action target. No large card padding, promotional
heading, hidden action, clipped option label or horizontal page overflow.

Height applies at ordinary browser text size and excludes an open native menu or temporary
error feedback. At enlarged text, retain operability and reflow rather than imposing a
fixed clipped height. Measure real target/row geometry in browser acceptance for both
themes and the longest review label; do not rely solely on declared CSS dimensions.

Keyboard users can Tab to the selector, change its native options and reach the relevant
review action. Pointer status selection takes at most opening the selector and choosing
the option. The row must have understandable names and status text independent of color.

## Integration and preservation

Reuse learning-state version/key, confidence events, review cycles/history and backup
envelope. Preserve unknown imported topics and exact old records except effects of an
explicitly tested action or normal visit. Verify seeded records from all nine current
branches; use isolated contexts and a fixed clock for comparisons and review boundaries.

Check sidebar/ancestor/global progress, Continue Learning, due queue and JSON backups
against the same known-topic state. Advance the controlled visit clock when proving a
strictly most-recent Continue Learning shortcut, so timestamp ties do not create a false
failure. Test immediate-before/at-due 3/7/14/30-day boundaries and review replay protection.

## Print and browser coverage

The row retains `data-host-controls` and is hidden by current print rules. Do not modify
the behavior opening all details for print and restoring their prior states afterward.
PDFs must include the actual Feynman module and every source/answer/diagram label.

Feature checks cover 1024/1440px and 360px, both themes and base paths, status/review matrix,
selector/review/card focus, reload/import active sessions, corrupt storage/write failures,
target geometry, no banner/duplicate controls, and all current application journeys.
