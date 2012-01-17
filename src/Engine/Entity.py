""""
Standard game entity.
"""
import Collision.Shapes
import ID

class Entity(object):
    """
    Standard game entity.
    Add a collider with add_collider(collider).
    Colliders will always try to keep their center equal to the 
    entity's center.
    """
    def __init__(self, **kwargs):
        self._x, self._y = kwargs.get('x', 0), kwargs.get('y', 0) #pylint:disable-msg=C0103,C0301
        self._timescale = 1.0
        self._collider = None
        self._last_dmg_src = None
        self._id = ID.get_id(self)
        self._dirty = False
        self._dt = 0.0
    
    def _get_timescale(self):
        """
        Returns the entity's timescale.
        
        The entity's update method will multiply dt by its timescale before
        other effects are considered.  See update's doc for more information
        on timescale, etc.
        """
        return self._timescale
    def _set_timescale(self, value):
        """Set the entity's timescale to value.  Can be negative."""
        self._timescale = value
    timescale = property(_get_timescale, _set_timescale)
    
    def damage(self, source, amount): #pylint:disable-msg=W0613
        """
        Attempt to apply `amount` damage to the entity from `source`.
        
        Returns the amount of damage that was applied.  
        Can return negative numbers.
        
        If the source damages the entity, use self._last_dmg_src = source
        so that the damage dealer can be notified on state changes.
        """
        return 0
    
    def destroy(self, source=None, as_cleanup=True): #pylint:disable-msg=W0613
        """
        Destroy the entity.
        
        optional args:
        `source`: The entity that is destroying this entity.
                    default is None
        `as_cleanup`: The entity is being destroyed as part of a cleanup step,
                    and authored animations or triggered events 
                    should be suppressed so that the destroy is as close to instant
                    as possible.  Ideally, the entity is cleaned up before it can
                    influence the next frame of game logic.
                    default is True
        """
        
        self._collider = None
        self._dirty = False
                    
    def get_center(self):
        """
        Return the center (or an approximation thereof) of the entity
        """
        return Collision.Shapes.Point(self._x, self._y)
    
    def update(self, dt): #pylint:disable-msg=C0103,W0613
        """
        Update the entity.
        
        dt is the time since the last update call,
        post global-timescale modifiers.
        """
        self._dt = dt * self.timescale #pylint:disable-msg=C0103,
        self._pre_update()
        self._update()
        self._post_update()
        
    def _pre_update(self):
        """
        Pre-update logic should be performed here.
        
        Any logic performed here should keep in mind that the entity's values
        are all (relative to some/most other entities) one frame behind.
        
        ONLY `self._dt` IS CURRENT TO THIS FRAME
        
        This is a 'last chance' of sorts to run any code that could
        also have been run in last frame's _post_update.
        """
        pass  
    
    def _update(self): #pylint:disable-msg=C0103
        """
        Update the entity.
        
        global/local timescale adjustments have already been applied to
        this frame's dt, and the correct dt is at `self._dt`.
        
        Logic which moves the entity into this frame should occur here.
        
        Take care of last-minute changes (before the frame) in _pre_update. 
        Take care of cleanup in _post_update.
        """
        pass
    
    def _post_update(self):
        """
        Called after the main update method.
        
        Any methods which require the very latest information about the entity
        should be taken care of here.  These methods should NOT make significant
        changes to any of the entity's core information.
            (Special exception is made for a cleanup destroy call if needed)
        As an example, collision updating is taken care of here, as the entity's
        position shouldn't change until the next frame. 
        
        Any frame-based flags should be cleared here (such as _dirty).
        """
        self._update_collider()
        self._dirty = False
    
    def _update_collider(self):
        """
        Update the collider, if any, associated with this entity.
        """
        if self._collider:
            center = self.get_center()
            self._collider.center_at(center.x, center.y)