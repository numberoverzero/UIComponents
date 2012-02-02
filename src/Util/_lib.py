"""
General utility classes and functions
"""
__all__ = ['class_name', 'ensure_type', 'profile']

import cProfile
import pstats

def class_name(obj):
    """
    Returns the class name of an object.
    
    Includes namespaces; for example-
    in module a.py:
    class b(object):
        def __init__(self):
            class c(object):
                pass
            self.c = c()
    d = b().c
    class_name(d) == "a.b.c"
    """
    return ".".join(str(obj.__class__).split("'")[1].split(".")[1:])

def ensure_type(iterable, dtype):
    """Attempts to convert each item in iterable to type dtype."""
    return type(iterable)(dtype(item) for item in iterable)

def profile(str_to_execute, max_results= -1):
    """Runs a quick profile on the str_to_execute, and 
            outputs max_results of function details for calls and time."""
    
    cProfile.run(str_to_execute, 'profile')
    profile_ = pstats.Stats('profile')

    print "\nNCALLS"
    if max_results > 0:
        profile_.sort_stats('calls').print_stats(max_results)
    else:
        profile_.sort_stats('calls').print_stats()

    print "\nTIME"
    if max_results > 0:
        profile_.sort_stats('time').print_stats(max_results)
    else:
        profile_.sort_stats('time').print_stats()