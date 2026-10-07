# Gauntlet implementation demonstration

Controlled authored fixture: intentionally incomplete first implementation, followed by real sub-agent reviews and executed checks. Not a benchmark or production audit.

Target: csv.mjs and baseline.mjs; no production consumers. Authority: implement and repair this isolated demo. Repository release and ZIP remain unchanged.
Contract: request.md; prevalidated scalar matrix, literal plain-text interchange.
Tier: focused; pure local utility, no external system, persistence or security boundary.
Budget: 2 review rounds, 20 minutes; 1 clean re-attack after the repair round.
Selected: core and correctness-api. Excluded security/privacy: no I/O or untrusted parsing, formula policy explicitly out of scope. Reliability/frontend/operations omitted: no state, UI, infrastructure, or meaningful load requirement.
Required checks: baseline; directed regressions distinguishing original defects; fresh independent bounded round-trip attack; input immutability.
Available tools: Node and two real delegated reviewers, persistent Markdown ledger. No service, API key or dependency needed for fixture execution.

| Stage | State | Evidence |
| --- | --- | --- |
| Initial implementation | done; 3 baseline assertions passed | baseline.log |
| Round 1 core review | done | round-1-review.md |
| Round 1 correctness review | done | round-1-review.md |
| Repairs and regressions | verified | regressions-before.json: 2 fail; regressions-final.json: 9/9 pass |
| Round 2 fresh re-attack | clean | round-2-review.md, roundtrip.log |

Round 1 snapshot: csv.mjs SHA-256 4c4782a8978d4321ad560b2205acdeea4e29877fd243b1cd9008a9b9eb60ba80. Two reviewers launched independently: csv_contract_review (core/data preservation) and csv_encoding_review (correctness/encoding). Baseline tests are intentionally incomplete; a green baseline is not review closure.
Round 1 tasks completed: both sub-agents returned evidence; parent reproduced findings independently. F-01 and F-02 confirmed, medium in this isolated scope. Shared conversion and quoting path owns both invariants; no sibling encoder exists.
Regressions run against saved original before repair: expected failures recorded in regressions-before.json. Minimal repair: nullish fallback and CR quote trigger. Round 1 is not clean because it changed the target. Prior evidence invalidated for final closure.
Round 2 snapshot: csv.mjs SHA-256 99aaf5953069b99aa70215962abed6a3042da1ce6605d716bbc96692e12849b8; unchanged during both reviewer passes. Fresh attack strategies: mixed scalar literal outputs and independent parser round trips. Baseline 3 passed, regressions 9/9, 13 extra contract probes, 32,056 round trips, 12 parser checks, 3 explicit empty-cell checks. Parent inspected oracle and reran verifier.
F-01 and F-02 verified. Selected core/correctness tasks complete for final snapshot. No unresolved candidates, confirmed defects, unverified fixes or failed/blocked required check. No exceptions accepted.
Clean streak: 1, in separate round after repairs. Outcome: PASS_WITHIN_SCOPE. Budget: 2/2 used. Stop now; no ceremonial extra round. No external integration or deployment. Broader behavioral evaluation remains pending.
