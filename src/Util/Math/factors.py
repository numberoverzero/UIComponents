"""
Common factoring operations on numbers,
mostly imported from project euler problems.
"""

from collections import defaultdict

def factors_dict(number):
    """
    Returns a dictionary of (factor: count) pairs,
    
    such that prod(factor**count) for factor in factors = number
    """
    factors = defaultdict(int)
    for factor in gen_factors(number):
        factors[factor] += 1
    return factors

def gen_factors(number):
    """Generator that returns the prime factors of number"""
    factor = 2
    while abs(number) > 1:
        if number % factor == 0:
            number /= factor
            yield factor
        else:
            factor += 1

def is_any_factor(number, factors):
    """Check if any of the factors evenly divide number"""
    return any(is_factor(number, f) for f in factors)

def is_factor(number, factor):
    """Check if factor evenly divides number"""
    return not number % factor

