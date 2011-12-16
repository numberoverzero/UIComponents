import ConfigParser
import Util

class Setting(object):
    __no_opt_err = "Tried to set current to option not in list: {0}"
    def __init__(self, name = "", description = "",
                 default = None, selection = -1,
                 options = []):

        self._options = options[:]
        self._name = name
        self._description = description
        self._default = None
        self._selection = selection

    def __gCurrentIndex(self):
        return self._selection
    def __sCurrentIndex(self, value):
        value = value%len(self._options)
        self._selection = value
    CurrentIndex = property(__gCurrentIndex)

    def __gCurrent(self):
        if len(self._options) < 1:
            return None
        else:
            return self._options[self.CurrentIndex]

    def __sCurrent(self, value):
        if value not in self._options:
            raise KeyError(self.__no_opt_err.format(value))
        else:
            self.CurrentIndex = self._options.index(value)

    def __gPrevious(self):
        index = (self.CurrentIndex-1)%len(self._options)
        return self._options[index]
    def __gNext(self):
        index = (self.CurrentIndex+1)%len(self._options)
        return self._options[index]

    Current = property(__gCurrent, __sCurrent)
    Previous = property(__gPrevious)
    Next = property(__gNext)

    def AddOption(self, value):
        self._options.append(value)
        if len(self._options) == 1:
            self.CurrentIndex = 0

    def RemoveOption(self, value):
        if self._options.count(value) > 0:
            self._options.remove(value)
        if self.CurrentIndex > len(self._options):
            self.CurrentIndex = len(self._options) - 1

class Settings(object):
    __no_setting_err = 'No setting with name: "{0}"'
    def __init__(self, loadFrom = None):
        #If loadFrom is a string, load as if it's a file
        #If loadFrom is a dict, update
        
        self.dict = {}
        self.LoadFrom(loadFrom)
        
    
    def LoadFrom(self, loadFrom):
        if loadFrom is None:
            return
        
        if hasattr(loadFrom, '__iter__'):
            self.dict.update(loadFrom)
            
        #Try loading from file (in case it supports open/close)
        else:
            added_settings = []
            try:
                config = ConfigParser.ConfigParser()
                config.read(levelFile)
                fields = config.sections()
                for field in fields:
                    name = ""
                    description = ""
                    default = None
                    selection = -1
                    options = []
                    try:
                        name = config.get(field, 'name')
                        description = config.get(field, 'description')
                        default = config.get(field, 'default')
                        selection = config.get(field, 'selection')
                        options = config.get(field, 'options')
                        options = list(Util.Formatting.str2tuple(options,str))
                    except:
                        pass
                    finally:
                        new_setting = Setting(name, description, 
                                              default, selection, options)
                    self.AddSetting(field, new_setting)
                    added_settings.append(field)
            except:
                for field in added_settings:
                    if self.HasSetting(field):
                        self.RemoveSetting(field)
    
    def __getitem__(self, key):
        if self.dict.has_key(key):
            return self.dict[key]
        else:
            raise KeyError(self.__no_setting_err.format(key))
        
    def __setitem__(self, key, value):
        self.dict[key] = value

    def HasSetting(self, key):
        return self.has_key(key)
    
    def has_key(self, key):
        try:
            return bool(self[key])
        except KeyError:
            return False

    def AddSetting(self, key, setting):
        self[key] = setting

    def RemoveSetting(self, key):
        if self.has_key(key):
            return self.dict.pop(key)
        else:
            raise KeyError(self.__no_setting_err.format(key))

    def AddOption(self, key, option):
        if self.has_key(key):
            self[key].AddOption(option)
        else:
            raise KeyError(self.__no_setting_err.format(key))

    def RemoveOption(self, key, option):
        if self.has_key(key):
            self[key].RemoveOption(option)
        else:
            raise KeyError(self.__no_setting_err.format(key))

    
