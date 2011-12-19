import ConfigParser
import Util

class Setting(object):
    __no_opt_err = "Tried to set current to option not in list: {0}"
    def __init__(self, name = "", description = "",
                 default = -1, selection = -1,
                 options = []):

        self._name = name
        self._description = description
        self._default = default
        self._selection = selection
        self._options = options[:]

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
    
    def LoadUsingConfigParser(self, config, name = None):
        if name is None:
            if self._name is None:
                raise AttributeError("No section name specified.") 
            else:
                section = self._name
        else:
            section = name
            
        try:
            description = config.get(section, 'description')
            default = int(config.get(section, 'default'))
            selection = int(config.get(section, 'selection'))
            options_str = config.get(section, 'options')
            options = list(Util.Formatting.str2tuple(options_str,str))
        except:
            #This is terrible code.  I dislike I/O
            pass
        finally:
            self._description = description
            self._default = default
            self._options = options[:]
    
    def SaveUsingConfigParser(self, config, name = None):
        if name is None:
            if self._name is None:
                raise AttributeError("No section name specified.") 
            else:
                section = self._name
        else:
            section = name
            
        if not config.has_section(section):
            config.add_section(section)
        
        config.set(section, 'description', self._description)
        config.set(section, 'default', str(self._default))
        config.set(section, 'selection', str(self._selection))
        config.set(section, 'options', str(self._options))
        
class Settings(object):
    __no_setting_err = 'No setting with name: "{0}"'
    def __init__(self, filename = None):
        
        self.__filename = filename
        self.dict = {}
    
    def Load(self, filename):
        if filename is None:
            if self.__filename is None:
                return
            else:
                filename = self.__filename
        else:
            if hasattr(filename, '__iter__'):
                #Not a string pointing to the file, don't update self.__filename
                self.dict.update(filename)
            else:
                self.__filename = filename

                #Try loading from file (in case it supports open/close)
                added_settings = []
                try:
                    config = ConfigParser.ConfigParser()
                    config.read(filename)
                    sections = config.sections()
                    for section in sections:
                        new_setting = Setting()
                        new_setting.LoadUsingConfigParser(config, section)
                        self.AddSetting(section, new_setting)
                        added_settings.append(section)
                except:
                    #If there was an exception while loading,
                        #undo all added fields
                    for section in added_settings:
                        if self.HasSetting(section):
                            self.RemoveSetting(section)
    
    def Save(self, filename = None):
        """If the settings were loaded from a file and no
            filename is specified, saves to the same place it was loaded from."""
        if filename is None:
            if self.__filename is None:
                raise AttributeError("No save location specified.")
            else:
                filename = self.__filename
        else:
            filename = self.__filename
        
        config = ConfigParser.ConfigParser()
        config.write(filename)
        sections = self.dict.keys()
        for section in sections:
            self.dict[section].SaveUsingConfigParser(config, section)
        
        
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

    
