"""
Collision checking using mediator pattern to decouple shapes.
"""

import functools
import Shapes
import lib

COLL_SHAPES = Shapes.COLLISION_SHAPETYPES

COLLIDE_FNS = {
    #Collection-x collisions
    (COLL_SHAPES.Collection, COLL_SHAPES.Collection): lib.coll_collect_collect,
    (COLL_SHAPES.Collection, COLL_SHAPES.Circle): lib.coll_collect_single,
    (COLL_SHAPES.Collection, COLL_SHAPES.Line): lib.coll_collect_single,
    (COLL_SHAPES.Collection, COLL_SHAPES.Point): lib.coll_collect_single,
    (COLL_SHAPES.Collection, COLL_SHAPES.Rectangle): lib.coll_collect_single,
    
    #Circle-x collisions
    (COLL_SHAPES.Circle, COLL_SHAPES.Circle): lib.coll_circle_circle,
    (COLL_SHAPES.Circle, COLL_SHAPES.Line): lib.coll_circle_line,
    (COLL_SHAPES.Circle, COLL_SHAPES.Point): lib.coll_circle_point,
    (COLL_SHAPES.Circle, COLL_SHAPES.Rectangle): lib.coll_circle_rect,
    
    #Line-x collisions
    (COLL_SHAPES.Line, COLL_SHAPES.Line): lib.coll_line_line,
    (COLL_SHAPES.Line, COLL_SHAPES.Point): lib.coll_line_point,
    (COLL_SHAPES.Line, COLL_SHAPES.Rectangle): lib.coll_line_rect,
    
    #Point-x collisions
    (COLL_SHAPES.Point, COLL_SHAPES.Point): lib.coll_point_point,
    (COLL_SHAPES.Point, COLL_SHAPES.Rectangle): lib.coll_point_rect,

    #Rectangle-x collisions
    (COLL_SHAPES.Rectangle, COLL_SHAPES.Rectangle): lib.coll_rect_rect,    
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
        _k1 = shape1.collision_type
        _k2 = shape2.collision_type
        try:
            return COLLIDE_FNS[(_k1, _k2)]
        except KeyError:
            return Collider.reverse_args(COLLIDE_FNS[(_k2, _k1)])
    
    @staticmethod
    def reverse_args(func):
        """
        Returns a fuction that passes arguments
        to an underlying function in reverse order
        """
        @functools.wraps(func)
        def wrapper(arg1, arg2): #pylint:disable-msg=C0111
            return func(arg2, arg1)
        return wrapper

    @staticmethod
    def collision_check(shape1, shape2, eps=0):
        """
            Returns true if the shapes collide.

            Not all methods make use of epsilon 'fuzzing'
        """
        check_fn = Collider._collision_fn(shape1, shape2)
        return check_fn(shape1, shape2, eps)

    check = collision_check
