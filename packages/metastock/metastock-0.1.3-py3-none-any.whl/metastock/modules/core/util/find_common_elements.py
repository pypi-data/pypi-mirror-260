def find_common_elements(*lists) -> list:
    if len(lists) == 0:
        return []

    common_set = set(lists[0])

    for list_ in lists[1:]:
        common_set &= set(list_)

    return list(common_set)
