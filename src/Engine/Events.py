"""
Describes EventArgs and EventHandlers
"""

import Engine
import Util

class EventArgs(object): #pylint: disable-msg=R0903
    """Base class for arguments of an event."""
    def __init__(self):
        self._ID = Engine.ID_Manager.next_id(self) # pylint: disable-msg=C0103
    def __eq__(self, other):
        if not isinstance(other, EventArgs):
            return False
        return self.ID == other.ID
    def __get_id(self): # pylint: disable-msg=C0103
        """Returns the event's id"""
        return self._ID
    def __str__(self):
        return self._str()
    def _str(self): # pylint: disable-msg=C0103
        """Inheritable and overrideable __str__"""
        return "EventArgs(ID={id})".format(str(self.ID))
    
    ID = property(__get_id, None, None, "Unique ID to reference the EventArgs")

#Allows handlers to be invoked without arguments
#Also allows us to check against ComUtil.NoneArgs instead of using isinstance()
NONEARGS = EventArgs()

class EventHandler(object): #pylint: disable-msg=R0903
    """Takes events and dispatches them to its listeners."""
    def __init__(self):
        self.listeners = []
        
    def __iadd__(self, listener):
        if not Util.contains(self.listeners, listener):
            self.listeners.append(listener)
    
    def __isub__(self, listener):
        if Util.contains(self.listeners, listener):
            self.listeners.remove(listener)
    
    def __call__(self, sender, event_args = NONEARGS):
        for listener in self.listeners:
            listener(sender, event_args)
    
    def __del__(self):
        self.listeners = None