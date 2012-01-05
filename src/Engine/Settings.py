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
        self._default_index = default
        self._selection = selection
        if options is None:
            self._options = []
        else:
            self._options = list(options)

    def __g_current_index(self):
        """Returns the current index of the selection"""
        if self._selection < 0:
            if len(self._options) > 0:
                self._selection = 0
        return self._selection
    def __s_current_index(self, value):
        """Sets the current index of the selection, safely. (In range)"""
        if len(self._options) == 0:
            value = -1
        else:
            value %= len(self._options)
        self._selection = value
    current_index = property(__g_current_index, __s_current_index)

    def __g_default_index(self):
        """Returns the default value for the setting"""
        return self._default_index
    def __s_default_index(self, value):
        """Set the default value for the setting, safely. (In range)"""
        value %= len(self._options)
        self._default_index = value
    default_index = property(__g_default_index, __s_default_index)
    
    def __g_description(self):
        """Gets the string description of the setting"""
        return self._description
    def __s_description(self, value):
        """Sets the description of the setting- no checking"""
        self._description = value
    description = property(__g_description, __s_description)

    def __g_current_option(self):
        """Gets the current selection item, if there can be one.
                If there are no items, returns None"""
        if len(self._options) < 1:
            return None
        else:
            return self._options[self.current_index]
    def __s_current_option(self, value):
        """Only sets the current item if the requested new current
            is one of the options.  If the specified item isn't,
            raises KeyError"""
        if value not in self._options:
            raise KeyError(self.__no_opt_err.format(value))
        else:
            self.current_index = self._options.index(value)
    current_option = property(__g_current_option, __s_current_option)
    
    def __g_previous_option(self):
        """Gets the previous option"""
        index = (self.current_index-1)%len(self._options)
        return self._options[index]
    def __g_next_option(self):
        """Gets the next option"""
        index = (self.current_index+1)%len(self._options)
        return self._options[index]
    previous_option = property(__g_previous_option)
    next_option = property(__g_next_option)

    def add_option(self, value):
        """Adds the option to the list of options"""
        self._options.append(value)
        if len(self._options) == 1:
            self.current_index = 0

    def remove_option(self, value):
        """Removes an option from the options, and
            updates the current selection as needed."""
        if Util.contains(self._options, value):
            self._options.remove(value)
        if self.current_index >= len(self._options):
            self.current_index = len(self._options) - 1
    
    def __g_options(self):
        """Return a copy of the options"""
        return self._options[:]
    
    options = property(__g_options)
    
    def load_using_config_parser(self, config, name = None):
        """Load a setting from a config file.
            Name only needs to be passed when the Setting doesn't
            have a remembered filename.  In case the setting
            has a self._name and a name is passed, the passed name is
            taken as more current.  self._name is NOT updated to name,
            unless self._name is None."""
            
        if name is None:
            if self._name is None:
                raise AttributeError("No section name specified.") 
            else:
                section = self._name
        else:
            section = name
            
        try:
            description = config.get(section, 'description')
            default_index = int(config.get(section, 'default'))
            selection = int(config.get(section, 'selection'))
            options_str = config.get(section, 'options')
            options = list(Util.Formatting.str_to_tuple(options_str, str))
        except: # pylint: disable-msg=W0702
            #This is terrible code.  I dislike I/O
            pass
        finally:
            self._options = options[:]
            self.description = description
            self.default_index = default_index
            self.current_index = selection
    load = load_using_config_parser
    
    def save_using_config_parser(self, config, name = None):
        """Save the setting to a config file.
            Name only needs to be passed when the Setting doesn't
            have a remembered filename.  In case the setting
            has a self._name and a name is passed, the passed name is
            taken as more current.  self._name is NOT updated to name,
            unless self._name is None."""
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
        config.set(section, 'default', str(self._default_index))
        config.set(section, 'selection', str(self._selection))
        config.set(section, 'options', str(self._options))
    save = save_using_config_parser
    
    def __len__(self):
        return len(self._options)
        
class Settings(object):
    """Manages multiple settings, including loading and saving from/to
        config files.  Makes building and passing 
        around a group of settings easy."""
    __no_setting_err = 'No setting with name: "{0}"'
    def __init__(self, fp=None):
        self.__fp = fp
        self.dict = {}
    
    def load(self, fp=None):
        """Load settings from a config file or file-like object.
            The file-like object should support readline() and write().
            Filename only needs to be passed when the Settings doesn't
            have a remembered filename.  In case the settings
            has a self.__filename and a filename is passed, the passed 
            filename is taken as more current.  self.__filename is 
            NOT updated to name, unless self.__filename is None."""
        if fp is None:
            if self.__fp is None:
                raise AttributeError("No save location specified.")
            else:
                fp = self.__fp
        else:
            self.__fp = fp
            
        opened = True
        #Try to open fp, if it's an openable file
        try:
            open_file = open(fp)
        except IOError:
            opened = False
            
        #Try loading from file (in case it supports open/close)
        added_settings = []
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(fp)
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
        
        if opened:
            open_file.close()
    
    def save(self, fp=None):
        """If the settings were loaded from a file and no
               filename is specified, saves to same place it was loaded from."""
        if fp is None:
            if self.__fp is None:
                raise AttributeError("No save location specified.")
            else:
                fp = self.__fp
        else:
            self.__fp = fp
        
        config = ConfigParser.ConfigParser()
        sections = self.dict.keys()
        for section in sections:
            self.dict[section].save_using_config_parser(config, section)
        
        opened = True
        #Try to open fp, if it's an openable file
        try:
            open_file = open(fp, 'w')
        except IOError:
            opened = False
        
        config.write(fp)
        
        if opened:
            open_file.close()
        
    def __getitem__(self, key):
        if self.dict.has_key(key):
            return self.dict[key]
        else:
            raise KeyError(self.__no_setting_err.format(key))
        
    def __setitem__(self, key, value):
        self.dict[key] = value

    def has_setting(self, key):
        """Check if the setting with name 'key' exists.
            Alias for has_key"""
        return self.has_key(key)
    
    def has_key(self, key):
        """Same as has_setting(key), passes through the has_key
                to the underlying dict of (str(name), setting)."""
        return self.dict.has_key(key) 

    def add_setting(self, key, setting):
        """Adds a setting to the dict of settings.
            If an entry with key = key already exists, it is replaced."""
        self[key] = setting

    def remove_setting(self, key):
        """Removes the setting with key = key from the dict of settings.
            Raises KeyError if there is no entry with that key."""
        if self.has_key(key):
            return self.dict.pop(key)
        else:
            raise KeyError(self.__no_setting_err.format(key))

    def add_option(self, key, option):
        """Adds an option to a setting.  The new option is added to the end
                of the list of options.  Raises KeyError if there is no
                such setting in self.dict"""
        if self.has_key(key):
            self[key].add_option(option)
        else:
            raise KeyError(self.__no_setting_err.format(key))

    def remove_option(self, key, option):
        """Removes an option from the specified setting.
            Raises KeyError if there is no such setting 
            with key = key."""
        if self.has_key(key):
            self[key].remove_option(option)
        else:
            raise KeyError(self.__no_setting_err.format(key))
        
    def __len__(self):
        return len(self.dict)
    
