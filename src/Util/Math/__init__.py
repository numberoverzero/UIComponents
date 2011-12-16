print "Math.__init__"
import math
import random
import trig_tables

cos = trig_tables.cos
sin = trig_tables.sin

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

def rotate(px,py, ox,oy, theta):
    theta = iwrap(trig_tables.factor * theta, trig_tables.values)
    px1 = cos[theta] * (px - ox) - sin[theta] * (py - oy) + ox
    py1 = sin[theta] * (px - ox) + cos[theta] * (py - oy) + oy
    return px1, py1

def mkRotFn(ox, oy, r):
    if isZero(r):
        #Don't send it through transforms for no rotation.
        def rot(px, py):
            return px, py
    else:
        def rot(px, py):
            return rotate(px, py, ox, oy, r)
    return rot

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
    m = (vx**2 + vy**2 ) ** 0.5
    if m > maxV:
        vx, vy = unitV(vx,vy)
        return vx*maxV, vy*maxV
    return vx, vy

def angleFromVector(vx, vy):
    return math.atan2(vy, vx)

def distance(p1, p2):
    x2 = (p2[0]-p1[0]) ** 2.0
    y2 = (p2[1]-p1[1]) ** 2.0
    return (x2 + y2) ** 0.5

def isZero(v, precision = 1E-8):
    return abs(v) <= precision

def normalize(vals):
    if len(vals) == 1:
        vals[0] = 1.0
    elif len(vals) > 0:
        m = float(min(vals))
        M = float(max(vals))
        if isZero(M-m):
            for i in xrange(len(vals)):
                vals[i] = 1.0
        else:
            for i in xrange(len(vals)):
                vals[i] = (vals[i] - m) / (M - m)
    else:
        pass