"""
Functions set up to use the Pipe decorator; usually generators for space
"""

import itertools
from Wrappers import Pipe

@Pipe
def all_true(iterable, predicate):
    """builtin all for iterable"""
    return all(predicate(x) for x in iterable)

@Pipe
def any_true(iterable, predicate):
    """builtin any for iterable"""
    return any(predicate(x) for x in iterable)

@Pipe
def as_type(iterable, dtype):
    """Returns the generator (dtype(item) for item in iterable)"""
    return (dtype(item) for item in iterable)

@Pipe
def cast_as(iterable, dtype):
    """Returns dtype(iterable)"""
    return dtype(iterable)

@Pipe
def islice(iterable, start, stop, step):
    """itertools.islice"""
    return itertools.islice(iterable, start, stop, step)
@Pipe
def reverse(iterable):
    """builtin reverse generator of iterable"""
    return reversed(iterable)

@Pipe
def take(iterable, nitems):
    """Returns a generator of first nitems of iterable"""
    return itertools.islice(iterable, 0, nitems)

def take_every(iterable, step):
    """Returns a generator of iterable[::step]"""
    return itertools.islice(iterable, None, None, step)

@Pipe
def take_until(iterable, predicate):
    """Returns items until predicate(item) is true for an item in iterable"""
    for item in iterable:
        if not predicate(item):
            yield item
        else:
            return

@Pipe
def take_while(iterable, predicate):
    """Returns items while predicate(item) is true for item in iterable"""
    return itertools.takewhile(predicate, iterable)

@Pipe
def where(iterable, predicate):
    """Returns a generator on iterable of items where predicate(item)"""
    return (x for x in iterable if predicate(x))

@Pipe
def where_not(iterable, predicate):
    """Returns a generator on iterable of items where not predicate(item)"""
    return (x for x in iterable if not predicate(x))
