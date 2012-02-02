"""
Math functions
"""

__all__ = ['PI', 'angle_from_vector', 'clamp', 'cos', 'distance', 'fwrap', 
           'gcd', 'is_zero', 'iwrap', 'lerp', 'limit_vector', 'mk_rand_fn',
           'mk_rand_with_gap_fn', 'mk_rot_fn', 'mk_wrap_fn', 'normalize',
           'rand', 'rand_with_gap', 'randint', 'rotate', 'sin', 'unit']

import math, random
import trig_tables

PI = math.pi
_TT_COS = trig_tables.COS
_TT_SIN = trig_tables.SIN
_TT_SIZE = trig_tables.SIZE

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

def cos(theta):
    """Uses pre-computed trig tables for faster calcs"""
    index = int(0.00001 + theta * _TT_SIZE / (2 * PI) % _TT_SIZE)
    return _TT_COS[index]

def distance(pt1, pt2):
    """Checks the distance between two vectors pt1, pt2"""
    if len(pt1) != len(pt2):
        raise IndexError("Unequal length vectors")
    sum_ = 0.0
    for pt1, pt2 in zip(pt1, pt2):
        sum_ += (pt2 - pt1) ** 2.0
    return sum_ ** 0.5

def fwrap(val, min_, max_):
    """Returns the wrapped float on [min_, max_]"""
    nmin = -min_
    return ((val + nmin) % (max_ + nmin)) - nmin

def gcd(num1, num2):
    """Assumes num1, num2 are int"""
    num1 = abs(num1)
    num2 = abs(num2)
    while num2:
        num1, num2 = num2, num1 % num2
    return num1

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

def mk_rand_with_gap_fn(min_, max_):
    """
    Returns a function that creates random values on a discontinuous range 
    
    [-max_,-min_] or [min_,max_]
    """
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
    """
    Returns a normalized list
    
    When the values are all within 1E-8, returns a list of [1.0 / len(vals)]
    """
    
    size = len(vals)
    norm_vals = [0]*size
    
    if size == 1:
        norm_vals[0] = 1.0
    else:
        #Size > 1
        min_ = float(min(vals))
        max_ = float(max(vals))
        if is_zero(max_ - min_):
            norm_vals = [1.0 / size] * size
        else:
            for i in xrange(size):
                norm_vals[i] = (vals[i] - min_) / (max_ - min_)
    
    return norm_vals
    
    
def rand(min_, max_):
    """Returns a random float on [min_, max_)"""
    return lerp(min_, max_, random.random())

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
    index = int(0.00001 + theta * _TT_SIZE / (2 * PI) % _TT_SIZE)
    
    
    px1 = _TT_COS[index] * (p_x - o_x) - _TT_SIN[index] * (p_y - o_y) + o_x
    py1 = _TT_SIN[index] * (p_x - o_x) + _TT_COS[index] * (p_y - o_y) + o_y
    return px1, py1

def sin(theta):
    """Uses pre-computed trig tables for faster calcs"""
    index = int(0.00001 + theta * _TT_SIZE / (2 * PI) % _TT_SIZE)
    return _TT_COS[index]

def unit(vec_x, vec_y):
    """Returns the unit vector components of the vector (vec_x, vec_y)"""
    mag = (vec_x ** 2 + vec_y ** 2) ** 0.5
    vec_x /= mag
    vec_y /= mag
    return vec_x, vec_y