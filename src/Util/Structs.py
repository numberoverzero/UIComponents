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
    def __init__(self, dtype, items = None, suppress_type_errors = False):
        super(TypeCheckedList, self).__init__()
        
        self._dtype = dtype
        self._suppress_type_errors = suppress_type_errors
        
        if items is not None:
            self.extend(items)
    
    def append(self, item):
        if not isinstance(item, self._dtype):
            if not self._suppress_type_errors:
                msg = "Cannot append item {it}: not an instance of {lt}."
                raise TypeError(msg.format(it=item, lt=self._dtype))
        else:
            super(TypeCheckedList, self).append(item)
    
    def clear(self):
        """Since we can't do TypeCheckedList = [],
            need to have an explicit method of clearing"""
        while len(self) > 0:
            self.pop()
    
    def extend(self, items):
        if hasattr(items, "__iter__"):
            for item in items:
                self.append(item)
        else:
            self.append(items)           
    
class TypedDoubleBuffer(object):
    """A double buffered object with specific type.
            Can be cleared and flipped a few ways, read the docstring
            for details on what each mode does."""
        
    def __init__(self, dtype, suppress_type_errors = False):
        self.__bbuffer = TypeCheckedList(dtype, items = None,
                            suppress_type_errors = suppress_type_errors)
        self.__fbuffer = TypeCheckedList(dtype, items = None,
                            suppress_type_errors = suppress_type_errors)
            
    def clear(self, front = True, back = False):
        """Clears the front or back buffer, or both."""
        if front:
            self.__fbuffer.clear()
        if back:
            self.__bbuffer.clear()
            
    def flip(self, mode = 'exact'):
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
            self.__bbuffer.clear()
        
        elif mode == 'discard':
            temp = self.__fbuffer
            self.__fbuffer = self.__bbuffer
            self.__bbuffer = temp
            self.__bbuffer.clear()
        
        elif mode == 'transfer_front':
            temp = self.__fbuffer
            self.__fbuffer = self.__bbuffer
            self.__bbuffer = temp
            self.__fbuffer.extend(self.__bbuffer)
            self.__bbuffer.clear()
        
        else:
            raise ValueError("Mode {m} not recognized.".format(m=mode))
    
    def get_front_buffer_items(self):
        """Returns a copy of the items in the front buffer"""
        return self.__fbuffer[:]
    
    def get_back_buffer_items(self):
        """Returns a copy of the items in the back buffer"""
        return self.__bbuffer[:]
    
    def pop(self):
        """Pops an item from the front buffer."""
        return self.__fbuffer.pop(0)

    def push(self, item):
        """Push an item onto the back buffer."""
        self.__bbuffer.append(item)

class TypedLockableList(TypeCheckedList):
    """Does not protect many of the possible assignments, 
            such as LockableList[i] =k 
            Protects basic actions"""
    
    _locked = False
    _needs_update = False
    _to_add = []
    _to_remove = []
    _changed_since_last_call = False
    
    def __init__(self, dtype, items = None, suppress_type_errors = False):
        
        super(TypedLockableList, self).__init__(dtype, items = items,
                            suppress_type_errors = suppress_type_errors)
        
    def append(self, item):
        self._changed_since_last_call = True
        if not self._locked:
            super(TypedLockableList, self).append(item)
        else:
            self._to_add.append(item)
            self._needs_update = True

    def extend(self, items):
        self._changed_since_last_call = True
        if not self._locked:
            super(TypedLockableList, self).extend(items)
        else:
            self._to_add.extend(items)
            self._needs_update = True
            
    def remove(self, item):
        self._changed_since_last_call = True
        if not self._locked:
            super(TypedLockableList, self).remove(item)
        else:
            self._to_remove.append(item)
            self._needs_update = True

    def lock(self, set_lock = None, force_update = True):
        """If set_lock is not True or False, toggles lock state."""
        if set_lock is None:
            self._locked = not self._locked
        elif set_lock:
            self._locked = True
        else:
            self._locked = False

        if force_update:
            self._apply_pending_changes()

    def __call_(self):
        """Calling this object applys pending changes"""
        self._apply_pending_changes()

    def _apply_pending_changes(self):
        """Apply changes that are pending, only if it is locked."""
        if self._locked:
            return

        for item in self._to_add:
            super(TypedLockableList, self).append(item)
        self._to_add = []

        for item in self._to_remove:
            super(TypedLockableList, self).remove(item)
        self._to_remove = []

        self._needs_update = False

    def sort(self, _cmp = None, key = None, reverse = False):
        if self._locked:
            return
        super(TypedLockableList, self).sort(_cmp, key = key, reverse = reverse)

    def __get_needs_update(self):
        """Needs update when there are pending changes."""
        return self._needs_update
    HasPendingUpdates = property(__get_needs_update)

    def __get_is_locked(self):
        """Locked prevents direct append/removal, such as when looping over."""
        return self._locked

    IsLocked = property(__get_is_locked)

    def __g_changed_since_last_call(self):
        """If there are pending updates 
            (almost always same as HasPendingChanges)"""
        return self._changed_since_last_call
    ChangedSinceLastCall = property(__g_changed_since_last_call)

    def clear_change_flag(self):
        """Manually clear the change flag.
            Useful when you want to ignore behavior that triggers off of
            changes, even if changes HAVE taken place."""
        self._changed_since_last_call = False

    def clear(self):
        if self.IsLocked:
            raise RuntimeError("Tried to clear a locked list.")
        else:
            for item in self:
                self.remove(item)
            while len(self._to_add) > 0:
                self._to_add.pop()
            while len(self._to_remove) > 0:
                self._to_remove.pop()
