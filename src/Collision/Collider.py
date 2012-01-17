"""
Collision checking using mediator pattern to decouple shapes.
"""

import functools
import Shapes
from Shapes import Circle, Line, Point, Rectangle
import lib

def reverse_args(func):
    """
        Returns a fuction that passes arguments
        to an underlying function in reverse order"""
    @functools.wraps(func)
    def wrapper(arg1, arg2): #pylint:disable-msg=C0111
        return func(arg2, arg1)
    return wrapper

COLLIDE_FNS = {
    #Circle-x collisions
    (Shapes.Circle, Shapes.Circle): lib.coll_circle_circle,
    (Shapes.Circle, Shapes.Line): lib.coll_circle_line,
    (Shapes.Circle, Shapes.Point): lib.coll_circle_point,
    (Shapes.Circle, Shapes.Rectangle): lib.coll_circle_rect,
    
    #Line-x collisions
    (Shapes.Line, Shapes.Line): lib.coll_line_line,
    (Shapes.Line, Shapes.Point): lib.coll_line_point,
    (Shapes.Line, Shapes.Rectangle): lib.coll_line_rect,
    
    #Point-x collisions
    (Shapes.Point, Shapes.Point): lib.coll_point_point,
    (Shapes.Point, Shapes.Rectangle): lib.coll_point_rect,

    #Rectangle-x collisions
    (Shapes.Rectangle, Shapes.Rectangle): lib.coll_rect_rect,    
    }

class Collider(object):
    """
        Handles collision checks between two objects.

        Fast method-detection is based upon the type of
        objects passed into collision_check.  Currently supports:
        Shapes.Circle
        Shapes.Line
        Shapes.Point
        Shapes.Rectangle
    """
    @staticmethod
    def _collision_fn(shape1, shape2):
        """
            Returns a function that checks for collision between
            shape1 and shape2 (IN THAT ORDER)
        """
        _t1 = type(shape1)
        _t2 = type(shape2)
        try:
            return COLLIDE_FNS[(_t1, _t2)]
        except KeyError:
            return reverse_args(COLLIDE_FNS[(_t2, _t1)])

    @staticmethod
    def collision_check(shape1, shape2, eps=0):
        """
            Returns true if the shapes collide.

            Not all methods make use of epsilon 'fuzzing'
        """
        check_fn = Collider._collision_fn(shape1, shape2)
        return check_fn(shape1, shape2, eps)

    check = collision_check
