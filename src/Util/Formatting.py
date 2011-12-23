
def surrounded_by_parens(s):
    return (s[0] + s[-1]) in ['()','{}','[]']

def str2tuple(s, dType, hasParens = True):
    """Convert tuple-like strings to real tuples.
    eg '(1,2,3,4)' -> (1, 2, 3, 4)
    """
    if not surrounded_by_parens(s) and hasParens:
        raise ValueError("Badly formatted string (missing supposed brackets).")
    elif surrounded_by_parens(s) and not hasParens:
        raise ValueError("Badly formatted string (has brackets, said it did not).")
    if hasParens:
        items = s[1:-1].split(',')
    else:
        items = s.split(',')
    return tuple(dType(i.strip()) for i in items)