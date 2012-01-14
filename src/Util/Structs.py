"""
Useful structures such as double buffers and typechecked lists
"""

def enum(*sequential, **named):
    """Creates a classic enumerable.  For details,
            see http://stackoverflow.com/q/1695250""" 
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

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
        """Push an value onto the back buffer."""
        self._write_back_buffer(value)
    
    def _write_front_buffer(self, value):
        """For directly appending to the front buffer"""
        self.__fbuffer.append(value)
    
    def _write_back_buffer(self, value):
        """For directly appending to the back buffer"""
        self.__bbuffer.append(value)

class LockableList(list):
    """Does not protect many of the possible assignments, 
            such as LockableList[i] =k 
            Protects basic actions"""
    
    _locked = False
    _needs_update = False
    _changed_since_last_call = False
    
    def __init__(self, values=None):
        self._to_change = {}
        if values is None:
            values = []
        super(LockableList, self).__init__(values)
    
    def _apply_change_diff(self, value, amt):
        """Checks self._to_change and if there is an existing value, 
            increments by value. 
            
            Otherwise, sets self._to_change[value] = amt"""
        if self._to_change.has_key(value):
            self._to_change[value] += amt
        else:
            self._to_change[value] = amt
    
    def append(self, value):
        self._changed_since_last_call = True
        if not self._locked:
            super(LockableList, self).append(value)
        else:
            self._apply_change_diff(value, 1)
            self._needs_update = True
    
    def clear(self):
        """Clear all values from the list and pending changes.
        Does not check lock status. This might need to be changed..."""
        while len(self) > 0:
            self.pop()
        self._to_change = {}
    
    def clear_change_flag(self):
        """Manually clear the change flag.
            Useful when you want to ignore behavior that triggers off of
            changes, even if changes HAVE taken place."""
        self._changed_since_last_call = False
        
    def extend(self, values):
        self._changed_since_last_call = True
        if not self._locked:
            super(LockableList, self).extend(values)
        else:
            for value in values:
                self._apply_change_diff(value, 1)
            self._needs_update = True
            
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

    def remove(self, value):
        self._changed_since_last_call = True
        if not self._locked:
            super(LockableList, self).remove(value)
        else:
            self._apply_change_diff(value, -1)
            self._needs_update = True

    def sort(self, cmp_=None, key_=None, reverse_=False):
        self._apply_pending_changes()
        self._changed_since_last_call = True
        super(LockableList, self).sort(cmp_,
                                            key=key_,
                                            reverse=reverse_)

    def _apply_pending_changes(self):
        """Apply changes that are pending, only if unlocked."""
        if self._locked:
            return

        for key in self._to_change:
            if self._to_change[key] > 0:
                super(LockableList, self).append(key)
            else:
                super(LockableList, self).remove(key)
        
        self._needs_update = False
    
    def __iter__(self):
        self._apply_pending_changes()
        return super(LockableList, self).__iter__()

    def __g_has_pending_updates(self):
        """Needs update when there are pending changes."""
        return self._needs_update
    HasPendingUpdates = property(__g_has_pending_updates)

    def __g_is_locked(self):
        """Locked prevents direct append/removal, such as when looping over."""
        return self._locked
    IsLocked = property(__g_is_locked)

    def __g_changed_since_last_call(self):
        """If there are pending updates 
            (almost always same as HasPendingChanges)"""
        return self._changed_since_last_call
    ChangedSinceLastCall = property(__g_changed_since_last_call)
    
    
    def __g_pending_additions(self):
        """Returns a list of all values to be added when next unlocked"""
        #self._apply_change_diff(value,1
        additions = []
        for key in self._to_change:
            if self._to_change[key] > 0:
                additions.append(key)
        return additions
    PendingAdditions = property(__g_pending_additions)
    
    def __g_pending_removals(self):
        """Returns a list of all values to be removed when next unlocked"""
        removals = []
        for key in self._to_change:
            if self._to_change[key] <= 0:
                removals.append(key)
        return removals
    PendingRemovals = property(__g_pending_removals)



    
