import functools

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
        try:
            kw_count = len(fn.func_defaults)
        except TypeError:
            kw_count = 0
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