"""
Component that contains other components.
"""

import pyglet
from Component import Component

class Container(Component):
    """
    A component that contains other components.
    """
    def __init__(self, **kwargs):
        Component.__init__(self, **kwargs)
        self._children = []
        
    def add_child(self, child):
        """
        Add a child component to the component's children.
        
        A component's parent should fully contain it for proper hit testing.
        """
        
        self._children.append(child)
        self.update_batch(self._batch, self._group)
    
    def remove(self):
        Component.remove(self)
        for child in self._children:
            child.remove()
        self._children = []
    
    def remove_and_preserve_children(self):
        """
        Remove the component, but preserve children.
        
        Children are appended to parent, if parent can take them.
        If parent takes children, children keep their _global_
        position, which may require changing their local offsets.
        """
        
        if self.parent and hasattr(self.parent, 'add_child)'):
            for child in self._children:
                #Correct offsets
                child.x += self.x
                child.y += self.y
                self.parent.add_child(child)
        self._children = []
        self.remove()
    
    def remove_child(self, child):
        """Remove a child from this container's list of children"""
        try:
            self._children.remove(child)
        except ValueError:
            #Don't care if it's not in the list
            pass
        
    
    def update(self, dt): #pylint:disable-msg=C0103
        Component.update(self, dt)
        for child in self._children:
            child.update(dt)
    
    def update_batch(self, batch, group):
        Component.update_batch(self, batch, group)
        
        child_group = pyglet.graphics.OrderedGroup(0, group)
        
        for child in self._children:
            #Pass children the lower of the layers
            child.update_batch((batch if self.visible else None), child_group)
            
    def update_global_coords(self):
        Component.update_global_coords(self)
        for child in self._children:
            child.update_global_coords()