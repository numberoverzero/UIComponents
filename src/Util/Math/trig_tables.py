import math

resolution = 2000
size = 360 * resolution

cos = {}
sin = {}

for i in xrange(size):
    pct = float(i) / size
    cos[i] = math.cos(pct * 2 * math.pi)
    sin[i] = math.sin(pct * 2 * math.pi)

def index(theta):
    ind = int(0.001 + theta * size / (2*math.pi))
    return ind % size

def isCorrect(theta, print_ = False):
    
    expected = math.cos(theta)
    actual = cos[index(theta)]
    diff = abs(expected-actual)
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

def check_all(n):
    errors = []
    for i in xrange(int(size*n)):
        pct = float(i) / size
        theta = 2*math.pi * pct
        if not isCorrect(theta):
            errors.append(i)
    return (len(errors)>0, errors)
    

def check_random(n):
    import random
    errors = 0
    for _ in xrange(n):
        theta = random.random() * math.pi * 13.0
        if not isCorrect(theta):
            errors += 1
            print "\nERROR: "
            isCorrect(theta, True)
            
    print "{0} ERRORS".format(errors)
    
            
if __name__ == "__main__":
    res = 5
    nrand = 10000000
    print "Checking trig tables, {0}x resolution".format(res)
    check_all(res)
    print "Finished checking"
    print
    print "Checking {0} random values".format(nrand)
    check_random(nrand)
    print "Finished checking"
    print