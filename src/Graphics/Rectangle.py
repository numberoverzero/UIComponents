"""
Quick drawable rectangles.
"""

import pyglet
import Util.Math
MKROT = Util.Math.mk_rot_fn

class Rectangle(object):
    """Displayable rectangle"""
    
    __slots__ = ['x', 'y', 'w', 'h', 'r', 'c',
                 'batch', 'group', 'verts',
                 '__batching_updates',
                 '_dirty', 'auto_batch',
                 ]
    
    __trig_vert_recalc = ['x', 'y', 'w', 'h', 'r']
    __trig_color_recalc = ['c']
    
    def __init__(self, x, y, w, h, r, c, batch, group): #pylint:disable-msg=C0103,C0301
        self.__batching_updates = False
        self._dirty = [False, False]
        self.auto_batch = True
    
        self.begin_batched_update()
            
        self.x = x #pylint:disable-msg=C0103
        self.y = y #pylint:disable-msg=C0103
        self.w = w #pylint:disable-msg=C0103
        self.h = h #pylint:disable-msg=C0103
        self.r = r #pylint:disable-msg=C0103
        self.c = c #pylint:disable-msg=C0103
        self._batch = batch
        self._group = group
        self.verts = None
    
    def _get_batch(self):
        """The rectangle's vertex batch"""
        return self._batch
    batch = property(_get_batch)
    
    def _get_group(self):
        """The rectangle's vertex group"""
        return self._group
    group = property(_get_group)
      
    def begin_batched_update(self):
        """Useful when making many value changes in a short period of time.

            Batches changes together so that there is only one** recalculation
            and push to the graphics card.

            Use end_batched_update to push changes.
            
            **Two changes in the case of vert and color changes
        """
        self.__batching_updates = True
            
    def delete(self):
        """Delete the rectangle.

        All cleanup (including verts) is done here.
        """
        self._clear_verts()
        
    def end_batched_update(self):
        """Finish a batched update.  See begin_batched_update for details."""
        if self.__batching_updates:
            self._recalc_verts()
            self.__batching_updates = False
    
    def update(self, dt): #pylint:disable-msg=C0103,W0613
        """
        Update the rectangle.
        
        dt is the elapsed time since the last update
        """
            
        if self.auto_batch:
            self.end_batched_update()
            self.begin_batched_update()
    
    def update_batch(self, batch, group):
        """Update batch and group"""
        if self._batch != batch or self._group != group:
            self._clear_verts()
        self._batch, self._group = batch, group
        
    def _clear_verts(self):
        """Clears verts if there are any."""
        if self.verts:
            self.verts.delete()
            self.verts = None
        self._dirty = [False, False]
        
    def _full_redraw(self):
        """Forced vertex clear and recalc"""
        self._clear_verts()
        self._recalc_verts()
        
    def _recalc_verts(self):
        """
        Calculates vertices and passes that info to the gfx card
        
        If self.verts is None, does a full recalc
        If self._dirty[0], recalcs vert position
        If self._dirty[1], recalcs vert colors
        """
        rot = MKROT(self.x, self.y, self.r)
        if self._dirty[0] or not self.verts:
            p0x, p0y = rot(self.x - self.w / 2.0, self.y - self.h / 2.0)
            p1x, p1y = rot(self.x + self.w / 2.0, self.y - self.h / 2.0)
            p2x, p2y = rot(self.x + self.w / 2.0, self.y + self.h / 2.0)
            p3x, p3y = rot(self.x - self.w / 2.0, self.y + self.h / 2.0)
        if not self.verts:
            self.verts = self._batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, 
                                                self._group,
                                                [0, 1, 2, 0, 2, 3],
                                                ('v2f', (p0x, p0y,
                                                         p1x, p1y,
                                                         p2x, p2y,
                                                         p3x, p3y)),
                                                ('c4B', self.c * 4),
                                                )
        else:
            if self._dirty[0]:
                self.verts.vertices = (p0x, p0y, p1x, p1y, p2x, p2y, p3x, p3y)
            if self._dirty[1]:
                self.verts.colors = self.c[:] * 4
        self._dirty = [False, False]

    def __setattr__(self, name, value):
        changed = getattr(self, name) != value
        super(Rectangle, self).__setattr__(name, value)
        
        if not changed:
            return
        
        if name in Rectangle.__trig_vert_recalc:
            self._dirty[0] = True
        elif name in Rectangle.__trig_color_recalc:
            self._dirty[1] = True
        
        elif name == "auto_batch":
            if value and not self.__batching_updates:
                #Setting auto from off state
                self.begin_batched_update()
            elif self.__batching_updates and not value:
                #Turning auto off from on state
                self.end_batched_update()
            
            # If we were toggling auto_batch, we DO NOT
            # want to trigger another recalc below
            return
        
        #Apply changes immediately if we're not batching
        if not self.__batching_updates:
            self._recalc_verts()
                