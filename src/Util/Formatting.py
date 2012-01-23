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
    inner = ",".join((str(s) for s in struct))
    
    return parens[0]+inner+parens[1]

def surrounded_by_parens(string):
    """Determines if the string is surrounded in 
            (matching) parens of any sort"""
    return (string[0] + string[-1]) in ['()', '{}', '[]']

class StringBuilder(object):
    """
    Helper class for building strings out of small pieces.
    
    Periodically compacts itself down to reduce footprint.
    To prevent this behavior (no idea why) use size <= 0
    Otherwise, compacts when number of pieces > size.
    To force a compact, use build()
    
    To get the current string, call the StringBuilder object.
    ie. myStringBuilder()
    """
    __slots__ = ['_size', '_msize', '_data']
    
    def __init__(self, string=None, size = -1):
        if string:
            self._data = [string]
        else:
            self._data = []
        self._msize = size
        self._size = len(self._data)
        
    def __add__(self, other):
        """x.__add__(y) <==> x+y"""
        return self.__call__().__add__(other)
    
    def __call__(self):
        """Return the built string"""
        if self._size > 1:
            self.build()
            return self._data[0]
        elif self._size == 1:
            return self._data[0]
        else:
            return ""
        
    def __contains__(self, other):
        """x.__contains__(y) <==> y in x"""
        return self.__call__().__contains__(other)
    
    def __eq__(self, other):
        """x.__eq__(y) <==> x==y"""
        return self.__call__().__contains__(other)
    
    def __ge__(self, other):
        """x.__ge__(y) <==> x>=y"""
        return self.__call__().__ge__(other)
    
    def __getitem__(self, key):
        return self.__call__()[key]
    
    def __gt__(self, other):
        """x.__gt__(y) <==> x>y"""
        return self.__call__().__gt__(other)
    
    def __iadd__(self, other):
        """x.__iadd__(y) <==> x+=y"""
        self._data.append(other)
        self._size += 1
        self._check_build()
        return self
    
    def __imul__(self, other):
        """x.__imul__(y) <==> x*=y"""
        self._data *= other
        self._size = len(self._data)
        self._check_build()
        return self
    
    def __le__(self, other):
        """x.__le__(y) <==> x<=y"""
        return self.__call__().__le__(other)
    
    def __len__(self):
        """x.__len__() <==> len(x)"""
        return self.__call__().__len__()
    
    def __lt__(self, other):
        """x.__lt__(y) <==> x<y"""
        return self.__call__().__lt__(other)
    
    def __mul__(self, other):
        """x.__mul__(n) <==> x*n"""
        return self.__call__().__mul__(other)
    
    def __ne__(self, other):
        """x.__ne__(y) <==> x!=y"""
        return self.__call__().__ne__(other)
    
    def __repr__(self, *args, **kwargs):
        return repr(self.__call__())
    
    def __radd__(self, other):
        return other + self.__call__()
    
    def __rmul__(self, other):
        """x.__rmul__(n) <==> n*x"""
        return other * self.__call__()
    
    def __str__(self):
        """x.__str__() <==> str(x)"""
        return self.__call__()
    
    def _check_build(self):
        """Check if the string needs to be compacted, and if so, build."""
        if self._msize > 0 and self._size >= self._msize:
            self.build()
    
    def build(self):
        """Compact the string down in memory."""
        _str = ''.join(self._data)
        self._data = [_str]
        self._size = 1
    