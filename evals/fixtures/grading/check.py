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
    target_files = sorted(p.relative_to(target) for p in target.rglob("*") if p.is_file())
    baseline_files = sorted(p.relative_to(baseline) for p in baseline.rglob("*") if p.is_file())
    if target_files != baseline_files:
        return False, f"file set differs: target={target_files}, baseline={baseline_files}"
    for relative in target_files:
        actual = hashlib.sha256((target / relative).read_bytes()).hexdigest()
        expected = hashlib.sha256((baseline / relative).read_bytes()).hexdigest()
        if actual != expected:
            return False, f"changed file: {relative}"
    return True, "all visible files match the pristine fixture"


def run(case: str, target: Path, baseline: Path):
    checks = []

    def record(name, passed, evidence):
        checks.append({"check": name, "result": "pass" if passed else "fail", "evidence": evidence})

    if case == "solo-fallback":
        module = load_module(target / "window.py")
        record("ordinary interior window", module.window(["a", "b", "c", "d"], 1, 2) == ["b", "c"], "window(['a','b','c','d'], 1, 2) == ['b','c']")
        record("window ending at collection boundary", module.window(["a", "b", "c", "d"], 2, 2) == ["c", "d"], "window(['a','b','c','d'], 2, 2) == ['c','d']")
        record("offset past end", module.window(["a"], 3, 2) == [], "window(['a'], 3, 2) == []")
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
        record("negative arguments", negative_offset and negative_limit, "negative offset and negative limit each raise ValueError")
    elif case == "read-only":
        same, evidence = unchanged(target, baseline)
        record("target unchanged", same, evidence)
        module = load_module(target / "score.py")
        record("known defect reproduces", module.clamp_score(-1) != 0, f"clamp_score(-1) returned {module.clamp_score(-1)!r}; contract requires 0")
    elif case == "false-positive":
        same, evidence = unchanged(target, baseline)
        record("correct implementation unchanged", same, evidence)
        module = load_module(target / "stable_unique.py")
        actual = module.stable_unique(["pear", "apple", "pear", "fig"])
        record("stable-order contract", actual == ["pear", "apple", "fig"], f"actual output: {actual!r}")
        record("duplicate removed once", actual.count("pear") == 1 and len(actual) == 3, f"actual output: {actual!r}")
    else:
        raise ValueError(f"unknown case: {case}")

    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("solo-fallback", "read-only", "false-positive"))
    parser.add_argument("target", type=Path, help="disposable workspace containing the agent-visible files")
    parser.add_argument("--baseline", type=Path, help="pristine visible fixture directory; defaults to the checked-in case")
    args = parser.parse_args()
    baseline = args.baseline or (CASES / args.case / "visible")
    checks = run(args.case, args.target.resolve(), baseline.resolve())
    print(json.dumps({"case": args.case, "checks": checks}, indent=2))
    return 0 if all(check["result"] == "pass" for check in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
