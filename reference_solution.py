import math
from numbers import Real


def robust_mean(values, trim_fraction=0.1):
    if isinstance(trim_fraction, bool) or not isinstance(trim_fraction, Real):
        raise TypeError("trim_fraction must be a real number")
    if not math.isfinite(float(trim_fraction)):
        raise ValueError("trim_fraction must be finite")
    if not 0 <= float(trim_fraction) < 0.5:
        raise ValueError("trim_fraction must satisfy 0 <= trim_fraction < 0.5")

    try:
        data = list(values)
    except TypeError as exc:
        raise TypeError("values must be iterable") from exc

    if not data:
        raise ValueError("values must not be empty")

    cleaned = []
    for value in data:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("every value must be a real number")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("every value must be finite")
        cleaned.append(number)

    cleaned.sort()
    trim_count = math.floor(len(cleaned) * float(trim_fraction))
    kept = cleaned[trim_count : len(cleaned) - trim_count if trim_count else None]
    if not kept:
        raise ValueError("trimming removed every value")
    return float(sum(kept) / len(kept))

