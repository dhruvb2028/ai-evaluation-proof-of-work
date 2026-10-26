def robust_mean(values, trim_fraction=0.1):
    # Intentionally flawed: mutates lists, ignores validation, and trims one item
    # from each side regardless of the requested fraction.
    if isinstance(values, list):
        values.sort()
        data = values
    else:
        data = sorted(values)
    if len(data) > 2:
        data = data[1:-1]
    return sum(data) / len(data)

