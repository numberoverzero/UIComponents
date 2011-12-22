import math
import random
import trig_tables

PI = math.pi
tt_cos = trig_tables.cos
tt_sin = trig_tables.sin
tt_size = trig_tables.size


def iwrap(x, M):
    """Returns the wrapped integer on [0,M]"""
    return int(x%M)

def fwrap(x, m, M):
    """Returns the wrapped float on [m, M]"""
    s = -m
    return ( (x + s) % (M + s) ) - s

def mkWrapFn(m, M):
    def _wrap(x):
        s = -m
        return ( (x + s) % (M + s) ) - s
    return _wrap

def clamp(v, vmin, vmax):
    if v < vmin:
        v = vmin
    elif v > vmax:
        v = vmax
    return v

def rotate(ox, oy, px, py, theta):
    index = int(0.001 + theta * tt_size / (2*PI) % tt_size)
    
    px1 = tt_cos[index] * (px - ox) - tt_sin[index] * (py - oy) + ox
    py1 = tt_sin[index] * (px - ox) + tt_cos[index] * (py - oy) + oy
    return px1, py1

def mkRotFn(ox, oy, r):
    def rot_(px, py):
        return rotate(ox, oy, px, py, r)
    return rot_

def randint(rMin, rMax):
    """Random Integer on [rMin, rMax]"""
    return random.randint(rMin, rMax)

def rand(rMin, rMax):
    return (rMax-rMin) * random.random() + rMin

def mkRndFn(rMin, rMax):
    def rnd():
        return rand(rMin, rMax)
    return rnd

def randWithGap(rMin, rMax):
    r = random.random()
    if r <= 0.5:
        return -( (rMax-rMin) * 2 * r + rMin )
    else:
        return (rMax-rMin) * (2*r - 1) + rMin

def mkRndWGapFn(rMin, rMax):
    def rnd():
        return randWithGap(rMin, rMax)
    return rnd

def unitV(vx, vy):
    m = (vx**2 + vy**2 ) ** 0.5
    vx /= m
    vy /= m
    return vx, vy

def limV(vx, vy, maxV):
    if maxV < 0:
        raise ArithmeticError("max_magnitude can't be negative: {0}".format(maxV))
    m = (vx**2 + vy**2 ) ** 0.5
    if m > maxV:
        vx, vy = unitV(vx,vy)
        return vx*maxV, vy*maxV
    return vx, vy

def angleFromVector(vx, vy):
    return math.atan2(vy, vx)

def distance(p1, p2):
    if len(p1) != len(p2):
        raise IndexError("Unequal length vectors")
    n = len(p1)
    s = 0.0
    for i in xrange(n):
        s += (p2[i]-p1[i]) ** 2.0
    return s ** 0.5

def isZero(v, precision = 1E-8):
    return abs(v) <= precision

def normalize(vals):
    """No return value- takes sequences and replaces their values"""
    n = len(vals)
    if n == 1:
        vals[0] = 1.0
    elif n > 0:
        m = float(min(vals))
        M = float(max(vals))
        if isZero(M-m):
            for i in xrange(n):
                vals[i] = 1.0
        else:
            for i in xrange(n):
                vals[i] = (vals[i] - m) / (M - m)
    else:
        pass
    

