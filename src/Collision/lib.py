"""
Collection of collision functions that check between two shapes.
Use Collision.check(shape1, shape2) to check supported shapes.
"""

import Shapes

def d2(shape1, shape2): #pylint:disable-msg=C0103
    """Returns the square of the distance between two shapes' centers"""
    c1, c2 = shape1.get_center(), shape2.get_center() #pylint:disable-msg=C0103
    return (c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2

def coll_collect_collect(collect1, collect2, eps):
    """Collection-collection collision detection."""
    from Collider import Collider
    for item1 in collect1:
        for item2 in collect2:
            colliding = Collider.check(item1, item2, eps)
            if colliding:
                return colliding
    return False

def coll_collect_single(collect, other_shape, eps):
    """
    Collection-x collision detection.
    
    x should not be a collision collection.
    """
    from Collider import Collider
    for shape in collect:
        colliding = Collider.check(shape, other_shape, eps)
        if colliding:
            return colliding
    return False

def coll_circle_circle(circle1, circle2, eps):
    """Circle-circle collision detection."""
    cd2 = d2(circle1, circle2)
    return cd2 <= (circle1.radius + circle2.radius + eps) ** 2

def coll_circle_line(circle, line, eps):
    """Circle-line collision detection."""
    d = Shapes.vec(line.p2 - line.p1) #pylint:disable-msg=C0103
    f = Shapes.vec(line.p1 - circle.get_center()) #pylint:disable-msg=C0103

    a = d.dot(d) #pylint:disable-msg=C0103
    b = 2 * f.dot(d) #pylint:disable-msg=C0103
    c = f.dot(f) - (circle.radius * circle.radius + eps) #pylint:disable-msg=C0103,C0301
    disc = b * b - 4 * a * c

    if disc < 0:
        #No intersection
        return False

    disc **= 0.5
    t1 = (-b + disc) / (2 * a) #pylint:disable-msg=C0103
    t2 = (-b - disc) / (2 * a) #pylint:disable-msg=C0103

    if 0 <= t1 <= 1:
        return True
    if 0 <= t2 <= 1:
        return True

    return False

def coll_circle_point(circle, point, eps):
    """Circle-point collision detection."""
    cd2 = d2(circle, point)
    return cd2 <= (circle.radius + eps) ** 2

def coll_circle_rect(circle, rect, eps):
    """
    Circle-rect collision detection.
    
    Extend the rectangle's width and height by 2*radius and check 
    if the center of the circle is inside that square
    """
    big_rect = rect.copy()
    big_rect.w += 2 * circle.radius
    big_rect.h += 2 * circle.radius
    return coll_point_rect(circle.get_center(), big_rect, eps)

def coll_line_line(line1, line2, eps):
    """Line-line collision detection."""

    #Get eq line1
    m1, b1, is_vert1 = line1.slope_intercept()  #pylint:disable-msg=C0103

    #Get eq line 2
    m2, b2, is_vert2 = line2.slope_intercept()  #pylint:disable-msg=C0103

    if is_vert1 and is_vert2:
        #Both vertical lines
        if abs(line1.p1.x - line2.p1.x) > eps:
            #Too far apart
            return False

        #Check for either endpoint colliding with the other line
        return (coll_line_point(line1, line2.p1, eps) or
                coll_line_point(line1, line2.p2, eps))

    elif is_vert1:
        #Can't use line 1 for the slope
        coll_x = line1.p1.x
        coll_y = m2 * coll_x + b2
    elif is_vert2:
        #Can't use line 2 for the slope
        coll_x = line2.p1.x
        coll_y = m1 * coll_x + b1
    else:
        #Both slopes ok, solve linear equation w/substitution
        coll_x = (b2 - b1) / (m1 - m2)
        coll_y = m1 * coll_x + b1
    
    #Get the supposed collision point
    coll_pt = Shapes.Point(coll_x, coll_y)

    #Check that the collision point interacts with both line segments
    return (coll_line_point(line1, coll_pt, eps) and
            coll_line_point(line2, coll_pt, eps))

def coll_line_point(line, point, eps):
    """Line-point collision detection."""
    line_bbox = line.get_bbox()

    return coll_point_rect(point, line_bbox, eps)

def coll_line_rect(line, rect, eps):
    """Line-rect collision detection."""
    line_bbox = line.get_bbox()
    return coll_rect_rect(line_bbox, rect, eps)

def coll_point_point(point1, point2, eps):
    """Point-point collision detection."""
    return d2(point1, point2) <= eps ** 2

def coll_point_rect(point, rect, eps):
    """Point-rect collision detection."""
    if abs(rect.rot) <= 1E-8:
        #Close enough to zero rotation
        eps2 = eps / 2.0
        w2, h2 = rect.dims / 2.0 #pylint:disable-msg=C0103
        return ((rect.x - eps2 - w2 <= point.x <= rect.x + eps2 + w2) and
                (rect.h - eps2 - h2 <= point.y <= rect.y + eps2 + h2))
    
    #Rectangle is rotated- unrotate it, pivot the point to be compared
    #about the rectangle's center, compare, undo rotations
    
    pivot = rect.get_center()
    rot = rect.rot
    
    #unrotate the rect
    rect.rotate(-rot)
    #rotate the point by negrot around the pivot
    point.rotate_about(-rot, pivot)
    #Close enough to zero rotation
    eps2 = eps / 2.0
    w2, h2 = rect.dims / 2.0 #pylint:disable-msg=C0103
    coll = ((rect.x - eps2 - w2 <= point.x <= rect.x + eps2 + w2) and
            (rect.h - eps2 - h2 <= point.y <= rect.y + eps2 + h2))
    
    #undo rotation
    rect.rotate(rot)
    point.rotate_about(rot, pivot)
    return coll
    

def _dni(rect1, rect2, eps):
    """
    Definitely not intersecting function 
    
    unrotates rect1, pivots rect2 by the same amount about rect1.center,
    then checks for intersection.  Use _dni(r1, r2) and _dni(r2, r1) to check
    rotated rectangle collision.
    """
    #we're unrotating around the center of rect1
    pivot = rect1.get_center()
    rot = rect1.rot
    
    #unrotate rect1
    rect1.rotate(-rot)
    
    #pivot rect2 by same rotation
    rect2.rotate_about(-rot, pivot)
    #get rect2's min bounding box
    r2bbox = rect2.get_bbox()
    
    #check for collision
    r1w2, r1h2 = rect1.dims / 2.0
    r2w2, r2h2 = r2bbox.dims / 2.0
    coll = ((rect1.x + r1w2 + eps >= r2bbox.x - r2w2) and
            (rect1.x - r1w2 <= r2bbox.x + r2w2 + eps) and
            (rect1.y + r1h2 + eps >= r2bbox.h - r2h2) and
            (rect1.y - r1h2 <= r2bbox.y + r2h2 + eps))
    
    #undo rotations and pivots
    rect1.rotate(rot)
    rect2.rotate_about(rot, pivot)
    
    return coll
    
def coll_rect_rect(rect1, rect2, eps):
    """Rect-rect collision detection."""
    if abs(rect1.rot) <= 1E-5 and abs(rect2.rot) <= 1E-5:
        r1w2, r1h2 = rect1.dims / 2.0
        r2w2, r2h2 = rect2.dims / 2.0
        return ((rect1.x + r1w2 + eps >= rect2.x - r2w2) and
                (rect1.x - r1w2 <= rect2.x + r2w2 + eps) and
                (rect1.y + r1h2 + eps >= rect2.h - r2h2) and
                (rect1.y - r1h2 <= rect2.y + r2h2 + eps))
    
    #SAT dni from:
    #http://forums.xkcd.com/viewtopic.php?f=11&t=63710
    return not (_dni(rect1, rect2, eps) and _dni(rect2, rect1, eps))
    