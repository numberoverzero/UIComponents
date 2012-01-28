""""
Common operations and queries regarding a numbers' digits.
These are largely imported from various project euler problems.
"""
from math import floor, log10

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

def get_digit(number, index):
    """
    Return the digit at number[index]
    
    index is 0-based, left to right.
    """
    return int(str(number)[index])
    
def has_digit(number, digit):
    """True if the digit is anywhere in number."""
    return str(digit) in str(number)

def has_any_digit(number, digits):
    """True if any one of digits is a digit of number."""
    snumber = str(number)
    for digit in digits:
        if str(digit) in snumber:
            return True
    return False

def is_made_of(number, digits):
    """Returns true if number is only made of values in digits."""
    for digit in gen_digits(number):
        if digit not in digits:
            return False
    return True
 
def join_digits(digits):
    """
    Combines an iterable of digits, into an integer.
    
    Digits are passed in increasing order of magnitude,
    so the sequence (2, 7, 1, 4) would return 4172
    """
    return sum(d * 10 ** i for i, d in enumerate(digits))

def ndigits(number):
    """
    Returns the number of digits in number.
    
    Accurate for values of number < 1E15 - 1 """
    return 1 + floor(log10(number))

def push_digit_left(number, digit):
    """Push a digit onto the left (most sig) side of the number."""
    return number + digit * 10 ** ndigits(number)

def push_digit_right(number, digit):
    """
    Push a digit onto the right( least sig) side of the number.
    
    Also known as "adding".  Provided for symmetry to push_digit_left."""
    return number + digit

def rotate_digit_left(number):
    """
    Moves the rightmost digit (least sig) to the left of the number (most sig).
    
    Returns number, digit where 
    number is the new, rotated number
    digit is the digit that was moved.  Can return 0.
            (a 0 means the number is now 1 order mag smaller,
                and the new number has 1 less digit.)
    """
    digit = number % 10
    number /= 10
    number = push_digit_left(number, digit)
    return number, digit

def rotate_digit_right(number):
    """
    Moves the leftmost digit (most sig) to the right of the number (least sig).
    
    Returns number, digit where 
    number is the new, rotated number
    digit is the digit that was moved.  Cannot return digit = 0
            (a 0 ins't moved- number will remain on the same order mag.)
    """
    digit = get_digit(number, 0)
    number /= 10
    number = push_digit_right(number, digit)
    return number, digit