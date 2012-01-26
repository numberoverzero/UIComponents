""""
Common operations and queries regarding a numbers' digits.
These are largely imported from various project euler problems.
"""

def filter_numbers_with_digits(numbers, good_digits):
    """
    Returns a new list w/numbers that only have digits in good_digits.
    
    For example:
    numbers = [1,62,16,723,975,968,46,45]
    good_digits = [1,6,4]
    
    returns: [1,16,46]
    """
    is_good = lambda number: is_made_of(number, good_digits)
    return [number for number in numbers if is_good(number)]

def gen_digits(number):
    """
    Digit generator that returns the digits of n.
    
    Digits are returned in increasing order of magnitude,
    so for the number 1953, gen_digits would return
    3, 5, 9, 1.
    """
    while number:
        yield number % 10
        number /= 10

def has_digit(number, digit):
    """True if the digit is anywhere in number."""
    while number:
        d_curr = number % 10
        if d_curr == digit:
            return True
        number /= 10
    return False

def has_any_digit(number, digits):
    """True if any one of digits is a digit of number."""
    while number:
        d_curr = number % 10
        if d_curr in digits:
            return True
        number /= 10
    return False

def is_made_of(number, digits):
    """Returns true if number is only made of values in digits."""
    for digit in gen_digits(number):
        if digit not in digits:
            return False
    return True
 
def join_digits(digits, reverse=False):
    """
    Combines an iterable of digits, into an integer.
    
    Digits are passed in decreasing order of magnitude,
    so the sequence (2, 7, 1, 4) would return 2714
    
    To pass digits in INCREASING order of magnitude,
    ie. from gen_digits, use reversed = True
    the sequence (2, 7, 1, 4) would now return 4172
    """
    ttl = 0
    if reverse:
        for digit in reversed(digits):
            ttl *= 10
            ttl += digit
    else:
        for digit in digits:
            ttl *= 10
            ttl += digit
    return ttl

def ndigits(number):
    """Returns the number of digits in number."""
    ttl = 0
    while number:
        number /= 10
        ttl += 1
    return ttl

def rotate_digit(number):
    """
    Moves the rightmost digit (least sig) to the left of the number (most sig).
    
    Returns number, digit where 
    number is the new, rotated number
    digit is the digit that was moved.  Can return 0.
    """
    nd_ = ndigits(number) - 1
    digit = number % 10
    number /= 10
    number += digit * 10 ** nd_
    return number, digit