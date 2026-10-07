# Implementation, adversarial review, and repair demo

The [user task](request.md) is to finish a CSV exporter. The agent implements it, uses Gauntlet with two sub-agents to review the result, reproduces two defects, repairs their shared causes, and runs a fresh review on the final snapshot. See the [complete result](result.md) and [run ledger](ledger.md).

This is a controlled authored demonstration with a deliberately incomplete first draft. The sub-agent reviews, failing reproductions, repairs, and verification were actually executed. It is not a production audit or a behavioral benchmark.

## Reproduce the checks

Run from this directory with Node.js. The recorded run used Node v24.18.0; no dependencies are needed. Node is only required for this example, not for the Gauntlet skill.

```sh
node baseline.mjs
node regressions.mjs ./csv-before.mjs
node regressions.mjs
node verify-roundtrip.mjs
```

Expected results, in order: 3 baseline assertions pass; the saved original fails 2 of 9 regression checks and exits with status 1; the repaired implementation passes 9/9; the independent parser verifies 32,056 round trips, 12 parser-oracle checks, and 3 explicit empty-cell cases. The round-trip verifier binds itself to the recorded final source hash.

The [first review](round-1-review.md), [fresh review](round-2-review.md), [original regression output](regressions-before.json), [final regression output](regressions-final.json), and [round-trip output](roundtrip.log) preserve the recorded evidence. Unsupported input types, spreadsheet formula evaluation, external CSV consumers, UI integration, and deployment are outside scope.

## Listing visuals

The [cover](../../assets/demo/cover.png), [workflow screenshot](../../assets/demo/workflow.jpg), and [result screenshot](../../assets/demo/result.jpg) are the current listing images. Editable HTML sources for the two screenshots and the cover generation prompt are saved alongside them in `assets/demo/`.
