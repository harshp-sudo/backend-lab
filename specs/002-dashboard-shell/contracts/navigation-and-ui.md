# Navigation and Dashboard UI Contract

**Version**: 1 | **Scope**: FR-001–016/024/030–032

## Manifest profile

Read `./manifest.json` and conform to the existing [canonical schema](../../001-backend-architecture/contracts/manifest.schema.json). Enforce IDs/routes unique globally and sibling slugs unique. Preserve opaque IDs and metadata. Do not add a runtime schema-library dependency.

Explicit runtime-only initialization sentinel: `schemaVersion:1` with `roots:[]` shows the empty-library dashboard. It is not a publish-valid catalog and does not change the canonical schema. Nonempty catalogs must enforce every canonical recursive restriction, including roots being hubs and hubs having nonempty children. A malformed catalog produces a blocking catalog error with Retry.

## Routes and resources

| Destination | Hash | Resource |
| --- | --- | --- |
| Home | empty hash, `#`, `#/` | Rendered dashboard; no home partial. |
| Hub | `#/<ancestor-slugs>/<slug>` | `./topics/<ancestor-slugs>/<slug>/_overview.html` |
| Topic | `#/<ancestor-slugs>/<slug>` | `./topics/<ancestor-slugs>/<slug>.html` |
| Topic section | Same hash + `?section=<key>` | Same topic, then scroll to recognized section. |

Allowed section values are the six existing section keys. Exactly one `section` parameter is allowed, only for topics. No trailing slash except home. Validate raw hash grammar before any URL normalization: reject percent-encoded path characters, dot segments, doubled slashes, backslashes, extra query entries, empty section values, and unknown routes. Current slugs require no URL decoding. Never turn user route text directly into a fetch path; fetch only a preindexed known resource.

Root `app.js` computes its own directory from `import.meta.url` and supplies that base to other modules. All app-owned HTML asset URLs start with `./`; no `<base href>` or origin-root asset references. Fonts/libraries may use the explicit HTTPS assets documented in the content contract.

Use ordinary hash anchors. Preserve modified clicks/new-tab behavior, browser back/forward, and existing authored partial links. Same-route activation may focus the article or retry its failed loading state; section-only changes retain the article. Invalid routes display an error and Home/Retry rather than mounting stale content.

## Application landmarks and status

One header, navigation landmark, main canvas, and skip-to-content control. Announce loading/completion/errors through a polite status region; expose `aria-busy` while the active content request is pending. On successful route navigation, focus the article/home heading with programmatic `tabindex=-1`; section links focus the target heading instead. Failed routes get an error heading.

Clear or explicitly cover stale canvas content when a different destination starts loading. Update breadcrumbs/title/active selection only for the current generation. A selected node may appear as loading; it must not claim its article succeeded before envelope validation.

## Recursive sidebar

- Render nested ordered-in-source lists with normal links, separate buttons labeled Expand/Collapse plus node title, and `aria-expanded`/`aria-controls`.
- Do not apply `role=tree`; standard tab navigation and native links are the keyboard model.
- Keep collapsed branches in the DOM with hidden sublists, preserving expansion choices during navigation and progress updates.
- Ensure the active path's ancestors are expanded. Use `aria-current=page` on the active link.
- Topic badge labels are Not Started, In Progress, and Mastered, with distinct text/icon shapes. Hubs show descendant mastered/total and percentage; zero descendants never means completed.
- No hard-coded depth limit. Deep indentation must not push every label/control out of the narrow drawer; cap visual indentation or allow local navigation overflow while retaining the complete hierarchy.

At viewport widths below 64rem, move the one sidebar element into a labeled modal drawer; at or above 64rem move it back to the desktop sidebar mount. Close the drawer on successful destination choice, Escape, close button, backdrop click, or transition to desktop. Restore opener focus on dismissal; for route activation, focus the destination heading after load.

## Dashboard home

Compute all views from the catalog and the same workspace snapshot:

- Overall mastered/total plus rounded percentage.
- Category cards from each root's immediate hub children; use that root if it has none. For the current manifest this means one Backend Architecture card linking to its existing overview with four category cards.
- Continue Learning: last visited unfinished topic; manifest-order tie/fallback. Hubs do not change it. All-mastered state offers earliest due or next scheduled review.
- Due for Review: current mastered topics only, earliest due first, manifest-order ties, inclusive due boundary. Show title/path, due information, and a normal topic link.
- Friendly empty/no-review/all-complete states; never manufacture sample learning records.

Recompute on learning changes, Home entry, focus regain, and visibility return. While Home remains visible, use one next-boundary timer capped to the platform timer range so a review can become due without a reload. Use absolute timestamps for logic and localized dates for display.

## Header and search

Header includes breadcrumbs, a visible search opener and shortcut hint, labeled global `<progress>` or equivalent semantic bar, theme control, Export, and Import. Controls may wrap on mobile rather than overflow.

Search uses a native labeled dialog, focused input, and a result list with a selected/active-descendant indication. Keyboard ArrowUp/Down changes selection, Enter opens it, and Escape closes. List results have ordinary accessible links. Empty query lists the catalog in preorder; no matches has a visible message.

Match normalization: trim/collapse whitespace and lowercase; include title and full title/slug paths. Ranking buckets are exact title, exact title/path phrase or words (all query words present), then title/title-token edit distance <=1 for a query >=4 characters. Exact title is always first; manifest index breaks ties within each bucket. This defines insertion/deletion/substitution behavior without a fuzzy-search package.

Cmd+K or Ctrl+K opens/focuses search and prevents the browser shortcut. Avoid opening a second modal: close the existing modal first with its correct cancellation semantics. Search dismissal restores its opener, unless a result navigation intentionally moves focus to content.

## Theme, backups, and focus

Explicit theme uses the workspace preference. Null follows `prefers-color-scheme`, with light fallback; observe device changes only while null. Switching theme updates only appearance and saved preference, not status/review data.

Import uses a labeled native preview dialog showing supported backup metadata, counts of matched and unmatched topic records, and known/unknown recall-key information when mounted content makes it available. Never fetch every lesson solely to enumerate recall keys during a preview; unmatched question records are retained regardless. Confirm replacement or Cancel are explicit. Persistence failure leaves the existing record and open failure explanation intact.

Only one modal is open at a time. Use `showModal()`, explicit close/backdrop handling, and native Escape support; no dependency on newer optional dialog invocation attributes. Confirm keyboard focus is contained and restored through real-browser tests.

## External boundary

No server endpoints, accounts, remote progress calls, custom rewrite configuration, or hosting-setting mutation. The externally portable data interface is the versioned [progress backup](progress-backup.schema.json); trusted repository HTML is the content input, not an arbitrary user HTML upload.
