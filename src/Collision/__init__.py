"""
Collision processors and structures
"""

from Collider import Collider
import Shapes

def make_rect_at_bottom_left(x, y, w, h, rot=0): #pylint:disable-msg=C0103
    """
    Makes a collision rectangle.
    
    x, y specify the bottom left corner of the rectangle.
    """
    return Shapes.Rectangle(x + w / 2.0, y + w / 2.0, w, h, rot)
    
def make_rect_at_center(x, y, w, h, rot=0): #pylint:disable-msg=C0103
    """
    Makes a collision rectangle.
    
    x, y specify the center of the rectangle.
    """
    return Shapes.Rectangle(x, y, w, h, rot)