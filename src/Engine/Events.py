"""
Describes EventArgs and EventHandlers
"""

import Engine
import Util

class EventArgs(object):
    """Base class for arguments of an event.
        Default id_manager is Engine.Global_Id_Manager
        Using custom ids can break equality checks and the like."""
    def __init__(self, id_manager = None, custom_id = None):
        if custom_id is not None:
            self._id = custom_id
            self.__id_manager = None
        else:
            if not isinstance(id_manager, Engine.id_manager):
                id_manager = Engine.GLOBAL_ID_MANAGER
            self.__id_manager = id_manager
            self._id = self.__id_manager.next_id(self)
    def __eq__(self, other):
        if not isinstance(other, EventArgs):
            return False
        return self.ID == other.ID
    def __get_id(self):
        """Returns the event's id"""
        return self._id
    def __str__(self):
        return self._str()
    def _str(self):
        """Inheritable and overrideable __str__"""
        return "EventArgs(ID={}, id_manager={})".format(
            str(self.ID), str(self.__id_manager))
    
    ID = property(__get_id, None, None, "Unique ID to reference the EventArgs")

#Allows handlers to be invoked without arguments
#Also allows us to check against Engine.NoneArgs instead of using isinstance()
NONEARGS = EventArgs(custom_id = -1)

class EventHandler(object):
    """Takes events and dispatches them to its listeners."""
    def __init__(self):
        self._listeners = []
    
    def add_listener(self, listener):
        """Adds the listener to those pushed on invocation."""
        if not Util.contains(self._listeners, listener):
            self._listeners.append(listener)                
    
    def __iadd__(self, listener):
        """Add a listener"""
        self.add_listener(listener)
        
    def remove_listener(self, listener):
        """Removes the listener from those pushed on invocation."""
        if Util.contains(self._listeners, listener):
            self._listeners.remove(listener)
            
    def __isub__(self, listener):
        """Remove a listener"""
        self.remove_listener(listener)
    
    def invoke(self, sender, event_args = NONEARGS):
        """Invoke the handler with sender and args information.
            Default args are NONEARGS."""
        dead_listeners = []
        for listener in self._listeners:
            if listener is not None:
                listener(sender, event_args)
            else:
                dead_listeners.append(listener)
        for listener in dead_listeners:
            self.remove_listener(listener)
        dead_listeners = None
    
    def __call__(self, sender, event_args = NONEARGS):
        """Invoke the EventHandler.  If no event_args are passed,
            passes NONEARGS."""
        self.invoke(sender, event_args)
    
    def __del__(self):
        self._listeners = None
    
    def __get_listeners(self):
        """Return a copy of the listeners"""
        return self._listeners[:]
    
    Listeners = property(__get_listeners, None, None, 
                         "Copy of the handler's listeners")