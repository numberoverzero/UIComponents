'''
A text label
'''

import pyglet.text
import Component
import Util

class Label(Component.Component):
    """A text label with multiple formatting options.
    
    If no parent is provided, coordinates are global.
    Otherwise, coords are offsets to parent x,y
    """
    
    _triggers_redraw = ['text', 'font_name', 'font_size', 'bold',
                        'italic', 'font_color', 'background_color',
                        'halign', 'multiline', 'dpi']
    
    @Util.Wrappers.inject_args(['X', 'Y', 'Width', 'Height', 'anchor_x',
                                'anchor_y', 'Parent', 'Tooltip', 'Visible',
                                'Enabled', 'custom_id'])
    def __init__(self, Text='', font_name=None, font_size=None, bold=False,
                 italic=False, font_color=(255, 255, 255, 255), 
                 background_color=(255, 255, 255, 255), X=0, Y=0,
                 Width=None, Height=None, anchor_x='left', anchor_y='baseline',
                 halign='left', multiline=False, dpi=None, Parent=None, 
                 Tooltip="My Label", Visible=True, Enabled=True, 
                 custom_id=None):
        """See pyglet.text.Label docs for info on options.
            
            Does not render without a Parent- even if Visible is True.
            Background colors are not supported yet.
        """
        
        #Load iff we have a parent
        Visible = Visible and Parent
        
        super(Label, self).__init__(Parent=Parent, X=X, Y=Y, Width=Width,
                                    Height=Height,anchor_x=anchor_x,
                                    anchor_y=anchor_y, coords="local",
                                    Name="LabelComponent",Tooltip=Tooltip,
                                    Visible=Visible,Enabled=Enabled,
                                    custom_id=custom_id)
        
        self._triggers_redraw.extend(Label._triggers_redraw)
        
    def _load_content(self, recursive=True):
        Component.Component._load_content(self, recursive=recursive)
        
        #Load text and background here
        self._label = pyglet.text.Label(text, font_name, font_size, bold, italic, color, x, y, width, height, anchor_x, anchor_y, halign, multiline, dpi, batch, group)

    def _reload_content(self, recursive=True):
        Component.Component._reload_content(self, recursive=recursive)
        
        self._label.begin_update()
        #Reload text and background here
        self._label.end_update()
        
    
    