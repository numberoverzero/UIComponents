
NEXT_ID = 0

def _get_next_id():
    global NEXT_ID
    NEXT_ID += 1
    return NEXT_ID - 1

def contains(_list, item):
    return _list.count(item) > 0

def OnChange(var_name, flagOnChange):
    """If self.var_name != new_value, self.flagOnChange = True"""
    def fn_wrapper(fn):
        def wrapped_call(self, new_value):
            old_value = getattr(self, var_name)
            fn(self, new_value)
            if new_value != old_value:
                setattr(self, flagOnChange, True)
        return wrapped_call
    return fn_wrapper

            