"""
Collision shapes.  Use Collider.check(shape1, shape2) to
check for collision between supported shapes.
"""

import Util.Math

_CIRCLE_FMT = "Circle<c:{}, rad:{}, rot:{}>"
_LINE_FMT = "Line<p1:{}, p2:{}, rot:{}>"
_PILL_FMT = "Pill<c:{}, rad:{}, height:{}, rot:{}>"
_POINT_FMT = "Point<({},{}), rot:{}>"
_RECT_FMT = "Rect<pos:({},{}), dim:({},{}), rot:{}>"
_VEC_MUL_ERR = "Multiplication of vectors is ambiguous ({}, {})."
_VEC_FMT = "<{},{}>"


class Circle(object):
    """Collidable circle"""
    
    __slots__ = ['x', 'y', 'radius', 'rot']
    
    def __init__(self, x, y, radius, rot): #pylint:disable-msg=C0103
        self.x = x #pylint:disable-msg=C0103
        self.y = y #pylint:disable-msg=C0103
        self.radius = radius
        self.rot = rot

    
    def center_at(self, point):
        """Attempt to center the shape at the point"""
        self.x, self.y = point.x, point.y
    
    def copy(self):
        """Return a copy of the object"""
        return Circle(self.x, self.y, self.radius, self.rot)
        
    def get_center(self):
        """
        Returns a point at the center of the circle
        """
        return Point(self.x, self.y)
    
    def rotate(self, theta):
        """Rotate the shape about its center by theta radians"""
        self.rot += theta
    
    def rotate_about(self, theta, pivot):
        """
        Rotate the shape theta degrees around another point
        
        The shape is pivoted at its center; for exmaple:
        >>> c = Circle(10, 0, 5)
        >>> pivot = Point(10, 10)
        >>> c.rotate_about(PI / 2)
        
        c.x == 20
        c.y == 10
        
        c is now positioned at (20, 10), having rotated 90 degrees
        counter-clockwise about the point (10, 10)
        """
        center = self.get_center()
        center.rotate_about(theta, pivot)
        self.center_at(center)
        self.rotate(theta)
    
    def __eq__(self, other):
        try:
            return ((self.radius == other.radius) and
                    (self.rot == other.rot) and
                    (self.x == other.x) and
                    (self.y == other.y))
        except AttributeError:
            return False
    
    def __str__(self):
        return _CIRCLE_FMT.format(self.get_center(), self.radius, self.rot)
        
class Line(object):
    """Collidable line segment"""

    __slots__ = ['p1', 'p2', 'rot']

    def __init__(self, p1, p2, rot): #pylint:disable-msg=C0103
        self.p1 = p1 #pylint:disable-msg=C0103
        self.p2 = p2 #pylint:disable-msg=C0103
        self.rot = rot

    def center_at(self, point):
        """Attempt to center the shape at the point"""
        center = self.get_center()
        diff = point - center
        self.p1.x += diff.x
        self.p1.y += diff.y
        
        self.p2.x += diff.x
        self.p2.y += diff.y
        
    def copy(self):
        """Return a copy of the object"""
        return Line(self.p1.copy(), self.p2.copy(), self.rot)
    
    @property
    def dx(self): #pylint:disable-msg=C0103
        """Return delta x between endpoints"""
        return self.p2.x - self.p1.x
    
    @property
    def dy(self): #pylint:disable-msg=C0103
        """Return delta y between endpoints"""
        return self.p2.y - self.p1.y
    
    def get_center(self):
        """
        Returns a point at the midpoint of the line
        """
        return Point(Util.Math.lerp(self.p1.x, self.p2.x, 0.5),
                     Util.Math.lerp(self.p1.y, self.p2.y, 0.5))
    
    def rotate(self, theta):
        """Rotate the shape about its center by theta radians"""
        center = self.get_center()
        self.p1.rotate_about(theta, center)
        self.p2.rotate_about(theta, center)
        self.rot += theta
    
    def rotate_about(self, theta, pivot):
        """
        Rotate the shape theta degrees around another point
        
        For more details see Circle.rotate_about()
        """
        new_center = self.get_center()
        new_center.rotate_about(theta, pivot)
        self.center_at(new_center)
        self.rotate(theta)

    def __eq__(self, other):
        try:
            return (self.p1 == other.p1 and
                    self.p2 == other.p2 and
                    self.rot == other.rot)
        except AttributeError:
            return False
    
    def __str__(self):
        return _LINE_FMT.format(self.p1, self.p2, self.rot)

class Pill(object):
    """Collidable pill-shaped object"""
    __slots__ = ['center', 'radius', 'height', 
                 'top', 'middle', 'bottom', 'rot']
    
    def __init__(self, center, radius, height, rot=0):
        """
        Construct a collidable pill
        
        center is a point at the center of the pill
        radius is the radius of the circles, and the width of the body
        height is the distance between the centers of the two circles
        """
        self.top = self.middle = self.bottom = None
        self.center = center
        self.radius = radius
        self.height = height
        self.rot = rot
        self._calc_segments()
    
    def _calc_segments(self):
        """Always create the shape un-rotated, then rotate"""
        self.top = Circle(self.center.x, 
                          self.center.y + self.height / 2.0, 
                          self.radius)
        self.bottom = Circle(self.center.x, 
                          self.center.y - self.height / 2.0, 
                          self.radius)
        self.middle = Rectangle(self.center.x - self.radius,
                                self.center.y - self.height / 2.0,
                                self.radius * 2.0,
                                self.height)
        rot = self.rot
        self.rotate(rot)
        self.rot = rot
    
    def center_at(self, point):
        """Attempt to center the shape at the point"""
        self.center = point.copy()
        self._calc_segments()
    
    def copy(self):
        """Return a copy of the object"""
        return Pill(self.center.copy(), self.radius, self.height, self.rot)
    
    def get_center(self):
        """Return the center of the pill (center of the rect)"""
        return self.middle.get_center()
    
    def rotate(self, theta):
        """Rotate the shape about its center by theta radians"""
        self.top.rotate_about(theta, self.center)
        self.middle.rotate(theta)
        self.bottom.rotate_about(theta, self.center)
        self.rot += theta
    
    def rotate_about(self, theta, pivot):
        """
        Rotate the shape theta degrees around another point
        
        For more details see Circle.rotate_about()
        """
        self.center.rotate_about(theta, pivot)
        self.rotate(theta)
    
    def __eq__(self, other):
        try:
            return (self.center == other.center and
                    self.radius == other.radius and
                    self.height == other.height and
                    self.rot == other.rot)
        except AttributeError:
            return False
    
    def __str__(self):
        return _PILL_FMT.format(self.center, self.radius,
                                self.height, self.rot)

class Point(object):
    """Collidable 2D point"""
    
    __slots__ = ['x', 'y', 'rot']
    
    def __init__(self, x, y, rot=0): #pylint:disable-msg=C0103
        self.x = x #pylint:disable-msg=C0103
        self.y = y #pylint:disable-msg=C0103
        self.rot = rot

    def center_at(self, point):
        """Attempt to center the shape at the point"""
        self.x, self.y = point.x, point.y
    
    def copy(self):
        """Return a copy of the object"""
        return Point(self.x, self.y, self.rot)
    
    def get_center(self):
        """
        Returns itself (points have no size)
        """
        return self
    
    def rotate(self, theta):
        """Rotate the shape about its center by theta radians"""
        self.rot += theta
    
    def rotate_about(self, theta, pivot):
        """
        Rotate the shape theta degrees around another point
        
        For more details see Circle.rotate_about()
        """
        self.x, self.y = Util.Math.rotate(pivot.x, pivot.y, 
                                          self.x, self.y, theta)
        self.rotate(theta)
        
    def __diff__(self, other):
        return Point(self.x-other.x, self.y-other.y)
    
    def __eq__(self, other):
        try:
            #Equality checks ignore rotation
            return (self.x == other.x and 
                    self.y == other.y)
        except AttributeError:
            return False
    
    def __str__(self):
        return _POINT_FMT.format(self.x, self.y, self.rot)

class Rectangle(object):
    """Collidable rectangle"""
    
    __slots__ = ['x', 'y', 'w', 'h', 'rot']
    
    def __init__(self, x, y, w, h, rot=0): #pylint:disable-msg=C0103
        self.x = x #pylint:disable-msg=C0103
        self.y = y #pylint:disable-msg=C0103
        self.w = w #pylint:disable-msg=C0103
        self.h = h #pylint:disable-msg=C0103
        self.rot = rot

    def center_at(self, point):
        """Attempt to center the shape at the point"""
        self.x, self.y = point.x - self.w / 2.0, point.y - self.h / 2.0
    
    def copy(self):
        """Return a copy of the object"""
        return Rectangle(self.x, self.y, self.w, self.h, self.rot)
        
    def get_center(self):
        """
        Returns a point at the center of the rectangle
        """
        return Point(self.x + self.w / 2.0, self.y + self.h / 2.0)
    
    def rotate(self, theta):
        """Rotate the shape about its center by theta radians"""
        raise NotImplementedError()
    
    def rotate_about(self, theta, pivot):
        """
        Rotate the shape theta degrees around another point
        
        For more details see Circle.rotate_about()
        """
        raise NotImplementedError()

    def __eq__(self, other):
        try:
            return ((self.w == other.w) and
                    (self.h == other.h) and
                    (self.x == other.x) and
                    (self.y == other.y))
        except AttributeError:
            return False
    
    def __str__(self):
        return _RECT_FMT.format(self.x, self.y,
                                self.w, self.h, self.rot)

class vec(object): #pylint:disable-msg=C0103
    """2d vector"""
    __slots__ = ['x', 'y']
    def __init__(self, x, y=None): #pylint:disable-msg=C0103
        if not y:
            #Either single value, or structure with x, y values
            try:
                self.x, self.y = x.x, x.y #pylint:disable-msg=C0103
            except AttributeError:
                self.x = self.y = x
        else:
            self.x, self.y = x, y #pylint:disable-msg=C0103

    def dot(self, other):
        """Returns the dot product of two vectors/points"""
        return self.x * other.x + self.y * other.y

    def mag2(self):
        """Returns the magnitude squared of the vector/point"""
        return self.x*self.x + self.y*self.y

    def unit2(self):
        """Returns the unit squared vector of the point."""
        mag2 = self.mag2()
        return vec(self.x * self.x / mag2, self.y * self.y / mag2)

    def __diff__(self, other):
        return vec(self.x-other.x, self.y-other.y)

    def __add__(self, other):
        try:
            return vec(self.x+other.x, self.y-other.y)
        except AttributeError:
            try:
                return vec(self.x+other, self.y+other)
            except: #pylint:disable-msg=W0702
                return vec(0, 0)

    def __mul__(self, other):
        if hasattr(other, 'x') or hasattr(other, 'y'):
            raise ArithmeticError(_VEC_MUL_ERR.format(self, other))
        else:
            return vec(self.x*other, self.y*other)

    def __radd__(self, other):
        return self + other

    def __repr__(self):
        return self.__str__()
    
    def __rmul__(self, other):
        return self * other
    
    def __str__(self):
        return _VEC_FMT.format(self.x, self.y)

    
