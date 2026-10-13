"""Clamp an integer score into the inclusive range 0..100."""


def clamp_score(score):
    """Return score clamped to the documented inclusive range."""
    if score > 100:
        return 100
    return score
