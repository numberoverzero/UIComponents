

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