"""
Base component, handles layering management, position, selection, etc.
"""

import Engine.ID
import Collision.Shapes
import pyglet

class Component(object):
    """
    Base Component from which all components (combo/check boxes, list selection boxes)
    are derived.
    """
    
    __dirty_vars = ['x', 'y', 'w', 'h',]
    
    def __init__(self, **kwargs):
        """
        Create a component.
        
        kwarg : description : default
              x : local x coordinate of bottom-left corner  : 0
              y : local y coordinate of bottom-left corner  : 0
              w :            width of the component         : 0
              h :            height of the component        : 0
         parent :              parent's component           : None
          batch :             rendering batch               : None
          group :    the component's base rendering group   : None
        visible :      if the component is drawing/visible  : True
        enabled : if the component is taking input/updating : True
        """
        self._x, self._y = kwargs.get('x', 0), kwargs.get('y', 0) #pylint:disable-msg=C0103,C0301
        self._w, self._h = kwargs.get('w', 0), kwargs.get('h', 0) #pylint:disable-msg=C0103,C0301
        
        self._visible = kwargs.get('visible', True)
        self._enabled = kwargs.get('enabled', True)
        
        self._collider = Collision.Shapes.Rectangle(self._x, self._y, 
                                                    self._w, self._h)
        self._id = Engine.ID.get_id(self)
        self._parent = kwargs.get('parent', None)
        self._batch = kwargs.get('batch', None)
        self._group = kwargs.get('group', None)
        self._children = []
        self._elements = []
        
        self._dirty = False
    
    def _get_x(self):
        """Local x position"""
        return self._x
    def _set_x(self, value):
        """Set local x position"""
        self._x = value
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        """Local y position"""
        return self._y
    def _set_y(self, value):
        """Set local y position"""
        self._y = value
    y = property(_get_y, _set_y)
    
    def _get_w(self):
        """Width"""
        return self._w
    def _set_w(self, value):
        """Set width"""
        self._w = value
    w = property(_get_w, _set_w)
    
    def _get_h(self):
        """Height"""
        return self._h
    def _set_h(self, value):
        """Set height"""
        self._h = value
    h = property(_get_h, _set_h)
    
    def _get_visible(self):
        """The visible state of the component"""
        return self._visible
    def _set_visible(self, value):
        """Set the visible state of the component"""
        self._visible = value
        self.update_batch(self._batch, self._group)
    visible = property(_get_visible, _set_visible)
    
    def _get_parent(self):
        """Get the component's parent"""
        return self._parent
    parent = property(_get_parent)
    
    def _get_enabled(self):
        """The component is updating and handling input"""
        return self._enabled
    def _set_enabled(self, value):
        """Set the component's enabled state"""
        self._enabled = value
    enabled = property(_get_enabled, _set_enabled)
    
    def add_child(self, child):
        """
        Add a child component to the component's children.
        
        A component's parent should fully contain it for proper hit testing.
        """
        
        #Update the child's parent
        child.update_parent(self)
        
        #Add the child to our children
        self._children.append(child)
        
        
        #Update our batch and group
        self.update_batch(self._batch, self._group)
    
    def find_root(self):
        """Find the root component"""
        parent = self
        while parent.parent:
            parent = parent.parent
        return parent
    
    def remove(self, recursive=True):
        """
        Remove the component.
        
        If recursive, removes children as well.
        If has children and not recursive, children are appended to
            this parent.
            If this parent is None, children are discarded
        """
        
        if not recursive and not self.parent:
            #No parent to attach children to, remove them anyway
            recursive = True
        
        if recursive:
            #Remove all children
            for child in self._children:
                child.remove(recursive)
        else:
            for child in self._children:
                #self.x, self.y are local offsets to parent
                #add them so the components don't move from their
                #current position
                child.x += self.x
                child.y += self.y
                child.update_parent(self.parent)
        self._children = []
    
    def update_batch(self, batch, group):
        """
        Update the batch and group of the component.
        
        Called when visibility changes and children are added.
        """
        self._batch, self._group = batch, group
        
        child_group = pyglet.graphics.OrderedGroup(0, group)
        own_group = pyglet.graphics.OrderedGroup(1, group)
        
        for child in self._children:
            #Pass children the lower of the layers
            child.update_batch((batch if self.visible else None), child_group)
        
        for element in self._elements:
            element.update_batch((batch if self.visible else None), own_group)
    
    def update_global_coords(self):
        """Update global coordinates"""
        self._gx, self._gy = self.x, self.y #pylint:disable-msg=W0201
        if self.parent:
            self._gx += self.parent.gx
            self._gy += self.parent.gy
        for child in self._children:
            child.update_global_coords()