"""
Describes EventArgs and EventHandlers
"""

import ID

class EventArgs(object):
    """Base class for arguments of an event."""
    def __init__(self, custom_id = None):
        self.eid = ID.get_id(self, custom_id = custom_id)
    
    def __eq__(self, other):
        try:
            return self.eid == other.eid
        except AttributeError:
            return False
    
    def __str__(self):
        return "EventArgs(ID={})".format(self.eid)
        
NONEARGS = EventArgs(custom_id = -1)

class EventHandler(object):
    """Takes events and dispatches them to its listeners."""
    def __init__(self, custom_id=None):
        self.id = ID.get_id(self, custom_id = custom_id) #pylint:disable-msg=C0103,C0301
        self._listeners = []
    
    def add_listener(self, listener_or_iter):
        """Adds the listener to those pushed on invocation.
            Can add iterable structures of listeners.  Uses recursion."""
        if hasattr(listener_or_iter, '__iter__'):
            for listener in listener_or_iter:
                self.add_listener(listener)
        else:
            if not listener_or_iter in self._listeners:
                self._listeners.append(listener_or_iter)                
    
    def __call__(self, sender, event_args=NONEARGS):
        """Invoke the EventHandler.  If no event_args are passed,
            passes NONEARGS."""
        self.invoke(sender, event_args)
    
    def __eq__(self, other):
        try:
            id_eq = self.id == other.id
            list_eq = self.Listeners == other.Listeners
            return id_eq and list_eq
        except AttributeError:
            return False
        
    def __iadd__(self, listener_or_iter):
        """Add a listener"""
        self.add_listener(listener_or_iter)
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
    
    def __isub__(self, listener):
        """Remove a listener"""
        self.remove_listener(listener)
        return self
    
    def __get_listeners(self):
        """Return a copy of the listeners"""
        return self._listeners[:]
    Listeners = property(__get_listeners)
    
    def remove_listener(self, listener):
        """Removes the listener from those pushed on invocation."""
        if listener in self._listeners:
            self._listeners.remove(listener)
