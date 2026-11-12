# Frontend, accessibility, and interaction lens

Trigger: browser/app interaction, UI state, forms, asynchronous views, or client-side changes.

Trace user state across loading, success, error, retry, navigation, reconnect, cancellation, and unmount. Check stale responses overwriting newer input, duplicate submit, pending actions after logout/tenant switch, optimistic updates that cannot roll back, missing cleanup, and derived state drifting from the source of truth. Controlled deferred responses are more useful than fast happy-path mocks for races.

Inspect keyboard order, focus visibility and restoration, accessible names, semantic controls, disabled/error states, screen-reader announcements, contrast, zoom/reflow, motion preferences, touch targets, and non-color-only feedback where applicable. Use the project's target accessibility standard and primary official documentation when compliance is claimed. Do not call a visual inspection an accessibility certification.

Test responsive and overflow behavior with long labels, translated text, empty content, large content, and slow/failing requests. For forms, distinguish client guidance from server validation; the server still owns security and data invariants. Confirm destructive actions have the intended confirmation and recoverability, not simply a hidden button.

Inspect browser/server rendering boundaries, hydration assumptions, storage permissions, multi-tab state, history/back navigation, clipboard/file APIs, and focus traps only when present in the scope.

## Ownership and external lifecycle

Treat DOM nodes, cached element references, observers, listeners, scheduled callbacks, pending requests, subscriptions, and view state as resources with explicit owners and validity conditions. The component that creates or caches a resource is not necessarily the only component that can invalidate it.

Trace both sides of shared UI boundaries: identify the component that owns the resource, the parent/host that owns its container, every sibling or route that can replace or mutate that container, and every callback or consumer that may still run afterward. Search all relevant replacement paths, including loading, empty, error, retry, filter/subject changes, layout switches, navigation, parent re-renders, unmount, and direct DOM replacement (`innerHTML`, `replaceChildren`, or equivalent). Do not assume the owning component's `clear()` or `destroy()` runs when another owner replaces its backing DOM.

Coordinate disposal or invalidation before the backing resource is replaced. Stop or cancel animation frames, timers, observers, subscriptions, and obsolete requests before they can continue against invalid state; release detached references; and reacquire references when a new resource generation is created. Make cleanup safe when called more than once. A generation check or connectivity check can be useful defense in depth, but it does not replace an explicit ownership/lifecycle contract between the component and the code that can invalidate it.

Test external invalidation while work is pending, not only the component's own `clear()`/`destroy()` methods. Exercise successful replacement, loading and error fallbacks, navigation/layout changes, retry/recreation, and delayed callbacks. Verify that no stale reference is updated, no obsolete work continues, the replacement view behaves normally, and a later mount can establish fresh references.

## Evidence

Evidence should identify the interaction sequence, snapshot, environment, expected/actual state, and screenshot or reproducible automated check where available. Test the original failure plus a neighboring schedule and normal behavior. If no browser is available, perform source-level review and explicitly label untested layout, accessibility, and runtime behavior.
