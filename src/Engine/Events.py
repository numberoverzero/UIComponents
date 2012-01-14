"""
Describes EventArgs and EventHandlers
"""

import Engine
import Util

class EventArgs(Engine.HasID):
    """Base class for arguments of an event.
        Default id_manager is Engine.Global_Id_Manager
        Using custom ids can break equality checks and the like."""
    def __init__(self, id_manager=None, custom_id=None):
        Engine.HasID.__init__(self, id_manager, custom_id)
    def __eq__(self, other):
        try:
            return Engine.HasID.__eq__(self, other)
        except AttributeError:
            return False
    def __str__(self):
        return self._str()
    def _str(self):
        """Inheritable and overrideable __str__"""
        return "EventArgs(ID={}, id_manager={})".format(
            str(self.ID), str(self.__id_manager))

NONEARGS = EventArgs(custom_id= -1)

class EventHandler(Engine.HasID):
    """Takes events and dispatches them to its listeners."""
    def __init__(self, id_manager=None, custom_id=None):
        Engine.HasID.__init__(self, id_manager, custom_id)
        self._listeners = []
    
    def add_listener(self, listener_or_iter):
        """Adds the listener to those pushed on invocation.
            Can add iterable structures of listeners.  Uses recursion."""
        if hasattr(listener_or_iter, '__iter__'):
            for listener in listener_or_iter:
                self.add_listener(listener)
        else:
            if not Util.contains(self._listeners, listener_or_iter):
                self._listeners.append(listener_or_iter)                
    
    def __iadd__(self, listener_or_iter):
        """Add a listener"""
        self.add_listener(listener_or_iter)
        return self
        
    def remove_listener(self, listener):
        """Removes the listener from those pushed on invocation."""
        if Util.contains(self._listeners, listener):
            self._listeners.remove(listener)
            
    def __isub__(self, listener):
        """Remove a listener"""
        self.remove_listener(listener)
        return self
    
    def invoke(self, sender=None, event_args=NONEARGS):
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
    
    def __call__(self, sender, event_args=NONEARGS):
        """Invoke the EventHandler.  If no event_args are passed,
            passes NONEARGS."""
        self.invoke(sender, event_args)
    
    def __get_listeners(self):
        """Return a copy of the listeners"""
        return self._listeners[:]
    
    def __eq__(self, other):
        try:
            id_eq = Engine.HasID.__eq__(self, other)
            #This may be a slow comparison as it requires two copies
            list_eq = self.Listeners == other.Listeners
            return id_eq and list_eq
        except AttributeError:
            return False
    Listeners = property(__get_listeners, None, None,
                         "Copy of the handler's listeners")