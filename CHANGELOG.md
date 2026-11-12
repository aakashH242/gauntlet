# Changelog

## 1.2.0

### Added

- Generalized cross-boundary resource-lifecycle review. Agents now map the creator/owner, backing resource, every writer or external invalidator, active consumers, cleanup/cancellation ordering, and recreation/rebinding paths.
- Frontend guidance for parent/host-driven DOM replacement, route/layout transitions, loading and error fallbacks, retries, unmount, and callbacks that may outlive the replaced container.
- Performance/operations guidance requiring all external invalidation paths to be traced for retained references, caches, handles, observers, subscriptions, tasks, connections, and other resources.
- Root-cause guidance explaining that the missing invariant can be a lifecycle handoff between separate owners, not merely cleanup inside the component that cached the resource.
- Triage routing for cross-component lifecycle risks.
- An evaluation specification, `external-resource-invalidation`, for testing whether agents detect external replacement while work is pending and verify cleanup plus rebinding.

### Changed

- Bumped the Agent Skill metadata version from 1.1.0 to 1.2.0.

### Evaluation status

The new case is a behavioral evaluation specification only. It has not been run against models or hosts as part of this release. No model-quality improvement is claimed without measured trials.
