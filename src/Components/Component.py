"""
Base component, handles layering management, position, selection, etc.
"""

import Engine.ID
import Collision
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
        """
        self._x, self._y = kwargs.get('x', 0), kwargs.get('y', 0) #pylint:disable-msg=C0103,C0301
        self._w, self._h = kwargs.get('w', 0), kwargs.get('h', 0) #pylint:disable-msg=C0103,C0301
        
        self._visible = kwargs.get('visible', True)
        
        self._collider = Collision.make_rect_at_bottom_left(
                            self._x, self._y, self._w, self._h)
        self._id = Engine.ID.get_id(self)
        self._parent = kwargs.get('parent', None)
        self._elements = []
        
        
        self._batch = kwargs.get('batch', None)
        self._group = kwargs.get('group', None)
        self._element_group = None
        self.update_batch(self._batch, self._group)
        self._dirty = False
    
    def __setattr__(self, name, value):
        super(Component, self).__setattr__(name, value)
        if name in Component.__dirty_vars:
            self._dirty = True
    
    def _get_x(self):
        """Local x position"""
        return self._x
    def _set_x(self, value):
        """Set local x position"""
        self._x = value
    x = property(_get_x, _set_x)
    
    @property
    def gx(self): #pylint:disable-msg=C0103
        """Global x position"""
        return self._gx
    
    def _get_y(self):
        """Local y position"""
        return self._y
    def _set_y(self, value):
        """Set local y position"""
        self._y = value
    y = property(_get_y, _set_y)
    
    @property
    def gy(self): #pylint:disable-msg=C0103
        """Global y position"""
        return self._gy
    
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
    
    @property
    def parent(self):
        """Get the component's parent"""
        return self._parent
    
    def add_element(self, element):
        """
        Add an element to this component.
        
        Elements are _part of_ the component
        (Containers' children are contained by the component)
        """
        group = pyglet.graphics.OrderedGroup(len(self._elements),
                                             self._element_group)
        element.update_batch((self._batch if self.visible else None), group)
        self._elements.append(element)
    
    def find_root(self):
        """Find the root component (should be a screen)"""
        parent = self
        while parent.parent:
            parent = parent.parent
        return parent
    
    def remove(self):
        """
        Remove the component.
        
        Calls remove on each of its elements.
        """
        self.update_parent(None)
        for element in self._elements:
            element.remove()
        self._elements = []
    
    def update(self, dt): #pylint:disable-msg=C0103
        """
        Updates component elements, graphical and logical.
        """
        self.update_global_coords()
        
        for element in self._elements:
            element.update(dt)
        
        self._dirty = False
    
    def update_batch(self, batch, group):
        """
        Update the batch and group of the component.
        
        Auto-called when visibility changes.
        """
        self._batch, self._group = batch, group
        self._element_group = pyglet.graphics.OrderedGroup(1, group)
        for element in self._elements:
            element.update_batch((batch if self.visible else None), 
                                 self._element_group)
        self._dirty = True
    
    def update_global_coords(self):
        """Update global coordinates"""
        self._gx, self._gy = self.x, self.y #pylint:disable-msg=W0201
        if self.parent:
            self._gx += self.parent.gx
            self._gy += self.parent.gy
    
    def update_parent(self, parent):
        """
        Update the component's parent.
        
        Removes the component from its old parent, if it can.
        Adds the component to its new parent, if it can.
        """
        if self._parent:
            try:
                self._parent.remove_child(self)
            except AttributeError:
                #Old parent doesn't have a remove_child method
                pass
        self._parent = parent
        if self._parent:
            try:
                self._parent.add_child(self)
            except AttributeError:
                #New parent doesn't have an add_child method
                pass
        
    