"""
common queries related to primes.
mostly imported from project euler problems
"""

MAX_NUMBER = 1000000
PRIMES = []

def generate_primes(n): #pylint:disable-msg=C0103
    """
    Populates PRIMES with the primes on [2, n]
    
    Method taken from someone on Project Euler forums,
    I think on #35.  Need to check that and add attribution.
    """
    global PRIMES #pylint:disable-msg=W0603
    
    if n == 2: 
        PRIMES = [2]
    elif n < 2: 
        PRIMES = []
    s = range(3, n + 1, 2) #pylint:disable-msg=C0103
    mroot = n ** 0.5
    half = (n + 1) / 2 - 1
    i = 0 #pylint:disable-msg=C0103
    m = 3 #pylint:disable-msg=C0103
    while m <= mroot:
        if s[i]:
            j = (m * m - 3) / 2 #pylint:disable-msg=C0103
            s[j] = 0 #pylint:disable-msg=C0103
            while j < half:
                s[j] = 0
                j += m #pylint:disable-msg=C0103
        i += 1 #pylint:disable-msg=C0103
        m = 2 * i + 3 #pylint:disable-msg=C0103
    PRIMES = [2]+[x for x in s if x]

def is_prime(number, adjust_table=False, growth_margin=10):
    """
    Used to check if a number is prime.
    
    When checking large values, or values > primes.MAX_NUMBER,
    there are two solutions:
        - do a one-off check for this value using a custom algorithm
        - expand the table of primes to include the number,
                plus growth_margin% further values.
    
    Use the first option when you wont be checking many values that
        are outside the range of the table.
    
    Use the second if you'll be checking many values that are larger
        than the table- at that point, the amortized cost of
        expanding and then doing lookups is small.
    
    growth_margin is a percentage of the offset (number-MAX_NUMBER)
        to expand the table by; for example:
        number = 1 000 000
        MAX_NUMBER = 8 000 000
        growth_margin = 25
        offset = growth_margin / 100 * (number - MAX_NUMBER)
        offset = 50 000
        new max number = 1 050 000
    
    When expanding the table, it will always expand to 
        include the queried value.  offset simply adjusts how much
        _further_ to calculate as a sort of safety against needing
        to recalculate again.
    """
    if not adjust_table:
        if number <= MAX_NUMBER:
            return number in PRIMES
        else:
            return is_prime_dirty(number)
    
    #Adjust the table, return the result
    offset = int((number - MAX_NUMBER) * growth_margin * 0.01)
    try:
        generate_primes(number + offset)
        return number in PRIMES
    except MemoryError:
        return is_prime_dirty(number)
    
def is_prime_dirty(number):
    """Quick test if a single number is prime."""
    if number == 2:
        return True
    mid = int(number ** 0.5) + 1
    factor = 2
    while factor <= mid:
        if number % factor:
            factor += 1
        else:
            #No remainder, it's a factor
            return False
    return True

generate_primes(MAX_NUMBER)
