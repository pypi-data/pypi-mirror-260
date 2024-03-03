def lastElement(l: list) -> any:
    if l is None or len(l) == 0:
        return None
    return l[-1]