"""
Engine-level util and globals.
ex. ID_Manager is an __id_manager that can be accessed once
the engine has been imported.  This provides a single access
point to the id pool, so there are not id collisions.
"""

import Util

class HasID(object):
    """An object with an id from an id_manager"""
    def __init__(self, id_manager_=None, custom_id=None):
        if custom_id is not None:
            self._id = custom_id
            self.__id_manager = None
        else:
            if not hasattr(id_manager_, "next_id"):
                id_manager_ = GLOBAL_ID_MANAGER
            self.__id_manager = id_manager_
            self._id = self.__id_manager.next_id(self)
    
    def __eq__(self, other):
        try:
            return self.ID == other.ID
        except AttributeError:
            return False
    
    def __get_id(self):
        """Returns the object's id"""
        return self._id
    ID = property(__get_id)
    
class id_manager(object): # pylint: disable-msg=C0103
    """Used to track and hand out ids.  Currently only supports
            getting the next available id.  Uses seperate ids for
            different types of objects"""
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
    
    def reset(self):
        """Resets all counters."""
        self.__nid = {}
    
GLOBAL_ID_MANAGER = id_manager()
