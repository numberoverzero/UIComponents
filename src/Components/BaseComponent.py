'''
Created on Dec 8, 2011

@author: Joe Laptop
'''
import ComUtil

class BaseComponent(object):
    '''
    Base Component from which all components (combo/check boxes, list selection boxes)
    are derived.
    '''


    def __init__(self, parent=None, x=0, y=0, width=0, height=0,
                 anchor_x="left", anchor_y="top", coords="local"):
        '''
        Pass a screen as parent if this is DIRECTLY attached to the screen
        
        coords is either "global" or "local" referring to the value of x and y.
        EX. BaseComponent(None, 20, 20, "local", 10, 10) attached to a component
            with global x,y [50, 100] would have global coords [70, 120].
            Coordinates are stored in local, and transformed to global.
        '''
        
        #Either a Component or a Screen
        self._Parent = parent
        
        #Components contained in this Component
        self._Children = []
        
        self._Name = "BaseComponent"
        self._ID = ComUtil._get_next_id()
        
        self.__IsContentLoaded = False
        self._Visible = False
        self._Enabled = True
        self._HasFocus = False
        
        self._TabIndex = 0
        self._Tooltip = "Empty Tooltip"
        
        self._position(x, y, width, height, anchor_x, anchor_y)

    def get_screen(self):
        #No parent, no screen
        if self.Parent is None:
            return None
        #If parent is a component, use its screen
        if isinstance(self.Parent, BaseComponent):
            return self.Parent.Screen
        #Otherwise self._Parent IS the screen
        return self.Parent
    def get_parent(self):
        #This is expecting an actual BaseComponent- don't return true unless we
            #ACTUALLY have a Component for a parent.
        if isinstance(self._Parent, BaseComponent):
            return self._Parent
        return None
    def get_children(self):
        return self._Children[:]
    
    def get_name(self):
        return self._Name
    def get_id(self):
        return self._ID
    
    def get_visible(self):
        return self._Visible
    def get_enabled(self):
        return self._Enabled
    
    def get_has_focus(self):
        return self._HasFocus
    def get_is_content_loaded(self):
        return self.__IsContentLoaded
    def get_tab_index(self):
        return self._TabIndex
    def get_tooltip(self):
        return self._Tooltip

    def set_name(self, value):
        self._Name = value    
    def set_visible(self, value):
        self._Visible = value
        #Enabling Visible
            #only draw if not drawn
        if value and not self.IsContentLoaded:
            self._LoadContent()
        #Disabling Visible
            #only undraw if drawn
        if not value and self.IsContentLoaded:
            self._UnloadContent()        
    def set_enabled(self, value):
        self._Enabled = value
    def set_tab_index(self, value):
        self._TabIndex = value
    def set_tooltip(self, value):
        self._Tooltip = value
    
    
    def _LoadContent(self):
        """Protected method for loading graphical content when Visible set to True (from False)"""
        self.__IsContentLoaded = True
    def _UnloadContent(self):
        """Protected method for unloading graphical content when Visible set to False (from True)"""
        self.__IsContentLoaded = False        

    Screen = property(get_screen, None, None, "The screen which this is contained in")
    Parent = property(get_parent, None, None, "The Component this is contained in")
    Children = property(get_children, None, None, "Copy of the Component's child Components")
    Name = property(get_name, set_name, None, "Sting used to describe the Component")
    ID = property(get_id, None, None, "Unique ID to reference the Component")
    Visible = property(get_visible, set_visible, None, "If the Component is drawn")
    Enabled = property(get_enabled, set_enabled, None, "If the Component is Enabled")
    HasFocus = property(get_has_focus, None, None, "If the Component has key focus (tab, enter)")
    IsContentLoaded = property(get_is_content_loaded, None, None, 
                               "If the Component has loaded necessary drawing content")
    TabIndex = property(get_tab_index, set_tab_index, None, "The index for tabbing through Components")
    Tooltip = property(get_tooltip, set_tooltip, None, "Component tooltip for hover")
        
        
        