"""
generators and inspection functions for significant sequences
"""

def fib(index):
    """
    The n-th fibonnaci number, 0-indexed
    
    0-indexed, s.t.    n  |  fib(n)
                     --------------
                       0  |    1
                       1  |    1
                       2  |    2
                       3  |    3
                       4  |    5
                       5  |    8
    """
    i = 0
    first, second = 0, 1
    while i < index:
        first, second = second, first + second
        i += 1
    return second

def fib_gen():
    """
    Infinite generator of the fibonnaci sequence
    
    First 3 digits: [1,1,2]
    """
    first, second = 0, 1
    while 1:
        yield second
        first, second = second, first + second

def power_series_(x, c=0): #pylint:disable-msg=C0103
    """Returns a generator of (x - c) ** k for int k = 1 -> inf"""
    power = 0.0
    while 1:
        yield (x - c) ** power
        power += 1
