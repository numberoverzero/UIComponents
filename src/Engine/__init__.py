"""
Engine-level util and globals.
ex. ID_Manager is an __id_manager that can be accessed once
the engine has been imported.  This provides a single access
point to the id pool, so there are not id collisions.
"""


import Util

class __id_manager(object): # pylint: disable-msg=C0103
    """Used to track and hand out ids.  Currently only supports
            getting the next available id."""
    def __init__(self):
        self.__nid = {}
    
    def next_id(self, obj):
        """Returns the next id available from the manager."""
        otype = type(obj)
        if self.__nid.has_key(otype):
            self.__nid[otype] += 1
        else:
            self.__nid[otype] = 1
        return self.__nid[otype] - 1
    
ID_Manager = __id_manager() # pylint: disable-msg=C0103
