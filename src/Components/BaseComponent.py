'''
Created on Dec 8, 2011

@author: Joe Laptop
'''
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

    @Util.Wrappers.InjectArgs(['coords'])
    def __init__(self, Parent=None, x=0, y=0, width=0, height=0,
                 anchor_x="left", anchor_y="top", coords="local",
                 Name="BaseComponent", Tooltip="Empty Tooltip",
                 Visible = True, Enabled = True):
        '''
        Pass a screen as parent if this is DIRECTLY attached to the screen
        
        coords is either "global" or "local" referring to the value of x and y.
        EX. BaseComponent(None, 20, 20, "local", 10, 10) attached to a component
            with global x,y [50, 100] would have global coords [70, 120].
            Coordinates are stored in local, and transformed to global.
        '''
        
        self._ID = Engine.ID_Manager.NextID(self)        
        self._TabIndex = 0
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
        #This is expecting an actual BaseComponent- don't return true unless we
            #ACTUALLY have a Component for a parent.
        if isinstance(self._Parent, BaseComponent):
            return self._Parent
        return None
    def __get_children(self):
        return self._Children[:]
    def __get_name(self):
        return self._Name
    def __get_id(self):
        return self._ID
    def __get_visible(self):
        return self._Visible
    def __get_enabled(self):
        return self._Enabled
    def __get_has_focus(self):
        return self._HasFocus
    def __get_is_content_loaded(self):
        return self.__IsContentLoaded
    def __get_tab_index(self):
        return self._TabIndex
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
            self.Parent.RemoveChild(self)
        if parent is not None:
            parent.AddChild(self)
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
        self._TabIndex = value
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

    Settings = property(__get_settings, None, None, "The Settings inherited from Screen")
    Screen = property(__get_screen, None, None, "The screen which this is contained in")
    Parent = property(__get_parent, __set_parent, None, "The Component this is contained in")
    Children = property(__get_children, None, None, "Copy of the Component's child Components")
    Name = property(__get_name, __set_name, None, "Sting used to describe the Component")
    ID = property(__get_id, None, None, "Unique ID to reference the Component")
    Visible = property(__get_visible, __set_visible, None, "If the Component is drawn")
    Enabled = property(__get_enabled, __set_enabled, None, "If the Component is Enabled")
    HasFocus = property(__get_has_focus, None, None, "If the Component has key focus (tab, enter)")
    IsContentLoaded = property(__get_is_content_loaded, None, None, 
                               "If the Component has loaded necessary drawing content")
    TabIndex = property(__get_tab_index, __set_tab_index, None, "The index for tabbing through Components")
    Tooltip = property(__get_tooltip, __set_tooltip, None, "Component tooltip for hover")
    
    x = property(__get_x, __set_x, None, "Global x position")
    y = property(__get_y, __set_y, None, "Global y position")
    width = property(__get_width, __set_width, None, "Width of the Component")
    height = property(__get_height, __set_height, None, "Height of the Component")
    anchor_x = property(__get_anchor_x, __set_anchor_x, None, "Where the Component is connected to its x value. [left, center, right]")
    anchor_y = property(__get_anchor_y, __set_anchor_y, None, "Where the Component is connected to its y value. [top, center, bottom]")
    
    def AddChild(self, child):
        """Adds the Component to Children, as long as the Component
            isn't already considered a child."""
        if not Util.contains(self._Children, child):
            self._Children.append(child)
            
    def Contains(self, x, y):
        """Returns the Component that contains (x, y)- this allows parent
            Components to pass the contain check to their most appropriate
            child Component if they have one)."""
        for child in self._Children:
            #Containing component
            ccomponent = child.Contains(x, y)
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
    
    def ExitComponent(self):
        """Recursively exits the Component and all child Components.
            Exits components children-first so that they have reference
            to Screen while exiting."""
        
        #We pop because when child sets parent to none,
            #it calls parent.remove.
            #Popping safely removes it from the list0
            #otherwise we'd be doing list.remove during a list iteration
        while len(self._Children) > 0:
            child = self._Children.pop()
            child.ExitComponent()
            
        self._Needs_Redraw = False
        self.Enabled = False
        self.Visible = False
        self.Parent = None
        
    def HandleInput(self, InputBuffer):
        """Should pop each event in the InputBuffer, look at it, and then
            either push it back on the InputBuffer or not.  Any events "pushed back"
            are considered "unused" and will be seen by the next object to 
            inspect the InputBuffer.  Pushed events are not available until the InputBuffer
            is flipped again."""
        while InputBuffer.HasEvents:
            InputBuffer.Push(InputBuffer.Pop())
        InputBuffer.Flip()
    
    def RemoveChild(self, child):
        """Removes the Component from Children, as long as the Component
            is actually considered a child."""
        if Util.contains(self._Children, child):
            self._Children.remove(child)
    
    def Update(self, dt):
        """Derived classes should call this method AFTER their implementation,
            so that changes made to critical values (x, y, etc) are reflected in
            the frame of their change.  Calling base before overriding method logic
            will effectively apply that logic to the NEXT update call, not THIS call."""
        if self._Needs_Redraw:
            self._ReloadContent()
    
    
    
    
        
        
