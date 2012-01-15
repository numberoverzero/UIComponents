"""
Everything having to do with ids and id managers
"""

import Util

def get_id(obj, custom_id = None):
    """Returns an ID for an object, using the GLOBAL_ID_MANAGER"""
    return ID(obj, custom_value = custom_id)

class ID(object):
    """An id with a value from an id_manager"""
    def __init__(self, obj=None, id_manager_=None, custom_value=None):
        if custom_value is not None:
            self._value = custom_value
            self.__id_manager = None
        else:
            if not hasattr(id_manager_, "next_id"):
                id_manager_ = GLOBAL_ID_MANAGER
            self.__id_manager = id_manager_
            if obj is None:
                obj = self
            self._value = self.__id_manager.next_id(obj)
    
    def __eq__(self, other):
        try:
            val_eq = self.Value == other.Value
            idm_eq = self.ID_Manager == other.ID_Manager
            return val_eq and idm_eq
        except AttributeError:
            return False
    
    def __get_value(self):
        """Returns the ID's value"""
        return self._value
    Value = property(__get_value)
    
    def __get_id_manager(self):
        """Returns the object's id manager"""
        return self.__id_manager
    ID_Manager = property(__get_id_manager)
    
    def __str__(self):
        return "ID(id_manager={}, value={})".format(
            self.__id_manager, self._value)

ID_FMT = "{manager}:{cname}:{index}"
class id_manager(object): # pylint: disable-msg=C0103
    """Used to track and hand out ids.  Currently only supports
            getting the next available id.  Uses seperate ids for
            different types of objects"""
    def __init__(self, manager_name = None):
        self.__nid = {}
        self.__manager_name = manager_name
    
    def next_id(self, obj):
        """Returns the next id available from the manager."""
        #otype = type(obj)
        class_name = Util.class_name(obj)
        if self.__nid.has_key(class_name):
            self.__nid[class_name] += 1
        else:
            self.__nid[class_name] = 1
        index = self.__nid[class_name] - 1
        name = ID_FMT.format(manager = self.__manager_name,
                             cname = class_name,
                             index = index)
        return name
    
    def reset(self):
        """Resets all counters."""
        self.__nid = {}

GLOBAL_ID_MANAGER = id_manager("GLOBAL")