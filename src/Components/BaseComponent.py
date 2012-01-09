"""
Base component, handles layering management, position, selection, etc.
"""

import Util
import Engine

print "BaseComponent Loaded."

class BaseComponent(object):
    '''
    Base Component from which all components (combo/check boxes, list selection boxes)
    are derived.
    '''
    
    #Initial values
    _Visible = False
    _Enabled = False
    
    _Parent = None
    _Children = []
    
    _HasFocus = False
    __IsContentLoaded = False
    
    _x = _y = 0
    _width = _height = 0
    _anchor_x = 'left'
    _anchor_y = 'top'
    
    _Name = "BaseComponent"
    _Tooltip = "Empty Tooltip"
    
    __triggers_redraw = ["x", "y", "width", "height",
                         "anchor_x", "anchor_y", "parent"]

    @Util.Wrappers.inject_args(['coords', 'id_manager'])
    def __init__(self, Parent=None, x=0, y=0, width=0, height=0, # pylint: disable-msg=C0103,W0613,C0301
                 anchor_x="left", anchor_y="top", coords="local", # pylint: disable-msg=C0103,W0613,C0301
                 Name="BaseComponent", Tooltip="Empty Tooltip", # pylint: disable-msg=C0103,W0613,C0301
                 Visible=True, Enabled=True, id_manager=None): # pylint: disable-msg=C0103,W0613,C0301
        '''
        Pass a screen as parent if this is DIRECTLY attached to the screen
        
        coords is either "global" or "local" referring to the value of x and y.
        EX. BaseComponent(None, 20, 20, "local", 10, 10) attached to a component
            with global x,y [50, 100] would have global coords [70, 120].
            Coordinates are stored in local, and transformed to global.
        '''
        
        if id_manager is None:
            id_manager = Engine.GLOBAL_ID_MANAGER
        self._id = id_manager.next_id(self)        
        self._tab_index = 0
        if Visible:
            #Make sure that content loads properly, since args may have been
                #injected out of order
            self._LoadContent()
        
    def __setattr__(self, name, value):
        if name in BaseComponent.__triggers_redraw:
            old_value = getattr(self, name)
            if old_value != value:
                self._Needs_Redraw = True
        super(BaseComponent, self).__setattr__(name, value)
    
    def __get_settings(self):
        if self.Screen is None:
            return None
        else:
            return self.Screen.Settings;
    def __get_screen(self):
        #No parent, no screen
        if self.Parent is None:
            return None
        #If parent is a component, use its screen
        if isinstance(self.Parent, BaseComponent):
            return self.Parent.Screen
        #Otherwise self._Parent IS the screen
        return self.Parent
    def __get_parent(self):
        """Returns the parent component.
            This is expecting an actual BaseComponent- 
            don't return true unless we 
            ACTUALLY have a Component for a parent."""
        if isinstance(self._Parent, BaseComponent):
            return self._Parent
        return None
    
    def __get_children(self):
        return self._Children[:]
    def __get_name(self):
        return self._Name
    def __get_id(self):
        return self._id
    def __get_visible(self):
        return self._Visible
    def __get_enabled(self):
        return self._Enabled
    def __get_has_focus(self):
        return self._HasFocus
    def __get_is_content_loaded(self):
        return self.__IsContentLoaded
    def __get_tab_index(self):
        return self._tab_index
    def __get_tooltip(self):
        return self._Tooltip
    
    def __get_x(self):
        return self._x
    def __get_y(self):
        return self._y
    def __get_width(self):
        return self._width
    def __get_height(self):
        return self._height
    def __get_anchor_x(self):
        return self._anchor_x
    def __get_anchor_y(self):
        return self._anchor_y
    
    def __set_parent(self, parent):
        if self.Parent is not None:
            self.Parent.remove_child(self)
        if parent is not None:
            parent.add_child(self)
        else:
            self.Visible = False
        self._Parent = parent
    def __set_name(self, value):
        self._Name = value    
    def __set_visible(self, value):
        self._Visible = value
        #Enabling Visible
            #only draw if not drawn
        if value and not self.IsContentLoaded:
            self._Needs_Redraw = True
        #Disabling Visible
            #only undraw if drawn
        if not value and self.IsContentLoaded:
            self._UnloadContent()
    def __set_enabled(self, value):
        self._Enabled = value
    def __set_tab_index(self, value):
        self._tab_index = value
    def __set_tooltip(self, value):
        self._Tooltip = value
    
    def __set_x(self, value):
        self._x = value
    def __set_y(self, value):
        self._y = value
    def __set_width(self, value):
        self._width = value
    def __set_height(self, value):
        self._height = value
    def __set_anchor_x(self, value):
        self._anchor_x = value.lower()
    def __set_anchor_y(self, value):
        self._anchor_y = value.lower()
    
    def _LoadContent(self):
        """Protected method for loading graphical content when Visible set to True (from False)"""
        self.__IsContentLoaded = True
        self._Needs_Redraw = False
    def _UnloadContent(self):
        """Protected method for unloading graphical content when Visible set to False (from True)"""
        self.__IsContentLoaded = False
        self._Needs_Redraw = False
    def _ReloadContent(self):
        """Protected method for reloading graphical content.  Called when x, y, width, height, anchor_x, anchor_y change."""
        self.__IsContentLoaded = True
        self._Needs_Redraw = False        

    Settings = property(__get_settings)
    Screen = property(__get_screen)
    Parent = property(__get_parent, __set_parent)
    Children = property(__get_children)
    Name = property(__get_name, __set_name)
    ID = property(__get_id)
    Visible = property(__get_visible, __set_visible)
    Enabled = property(__get_enabled, __set_enabled)
    HasFocus = property(__get_has_focus)
    IsContentLoaded = property(__get_is_content_loaded)
    Tab_Index = property(__get_tab_index, __set_tab_index)
    Tooltip = property(__get_tooltip, __set_tooltip)
    
    x = property(__get_x, __set_x)
    y = property(__get_y, __set_y)
    width = property(__get_width, __set_width)
    height = property(__get_height, __set_height)
    anchor_x = property(__get_anchor_x, __set_anchor_x)
    anchor_y = property(__get_anchor_y, __set_anchor_y)
    
    def add_child(self, child):
        """Adds the Component to Children, as long as the Component
            isn't already considered a child."""
        if not Util.contains(self._Children, child):
            self._Children.append(child)
            
    def contains(self, x, y): # pylint: disable-msg=C0103
        """Returns the Component that contains (x, y)- this allows parent
            Components to pass the contain check to their most appropriate
            child Component if they have one).
            Trys to return the most specific (child-first) container.
            Returns None if not containing the point x,y"""
        for child in self._Children:
            #Containing component
            ccomponent = child.contains(x, y)
            if ccomponent is not None:
                return ccomponent
        
        #Didn't contain the point in any child, check this Component
        minx = maxx = self.x
        miny = maxy = self.y
        
        if self.anchor_x == "left":
            maxx += self.width
        elif self.anchor_x == "center":
            minx -= 0.5 * self.width
            maxx += 0.5 * self.width
        elif self.anchor_x == "right":
            maxx += self.width
        
        if self.anchor_y == "top":
            miny -= self.height
        elif self.anchor_y == "center":
            miny -= 0.5 * self.height
            maxy += 0.5 * self.height
        elif self.anchor_y == "bottom":
            maxy += self.height
        
        #Within this Component
        if (minx < x < maxx) and (miny < y < maxy):
            return self
        
        #Not within this or any child Component
        return None 
    
    def exit_component(self):
        """Recursively exits the Component and all child Components.
            Exits components children-first so that they have reference
            to Screen while exiting."""
        
        #We pop because when child sets parent to none,
            #it calls parent.remove.
            #Popping safely removes it from the list0
            #otherwise we'd be doing list.remove during a list iteration
        while len(self._Children) > 0:
            child = self._Children.pop()
            child.exit_component()
            
        self._Needs_Redraw = False
        self.Enabled = False
        self.Visible = False
        self.Parent = None
        
    def handle_input(self, input_buffer):
        """Should pop each event in the input_buffer, look at it, and then
            either push it back on the input_buffer or not.  Any events "pushed back"
            are considered "unused" and will be seen by the next object to 
            inspect the input_buffer.  Pushed events are not available until the input_buffer
            is flipped again."""
        while input_buffer.HasEvents:
            input_buffer.Push(input_buffer.Pop())
        input_buffer.Flip()
    
    def remove_child(self, child):
        """Removes the Component from Children, as long as the Component
            is actually considered a child."""
        if Util.contains(self._Children, child):
            self._Children.remove(child)
    
    def update(self, dt):
        """Derived classes should call this method AFTER their implementation,
            so that changes made to critical values (x, y, etc) are reflected
            in the frame of their change.  Calling base before overriding
            method logic will effectively apply that logic to the NEXT update
            call, not THIS call."""
        if self._Needs_Redraw:
            self._ReloadContent()