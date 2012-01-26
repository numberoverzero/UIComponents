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

def gen_digits(number, base=10):
    """
    Digit generator that returns the digits of n.
    
    Digits are returned in increasing order of magnitude,
    so for the number 1953, gen_digits would return
    3, 5, 9, 1.
    """
    while number:
        yield number % base
        number /= base

def get_digit(number, index, base=10):
    """
    Return the digit at number[index]
    
    index is 0-based, left to right.
    """
    ndig = ndigits(number, base)
    if index >= ndig:
        msg = "{} only has {} digits. (Asked for {} digit.)"
        raise IndexError(msg.format(number, ndig, index))
    if index < 0:
        msg = "get_digit doesn't handle index wrapping. (Asked for {} digit.)"
        raise IndexError(msg.format(index))
    
    #Move the digit indexed to the rightmost spot
    power = ndig - index - 1
    digit = number / (base ** power)
    
    #Pull the digit off the right side
    return digit % base
    
def has_digit(number, digit, base=10):
    """True if the digit is anywhere in number."""
    while number:
        d_curr = number % base
        if d_curr == digit:
            return True
        number /= base
    return False

def has_any_digit(number, digits, base=10):
    """True if any one of digits is a digit of number."""
    while number:
        d_curr = number % base
        if d_curr in digits:
            return True
        number /= base
    return False

def is_made_of(number, digits):
    """Returns true if number is only made of values in digits."""
    for digit in gen_digits(number):
        if digit not in digits:
            return False
    return True
 
def join_digits(digits, base=10, reverse=False):
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
            ttl *= base
            ttl += digit
    else:
        for digit in digits:
            ttl *= base
            ttl += digit
    return ttl

def ndigits(number, base=10):
    """Returns the number of digits in number."""
    ttl = 0
    while number:
        number /= base
        ttl += 1
    return ttl

def push_digit_left(number, digit, base=10):
    """Push a digit onto the left (most sig) side of the number."""
    return number + digit * base ** ndigits(number, base)

def push_digit_right(number, digit, base=10): #pylint:disable-msg=W0613
    """
    Push a digit onto the right( least sig) side of the number.
    
    Also known as "adding".  Provided for symmetry to push_digit_left."""
    return number + digit

def rotate_digit_left(number, base=10):
    """
    Moves the rightmost digit (least sig) to the left of the number (most sig).
    
    Returns number, digit where 
    number is the new, rotated number
    digit is the digit that was moved.  Can return 0.
            (a 0 means the number is now 1 order mag smaller,
                and the new number has 1 less digit.)
    """
    digit = number % base
    number /= base
    number = push_digit_left(number, digit, base)
    return number, digit

def rotate_digit_right(number, base=10):
    """
    Moves the leftmost digit (most sig) to the right of the number (least sig).
    
    Returns number, digit where 
    number is the new, rotated number
    digit is the digit that was moved.  Cannot return digit = 0
            (a 0 ins't moved- number will remain on the same order mag.)
    """
    digit = get_digit(number, 0, base)
    number /= base
    number = push_digit_right(number, digit, base)
    return number, digit