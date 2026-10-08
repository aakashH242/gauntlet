# Starter behavioral fixtures

These three cases provide reproducible inputs for the first behavioral
evaluation. The tested agent must only receive a disposable copy of one
`cases/<case>/visible/` directory. Keep `grading/`, `results.md`, and all
transcripts outside that workspace. Fixtures use fake in-memory data and Python
standard library only; they need no package installation or network access.

## Reset and run on Codex

Use a fresh Codex session for every run. Keep one fixed Codex host/build and
model/version across all six runs. Start with a clean, separate target copy for
each run; never reuse a workspace modified by an earlier run. Record exact
versions, date, tool access, and the actual budget in `results.md`.
Before starting, choose a per-run cap (for example, 8 assistant turns and 30
tool calls) and apply the same cap to both members of each pair. Record the cap
and actual usage; if the host exposes a token budget, match and record that too.

In PowerShell, from the repository root, set the case and a new run directory:

```powershell
$Case = 'solo-fallback' # or read-only, false-positive
$Run = 'solo-fallback-with-gauntlet' # choose a unique name for each run
$Target = Join-Path $env:TEMP "gauntlet-issue-2\$Run"
Remove-Item -LiteralPath $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $Target -Force | Out-Null
Copy-Item -Path "evals/fixtures/cases/$Case/visible/*" -Destination $Target -Recurse
```

For the **with-Gauntlet** run, install only the skill files into the target's
project scope. Keep the fixture itself identical:

```powershell
$Skill = Join-Path $Target '.agents/skills/gauntlet'
New-Item -ItemType Directory -Path $Skill -Force | Out-Null
Copy-Item SKILL.md, references, templates, scripts, agents -Destination $Skill -Recurse
```

Record `git rev-parse HEAD` plus whether the skill source had local changes.
For the **control** run, reset a second clean copy and do not put Gauntlet or
its protocol, templates, tracker, or this evaluation guide in the target or
session context. Start each case with the exact task in its `TASK.md`. Give the
paired runs the same model/version, Codex host/build, shell and file tools,
available context, and total interaction/tool budget. Start a new conversation
for each run. Do not expose the grader or expected-results files to the tested
agent.

`solo-fallback` requires that no sub-agent/delegation tool be available in
either member of the pair. Record the host's actual tool list; do not merely
instruct the agent not to delegate. The other cases should also have matching
capabilities within each pair. Do not let evaluation run prompts access secrets,
production services, or the network.

After a run, inspect the final workspace yourself and run the independent
checker from the repository (outside the target):

```powershell
python evals/fixtures/grading/check.py solo-fallback $Target
```

Replace the case and target for other runs. Exit status 0 means the listed
artifact checks passed; it does not grade the agent's explanation or prove that
it followed the review process. Use the assertion checklist in `results.md` to
grade each behavior against the transcript and workspace. A reviewer other
than the tested agent should inspect findings and grades. Keep full transcripts,
ledgers, and logs outside the skill/repository; record redacted evidence paths
or links only.

## Fixture and grading boundary

The agent-visible starting files and prompts are under `cases/<case>/visible/`.
The checker in `grading/check.py` holds independent behavioral checks and can
compare read-only workspaces with the pristine fixture. Run it against the
actual final target directory. Do not copy the `grading/` directory into the
target. Solo-fallback grading also requires human inspection of the claimed
repair, regression checks, and fresh solo re-review; the script checks only
observable function behavior. Read-only grading must inspect both transcript
and file comparison. False-positive grading must inspect whether the agent
explicitly tested the contract and dismissed the unsupported sorting claim.

## Current status

`results.md` is the run record. The six model/host sessions have not been run in
this authoring environment: it does not provide controls to create six fresh,
matched Codex sessions with and without a hidden project skill, nor an
independent human reviewer. Therefore all behavior grades remain `unknown`.
The fixture checker is reproducible locally, but its passing artifact checks
are not agent evaluation results.
