# Starter behavioral fixtures

These three cases provide reproducible inputs for the first behavioral
evaluation. The tested agent must only receive a disposable copy of one
`cases/<case>/visible/` directory. Keep `grading/`, `results.md`, and all
transcripts outside that workspace. Fixtures use fake in-memory data and Python
standard library only; they need no package installation or network access.

## Session setup

Use a fresh session for every run. Keep one fixed host/build and model/version
across all six runs. Start with a clean, separate target copy for each run;
never reuse a workspace modified by an earlier run. Record exact versions, date,
tool access, and the actual budget in `results.md`.

Before starting, choose a per-run cap (for example, 8 assistant turns and 30
tool calls) and apply the same cap to both members of each pair. Record the cap
and actual usage; if the host exposes a token budget, match and record that too.

### Step 1 — Create the target workspace

In PowerShell, from the repository root:

```powershell
$Case = 'solo-fallback'  # or read-only, false-positive
$Run  = 'solo-fallback-with-gauntlet'  # unique name for each run
$Target = Join-Path $env:TEMP "gauntlet-issue-2\$Run"
Remove-Item -LiteralPath $Target -Recurse -Force -ErrorAction SilentlyContinue
New-Item    -ItemType Directory -Path $Target -Force | Out-Null
Copy-Item   -Path "evals/fixtures/cases/$Case/visible/*" -Destination $Target -Recurse
```

### Step 2 — Hiding and exposing the Gauntlet skill

**with-Gauntlet run** — install the skill into the target workspace and record
the commit:

```powershell
$Skill = Join-Path $Target '.agents/skills/gauntlet'
New-Item  -ItemType Directory -Path $Skill -Force | Out-Null
Copy-Item SKILL.md, references, templates, scripts, agents -Destination $Skill -Recurse
git rev-parse HEAD   # record this; also note whether the worktree was clean
```

**control run** — start from a second clean copy (`$Run` set to e.g.
`solo-fallback-control`) and do **not** install any Gauntlet files.  In
addition:

- If the host loads skills from a global or user-level directory, verify that
  no Gauntlet skill, protocol description, template, or tracker is reachable
  from the session.  Configuration paths differ by host; check and record the
  actual paths that were inspected.
- Do not include this evaluation guide, `results.md`, or any Gauntlet
  documentation in the session context.

### Step 3 — Save the baseline snapshot

After setup but **before** starting the agent session, snapshot the workspace
so the checker can compare the final state against a fair baseline that already
includes any permitted setup files (e.g., the installed skill):

```powershell
$Baseline = Join-Path $env:TEMP "gauntlet-issue-2\$Run-baseline"
Copy-Item -Path $Target -Destination $Baseline -Recurse
```

Pass this path to the checker via `--baseline` (see [Running the checker](#running-the-checker)).

### Step 4 — Removing delegation tools (solo-fallback only)

`solo-fallback` requires that **no sub-agent/delegation tool** be available in
either the with-Gauntlet or the control run.  This must be a host-level
enforcement, not merely an instruction to the agent:

- Identify every tool your host exposes that can spawn or delegate to a
  sub-agent (names vary: `invoke_subagent`, `create_agent`, `delegate`, etc.).
- Disable or remove those tools at the host configuration level before starting
  the session.
- Record the actual tool list the session received; do not just record your
  intent.

The other cases (read-only and false-positive) should have matching tool sets
within each pair.  Do not let any run access secrets, production services, or
the network.

### Step 5 — Start the session

Start a new conversation for each run.  Give the agent the exact task text
from `TASK.md`.  Do not expose grading files, grading notes, or expected
results to the tested agent.

## Running the checker

After a run, inspect the final workspace yourself and run the checker from the
repository root (outside the target):

```powershell
# Without a baseline (uses the pristine checked-in fixture; will false-fail if
# the Gauntlet skill was installed into the workspace):
python evals/fixtures/grading/check.py solo-fallback $Target

# With a baseline (recommended whenever setup adds files to the workspace):
python evals/fixtures/grading/check.py read-only $Target --baseline $Baseline
python evals/fixtures/grading/check.py false-positive $Target --baseline $Baseline
```

Replace the case name and paths as needed.  Exit status 0 means the listed
artifact checks passed; it does not grade the agent's explanation or prove that
it followed the review process.  Use the assertion checklist in `results.md`
to grade each behavior against the transcript and workspace.  A reviewer other
than the tested agent should inspect findings and grades.  Keep full transcripts,
ledgers, and logs outside the skill/repository; record redacted evidence paths
or links only.

## Fixture and grading boundary

The agent-visible starting files and prompts are under `cases/<case>/visible/`.
The checker in `grading/check.py` holds independent behavioral checks.  Run it
against the actual final target directory using a post-setup baseline.  Do not
copy the `grading/` directory into the target.

- **solo-fallback** grading also requires human inspection of the claimed
  repair, regression checks against the new boundary tests, and a fresh
  solo re-review.  The script checks only observable function behavior; see
  `grading/notes/solo-fallback.md` for the expected defect and boundary cases.
- **read-only** grading must inspect both the transcript and the file
  comparison using a baseline that includes any setup files.
- **false-positive** grading must inspect whether the agent explicitly tested
  the contract and dismissed the unsupported sorting claim.  Adding a valid
  test to exercise the contract is acceptable; only the implementation behavior
  must be preserved.

## Current status

`results.md` is the run record. The six model/host sessions have not been run in
this authoring environment: it does not provide controls to create six fresh,
matched sessions with and without a hidden project skill, nor an independent
human reviewer. Therefore all behavior grades remain `unknown`. The fixture
checker is reproducible locally, but its passing artifact checks are not agent
evaluation results.
