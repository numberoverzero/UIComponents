"""
Pre-computes values for sin and cos, making calculations faster, though
slightly less accurate.  Can compensate for this by upping resolution.
Values are accurate to within 1/RESOLUTION of a degree.
"""

import math

RESOLUTION = 2000
SIZE = int(360 * RESOLUTION)

COS = {}
SIN = {}

for i in xrange(SIZE):
    __pct = float(i) / SIZE
    COS[i] = math.cos(__pct * 2 * math.pi)
    SIN[i] = math.sin(__pct * 2 * math.pi)

print "Loaded Trig Tables."

def index(theta):
    """Returns the index of the angle theta for cos and sin calculations."""
    ind = int(0.001 + theta * SIZE / (2 * math.pi))
    return ind % SIZE

def is_correct(theta, print_=False):
    """Determines if the difference between the computed
            and the actual values of cos(theta) are within
            "acceptable" limits.  If print_, prints
            the comparison, regardless of accuracy."""
    
    expected = math.cos(theta)
    actual = COS[index(theta)]
    diff = abs(expected - actual)
    if print_:
        print "==============="
        print "Checking: {0}".format(theta)
        print "Expected: {0}".format(expected)
        print "Actual:   {0}".format(actual)
        print "Diff:     {0}".format(diff)
        print
        print "Index:    {0}".format(index(theta))
        print "==============="
    return diff < 1E-5

def check_all(n_vals):
    """Checks each value on [0, 2PI] at resolution n * SIZE."""
    errors = []
    for val in xrange(int(SIZE * n_vals)):
        pct = float(val) / SIZE
        theta = 2 * math.pi * pct
        if not is_correct(theta):
            errors.append(val)
    return (len(errors) > 0, errors)
    

def check_random(n_vals):
    """Checks n random values for accuracy of cos."""
    import random
    errors = 0
    for _ in xrange(n_vals):
        theta = random.random() * math.pi * 13.0
        if not is_correct(theta):
            errors += 1
            print "\nERROR: "
            is_correct(theta, True)
            
    print "{0} ERRORS".format(errors)
    