def clamp(value: float, minimum: float, maximum: float) -> float:
    """Return value constrained to the inclusive range."""
    if minimum > maximum:
        raise ValueError("minimum must not exceed maximum")
    return min(maximum, max(minimum, value))
