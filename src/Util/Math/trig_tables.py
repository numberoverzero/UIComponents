import math

resolution = 100
size = 360 * resolution

cos = {}
sin = {}

for i in xrange(size):
    pct = float(i) / size
    cos[i] = math.cos(pct * 2 * math.pi)
    sin[i] = math.sin(pct * 2 * math.pi)

def index(theta):
    theta = int(0.001 + theta * size / (2*math.pi))
    return theta % size

def correct(theta):
    expected = math.cos(theta)
    actual = cos[index(theta)]
    diff = abs(expected-actual)
    return diff < 1E-5


def check_all(n):
    for i in xrange(size*n):
        pct = float(i) / size
        theta = 2*math.pi * pct
        if not correct(theta):
            print i
            
print "Checking 100xresolution"
check_all(100)
print "Finished checking"