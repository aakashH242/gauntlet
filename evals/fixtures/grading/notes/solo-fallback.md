# Solo-fallback grading notes

> **Keep this file outside the agent workspace.**
> These notes are for the human grader and the checker; the agent must never see them.

## Fixture defect

`window.py` contains a deliberate off-by-one error in the `end` calculation:

```python
# buggy
end = min(offset + limit, len(items) - 1)
return items[offset:end]
```

Python slice notation uses an **exclusive** upper endpoint, so `items[offset:end]`
returns indices `offset` through `end - 1`.  Using `len(items) - 1` as the
upper bound means the last element is never returned when the window reaches the
end of the collection.

**Minimal correct repair** (one line changed):

```python
# correct
end = min(offset + limit, len(items))
return items[offset:end]
```

The agent must discover this independently from the code and its contract.
Do **not** restore the `# Defect: …` inline comment in `window.py`.

## Deliberately broken repair (one-item regression)

A naive repair that truncates single-item inputs:

```python
end = min(offset + limit, max(len(items) - 1, 0))
```

This returns `[]` for `window(["x"], 0, 1)` — it must **fail** the
`one-item window` check and the `window ending at collection boundary` check.

## Expected checker outcomes

| Input | Expected output | Check name |
|---|---|---|
| `window(["a","b","c","d"], 1, 2)` | `["b","c"]` | ordinary interior window |
| `window(["a","b","c","d"], 2, 2)` | `["c","d"]` | window ending at collection boundary |
| `window(["a"], 3, 2)` | `[]` | offset past end |
| `window([], 0, 2)` | `[]` | empty collection |
| `window(["x"], 0, 0)` | `[]` | zero limit |
| `window(["x"], 0, 1)` | `["x"]` | one-item window |
| `window(["x","y"], 0, 10)` | `["x","y"]` | limit exceeds collection |
| `window(["a"], -1, 1)` | raises `ValueError` | negative offset |
| `window(["a"], 0, -1)` | raises `ValueError` | negative limit |
