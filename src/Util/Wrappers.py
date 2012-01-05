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

ARG_MISSING_COUNT_ERRMSG = "{f}() takes at least {n} arguments ({x} given)"
ARG_EXTRA_COUNT_ERRMSG = "{f}() takes at most {n} arguments ({x} given)"
ARG_EXTRA_DEF_ERRMSG = "{f}() got mutliple values for keyword argument '{n}'"

def inject_args(ignores=None):
    """DECORATOR: Injects local args into class so that there isn't a lot of:
        def foo(self, x, y, b, w, h, r):
            self.x = x
            self.y = y
            self.b = b
            self.w = w
        NOTE: ignores any names in the vector "ignores"
    """
        
    if not hasattr(ignores, '__iter__'):
        if isinstance(ignores, str):
            ignores = [ignores]
        else:
            ignores = []
    else:
        #Note: use ignores = ignores[:] to copy the list
        #This makes the ignores list immutable.
        #However, having a mutable ignores could be useful, so it is
        #assumed by default.
        pass
    def fn_wrapper(func):
        """Wraps the function that will have args injected"""
        fname = func.func_name
        
        #Less 1 for the self arg
        ttl_var_count = func.func_code.co_argcount - 1
        
        try:
            kw_count = len(func.func_defaults)
        except TypeError:
            #func_defaults is None when the function has no kwargs
            kw_count = 0
        
        arg_count = ttl_var_count - kw_count
        
        #Don't include the first arg name (self)
        var_names = func.func_code.co_varnames[1:]
        arg_names = var_names[:arg_count]
        kwarg_names = var_names[arg_count:]
        
        #Load default kwargs
        default_passing_kwargs = {}
        for i in xrange(kw_count):
            default_passing_kwargs[kwarg_names[i]] = func.func_defaults[i]
        
        @functools.wraps(func)
        def wrapped_call(*args, **kwargs): # pylint: disable-msg=C0111
            #Pull self off of args
            self_ = args[0]
            args = list(args[1:])
            
            n_args = len(args)
            n_kwargs = len(kwargs)
            n_ttl_args = n_args + n_kwargs
                        
            #Didn't provide all necessary args as args- might be in kwargs
            if n_args < arg_count:
                #Load missing args from kwargs
                for key in kwargs.keys():
                    if key in arg_names:
                        #Find the index of the key in arg_names
                        arg_index = arg_names.index(key)
                        arg_value = kwargs.pop(key)
                        args.insert(arg_index, arg_value)
                
                #Recheck length of args
                n_args = len(args)
                n_kwargs = len(kwargs)
                n_ttl_args = n_args + n_kwargs
                
                if n_args != arg_count:
                    #Didn't get all args loaded in, raise the error.
                    raise TypeError(ARG_MISSING_COUNT_ERRMSG.format(
                        f=fname, n=arg_count + 1, x=n_args + 1))
                        #We add on 1 for self
            
            #Provided all args, all kwargs, and then some.
            if n_ttl_args > ttl_var_count:
                raise TypeError(ARG_EXTRA_COUNT_ERRMSG.format(
                    f=fname, n=ttl_var_count + 1, x=n_ttl_args + 1))
            
            #Load kwargs into default kwargs
            passing_kwargs = default_passing_kwargs.copy()
            passing_kwargs.update(kwargs)

            passing_args = list(args[:arg_count])

            #Load kwargs passed by position (in args)
            n_passed_as_args = n_args - arg_count
            if n_passed_as_args > 0:
                start = arg_count
                for i in xrange(n_passed_as_args):
                    #kwarg name index
                    kwni = i
                    #arg value index
                    avi = i + start
                    
                    passing_kwargs[kwarg_names[kwni]] = args[avi]
            
            #Inject args into object namespace
            for index, value in enumerate(passing_args):
                name = arg_names[index]
                if name not in ignores:
                    setattr(self_, name, value)                    
            
            #Inject kwargs into object namespace
            for key in passing_kwargs.keys():
                if key not in ignores:
                    setattr(self_, key, passing_kwargs[key])
            
            #Re-insert self into passing args for function call
            passing_args.insert(0, self_)
            
            #Execute the wrapped function 
            p_args = passing_args
            p_kwargs = passing_kwargs
            return func(*p_args, **p_kwargs) # pylint: disable-msg=W0142
        return wrapped_call
    return fn_wrapper

