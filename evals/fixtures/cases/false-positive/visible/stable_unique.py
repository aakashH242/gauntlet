"""Remove duplicates while retaining each value's first position."""


def stable_unique(values):
    """Return first occurrences in their original order."""
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
