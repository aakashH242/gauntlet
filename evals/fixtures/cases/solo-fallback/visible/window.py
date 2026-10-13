"""Return at most `limit` values starting at the zero-based offset."""


def window(items, offset, limit):
    """Return a bounded window. Negative offset/limit values are invalid."""
    if offset < 0 or limit < 0:
        raise ValueError("offset and limit must be non-negative")

    end = min(offset + limit, len(items) - 1)
    return items[offset:end]
