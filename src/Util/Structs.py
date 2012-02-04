"""
Useful structures such as double buffers and typechecked lists
"""

_ERR_LISTLOCK_AMBIGUOUS = "Can't {} while locked- behavior is ambiguous."

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


class ListLockException(Exception):
    """
    Exception during a list operation on a LockableList. 
    
    Some actions, such as insert, are non-deterministic in a locked state.
    The index 3 may have wildly different meanings for the snapshot and the full
    buffer list, and it's complex if at all possible to know which the user means.
    """
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        return repr(self.value)


class LockableList(list):
    """Does not protect many of the possible assignments, 
            such as LockableList[i] =k 
            Protects basic actions"""
    __hash__ = None
    _dirty = False
    _locked = False
    
    def __init__(self, values=None):
        if values is None:
            values = []
        
        list.__init__(self, values)
        self._buffer = []
        self.extend(values)
        
    def _copy_buff_to_self(self):
        """Helper method for copying the buffer to super (list)"""
        full_range = slice(len(self))
        list.__setitem__(self, full_range, self._buffer)
        
    def append(self, value):
        if not self._locked:
            list.append(self, value)
        else:
            self._buffer.append(value)
            self._dirty = True
    
    def clear(self):
        """
        Clear all values from the list and pending changes
        
        Does not check lock status. This might need to be changed...
        """
        self._buffer = []
        self._copy_buff_to_self()
        self._dirty = False
                
    def extend(self, iterable):
        for value in iterable:
            self.append(value)
        
    def insert(self, index, value):
        if self._dirty:
            raise ListLockException(_ERR_LISTLOCK_AMBIGUOUS.format("insert"))
        else:
            if self._locked:
                self._buffer.insert(index, value)
                self._dirty = True
            else:
                list.insert(self, index, value)
    
    @property
    def is_dirty(self):
        """Needs update when there are pending changes."""
        return self._dirty
    
    @property
    def is_locked(self):
        """Lock prevents direct append/removal, such as when looping over."""
        return self._locked
    
    def lock(self, set_lock=None):
        """If set_lock is None, toggles lock state"""
        if set_lock is None:
            set_lock = not self._locked
            
        if self._locked and not set_lock:
            #Unlocking - update from buffer
            self._copy_buff_to_self()
            self._dirty = False
        
        if not self._locked and set_lock:
            #Locking- copy to buffer
            self._buffer = self[:]
            
        self._locked = set_lock            
    
    def pop(self, index=-1):
        if self._dirty:
            msg = _ERR_LISTLOCK_AMBIGUOUS.format("pop (even when dirty)")
            raise ListLockException(msg)
        else:
            if self._locked:
                value = self._buffer.pop(index)
                self._dirty = True
            else:
                value = list.pop(self, index)
            return value
    
    def remove(self, value):
        if not self._locked:
            list.remove(self, value)
        else:
            self._buffer.remove(value)
            self._dirty = True
    
    def reverse(self):
        if not self._locked:
            list.reverse(self)
        else:
            self._buffer.reverse()
            self._dirty = True

    def sort(self, cmp=None, key=None, reverse=False): #pylint:disable-msg=W0622
        """stable sort *IN PLACE*; cmp(x, y) -> -1, 0, 1"""
        if self._locked:
            msg = _ERR_LISTLOCK_AMBIGUOUS.format("sort")
            raise ListLockException(msg)
        else:
            list.sort(self, cmp=cmp, key=key, reverse=reverse)
        
    def __delitem__(self, i):
        if self._dirty:
            msg = _ERR_LISTLOCK_AMBIGUOUS.format("del x[y]")
            raise ListLockException(msg)
        else:
            if self._locked:
                del self._buffer[i]
                self._dirty = True
            else:
                list.__delitem__(self, i)
        
    def __delslice__(self, i, j):
        if self._dirty:
            msg = _ERR_LISTLOCK_AMBIGUOUS.format("del x[i:j]")
            raise ListLockException(msg)
        else:
            if self._locked:
                del self._buffer[i:j]
                self._dirty = True
            else:
                list.__delslice__(self, i, j)
    
    def __eq__(self, other):
        try:
            return (self._buffer == other._buffer and #pylint:disable-msg=W0212
                    list.__eq__(self, other))
        except AttributeError:
            return False
          
    def __iadd__(self, other):
        self.extend(other)
        return self
      
    def __imul__(self, other):
        if self._dirty:
            old_buf = self._buffer[:]
        else:
            old_buf = self[:]
        for _ in xrange(other):
            self.extend(old_buf)
      
    def __iter__(self):
        if self._dirty and not self._locked:
            self._copy_buff_to_self()
            self._dirty = False
        return list.__iter__(self)
      
    def __reversed__(self):
        if self._dirty and not self._locked:
            self._copy_buff_to_self()
            self._dirty = False
        return list.__reversed__(self)
      
    def __setitem__(self, i, y): #pylint:disable-msg=C0103
        if self._dirty:
            msg = _ERR_LISTLOCK_AMBIGUOUS.format("x[i]=y")
            raise ListLockException(msg)
        else:
            if self._locked:
                self._buffer[i] = y
                self._dirty = True
            else:
                list.__setitem__(self, i, y)
      
    def __setslice__(self, i, j, y): #pylint:disable-msg=C0103
        if self._dirty:
            msg = _ERR_LISTLOCK_AMBIGUOUS.format("x[i]=y")
            raise ListLockException(msg)
        else:
            if self._locked:
                self._buffer[i:j] = y
                self._dirty = True
            else:
                list.__setslice__(self, i, j, y)

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