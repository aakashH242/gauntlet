# Performance, optimization, resources, and operations lens

Trigger: hot paths, large or variable inputs, high-frequency updates, data-heavy views or visualizations, repeated rendering or transformation, caches, queues, resource ownership, CI/CD, infrastructure, or production-readiness claims. Select this lens when scale or resource use can materially affect latency, throughput, cost, availability, or correctness—even if the request is framed as a feature or UI change rather than a performance task.

## Required optimization-pattern audit

For each relevant hot path and data path, perform a bounded scan of the patterns below. Mark each **applicable**, **not applicable** with a reason, or **not assessed** with the evidence gap. Do not silently skip a pattern that plausibly affects the target. These are investigation dimensions, not automatic prescriptions: recommend or implement a change only when its benefit, cost, invalidation rules, and semantic effects are understood.

1. **Recomputation versus reuse.** Look for invariant or derived values recalculated inside loops, repeated requests, event handlers, render cycles, animation frames, or repeated workflow stages. Check counts, indexes, parsed configuration, query results, layout, selectors, DOM references, and other stable intermediate results. Compute once per valid version or reuse a safely owned result when appropriate. For every cache or precomputation, define its key, invalidation condition, lifetime, concurrency behavior, and memory bound; stale or unbounded reuse is not an optimization.
2. **Repeated scans versus indexed lookup.** Look for nested iteration, repeated `find`/`includes`/`indexOf`-style searches, repeated group or relationship discovery, N+1 database/API calls, and query plans that scan or join the same data repeatedly. Consider a Map, Set, hash/sorted index, database index, batched lookup, or precomputed membership/position map. Account for index construction, update cost, memory, ordering, and freshness; an index is useful only when its total lifecycle cost is lower.
3. **Full rebuild versus incremental change.** Check whether a small input or state change reconstructs an entire page, component tree, DOM/SVG scene, result set, cache, index, serialized payload, or workflow output. Consider stable identities, diff/patch, incremental aggregation, targeted updates, and reuse of unchanged structures. Verify that incremental paths handle deletion, reordering, retries, invalidation, missed updates, and recovery without drift; a full rebuild may remain safer when changes are broad or consistency cannot be maintained.
4. **Entire dataset versus relevant working set.** Check whether a request loads, computes, stores, or renders more data than the current operation needs. Consider pagination, windowed queries, time/range partitioning, lazy detail loading, virtualization, viewport culling, projection, aggregation, sampling, and progressive disclosure. Preserve global semantics: a viewport-limited display must not silently change lifetime totals, filters, counts, completeness claims, or the meaning of an “all” view. Keep accessibility and navigation usable when content is virtualized or culled.
5. **Per-item work versus batching.** Look for one query, network request, serialization step, allocation, or expensive transformation per record when work can be grouped. Consider batch reads/writes, joins, prefetching, vectorized operations, bulk APIs, or bounded parallelism. Bound batch size and concurrency; preserve ordering, isolation, partial-failure reporting, rate limits, fairness, and cancellation.
6. **Stable work versus frequently changing work.** Separate data/layout/configuration that changes rarely from state that changes often. In interactive or animated systems, avoid rerunning static layout, collision, lookup, or DOM-discovery work at input-event or frame frequency. Update only active/visible elements and the state that actually changed. In non-UI systems, apply the same principle to stable pipeline stages, shared setup, and repeated background work.
7. **Repeated data movement and materialization.** Trace copies, allocations, parsing, encoding/decoding, object expansion, sorting, and serialization across the full path. Check whether data is transformed multiple times, fetched and discarded, or fully materialized when streaming, projection, query pushdown, or a compact representation would suffice. Move work to the layer that owns the data when it reduces transfer and total work without creating an unsafe coupling or moving pressure to an overloaded dependency.
8. **Scheduling, coalescing, and cancellation.** Inspect high-frequency inputs, duplicate refreshes, repeated invalidations, polling, animation scheduling, retries, and background tasks. Consider coalescing equivalent work, bounded debounce/throttle, demand-driven scheduling, single-flight requests, and cancellation propagation when semantics allow. Do not lose the final user input, delay correctness-critical work, add arbitrary sleeps, or leave obsolete work running after a newer request or cancellation.
9. **Retained state and resource lifecycle.** Check caches, maps, indexes, listeners, subscriptions, timers, tasks, pending requests, file handles, connections, and temporary results. Identify the owner, creation point, cleanup point, maximum size/lifetime, and behavior on errors, cancellation, navigation, restart, and shutdown. Look for duplicate listeners, orphaned tasks, stale references, and state that grows with total history when it should grow only with the active working set.

## Resource and complexity attack

Identify input-controlled loops, fan-out, recursion, expansion, regex backtracking, joins, scans, sorting, serialization, rendering, and cross-layer amplification. Trace the cost of a representative user action or job through the complete path: input cardinality → query/fetch → transformation → allocation/retention → compute/render/output. Ask how work and memory scale with records, groups, tenants, graph edges, concurrent users, update frequency, and retained history. Include algorithmic complexity where it helps explain the mechanism, but do not treat Big-O alone as a benchmark.

Ask what bounds memory, CPU, file descriptors, connections, queue length, retries, batch size, concurrency, response size, and retained state. A limit applied only after allocation or fan-out is too late to protect the allocation. Check N+1 work, unbounded caches, duplicate work, leaked listeners/tasks, and work continuing after cancellation. Check whether optimization merely moves pressure from the browser to the API, from the API to the database, or from request time to background jobs.

## Measurement and workload design

Prefer measured bottlenecks to speculative micro-optimization. Establish a baseline before changing the implementation. Use representative and adversarial-but-bounded fixtures that vary both data size and shape; include empty, sparse, dense, skewed, highly grouped, duplicate-heavy, and boundary-sized inputs where relevant. Exercise the actual interaction or workload, not only an isolated helper.

Record hardware, operating system, runtime and dependency versions, browser/device where applicable, dataset size and shape, concurrency, warmup, repetitions, cache state, measurement method, and observed result. Use distributions or percentiles for variable latency where useful, and include memory/CPU/frame-time or query counts when they explain the bottleneck. Compare before and after on the same workload and environment. Do not invent benchmark numbers, present an unrun test as evidence, or extrapolate a tiny fixture into production capacity.

## Operational attack

Check configuration validation, safe defaults, deployment ordering, rolling-version compatibility, readiness/liveness meaning, graceful shutdown, draining, rollback, backups, restore drills, resource requests/limits, secret delivery, and least-privilege identities as applicable. Infrastructure plans are review evidence, not authorization to apply them.

Inspect timeouts and retries as a coupled budget. Ensure backpressure and cancellation propagate to upstream work. Consider dependency outage, DNS failure, disk full, quota exhaustion, partial rollout, expired certificates/credentials, and lost telemetry. Review build/install hooks and CI permissions before running repository-supplied commands.

## Diagnosability and recovery

Could an operator distinguish rejection, retryable failure, partial commit, and permanent corruption? Are error codes and correlation identifiers sufficient without exposing secrets? Do metrics and logs show saturation, retry storms, dropped work, queue age, cache churn, slow queries, rendering stalls, and recovery failure? Are runbooks executable under the privileges operators actually have?

A recovery plan must address the durable state after failure, not only process restart. Do not mark a backup as useful without considering restoration compatibility and access.

## Evidence, implementation, and re-attack

For each proposed or applied optimization, record:

- The bounded workload and triggering condition.
- The repeated or amplified mechanism being changed.
- The metric, trace, query plan, profile, or source evidence that supports it.
- Baseline and post-change results, including environment and measurement limits.
- The invariant and user-visible semantics that must remain unchanged.
- The trade-offs introduced: memory, invalidation, complexity, consistency, accessibility, concurrency, or operational burden.

Test whether the repair moves pressure to another resource, changes semantics, creates stale results, weakens observability, or makes failure less recoverable. Re-attack cold and warm paths, small and large inputs, update and deletion paths, and relevant concurrency/cancellation cases.

In **review-only** mode, report substantiated opportunities and unresolved hypotheses without editing. In **review-and-fix** mode, implement the smallest evidence-backed optimizations within the authorized scope, add regression tests, measure again, and re-review the patch. Do not make changes solely to satisfy a checklist: if a pattern is not a demonstrated bottleneck or its trade-offs are unjustified, record that conclusion. Do not stress a live service, modify deployment policy, install telemetry, or increase cloud spend without authorization.
