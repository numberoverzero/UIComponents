import math

resolution = 100
values = 360 * resolution
factor = values / 360.0
inv_factor = 1.0 / factor
cos = {}
sin = {}

for i in xrange(values):
    cos[i] = math.cos(i * inv_factor)
    sin[i] = math.sin(i * inv_factor)


    
