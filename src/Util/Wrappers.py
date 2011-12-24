"""
Various function wrappers that make life easier-
ex. InjectArgs allows you to auto-import args into the object's namespace
so that you don't have 8 lines of "self.x = x" but also allows you to
ignore variables (so that they aren't loaded into the namespace.
"""

import functools

def on_change(var_name, flag_on_change):
    """DECORATOR: If self.var_name != new_value, self.flagOnChange = True"""
    def fn_wrapper(func):
        """Wraps the function that will have its var_name checked for change"""
        @functools.wraps(func)
        def wrapped_call(self, new_value):  # pylint: disable-msg=C0111
            old_value = getattr(self, var_name)
            func(self, new_value)
            if new_value != old_value:
                setattr(self, flag_on_change, True)
        return wrapped_call
    return fn_wrapper

def inject_args(ignores = None):
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
        
    def fn_wrapper(func):
        """Wraps the function that will have args injected"""
        
        #Non-kwarg count
        try:
            kw_count = len(func.func_defaults)
        except TypeError:
            kw_count = 0
        arg_count = func.func_code.co_argcount - kw_count

        #List of kwarg var names
        kw_names = func.func_code.co_varnames[arg_count:]
        
        @functools.wraps(func)
        def wrapped_call(*args, **kwargs):  # pylint: disable-msg=C0111
            nargs = len(args)

            #Kwargs have to be passed using keyword
            if nargs > arg_count:
                raise TypeError(err_str)

            #Pull out self
            self_ = args[0]

            #Inject defaults into kwargs if they're not already there
            vkwargs = {}
            start_index = nargs - arg_count
            for index in range(start_index, kw_count):
                if kw_names[index] not in ignores:
                    vkwargs[kw_names[index]] = func.func_defaults[index]

            #Filter only valid kwargs            
            for key in kwargs:
                if key not in ignores:
                    vkwargs[key] = kwargs[key]
            
            #Update kwargs, use setattr in case there are setters or getters
                #Using __dict__.update bypasses set/get
            for name in vkwargs:
                setattr(self_, name, vkwargs[name])
            
            #Grab all variable names except first- that's self
            all_names_ = func.func_code.co_varnames[1:]
            
            #Filter out var names that are in kwargs
            names_ = [n for n in all_names_ if not vkwargs.has_key(n)]
            
            #Don't grab first, it's self
            _values = args[1:]
            
            #Update using setattr, same reason as above
            for name, value in zip(names_, _values):
                setattr(self_, name, value)
            
            #Actually run the function and hand back it's return
            return func(*args, **kwargs)
        return wrapped_call
    return fn_wrapper