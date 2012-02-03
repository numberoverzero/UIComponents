"""
Useful structures such as double buffers and typechecked lists
"""



def enum(*sequential, **named):
    """Creates a classic enumerable.  For details,
            see http://stackoverflow.com/q/1695250""" 
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
    
class DoubleBuffer(object):
    """A double buffered object.
        Can be cleared and flipped a few ways, read the docstring
        for details on what each mode does."""
        
    def __init__(self):
        self.__bbuffer = []
        self.__fbuffer = []
            
    def clear(self, front=True, back=False):
        """Clears the front or back buffer, or both."""
        if front:
            self.__fbuffer = []
        if back:
            self.__bbuffer = []
            
    def flip(self, mode='exact'):
        """Mode is one of:
            exact: any values in either buffer are preserved, and the front
                        and back are simply flipped.
                    
                        --- PRESERVES ORDER, PRESERVES VALUES ---
                        EXAMPLE:
                            #Before flip:
                            front = [1,2,3,4]
                            back = [5,6,7,8]
                            
                            self.flip(mode = 'exact')
                            
                            #After flip:
                            self.front = [5,6,7,8]
                            self.back = [1,2,3,4]
                            
            transfer: any values still in front buffer stay, and the values in 
                        back buffer are pushed onto the front buffer.
                        
                        --- PRESERVES ORDER, PRESERVES VALUES ---
                        EXAMPLE:
                            #Before flip:
                            front = [1,2,3,4]
                            back = [5,6,7,8]
                            
                            self.flip(mode = 'transfer')
                            
                            #After flip:
                            self.front = [1,2,3,4,5,6,7,8]
                            self.back = []
            
            discard: any values still in front buffer are thrown away, 
                        then buffers are flipped.
                        
                        --- PRESERVES ORDER, DROPS FRONT VALUES---
                        EXAMPLE:
                            #Before flip:
                            front = [1,2,3,4]
                            back = [5,6,7,8]
                            
                            self.flip(mode = 'discard')
                            
                            #After flip:
                            self.front = [5,6,7,8]
                            self.back = []
            
            transfer_front: same as transfer, but values are reversed- 
                        back get popped before "old" front values.
                        
                        --- REVERSES BUFFER ORDER, PRESERVES VALUES ---
                        EXAMPLE:
                            #Before flip:
                            front = [1,2,3,4]
                            back = [5,6,7,8]
                            
                            self.flip(mode = 'transfer_front')
                            
                            #After flip:
                            self.front = [5,6,7,8,1,2,3,4]
                            self.back = []
            """
        if mode == 'exact':
            temp = self.__fbuffer
            self.__fbuffer = self.__bbuffer
            self.__bbuffer = temp
        
        elif mode == 'transfer':
            self.__fbuffer.extend(self.__bbuffer)
            self.__bbuffer = []
        
        elif mode == 'discard':
            temp = self.__fbuffer
            self.__fbuffer = self.__bbuffer
            self.__bbuffer = temp
            self.__bbuffer = []
        
        elif mode == 'transfer_front':
            temp = self.__fbuffer
            self.__fbuffer = self.__bbuffer
            self.__bbuffer = temp
            self.__fbuffer.extend(self.__bbuffer)
            self.__bbuffer = []
        
        else:
            raise ValueError("Mode {m} not recognized.".format(m=mode))
    
    def get_front_buffer_items(self):
        """Returns a copy of the values in the front buffer"""
        return self.__fbuffer[:]
    
    def get_back_buffer_items(self):
        """Returns a copy of the values in the back buffer"""
        return self.__bbuffer[:]
    
    def pop(self):
        """Pops the top value from the front buffer."""
        return self.__fbuffer.pop(0)

    def push(self, value):
        """Push a value onto the bottom of the back buffer."""
        self._write_back_buffer(value)
    
    def _write_back_buffer(self, value):
        """For directly appending to the bottom of the back buffer"""
        self.__bbuffer.append(value)
        
    def _write_front_buffer(self, value):
        """For directly appending to the bottom of the front buffer"""
        self.__fbuffer.append(value)

class LockableList(list):
    """Does not protect many of the possible assignments, 
            such as LockableList[i] =k 
            Protects basic actions"""
    
    _dirty = False
    _locked = False
    _pending_index = 0
    
    
    def __init__(self, values=None):
        self._to_change = {}
        if values is None:
            values = []
        super(LockableList, self).__init__(values)
    
    def _apply_pending_changes(self):
        """Apply changes that are pending, only if unlocked."""
        if self._locked:
            return

        changes = []
        for value, (index, count) in self._to_change.iteritems():
            changes.append((index, value, count))
        changes.sort()

        for index, value, count in changes:
            if count > 0:
                super(LockableList, self).append(value)
            else:
                super(LockableList, self).remove(value)
        self._to_change = {}
        self._pending_index = 0
        self._dirty = False

    def _track_change(self, value, count):
        """
        Start tracking a pending change
        
        Keeps track of the order that items were appended in.
        Keeps ref counter in case items are added/removed multiple times
            during a lock
        """
        if value in self._to_change:
            self._to_change[value][1] += count
        else:
            self._to_change[value] = [self._pending_index, 1 + count]
            self._pending_index += 1
            
    def append(self, value):
        if not self._locked:
            super(LockableList, self).append(value)
        else:
            self._track_change(value, 1)
            self._dirty = True
    
    def clear(self):
        """Clear all values from the list and pending changes.
        Does not check lock status. This might need to be changed..."""
        while len(self) > 0:
            self.pop()
        self._to_change = {}
        self._pending_index = 0
            
    def extend(self, values):
        if not self._locked:
            super(LockableList, self).extend(values)
        else:
            for value in values:
                self._track_change(value, 1)
            self._dirty = True
    
    @property
    def is_dirty(self): #pylint:disable-msg=C0103
        """Needs update when there are pending changes."""
        return self._dirty
    
    @property
    def is_locked(self):
        """Lock prevents direct append/removal, such as when looping over."""
        return self._locked
    
    def lock(self, set_lock=None, force_update=True):
        """If set_lock is not True or False, toggles lock state.
            force_update forces a call to apply_pending_changes."""
        if set_lock is None:
            self._locked = not self._locked
        elif set_lock:
            self._locked = True
        else:
            self._locked = False

        if force_update:
            self._apply_pending_changes()

    @property
    def pending_additions(self):
        """Returns a list of all values to be added when next unlocked"""
        additions = []
        for key in self._to_change:
            if self._to_change[key][1] > 0:
                additions.append(key)
        return additions
    
    @property
    def pending_removals(self):
        """Returns a list of all values to be removed when next unlocked"""
        removals = []
        for key in self._to_change:
            if self._to_change[key][1] <= 0:
                removals.append(key)
        return removals
    
    def remove(self, value):
        if not self._locked:
            super(LockableList, self).remove(value)
        else:
            self._track_change(value, -1)
            self._dirty = True

    def sort(self, cmp_=None, key_=None, reverse_=False):
        self._apply_pending_changes()
        super(LockableList, self).sort(cmp_,
                                            key=key_,
                                            reverse=reverse_)
    
    def __iadd__(self, other):
        self.extend(other)
        return self
        
    def __iter__(self):
        self._apply_pending_changes()
        return super(LockableList, self).__iter__()

class TypeCheckedList(list):
    """A list with a certain type that is checked
            at append/extend so that future use can assume type.
            Changing dtype will of course break this rule."""
    def __init__(self, dtype, values=None, suppress_type_errors=False):
        super(TypeCheckedList, self).__init__()
        
        self._dtype = dtype
        self._suppress_type_errors = suppress_type_errors
        
        if values is not None:
            self.extend(values)
    
    def append(self, value):
        if not isinstance(value, self._dtype):
            if not self._suppress_type_errors:
                msg = "Cannot append value {it}: not an instance of {lt}."
                raise TypeError(msg.format(it=value, lt=self._dtype))
        else:
            super(TypeCheckedList, self).append(value)
    
    def clear(self):
        """Since we can't do TypeCheckedList = [],
            need to have an explicit method of clearing"""
        while len(self) > 0:
            self.pop()
    
    def extend(self, values):
        if hasattr(values, "__iter__"):
            for value in values:
                self.append(value)
        else:
            self.append(values)    