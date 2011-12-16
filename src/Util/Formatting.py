
def str2tuple(s, dType, hasParens = True):
    """Convert tuple-like strings to real tuples.
    eg '(1,2,3,4)' -> (1, 2, 3, 4)
    """
    if (s[0] + s[-1] != "()") and hasParens:
        print "Error in str2tuple: "+str(s)
        raise ValueError("Badly formatted string (missing brackets).")
    if hasParens:
        items = s[1:-1].split(',')
    else:
        items = s.split(',')
    return tuple(dType(i.strip()) for i in items)