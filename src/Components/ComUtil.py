import functools

class __id_manager(object):
    def __init__(self):
        self.__nid = {}
    
    def NextID(self, obj):
        otype = type(obj)
        if self.__nid.has_key(otype):
            self.__nid[otype] += 1
        else:
            self.__nid[otype] = 1
        return self.__nid[otype] - 1
    
ID_Manager = __id_manager()

def contains(_list, item):
    return _list.count(item) > 0

def OnChange(var_name, flagOnChange):
    """DECORATOR: If self.var_name != new_value, self.flagOnChange = True"""
    def fn_wrapper(fn):
        @functools.wraps(fn)
        def wrapped_call(self, new_value):
            old_value = getattr(self, var_name)
            fn(self, new_value)
            if new_value != old_value:
                setattr(self, flagOnChange, True)
        return wrapped_call
    return fn_wrapper

def InjectArgs(ignores = None):
    """DECORATOR: Injects local args into class so that there isn't a lot of:
        def foo(self, x, y, b, w, h, r):
            self.x = x
            self.y = y
            self.b = b
            self.w = w
        NOTE: ignores any names in the vector "ignores"
    """
    err_str = "Must pass kwargs using keyword- can't pass using position."
    
    #Can't iterate on None object
    if ignores is None:
        ignores = []
    #Ensure that we wrap the object in a list if it's not already a sequence
    if not hasattr(ignores, '__iter__'):
        ignores = list(ignores)
        
    def fn_wrapper(fn):
        #Non-kwarg count
        kw_count = len(fn.func_defaults)
        arg_count = fn.func_code.co_argcount - kw_count

        #List of kwarg var names
        kw_names = fn.func_code.co_varnames[arg_count:]
        
        @functools.wraps(fn)
        def wrapped_call(*args, **kwargs):
            nargs = len(args)

            #Kwargs have to be passed using keyword
            if nargs > arg_count:
                raise TypeError(err_str)

            #Pull out self
            _self = args[0]

            #Inject defaults into kwargs if they're not already there
            vkwargs = {}
            start_index = nargs - arg_count
            for index in range(start_index, kw_count):
                if kw_names[index] not in ignores:
                    vkwargs[kw_names[index]] = fn.func_defaults[index]

            #Filter only valid kwargs            
            for key in kwargs:
                if key not in ignores:
                    vkwargs[key] = kwargs[key]
            
            #Update kwargs, use setattr in case there are setters or getters
                #Using __dict__.update bypasses set/get
            for name in vkwargs:
                setattr(_self, name, vkwargs[name])
            
            #Grab all variable names except first- that's self
            _all_names = fn.func_code.co_varnames[1:fn.func_code.co_argcount]
            
            #Filter out var names that are in kwargs
            _names = [n for n in _all_names if not vkwargs.has_key(n)]
            
            #Don't grab first, it's self
            _values = args[1:]
            
            #Update using setattr, same reason as above
            for name, value in zip(_names, _values):
                setattr(_self, name, value)
            
            #Actually run the function and hand back it's return
            return fn(*args, **kwargs)
        return wrapped_call
    return fn_wrapper

class TypeCheckedList(list):
    def __init__(self, dtype, items = None):
        self.__dtype = dtype
        if items is None:
            super(TypeCheckedList, self).__init__()
        else:
            self.extend(items)
    
    def append(self, item):
        if not isinstance(item, self.__dtype):
            raise TypeError("Cannot append item {ita}: not an instance of {lt}.".format(
                            ita=item, lt=self.__dtype))
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
        