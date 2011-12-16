__all__ = ['Math','Formatting','Structs','Wrappers']

import Math
import Formatting
import Structs
import Wrappers

import cProfile
import pstats

def contains(_list, item):
    return _list.count(item) > 0

def ensureType(iterable, dtype):
    return [dtype(i) for i in iterable]

def profile(strToExecute, maxResults = -1):
    
    cProfile.run(strToExecute, 'profile')
    p = pstats.Stats('profile')

    print "\nNCALLS"
    if maxResults > 0:
        p.sort_stats('calls').print_stats(maxResults)
    else:
        p.sort_stats('calls').print_stats()

    print "\nTIME"
    if maxResults > 0:
        p.sort_stats('time').print_stats(maxResults)
    else:
        p.sort_stats('time').print_stats()