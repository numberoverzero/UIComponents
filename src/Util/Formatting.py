"""
Common formatting functions and structures.
"""


def surrounded_by_parens(string):
    """Determines if the string is surrounded in 
            (matching) parens of any sort"""
    return (string[0] + string[-1]) in ['()', '{}', '[]']

def str_to_tuple(string, dtype, has_parens = True):
    """Convert tuple-like strings to real tuples.
    eg '(1,2,3,4)' -> (1, 2, 3, 4)
    """
    if not surrounded_by_parens(string) and has_parens:
        raise ValueError("Badly formatted string (missing supposed brackets).")
    elif surrounded_by_parens(string) and not has_parens:
        msg = "Badly formatted string (has brackets, said it did not)."
        raise ValueError(msg)
    if has_parens:
        items = string[1:-1].split(',')
    else:
        items = string.split(',')
    return tuple(dtype(item.strip()) for item in items)