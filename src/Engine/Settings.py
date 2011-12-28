"""
Classes for reading.writing from settings files,
and managing selection index/default index
"""

import ConfigParser
import Util

class Setting(object):
    """A setting option, with defaults, index, list of options,
        name, and description."""
    __no_opt_err = "Tried to set current to option not in list: {0}"
    def __init__(self, name = "", description = "",
                 default = -1, selection = -1,
                 options = None):

        self._name = name
        self._description = description
        self._default = default
        self._selection = selection
        if options is None:
            self._options = []
        else:
            self._options = options[:]

    def __gCurrentIndex(self): # pylint: disable-msg=C0103
        """Returns the current index of the selection"""
        return self._selection
    def __sCurrentIndex(self, value): # pylint: disable-msg=C0103
        """Sets the current index of the selection, safely. (In range)"""
        value %= len(self._options)
        self._selection = value
    current_index = property(__gCurrentIndex)

    def __gDefault(self): # pylint: disable-msg=C0103
        """Returns the default value for the setting"""
        return self._default
    def __sDefault(self, value): # pylint: disable-msg=C0103
        """Set the default value for the setting, safely. (In range)"""
        value %= len(self._options)
        self._default = value
    default = property(__gDefault, __sDefault)
    
    def __gDescription(self): # pylint: disable-msg=C0103
        return self._default
    def __sDescription(self, value): # pylint: disable-msg=C0103
        self._description = value
    description = property(__gDescription, __sDescription)

    def __gCurrent(self): # pylint: disable-msg=C0103
        if len(self._options) < 1:
            return None
        else:
            return self._options[self.current_index]

    def __sCurrent(self, value): # pylint: disable-msg=C0103
        if value not in self._options:
            raise KeyError(self.__no_opt_err.format(value))
        else:
            self.current_index = self._options.index(value)

    def __gPrevious(self): # pylint: disable-msg=C0103
        index = (self.current_index-1)%len(self._options)
        return self._options[index]
    def __gNext(self): # pylint: disable-msg=C0103
        index = (self.current_index+1)%len(self._options)
        return self._options[index]

    current = property(__gCurrent, __sCurrent)
    previous_option = property(__gPrevious)
    next_option = property(__gNext)

    def add_option(self, value):
        self._options.append(value)
        if len(self._options) == 1:
            self.current_index = 0

    def remove_option(self, value):
        if self._options.count(value) > 0:
            self._options.remove(value)
        if self.current_index > len(self._options):
            self.current_index = len(self._options) - 1
    
    def load_using_config_parser(self, config, name = None):
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
            options = list(Util.Formatting.str_to_tuple(options_str, str))
        except: # pylint: disable-msg=W0702
            #This is terrible code.  I dislike I/O
            pass
        finally:
            self._options = options[:]
            self.description = description
            self.default = default
            self.current_index = selection
    load = load_using_config_parser
    
    def save_using_config_parser(self, config, name = None):
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
    save = save_using_config_parser
        
class Settings(object):
    __no_setting_err = 'No setting with name: "{0}"'
    def __init__(self, filename = None):
        
        self.__filename = filename
        self.dict = {}
    
    def load(self, filename):
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
                        new_setting.load_using_config_parser(config, section)
                        self.add_setting(section, new_setting)
                        added_settings.append(section)
                except: # pylint: disable-msg=W0702
                    #If there was an exception while loading,
                        #undo all added fields
                    for section in added_settings:
                        if self.has_setting(section):
                            self.remove_setting(section)
    
    def save(self, filename = None):
        """If the settings were loaded from a file and no
               filename is specified, saves to same place it was loaded at."""
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
            self.dict[section].save_using_config_parser(config, section)
        
        
    def __getitem__(self, key):
        if self.dict.has_key(key):
            return self.dict[key]
        else:
            raise KeyError(self.__no_setting_err.format(key))
        
    def __setitem__(self, key, value):
        self.dict[key] = value

    def has_setting(self, key):
        return self.has_key(key)
    
    def has_key(self, key):
        try:
            return bool(self[key])
        except KeyError:
            return False

    def add_setting(self, key, setting):
        self[key] = setting

    def remove_setting(self, key):
        if self.has_key(key):
            return self.dict.pop(key)
        else:
            raise KeyError(self.__no_setting_err.format(key))

    def add_option(self, key, option):
        if self.has_key(key):
            self[key].add_option(option)
        else:
            raise KeyError(self.__no_setting_err.format(key))

    def remove_option(self, key, option):
        if self.has_key(key):
            self[key].remove_option(option)
        else:
            raise KeyError(self.__no_setting_err.format(key))

    
