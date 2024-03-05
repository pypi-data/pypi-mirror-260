def dict_deep_merge(dict1, dict2):
    """
    Merge two dictionaries deeply, prioritizing values from the second dictionary if keys are conflicting.

    Args:
    - dict1 (dict): First dictionary.
    - dict2 (dict): Second dictionary.

    Returns:
    - dict: Merged dictionary.
    """
    merged = dict1.copy()

    for key, value in dict2.items():
        if key in merged:
            if isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = dict_deep_merge(merged[key], value)
            else:
                merged[key] = value
        else:
            merged[key] = value

    return merged
