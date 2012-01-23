"""
Utility functions and classes

This level contains general functions that are useful 
for program-level analysis and methods (such as contains)
that are useful for general coding
"""

import cProfile
import pstats

import IO
import Math
import Formatting
import Structs
import Wrappers

#__all__ = ['Math', 'Formatting', 'Structs', 'Wrappers']

def class_name(obj):
    """Returns the class name of an object."""
    return ".".join(str(obj.__class__).split("'")[1].split(".")[1:])

def ensure_type(iterable, dtype):
    """Attempts to convert each item in iterable to type dtype."""
    return [dtype(item) for item in iterable]

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
        