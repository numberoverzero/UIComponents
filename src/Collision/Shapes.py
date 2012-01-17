"""
Collision shapes.  Use Collider.check(shape1, shape2) to
check for collision between supported shapes.
"""


class Circle(object):
    """Collidable circle"""
    
    __slots__ = ['x', 'y', 'r']
    
    def __init__(self, x, y, r): #pylint:disable-msg=C0103
        self.x = x #pylint:disable-msg=C0103
        self.y = y #pylint:disable-msg=C0103
        self.r = r #pylint:disable-msg=C0103

    def center(self):
        """
        Returns a point at the center of the circle
        """
        return Point(self.x, self.y)

    def __eq__(self, other):
        try:
            return ((self.r == other.r) and
                    (self.x == other.x) and
                    (self.y == other.y))
        except AttributeError:
            return False
        
class Line(object):
    """Collidable line segment"""

    __slots__ = ['p1','p2']

    def __init__(self, p1, p2): #pylint:disable-msg=C0103
        self.p1 = p1 #pylint:disable-msg=C0103
        self.p2 = p2 #pylint:disable-msg=C0103

    def center(self):
        """
        Returns a point at the midpoint of the line
        """
        dx, dy = self.dxdy() #pylint:disable-msg=C0103
        return Point(self.p1.x + 0.5 * dx, self.p1.y + 0.5 * dy)

    def dxdy(self):
        """
        Returns (delta x, delta y)
        """
        return (self.p2.x - self.p1.x), (self.p2.y - self.p1.y)

    def __eq__(self, other):
        try:
            return self.p1 == other.p1 and self.p2 == other.p2
        except AttributeError:
            return False

class Point(object):
    """Collidable 2D point"""
    
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y): #pylint:disable-msg=C0103
        self.x = x #pylint:disable-msg=C0103
        self.y = y #pylint:disable-msg=C0103

    def center(self):
        """
        Returns itself (points have no size)
        """
        return self
    
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __diff__(self, other):
        return vec(self.x-other.x, self.y-other.y)

class Rectangle(object):
    """Collidable rectangle"""
    
    __slots__ = ['x', 'y', 'w', 'h']
    
    def __init__(self, x, y, w, h): #pylint:disable-msg=C0103
        self.x = x #pylint:disable-msg=C0103
        self.y = y #pylint:disable-msg=C0103
        self.w = w #pylint:disable-msg=C0103
        self.h = h #pylint:disable-msg=C0103

    def center(self):
        """
        Returns a point at the center of the rectangle
        """
        return Point(self.x + self.w / 2.0, self.y + self.h / 2.0)

    def __eq__(self, other):
        try:
            return ((self.w == other.w) and
                    (self.h == other.h) and
                    (self.x == other.x) and
                    (self.y == other.y))
        except AttributeError:
            return False

class Square(Rectangle):
    """Collidable square"""
    def __init__(self, x, y, w): #pylint:disable-msg=C0103
        super(Square, self).__init__(x, y, w, w)

_VEC_MUL_ERR = "Multiplication of vectors is ambiguous ({}, {})."
_VEC_FMT = "<{},{}>"
class vec(object): #pylint:disable-msg=C0103
    """2d vector"""
    __slots__ = ['x', 'y']
    def __init__(self, x, y): #pylint:disable-msg=C0103
        self.x, self.y = x, y #pylint:disable-msg=C0103

    @staticmethod
    def as_vec(point):
        """Returns a point as a vec object"""
        return vec(point.x, point.y)

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

    
