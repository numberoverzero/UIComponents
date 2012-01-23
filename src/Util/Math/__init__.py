"""
Common math functions and structures.
Sub-modules will include (basic) 2d vectors and funcitons on them.
"""

import math
import random
import trig_tables

PI = math.pi
TT_COS = trig_tables.COS
TT_SIN = trig_tables.SIN
TT_SIZE = trig_tables.SIZE

def angle_from_vector(vec_x, vec_y):
    """Gets the angle (clockwise from origin in radians) of the vector."""
    return math.atan2(vec_y, vec_x)

def clamp(val, min_, max_):
    """Clamps val to the range [min_, max_]"""
    if val < min_:
        val = min_
    elif val > max_:
        val = max_
    return val

def distance(pt1, pt2):
    """Checks the distance between two vectors pt1, pt2"""
    if len(pt1) != len(pt2):
        raise IndexError("Unequal length vectors")
    size = len(pt1)
    sum_ = 0.0
    for i in xrange(size):
        sum_ += (pt2[i] - pt1[i]) ** 2.0
    return sum_ ** 0.5

def fwrap(val, min_, max_):
    """Returns the wrapped float on [min_, max_]"""
    nmin = -min_
    return ((val + nmin) % (max_ + nmin)) - nmin

def gcd(a, b): #pylint:disable-msg=C0103
    """Assumes a, b are int"""
    if a < 0:
        a = -a #pylint:disable-msg=C0103
    if b < 0:
        b = -b #pylint:disable-msg=C0103
    while b:
        a, b = b, a % b #pylint:disable-msg=C0103
    return a

def is_zero(val, precision=1E-8):
    """Helper function for ignoring rounding errors"""
    return abs(val) <= precision

def iwrap(val, max_):
    """Returns the wrapped integer on [0,max_]"""
    return int(val % max_)

def lerp(min_, max_, t): #pylint:disable-msg=C0103
    """Standard lerp from min_"""
    return min_ + float(t) * (max_ - min_)

def limit_vector(vec_x, vec_y, mag_max):
    """Limits the magnitude of the vector to no greater than mag_max."""
    if mag_max < 0:
        msg = "max_magnitude can't be negative: {0}"
        raise ArithmeticError(msg.format(mag_max))
    mag_actual = (vec_x ** 2 + vec_y ** 2) ** 0.5
    if mag_actual > mag_max:
        vec_x, vec_y = unit(vec_x, vec_y)
        return vec_x * mag_max, vec_y * mag_max
    return vec_x, vec_y

def mk_rand_fn(min_, max_):
    """Returns a function that gives random floats on [min_, max_)"""
    def rnd_():
        """Returns a random float on [min_, max_)"""
        return rand(min_, max_)
    return rnd_

def mk_rnd_with_gap_fn(min_, max_):
    """Returns a function that creates random values on 
            [-max_,-min_] or [min_,max_]"""
    def rnd():
        """Returns a random value on [-max_,-min_] or [min_,max_]"""
        return rand_with_gap(min_, max_)
    return rnd

def mk_rot_fn(o_x, o_y, theta):
    """Returns a function that rotates around (ox, oy) by theta degrees."""
    def rot_(p_x, p_y):
        """Rotate point (px, py) around origin (ox, oy) by theta degrees."""
        return rotate(o_x, o_y, p_x, p_y, theta)
    return rot_

def mk_wrap_fn(min_, max_):
    """Returns a function that wraps a value on min_, max_"""
    def wrap_(val):
        """Returns the wrapped float on [min_,max_]"""
        return fwrap(val, min_, max_)
    return wrap_

def normalize(vals):
    """No return value- takes sequences and replaces their values"""
    size = len(vals)
    if size == 1:
        vals[0] = 1.0
    elif size > 0:
        min_ = float(min(vals))
        max_ = float(max(vals))
        if is_zero(max_ - min_):
            for i in xrange(size):
                vals[i] = 1.0
        else:
            for i in xrange(size):
                vals[i] = (vals[i] - min_) / (max_ - min_)
    else:
        pass
    
def rand(min_, max_):
    """Returns a random float on [min_, max_)"""
    return (max_ - min_) * random.random() + min_

def rand_with_gap(min_, max_):
    """Returns a random value on [-max_,-min_] or [min_,max_]"""
    r_pct = random.random()
    if r_pct <= 0.5:
        return -((max_ - min_) * 2 * r_pct + min_)
    else:
        return (max_ - min_) * (2 * r_pct - 1) + min_

def randint(min_, max_):
    """Returns a random integer on [min_, max_]"""
    return random.randint(min_, max_)

def rotate(o_x, o_y, p_x, p_y, theta):
    """Rotate point (px, py) around origin (ox, oy) by theta degrees."""
    index = int(0.001 + theta * TT_SIZE / (2 * PI) % TT_SIZE)
    
    
    px1 = TT_COS[index] * (p_x - o_x) - TT_SIN[index] * (p_y - o_y) + o_x
    py1 = TT_SIN[index] * (p_x - o_x) + TT_COS[index] * (p_y - o_y) + o_y
    return px1, py1

def unit(vec_x, vec_y):
    """Returns the unit vector components of the vector (vec_x, vec_y)"""
    mag = (vec_x ** 2 + vec_y ** 2) ** 0.5
    vec_x /= mag
    vec_y /= mag
    return vec_x, vec_y
