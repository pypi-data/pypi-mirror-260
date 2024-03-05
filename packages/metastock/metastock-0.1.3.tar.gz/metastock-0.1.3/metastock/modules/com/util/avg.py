def avg(*args):
    if not args:
        return 0
    return sum(args) / len(args)
