print "Util Imported"

import cProfile
import pstats

import Wrappers
import Math
import Formatting
import Structs

__all__ = ['Math','Formatting','Structs','Wrappers']


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
        
if  __name__ == "__main__":
    #10,000,000
    n = 10000000
    
    def run(fn):
        for i in xrange(n):
            fn(1.0, 1.0, 1.0, 1.0, 1.5)
    
    print "NEW RUN"
    
    #profile("run(Math.rotate)", 20)
    
    print "OLD RUN"
        
    #profile("run(Math.old_rotate)", 20)

    print "INT RUN"
    
    #profile("run(Math.int_rotate)", 20)
    
    print "C++ Table Run"
    
    #profile("run(Math.rotateTable)", 20)
    