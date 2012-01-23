"""
Collision shapes.  Use Collider.check(shape1, shape2) to
check for collision between supported shapes.
"""
import Util.Structs
import Util.Math

COLLISION_SHAPETYPES = Util.Structs.enum("Circle",
                                         "Collection",
                                         "Line",
                                         "Pill",
                                         "Point",
                                         "Rectangle",
                                         )

_COLLECT_FMT = "Collection<{}>"
_CIRCLE_FMT = "Circle<c:{}, rad:{}, rot:{}>"
_LINE_FMT = "Line<p1:{}, p2:{}, rot:{}>"
_PILL_FMT = "Pill<c:{}, rad:{}, height:{}, rot:{}>"
_POINT_FMT = "Point<({},{}), rot:{}>"
_RECT_FMT = "Rect<c:{}, dim:({},{}), rot:{}>"
_VEC_ADD_ERR = "Couldn't add vec and other ({}, {})."
_VEC_DIV_ERR = "Division of vectors is ambiguous ({}, {})."
_VEC_MUL_ERR = "Multiplication of vectors is ambiguous ({}, {})."
_VEC_FMT = "<{},{}>"

class Collection(object):
    """Group of collision objects"""
    __slots__ = ['shapes']
    collision_type = COLLISION_SHAPETYPES.Collection
    def __init__(self, shapes = None):
        self.shapes = []
        if shapes:
            self.shapes.extend(shapes)
    
    def add_shape(self, shape):
        """Add a shape to the collection"""
        self.shapes.append(shape)
    
    def copy(self):
        """Return a copy of the object"""
        return Collection(shapes = [shape.copy() for shape in self.shapes])
    
    def center_at(self, point):
        """Attempt to center the collection at the point"""
        raise NotImplementedError()
    
    def get_center(self):
        """Return the center of the collection"""
        raise NotImplementedError()
    
    def remove_shape(self, shape):
        """Remove a shape from the collection"""
        self.shapes.remove(shape)
    
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
            if not self.collision_type == other.collision_type:
                return False
            self_shapes = set(self.shapes)
            other_shapes = set(other.shapes)
            return self_shapes == other_shapes
        except AttributeError:
            return False
    
    def __str__(self):
        return _COLLECT_FMT.format(", ".join(self.shapes))
        

class Circle(object):
    """Collidable circle"""
    
    __slots__ = ['center', 'radius', 'rot']
    collision_type = COLLISION_SHAPETYPES.Circle
    def __init__(self, x, y, radius, rot): #pylint:disable-msg=C0103
        self.center = Point(x, y)
        self.radius = radius
        self.rot = rot

    
    def center_at(self, point):
        """Attempt to center the shape at the point"""
        self.center.x, self.center.y = point.x, point.y
    
    def copy(self):
        """Return a copy of the object"""
        return Circle(self.center.x, self.center.y, self.radius, self.rot)
        
    def get_center(self):
        """
        Returns a point at the center of the circle
        """
        return self.center
    
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
        self.center.rotate_about(theta, pivot)
        self.center_at(self.center)
        self.rotate(theta)
    
    def __eq__(self, other):
        try:
            return (self.collision_type == other.collision_type and
                    self.radius == other.radius and
                    self.rot == other.rot and
                    self.center == other.center)
        except AttributeError:
            return False
    
    def __str__(self):
        return _CIRCLE_FMT.format(self.center, self.radius, self.rot)
        
class Line(object):
    """Collidable line segment"""

    __slots__ = ['p1', 'p2', 'rot', 'dirty', '_bbox']
    __triggers_dirty = ['p1', 'p2', 'rot']
    collision_type = COLLISION_SHAPETYPES.Line
    def __init__(self, p1, p2, rot): #pylint:disable-msg=C0103
        self.dirty = False
        self._bbox = None
        self.p1 = p1.copy() #pylint:disable-msg=C0103
        self.p2 = p2.copy() #pylint:disable-msg=C0103
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
    
    def get_bbox(self):
        """
        Returns the minimum axis-aligned bounding box of the line.
        
        Returns the smalled aabb that contains self.
        Caches value and lazy updates for performance.
        """
        is_dirty = self.dirty or self.p1.dirty or self.p2.dirty
        if self._bbox and not is_dirty:
            return self._bbox
        
        xmin, xmax = min(self.p1.x, self.p2.x), max(self.p1.x, self.p2.x)
        ymin, ymax = min(self.p1.y, self.p2.y), max(self.p1.y, self.p2.y)
        
        dx, dy = xmax - xmin, ymax - ymin #pylint:disable-msg=C0103
        
        self._bbox = Rectangle(xmin + dx / 2.0, ymin + dy / 2.0,
                               dx, dy, rot = 0)
        self.dirty = self.p1.dirty = self.p2.dirty = False
        return self._bbox
    
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
        center = self.get_center()
        center.rotate_about(theta, pivot)
        self.center_at(center)
        self.rotate(theta)
    
    def slope_intercept(self):
        """
        Returns m, b, is_vert for the equation y = mx + b
        
        if is_vert, m and b are None.
        """
        
        _dx = self.dx
        _dy = self.dy
        if abs(_dx <= 1E-8):
            return None, None, True
        
        m = _dy / _dx #pylint:disable-msg=C0103
        b = self.p1.y - m * self.p1.x #pylint:disable-msg=C0103
        return m, b, False

    def __eq__(self, other):
        try:
            return (self.collision_type == other.collision_type and
                    self.p1 == other.p1 and
                    self.p2 == other.p2 and
                    self.rot == other.rot)
        except AttributeError:
            return False
    
    def __setattr__(self, name, value):
        super(Line, self).__setattr__(name, value)
        if name in Line.__triggers_dirty:
            self.dirty = True
    
    def __str__(self):
        return _LINE_FMT.format(self.p1, self.p2, self.rot)

class Pill(Collection):
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
        Collection.__init__(self)
        self.center = center
        self.radius = radius
        self.height = height
        self.rot = rot
        self._calc_segments()
    
    def _calc_segments(self):
        """Always create the shape un-rotated, then rotate"""
        self.shapes = []
        self.shapes.append(Circle(self.center.x, 
                                  self.center.y + self.height / 2.0, 
                                  self.radius))
        self.shapes.append(Circle(self.center.x, 
                                  self.center.y - self.height / 2.0, 
                                  self.radius))
        self.shapes.append(Rectangle(self.center.x, self.center.y,
                                     self.radius * 2.0, self.height))
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
        return self.pill_body.get_center()
    
    @property
    def pill_body(self):
        """Returns the middle rectangle of the pill"""
        return self.shapes[1]
    
    @property
    def pill_bottom(self):
        """Return the bottom circle of the pill"""
        return self.shapes[2]
    
    @property
    def pill_top(self):
        """Returns the top circle of the pill"""
        return self.shapes[0]
    
    def rotate(self, theta):
        """Rotate the shape about its center by theta radians"""
        self.pill_top.rotate_about(theta, self.center)
        self.pill_body.rotate(theta)
        self.pill_bottom.rotate_about(theta, self.center)
        self.rot += theta
    
    def rotate_about(self, theta, pivot):
        """
        Rotate the shape theta degrees around another point
        
        For more details see Circle.rotate_about()
        """
        self.center.rotate_about(theta, pivot)
        self.rotate(theta)
        
    def __str__(self):
        return _PILL_FMT.format(self.center, self.radius,
                                self.height, self.rot)

class Point(object):
    """Collidable 2D point"""
    
    __slots__ = ['x', 'y', 'rot', 'dirty']
    __triggers_dirty = ['x', 'y']
    collision_type = COLLISION_SHAPETYPES.Point
    def __init__(self, x, y, rot=0): #pylint:disable-msg=C0103
        self.x = x #pylint:disable-msg=C0103
        self.y = y #pylint:disable-msg=C0103
        self.rot = rot
        self.dirty = False

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
    
    def __setattr__(self, name, value):
        super(Point, self).__setattr__(name, value)
        if name in Point.__triggers_dirty:
            self.dirty = True
            
    def __diff__(self, other):
        return Point(self.x-other.x, self.y-other.y)
    
    def __eq__(self, other):
        try:
            #Equality checks ignore rotation
            return (self.collision_type == other.collision_type and
                    self.x == other.x and 
                    self.y == other.y)
        except AttributeError:
            return False
    
    def __str__(self):
        return _POINT_FMT.format(self.x, self.y, self.rot)

class Rectangle(object):
    """
    Collidable rectangle
    
    x, y is the center of the rectangle"""
    
    __slots__ = ['center', 'w', 'h', 'rot', 'dirty', '_bbox']
    __triggers_dirty = ['x', 'y', 'w', 'h', 'rot']
    collision_type = COLLISION_SHAPETYPES.Rectangle
    def __init__(self, x, y, w, h, rot=0): #pylint:disable-msg=C0103
        self.dirty = False
        self._bbox = None
        self.center = Point(x, y)
        self.w = w #pylint:disable-msg=C0103
        self.h = h #pylint:disable-msg=C0103
        self.rot = rot
        
    def center_at(self, point):
        """Attempt to center the shape at the point"""
        self.center.x, self.center.y = point.x, point.y
    
    def copy(self):
        """Return a copy of the object"""
        return Rectangle(self.center.x, self.center.y, 
                         self.w, self.h, self.rot)
    
    @property
    def dims(self):
        """The dimensions of the rectangle, returned as a vec"""
        return vec(self.w, self.h)
    
    def get_center(self):
        """
        Returns a point at the center of the rectangle
        """
        return self.center
    
    def get_bbox(self):
        """
        Returns the minimum axis-aligned bounding box of the rectangle.
        
        Returns the smalled aabb that contains self.
        Caches value and lazy updates for performance.
        """
        is_dirty = self.dirty or self.center.dirty
        if self._bbox and not is_dirty:
            return self._bbox
        
        x, y = self.center.x, self.center.y #pylint:disable-msg=C0103
        w2, h2 = self.dims / 2.0 #pylint:disable-msg=C0103
        pivotfn = Util.Math.mk_rot_fn(x, y, self.rot)    
        
        x1, y1 = pivotfn(x - w2, y - h2) #pylint:disable-msg=C0103
        x2, y2 = pivotfn(x - w2, y + h2) #pylint:disable-msg=C0103
        x3, y3 = pivotfn(x + w2, y + h2) #pylint:disable-msg=C0103
        x4, y4 = pivotfn(x + w2, y - h2) #pylint:disable-msg=C0103
        
        xmin, xmax = min(x1, x2, x3, x4), max(x1, x2, x3, x4)
        ymin, ymax = min(y1, y2, y3, y4), max(y1, y2, y3, y4)
        
        self._bbox = Rectangle(xmin, ymin, xmax-xmin, ymax-ymin, rot = 0)
        self.dirty = self.center.dirty = False
        return self._bbox
    
    def rotate(self, theta):
        """Rotate the shape about its center by theta radians"""
        self.rot += theta
    
    def rotate_about(self, theta, pivot):
        """
        Rotate the shape theta degrees around another point
        
        For more details see Circle.rotate_about()
        """
        self.center.rotate_about(theta, pivot)
        self.center_at(self.center)
        self.rotate(theta)

    def __eq__(self, other):
        try:
            return (self.collision_type == other.collision_type and
                    self.center == other.center and
                    self.w == other.w and
                    self.h == other.h and
                    self.rot == other.rot)
        except AttributeError:
            return False
    
    def __setattr__(self, name, value):
        super(Rectangle, self).__setattr__(name, value)
        if name in Rectangle.__triggers_dirty:
            self.dirty = True
            
    def __str__(self):
        return _RECT_FMT.format(self.center, self.w, self.h, self.rot)

class Square(Rectangle):
    """Collidable square"""
    def __init__(self, x, y, s, rot=0): #pylint:disable-msg=C0103
        Rectangle.__init__(x, y, s, s, rot=rot)

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

    def __add__(self, other):
        try:
            return vec(self.x + other.x, self.y + other.y)
        except AttributeError:
            try:
                return vec(self.x+other, self.y+other)
            except: #pylint:disable-msg=W0702
                raise AttributeError(_VEC_ADD_ERR.format(self, other))
            
    def __diff__(self, other):
        return vec(self.x-other.x, self.y-other.y)

    def __div__(self, other):
        if hasattr(other, 'x'):
            raise ArithmeticError(_VEC_MUL_ERR.format(self, other))
        else:
            return vec(self.x*other, self.y*other)

    def __iter__(self):
        yield self.x
        yield self.y
    
    def __mul__(self, other):
        if hasattr(other, 'x'):
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

    
