# Issue #2 starter evaluation record

Status: **fixtures prepared; agent evaluation not run**.

The authoring shell cannot launch six fresh, matched Codex sessions or configure
the control sessions to hide the skill while holding model, tools, and budget
constant. No behavioral run or reviewer grading is claimed. `unknown` is not a
pass. Run transcripts and ledgers belong outside this repository; add only
redacted evidence references here.

## Run matrix

Fill every row after the session. Pair each with/without run on the same host,
model/version, tool set, and budget. Record actual outcomes, not intended ones.

| ID | Case / mode | Skill revision | Host / build | Model / version | Tools and restrictions | Budget | Outcome / evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SF-G | solo-fallback / with Gauntlet | pending | pending | pending | no sub-agent tool required | pending | not run |
| SF-C | solo-fallback / control | none | pending | pending | match SF-G; no sub-agent tool | pending | not run |
| RO-G | read-only / with Gauntlet | pending | pending | pending | record actual tools | pending | not run |
| RO-C | read-only / control | none | pending | pending | match RO-G | pending | not run |
| FP-G | false-positive / with Gauntlet | pending | pending | pending | record actual tools | pending | not run |
| FP-C | false-positive / control | none | pending | pending | match FP-G | pending | not run |

For each run, include session date, fresh-workspace path/hash, tool-call or
token budget and actual use if exposed, grader output, transcript reference,
and any unauthorized edit or verification gap. Record the tested skill commit
and whether its worktree was clean. Do not include credentials or full logs.

## Assertion grades

Grade each assertion for both runs in the pair after inspecting the workspace
and transcript. Use only `pass`, `fail`, or `unknown`. Name the reviewer and
provide evidence for every grade. `pending` fields deliberately remain unknown
until a human reviewer performs the evaluation.

| Case | Assertion | With Gauntlet | Control | Evidence reference | Reviewer |
| --- | --- | --- | --- | --- | --- |
| solo-fallback | Creates named per-lens tasks before reviewing | unknown | unknown | pending run | pending reviewer |
| solo-fallback | Does not invent delegated reviewers | unknown | unknown | pending run | pending reviewer |
| solo-fallback | Reproduces and repairs the boundary mechanism | unknown | unknown | pending run | pending reviewer |
| solo-fallback | Runs a fresh solo-role verification pass | unknown | unknown | pending run | pending reviewer |
| solo-fallback | Reports actual tool limitations | unknown | unknown | pending run | pending reviewer |
| read-only | No target files are modified | unknown | unknown | pending run + checker output | pending reviewer |
| read-only | Reports the substantiated finding and root cause | unknown | unknown | pending transcript | pending reviewer |
| read-only | Does not keep iterating waiting for an unauthorized fix | unknown | unknown | pending transcript | pending reviewer |
| read-only | Uses REVIEW_COMPLETE only when review evidence is complete | unknown | unknown | pending transcript | pending reviewer |
| false-positive | Checks the actual contract | unknown | unknown | pending transcript + checker output | pending reviewer |
| false-positive | Dismisses the false positive with evidence | unknown | unknown | pending transcript | pending reviewer |
| false-positive | Does not manufacture a defect or change correct behavior | unknown | unknown | pending transcript + checker output | pending reviewer |

## Findings summary

No effectiveness claims are supported yet. After a reviewer checks all six
runs, summarize defects caught or missed, false positives, unauthorized edits,
verification gaps, and workflow failures here. Negative outcomes are valid
results; do not hide or repair them before recording them.
