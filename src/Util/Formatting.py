"""
Common formatting functions and structures.
"""

def paren_type_func(string):
    """Checks the left and right ends of a string to determine parens type.
        Returns tuple if (), list if [], and 
            an identity fuction for all others"""
    type_func = lambda item: item
    
    ptype = string[0]+string[-1]
    if ptype == "()":
        type_func = tuple
    elif ptype == "[]":
        type_func = list
    
    return type_func

def surrounded_by_parens(string):
    """Determines if the string is surrounded in 
            (matching) parens of any sort"""
    return (string[0] + string[-1]) in ['()', '{}', '[]']

def str_to_struct(string, dtype, has_parens=True):
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
        struct = paren_type_func(string)
    else:
        items = string.split(',')
        struct = tuple
    
    return struct(dtype(item.strip()) for item in items)

def struct_to_str(struct):
    """Converts a struct of strings to a string that can be properly
        parsed back using str_to_struct.  This function is necessary because
        list -> str will make "['hello','bob']" which when converted
        back gives ["'hello'","'bob'"] which preserves the unnecessary
        inner single quotes.  This function would instead return
        "[hello,bob]" which when str_to_struct'd, gives ["hello","bob"]"""
    if type(struct) is list:
        parens = "[]"
    else:
        parens = "()"
    inner = ",".join(struct)
    
    return parens[0]+inner+parens[1]