
#From:
#http://stackoverflow.com/q/1695250
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

class TypeCheckedList(list):
    def __init__(self, dtype, items = None):
        self.__dtype = dtype
        if items is None:
            super(TypeCheckedList, self).__init__()
        else:
            self.extend(items)
    
    def append(self, item):
        if not isinstance(item, self.__dtype):
            raise TypeError("Cannot append item {it}: not an instance of {lt}.".format(
                            it=item, lt=self.__dtype))
        else:
            super(TypeCheckedList, self).append(item)
    
    def clear(self):
        """Since we can't do TypeCheckedList = [],
            need to have an explicit method of clearing"""
        while len(self) > 0:
            self.pop()
    
    def extend(self, items):
        map(self.append, items)
    
class TypedDoubleBuffer(object):
    def __init__(self, dtype):
        self.__b1 = TypeCheckedList(dtype)
        self.__b2 = TypeCheckedList(dtype)
        self.front_buffer = self.__b1
        self.back_buffer = self.__b2
        
    def push(self, item):
        self.back_buffer.append(item)
    
    def pop(self):
        """pops from the front, since new is appended to the back."""
        self.front_buffer.pop(0)
    
    def clear(self, front = True, back = False):
        """Clears the front or back buffer, or both."""
        if front:
            self.front.clear()
        if back:
            self.back.clear()
            
    def flip(self, mode = 'transfer'):
        """Mode is one of:
            transfer: any values still in front buffer stay, and the values in 
                        back buffer are pushed onto the front buffer.
                        
                        --- PRESERVES ORDER, PRESERVES VALUES ---
                        EXAMPLE:
                            #Before flip:
                            front = [1,2,3,4]
                            back = [5,6,7,8]
                            
                            self.flip()
                            
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
                        back get popped before old front values.
                        
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
        if mode == 'transfer':
            self.front_buffer.extend(self.back_buffer)
            self.back_buffer.clear()
        
        elif mode == 'discard':
            temp = self.front_buffer
            self.front_buffer = self.back_buffer
            self.back_buffer = temp
            self.back_buffer.clear()
        
        elif mode == 'transfer_front':
            temp = self.front_buffer
            self.front_buffer = self.back_buffer
            self.back_buffer = temp
            self.front_buffer.extend(self.back_buffer)
            self.back_buffer.clear()
        
        else:
            raise ValueError("Mode {m} not recognized.".format(m=mode))
        
class TypedLockableList(TypeCheckedList):
    """Does not protect many of the possible assignments, such as LockableList[i] =k
        Protects most basic actions"""
    def __init__(self, dtype, items = None):
        if items is None:
            super(TypedLockableList, self).__init__()
        else:
            super(TypedLockableList, self).__init__(items)
        self.__dtype = dtype
        self.__canModify = True
        self.__needsUpdate = False
        self.__toAdd = []
        self.__toRemove = []
        self.__changedSinceLastCall = False

    def append(self, item):
        if not isinstance(item, self.__dtype):
            return
        self.__changedSinceLastCall = True
        if self.__canModify:
            super(TypedLockableList, self).append(item)
        else:
            self.__toAdd.append(item)
            self.needsUpdate = True

    def extend(self, items):
        for item in items:
            if not isinstance(item, self.__dtype):
                return
        self.__changedSinceLastCall = True
        if self.__canModify:
            super(TypedLockableList, self).extend(items)
        else:
            self.__toAdd.extend(items)
            self.__needsUpdate = True
            
    def remove(self, item):
        self.__changedSinceLastCall = True
        if self.__canModify:
            super(TypedLockableList, self).remove(item)
        else:
            self.__toRemove.append(item)
            self.needsUpdate = True

    def Lock(self, setLock = None, forceUpdate = True):
        """If setLock is not True or False, toggles lock state."""
        if setLock is None:
            self.__canModify = not self.__canModify
        elif setLock:
            self.__canModify = False
        else:
            self.__canModify = True

        if forceUpdate:
            self.__applyPendingChanges()

    def __call_(self):
        self.__applyPendingChanges()

    def __applyPendingChanges(self):
        if not self.__canModify:
            return

        for item in self.__toAdd:
            super(TypedLockableList, self).append(item)
        self.__toAdd = []

        for item in self.__toRemove:
            super(TypedLockableList, self).remove(item)
        self.__toRemove = []

        self.__needsUpdate = False

    def sort(self, _cmp = None, key = None, reverse = False):
        if not self.__canModify:
            return
        super(TypedLockableList, self).sort(_cmp, key = key, reverse = reverse)

    def __getNeedsUpdate(self):
        return self.__needsUpdate
    HasPendingUpdates = property(__getNeedsUpdate)

    IsLocked = property(lambda self: not self.__canModify)

    def __gChangedSinceLastCall(self):
        return self.__changedSinceLastCall
    def __sChangedSinceLastCall(self, b):
        self.__changedSinceLastCall = b
    ChangedSinceLastCall = property(__gChangedSinceLastCall)

    def ClearChangeFlag(self):
        self.__sChangedSinceLastCall(False)

    def clear(self):
        map(self.remove, self)      
