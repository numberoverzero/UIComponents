"""
Quick drawable rectangles.
"""

import pyglet
import Util.Math
MKROT = Util.Math.mk_rot_fn

class Rectangle(object):
    """Displayable rectangle"""
    __triggers_recalc = ['x', 'y', 'w', 'h', 'r', 'c']
    __triggers_full_redraw = ['batch', 'group']

    __batching_updates = False
    __batch_or_group_changed = False
    auto_batch = True
    
    def __init__(self, x, y, w, h, r, c, batch, group): #pylint:disable-msg=C0103,C0301
        self.begin_batched_update()
            
        self.x = x #pylint:disable-msg=C0103
        self.y = y #pylint:disable-msg=C0103
        self.w = w #pylint:disable-msg=C0103
        self.h = h #pylint:disable-msg=C0103
        self.r = r #pylint:disable-msg=C0103
        self.c = c #pylint:disable-msg=C0103
        self.batch = batch
        self.group = group
        self.verts = None
        
    def begin_batched_update(self):
        """Useful when making many value changes in a short period of time.

            Batches changes together so that there is only one recalculation
            and push to the graphics card.

            Use end_batched_update to push changes.
        """
        self.__batching_updates = True

    def _clear_verts(self):
        """Clears verts if there are any."""
        if self.verts:
            self.verts.delete()
            self.verts = None
            
    def delete(self):
        """Delete the rectangle.

        All cleanup (including verts) is done here.
        """
        self._clear_verts()
        
    def end_batched_update(self):
        """Finish a batched update.  See begin_batched_update for details."""
        if self.__batch_or_group_changed:
            self._clear_verts()
            self.__batch_or_group_changed = False
        if self.__batching_updates:
            self._recalc_verts()
            self.__batching_updates = False

    def _recalc_verts(self):
        """Calculates vertices and passes that info to the gfx card"""
        #rot(o_x, o_y, p_x, p_y, theta)
        rot = MKROT(self.x, self.y, self.r)

        p0x, p0y = rot(self.x - self.w / 2.0, self.y - self.h / 2.0)
        p1x, p1y = rot(self.x + self.w / 2.0, self.y - self.h / 2.0)
        p2x, p2y = rot(self.x + self.w / 2.0, self.y + self.h / 2.0)
        p3x, p3y = rot(self.x - self.w / 2.0, self.y + self.h / 2.0)
        
        self.verts = self.batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, self.group, #pylint:disable-msg=C0301
                                            [0, 1, 2, 0, 2, 3],
                                            ('v2f', (p0x, p0y,
                                                     p1x, p1y,
                                                     p2x, p2y,
                                                     p3x, p3y)),
                                            ('c4B', self.c * 4),
                                            )

    def __setattr__(self, name, value):
        super(Rectangle, self).__setattr__(name, value)
        if self.__batching_updates:
            if name in Rectangle.__triggers_full_redraw:
                self.__batch_or_group_changed = True
            elif name == "auto_batch" and not value:
                #Turn auto_batch off
                self.end_batched_update()
        else:
            if name in Rectangle.__triggers_full_redraw:
                self._clear_verts()
                self._recalc_verts()
            elif name in Rectangle.__triggers_recalc:
                self._recalc_verts()
            elif name == "auto_batch" and value:
                #Turn auto_batch on
                self.begin_batched_update()
                
    def update(self):
        """If auto batching updates, applys the updates.

            Otherwise, does nothing.
        """
        if self.auto_batch:
            self.end_batched_update()
            self.begin_batched_update()
        
