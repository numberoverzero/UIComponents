"""
Collection of collision functions that check between two shapes.
Use Collision.check(shape1, shape2) to check supported shapes.
"""

import Shapes

def d2(shape1, shape2): #pylint:disable-msg=C0103
    """Returns the square of the distance between two shapes' centers"""
    c1, c2 = shape1.get_center(), shape2.get_center() #pylint:disable-msg=C0103
    return (c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2

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
    """Circle-rect collision detection."""
    big_rect = Shapes.Rectangle(rect.x - circle.radius,
                                rect.y - circle.radius,
                                rect.w + circle.radius * 2,
                                rect.h + circle.radius * 2)
    return coll_point_rect(circle.get_center(), big_rect, eps)

def coll_line_line(line1, line2, eps):
    """Line-line collision detection."""

    #Get eq line1
    dy1, dx1 = line1.dx, line1.dy
    vert1 = False
    if abs(dx1) > 1E-8:
        m1 = dy1/dx1 #pylint:disable-msg=C0103
        b1 = line1.p1.y - m1 * line1.p1.x #pylint:disable-msg=C0103
    else:
        vert1 = True

    #Get eq line 2
    dy2, dx2 = line2.dx, line2.dy
    vert2 = False
    if abs(dx2) > 1E-8:
        m2 = dy2/dx2 #pylint:disable-msg=C0103
        b2 = line2.p1.y - m2 * line2.p1.x #pylint:disable-msg=C0103
    else:
        vert2 = True

    if vert1 and vert2:
        #Both vertical lines
        if abs(vert1-vert2) > eps:
            #Too far apart
            return False

        #Check for either endpoint colliding with the other line
        return (coll_line_point(line1, line2.p1, eps) or
                coll_line_point(line1, line2.p2, eps))

    elif vert1:
        #Can't use line 1 for the slope
        coll_x = line1.p1.x
        coll_y = m2 * coll_x + b2
    elif vert2:
        #Can't use line 2 for the slope
        coll_x = line2.p1.x
        coll_y = m1 * coll_x + b1
    else:
        #Both slopes ok, solve linear equation w/substitution for x2
        dm = m2 / m1 #pylint:disable-msg=C0103
        coll_y = (b2 - dm * b1) / (1 - dm)
        coll_x = (coll_y - b1) / m1
    
    #Get the supposed collision point
    coll_pt = Shapes.Point(coll_x, coll_y)

    #Check that the collision point interacts with both line segments
    return (coll_line_point(line1, coll_pt, eps) and
            coll_line_point(line2, coll_pt, eps))

def coll_line_point(line, point, eps):
    """Line-point collision detection."""
    minx = min(line.p1.x, line.p2.x)
    maxx = max(line.p1.x, line.p2.x)
    miny = min(line.p1.y, line.p2.y)
    maxy = max(line.p1.y, line.p2.y)

    return ((minx - eps / 2.0 <= point.x <= maxx + eps / 2.0) and
            (miny - eps / 2.0 <= point.y <= maxy + eps / 2.0))

def coll_line_rect(line, rect, eps):
    """Line-rect collision detection."""
    minx = min(line.p1.x, line.p2.x)
    maxx = max(line.p1.x, line.p2.x)
    miny = min(line.p1.y, line.p2.y)
    maxy = max(line.p1.y, line.p2.y)
    line_as_rect = Shapes.Rectangle(minx, miny, maxx-minx, maxy-miny)
    return coll_rect_rect(line_as_rect, rect, eps)

def coll_point_point(point1, point2, eps):
    """Point-point collision detection."""
    return d2(point1, point2) <= eps ** 2

def coll_point_rect(point, rect, eps):
    """Point-rect collision detection."""
    if abs(rect.rot) <= 1E-5:
        #Close enough to zero rotation
        return ((rect.x - eps / 2.0 <= point.x <= rect.x+rect.w - eps / 2.0) and
                (rect.y - eps / 2.0 <= point.y <= rect.y+rect.h - eps / 2.0))
    
    #Rectangle is rotated- unrotate it, pivot the point to be compared
    #about the rectangle's center, compare, undo rotations
    
    pivot = rect.get_center()
    negrot = -rect.rot
    
    #unrotate the rect
    rect.rotate(negrot)
    #rotate the point by negrot around the pivot
    point.rotate_about(negrot, pivot)
    #Close enough to zero rotation
    coll =  ((rect.x - eps / 2.0 <= point.x <= rect.x+rect.w - eps / 2.0) and
             (rect.y - eps / 2.0 <= point.y <= rect.y+rect.h - eps / 2.0))
    
    #undo rotation
    rect.rotate(-negrot)
    point.rotate_about(-negrot, pivot)
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
    rect2_bbox = rect2.get_bbox()
    
    #check for collision
    coll = ((rect1.x + rect1.w + eps >= rect2_bbox.x) and
            (rect1.x <= rect2_bbox.x + rect2_bbox.w + eps) and
            (rect1.y + rect1.h + eps >= rect2_bbox.h) and
            (rect1.y <= rect2_bbox.y + rect2_bbox.h + eps))
    
    #undo rotations and pivots
    rect1.rotate(rot)
    rect2.rotate_about(rot, pivot)
    
    return coll
    
def coll_rect_rect(rect1, rect2, eps):
    """Rect-rect collision detection."""
    if abs(rect1.rot) <= 1E-5 and abs(rect1.rot) <= 1E-5:
        return ((rect1.x + rect1.w + eps >= rect2.x) and
                (rect1.x <= rect2.x + rect2.w + eps) and
                (rect1.y + rect1.h + eps >= rect2.h) and
                (rect1.y <= rect2.y + rect2.h + eps))
    
    #SAT dni from:
    #http://forums.xkcd.com/viewtopic.php?f=11&t=63710
    return not (_dni(rect1, rect2, eps) and _dni(rect2, rect1, eps))
    