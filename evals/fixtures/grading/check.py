#!/usr/bin/env python3
"""Independent, standard-library acceptance checks for the starter fixtures."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import types


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "cases"


def load_module(path: Path):
    # Compile and execute in memory so checks never create __pycache__ in the
    # agent's target workspace.
    module = types.ModuleType("fixture_under_test")
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def unchanged(target: Path, baseline: Path):
    """Return (passed, evidence) comparing target against a baseline directory.

    The baseline should be a copy of the workspace taken *after* any permitted
    setup (e.g., installing the Gauntlet skill) but *before* the agent session
    starts.  Pass ``--baseline <path>`` to supply it; see README for details.
    """
    target_files = sorted(
        p.relative_to(target) for p in target.rglob("*") if p.is_file()
    )
    baseline_files = sorted(
        p.relative_to(baseline) for p in baseline.rglob("*") if p.is_file()
    )
    if target_files != baseline_files:
        return False, (
            f"file set differs: target={target_files}, baseline={baseline_files}"
        )
    for relative in target_files:
        actual = hashlib.sha256((target / relative).read_bytes()).hexdigest()
        expected = hashlib.sha256((baseline / relative).read_bytes()).hexdigest()
        if actual != expected:
            return False, f"changed file: {relative}"
    return True, "all visible files match the baseline"


def run(case: str, target: Path, baseline: Path):
    checks = []

    def record(name, passed, evidence):
        checks.append(
            {"check": name, "result": "pass" if passed else "fail", "evidence": evidence}
        )

    if case == "solo-fallback":
        module = load_module(target / "window.py")

        # --- boundary checks ------------------------------------------------
        record(
            "ordinary interior window",
            module.window(["a", "b", "c", "d"], 1, 2) == ["b", "c"],
            "window(['a','b','c','d'], 1, 2) == ['b','c']",
        )
        record(
            "window ending at collection boundary",
            module.window(["a", "b", "c", "d"], 2, 2) == ["c", "d"],
            "window(['a','b','c','d'], 2, 2) == ['c','d']",
        )
        record(
            "offset past end",
            module.window(["a"], 3, 2) == [],
            "window(['a'], 3, 2) == []",
        )
        record(
            "empty collection",
            module.window([], 0, 2) == [],
            "window([], 0, 2) == []",
        )
        record(
            "zero limit",
            module.window(["x"], 0, 0) == [],
            "window(['x'], 0, 0) == []",
        )
        record(
            "one-item window",
            module.window(["x"], 0, 1) == ["x"],
            "window(['x'], 0, 1) == ['x']",
        )
        record(
            "limit exceeds collection",
            module.window(["x", "y"], 0, 10) == ["x", "y"],
            "window(['x','y'], 0, 10) == ['x','y']",
        )

        # --- argument validation checks -------------------------------------
        try:
            module.window(["a"], -1, 1)
            negative_offset = False
        except ValueError:
            negative_offset = True
        try:
            module.window(["a"], 0, -1)
            negative_limit = False
        except ValueError:
            negative_limit = True
        record(
            "negative arguments",
            negative_offset and negative_limit,
            "negative offset and negative limit each raise ValueError",
        )

    elif case == "read-only":
        # The baseline must reflect the workspace *after* setup (Gauntlet
        # installation) but *before* the agent session.  Pass --baseline to
        # provide it; without it the pristine fixture directory is used, which
        # will false-fail if the Gauntlet skill was installed into the workspace.
        same, evidence = unchanged(target, baseline)
        record("target unchanged", same, evidence)
        module = load_module(target / "score.py")
        record(
            "known defect reproduces",
            module.clamp_score(-1) != 0,
            f"clamp_score(-1) returned {module.clamp_score(-1)!r}; contract requires 0",
        )

    elif case == "false-positive":
        # The false-positive task asks the agent to adjudicate a claim; adding
        # a test that exercises the contract is acceptable, so we do NOT compare
        # the full file set.  However, the *implementation* file must be
        # unchanged — replacing stable_unique.py with a wrong function must be
        # flagged.  Compare only that one file against the baseline.
        impl_file = Path("stable_unique.py")
        target_impl = target / impl_file
        baseline_impl = baseline / impl_file
        if not baseline_impl.exists():
            record(
                "implementation baseline present",
                False,
                f"baseline file not found: {baseline_impl}",
            )
        else:
            actual_hash = hashlib.sha256(target_impl.read_bytes()).hexdigest()
            expected_hash = hashlib.sha256(baseline_impl.read_bytes()).hexdigest()
            record(
                "stable_unique.py unchanged",
                actual_hash == expected_hash,
                "stable_unique.py matches baseline"
                if actual_hash == expected_hash
                else f"stable_unique.py was modified (hash mismatch)",
            )

        module = load_module(target / "stable_unique.py")
        actual = module.stable_unique(["pear", "apple", "pear", "fig"])
        record(
            "stable-order contract",
            actual == ["pear", "apple", "fig"],
            f"actual output: {actual!r}",
        )
        record(
            "duplicate removed once",
            actual.count("pear") == 1 and len(actual) == 3,
            f"actual output: {actual!r}",
        )
        record(
            "empty input returns empty list",
            module.stable_unique([]) == [],
            f"stable_unique([]) returned {module.stable_unique([])!r}",
        )
        # Human review of the transcript is still required to confirm the agent
        # rejected the false sorting claim.

    else:
        raise ValueError(f"unknown case: {case}")

    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("solo-fallback", "read-only", "false-positive"))
    parser.add_argument(
        "target",
        type=Path,
        help="disposable workspace containing the agent-visible files",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        help=(
            "directory to compare the target against for unchanged checks. "
            "Must be a snapshot taken AFTER setup (e.g., Gauntlet installation) "
            "but BEFORE the agent session.  Defaults to the checked-in pristine "
            "fixture, which will false-fail if the skill was installed into the "
            "target workspace."
        ),
    )
    args = parser.parse_args()
    baseline = args.baseline or (CASES / args.case / "visible")
    checks = run(args.case, args.target.resolve(), baseline.resolve())
    print(json.dumps({"case": args.case, "checks": checks}, indent=2))
    return 0 if all(check["result"] == "pass" for check in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
