"""
Base component, handles layering management, position, selection, etc.
"""

import Util
import Engine.ID

class BaseComponent(object):
    """
    Base Component from which all components (combo/check boxes, list selection boxes)
    are derived.
    """
    
    #Initial values
    _visible = False
    _enabled = False
    
    _parent = None
    _children = []
    
    _has_focus = False
    __is_content_loaded = False
    _needs_redraw = True
    
    _x = _y = 0
    _width = _height = 0
    _anchor_x = 'left'
    _anchor_y = 'top'
    
    _name = "BaseComponent"
    _tooltip = "Empty Tooltip"
    
    __triggers_redraw = ["x", "y", "width", "height",
                         "anchor_x", "anchor_y", "parent"]

    @Util.Wrappers.inject_args(['coords', 'id_manager','custom_id'])
    def __init__(self, Parent=None, x=0, y=0, width=0, height=0, #pylint:disable-msg=C0103,W0613,C0301
                 anchor_x="left", anchor_y="top", coords="local", #pylint:disable-msg=C0103,W0613,C0301
                 Name="BaseComponent", Tooltip="Empty Tooltip", #pylint:disable-msg=C0103,W0613,C0301
                 Visible=True, Enabled=True, custom_id=None): #pylint:disable-msg=C0103,W0613,C0301
        """
        Pass a screen as parent if this is DIRECTLY attached to the screen
        
        coords is either "global" or "local" referring to the value of x and y.
        EX. BaseComponent(None, 20, 20, "local", 10, 10) attached to a component
            with global x,y [50, 100] would have global coords [70, 120].
            Coordinates are stored in local, and transformed to global.
        """
        
        self.id = Engine.ID.get_id(self, custom_id = custom_id)
        
        self._tab_index = 0
        if Visible:
            #Make sure that content loads properly, since args may have been
                #injected out of order
            self._load_content()
        
    def __setattr__(self, name, value):
        if name in BaseComponent.__triggers_redraw:
            old_value = getattr(self, name)
            if old_value != value:
                self._needs_redraw = True
        super(BaseComponent, self).__setattr__(name, value)
    
    def __get_settings(self):
        """Settings from screen (or parent's screen)"""
        if self.Screen is None:
            return None
        else:
            return self.Screen.Settings
    def __get_screen(self):
        """The screen this component is attached to
            (recurses up through parents)"""
        #No parent, no screen
        if self.Parent is None:
            return None
        #If parent is a component, use its screen
        if isinstance(self.Parent, BaseComponent):
            return self.Parent.Screen
        #Otherwise self._parent IS the screen
        return self.Parent
    def __get_parent(self):
        """Returns the parent component.
            This is expecting an actual BaseComponent- 
            don't return true unless we 
            ACTUALLY have a Component for a parent."""
        if isinstance(self._parent, BaseComponent):
            return self._parent
        return None
    
    def __get_children(self):
        """Returns a COPY of list of children components"""
        return self._children[:]
    def __get_name(self):
        """Get the component's name"""
        return self._name
    def __get_visible(self):
        """Get the component's visibility state"""
        return self._visible
    def __get_enabled(self):
        """Get the component's enabled state"""
        return self._enabled
    def __get_has_focus(self):
        """Get the component's focus state"""
        return self._has_focus
    def __get_is_content_loaded(self):
        """Returns if the component's content has been loaded"""
        return self.__is_content_loaded
    def __get_tab_index(self):
        """Returns the index used for tab control,
            such as tabbing through fields in a form
            or shifting focus between two panes"""
        return self._tab_index
    def __get_tooltip(self):
        """Get the tooltip for the component"""
        return self._tooltip
    
    def __get_x(self):
        """Get x coordinate.  Not sure if local or global..."""
        return self._x
    def __get_y(self):
        """Get y coordinate.  Not sure if local or global..."""
        return self._y
    def __get_width(self):
        """Get the width of the component"""
        return self._width
    def __get_height(self):
        """Get the height of the component"""
        return self._height
    def __get_anchor_x(self):
        """Get the horizontal anchor of the component
            (where it attaches to parent or screen)"""
        return self._anchor_x
    def __get_anchor_y(self):
        """Get the vertical anchor of the component
            (where it attaches to parent or screen)"""
        return self._anchor_y
    
    def __set_parent(self, parent):
        """Set the component's parent.  Setting to None
            when the component has a parent will trigger a 
            remove_child on the current parent, then set to none.
            If the parent being added is not None, we tell the parent
            to add the child (this)
            If parent is set to none, the component is set to
            invisible."""
        if self.Parent is not None:
            self.Parent.remove_child(self)
        if parent is not None:
            parent.add_child(self)
        else:
            self.Visible = False #pylint:disable-msg=C0103
        self._parent = parent
    def __set_name(self, value):
        """Set the component's name"""
        self._name = value    
    def __set_visible(self, value):
        """Set the component's visibility state.
            Lazy redraw if flipping on,
            immediate unload if flipping off."""
        self._visible = value
        #Enabling Visible
            #only draw if not drawn
        if value and not self.IsContentLoaded:
            self._needs_redraw = True
        #Disabling Visible
            #only undraw if drawn
        if not value and self.IsContentLoaded:
            self._unload_content()
    def __set_enabled(self, value):
        """Set the component's enabled state"""
        self._enabled = value
    def __set_tab_index(self, value):
        """Set the component's tab index"""
        self._tab_index = value
    def __set_tooltip(self, value):
        """Set the tooltip for the component"""
        self._tooltip = value
    def __set_x(self, value):
        """Set x coordinate.  Not sure if local or global..."""
        self._x = value #pylint:disable-msg=C0103
    def __set_y(self, value):
        """Set y coordinate.  Not sure if local or global..."""
        self._y = value #pylint:disable-msg=C0103
    def __set_width(self, value):
        """Set the width of the component"""
        self._width = value
    def __set_height(self, value):
        """Set the height of the component"""
        self._height = value
    def __set_anchor_x(self, value):
        """Set the horizontal anchor of the component
            (where it attaches to parent or screen)"""
        self._anchor_x = value.lower()
    def __set_anchor_y(self, value):
        """Set the vertical anchor of the component
            (where it attaches to parent or screen)"""
        self._anchor_y = value.lower()
    
    def _load_content(self, recursive=True):
        """Protected method for loading graphical content when 
            Visible set to True (from False)
            If recursive, calls on child components"""
        if recursive:
            for child in self._children:
                child._load_content(recursive) #pylint:disable-msg=W0212
        self.__is_content_loaded = True
        self._needs_redraw = False
        
    def _unload_content(self, recursive=True):
        """Protected method for unloading graphical content
            when Visible set to False (from True)
            If recursive, calls on child components"""
        if recursive:
            for child in self._children:
                child._unload_content(recursive) #pylint:disable-msg=W0212
        self.__is_content_loaded = False
        self._needs_redraw = False
        
    def _reload_content(self, recursive=True):
        """Protected method for reloading graphical content.  
            Called when x, y, width, height, anchor_x, anchor_y change.
            If recursive, calls on child components"""
        if recursive:
            for child in self._children:
                child._reload_content(recursive) #pylint:disable-msg=W0212
        self.__is_content_loaded = True
        self._needs_redraw = False        

    Settings = property(__get_settings)
    Screen = property(__get_screen)
    Parent = property(__get_parent, __set_parent)
    Children = property(__get_children)
    Name = property(__get_name, __set_name)
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
        if not Util.contains(self._children, child):
            self._children.append(child)
            
    def contains(self, x, y): # pylint: disable-msg=C0103
        """Returns the Component that contains (x, y)- this allows parent
            Components to pass the contain check to their most appropriate
            child Component if they have one).
            Trys to return the most specific (child-first) container.
            Returns None if not containing the point x,y"""
        for child in self._children:
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
        while len(self._children) > 0:
            child = self._children.pop()
            child.exit_component()
            
        self._needs_redraw = False
        self.Enabled = False #pylint:disable-msg=C0103
        self.Visible = False #pylint:disable-msg=C0103
        self.Parent = None #pylint:disable-msg=C0103
        
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
        if Util.contains(self._children, child):
            self._children.remove(child)
    
    def update(self, dt): #pylint:disable-msg=C0103
        """Derived classes should call this method AFTER their implementation,
            so that changes made to critical values (x, y, etc) are reflected
            in the frame of their change.  Calling base before overriding
            method logic will effectively apply that logic to the NEXT update
            call, not THIS call."""
        for child in self._children:
            child.update(dt)
        if self._needs_redraw:
            self._reload_content()
        