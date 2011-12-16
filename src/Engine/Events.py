class EventArgs(object):
    def __init__(self):
        self._ID = ID_Manager.NextID(self)
    def __eq__(self, other):
        if not isinstance(other, EventArgs):
            return False
        return self.ID == other.ID
    def __get_id(self):
        return self._ID
    def __str__(self):
        return self._str()
    def _str(self):
        return "EventArgs(ID={id})".format(str(self.ID))
    
    ID = property(__get_id, None, None, "Unique ID to reference the EventArgs")

#Allows handlers to be invoked without arguments
    #Also allows us to check against ComUtil.NoneArgs instead of using isinstance()
NoneArgs = EventArgs()

class EventHandler(object):
    def __init__(self):
        self.listeners = []
        
    def __iadd__(self, listener):
        if not contains(self.listeners, listener):
            self.listeners.append(listener)
    
    def __isub__(self, listener):
        if contains(self.listeners, listener):
            self.listeners.remove(listener)
    
    def __call__(self, sender, eventArgs = NoneArgs):
        for listener in self.listeners:
            listener(sender, args)
    
    def __del__(self):
        self.listeners = None