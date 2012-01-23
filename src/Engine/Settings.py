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
    def __init__(self, name="", description="",
                 default_index= -1, current_index= -1,
                 options=None):

        self._name = name
        self._description = description
        self._default_index = default_index
        self._current_index = current_index
        if options is None:
            self._options = []
        else:
            self._options = list(options)
    
    def add_option(self, value):
        """Adds the option to the list of options"""
        self._options.append(value)
        if len(self._options) == 1:
            self.current_index = 0
            
    def __g_current_index(self):
        """Returns the index of the current option"""
        if self._current_index < 0:
            if len(self._options) > 0:
                self._current_index = 0
        return self._current_index
    def __s_current_index(self, value):
        """Sets the index of the current option, safely. (In range)"""
        if len(self._options) == 0:
            value = -1
        else:
            value %= len(self._options)
        self._current_index = value
    current_index = property(__g_current_index, __s_current_index)
    
    def __g_current_option(self):
        """Returns the current option of the setting"""
        return self._options[self.current_index]
    def __s_current_option(self, value):
        """Sets the current option of the setting.
            If option is not a valid option, does not make a change"""
        if value in self._options:
            self._current_index = self._options.index(value)
        else:
            raise KeyError(self.__no_opt_err.format(value))            
    current_option = property(__g_current_option, __s_current_option)
    
    def __g_default_index(self):
        """Returns the index of the default option for the setting"""
        return self._default_index
    def __s_default_index(self, value):
        """Set the index of the default option for the setting, 
                safely. (In range)"""
        if len(self._options) == 0:
            value = -1
        value %= len(self._options)
        self._default_index = value
    default_index = property(__g_default_index, __s_default_index)
    
    def __g_default_option(self):
        """Returns the default option of the setting"""
        return self._options[self.default_index]
    def __s_default_option(self, value):
        """Sets the default option of the setting.
            If value is not a valid option, does not make a change"""
        if value in self._options:
            self._default_index = self._options.index(value)
        else:
            raise KeyError(self.__no_opt_err.format(value))            
    default_option = property(__g_default_option, __s_default_option)
    
    def __g_description(self):
        """Gets the string description of the setting"""
        return self._description
    def __s_description(self, value):
        """Sets the description of the setting- no checking"""
        self._description = value
    description = property(__g_description, __s_description)
    
    def _get_index(self, value):
        """Returns the index of the value in options. 
            Raises key error when value not in options."""
        err = None
        index = -1
        
        if not self._options:
            err = "No values loaded in options."
        elif value in self._options:
            index = self._options.index(value)
        else:
            err = "Could not find option {} in self.options".format(value)
        
        if err:
            raise KeyError(err)
        else:
            return index
    
    def load(self, config, name = None):
        """Load a setting from a config file.
            Name only needs to be passed when the Setting doesn't
            have a remembered filename.  In case the setting
            has a self._name and a name is passed, the passed name is
            taken as more current.  self._name is NOT updated to name,
            unless self._name is None."""
        section = self._resolve_name(name)
            
        description = config.get(section, 'description')
        default_value = config.get(section, 'default_option')
        current_value = config.get(section, 'current_option')
        options_str = config.get(section, 'options')
        options_lst = list(Util.Formatting.str_to_struct(options_str, str))
        
        self._options = options_lst[:]
        self.description = description
        
        
        self.default_index = self._get_index(default_value)
        self.current_index = self._get_index(current_value)
    
    def __g_name(self):
        """The name of the setting"""
        return self._name
    def __s_name(self, value):
        """Set the setting's name"""
        self._name = value
    name = property(__g_name, __s_name)
    
    def __g_next_option(self):
        """Gets the next option"""
        index = (self.current_index + 1) % len(self._options)
        return self._options[index]
    next_option = property(__g_next_option)
               
    def __g_nopts(self):
        """The number of options the setting has"""
        return len(self._options)
    nopts = property(__g_nopts)

    def __g_options(self):
        """A copy of the setting's options"""
        return self._options[:]
    options = property(__g_options)
    
    def __g_previous_option(self):
        """Gets the previous option"""
        index = (self.current_index - 1) % len(self._options)
        return self._options[index]
    previous_option = property(__g_previous_option)
    
    def _resolve_name(self, name):
        """Updates (if needed) the setting's name,
            and returns the proper name to use.
            raises AttributeError if neither name is good"""
        if name:
            self._name = name
        else:
            if self._name:
                name = self._name
            else:
                raise AttributeError("No name specified.")
        return name

    def remove_option(self, value):
        """Removes an option from the options, and
            updates the current selection as needed."""
        if value in self._options:
            self._options.remove(value)
        if self.current_index >= len(self._options):
            self.current_index = len(self._options) - 1
    
    def save(self, config, name = None):
        """Save the setting to a config file.
            Name only needs to be passed when the Setting doesn't
            have a remembered filename.  In case the setting
            has a self._name and a name is passed, the passed name is
            taken as more current.  self._name is NOT updated to name,
            unless self._name is None."""
        section = self._resolve_name(name)
            
        if not config.has_section(section):
            config.add_section(section)
        
        config.set(section, 'description', self._description)
        config.set(section, 'default_option', str(self.default_option))
        config.set(section, 'current_option', str(self.current_option))
        options_str = Util.Formatting.struct_to_str(self._options)
        config.set(section, 'options', options_str)
            
class Settings(object):
    """Manages multiple settings, including loading and saving from/to
        config files.  Makes building and passing 
        around a group of settings easy."""
    __no_setting_err = 'No setting with name: "{0}"'
    
    def __init__(self, fp=None): #pylint:disable-msg=C0103
        self.__fp = fp
        self.dict = {}

    def add_option(self, key, option):
        """Adds an option to a setting.  The new option is added to the end
                of the list of options.  Raises KeyError if there is no
                such setting in self.dict"""
        if self.has_setting(key):
            self[key].add_option(option)
        else:
            raise KeyError(self.__no_setting_err.format(key))

    def add_setting(self, key, setting):
        """Adds a setting to the dict of settings.
            If an entry with key = key already exists, it is replaced."""
        self[key] = setting
    
    def __getitem__(self, key):
        if self.has_setting(key):
            return self.dict[key]
        else:
            raise KeyError(self.__no_setting_err.format(key))
        
    def has_setting(self, key):
        """Check if the setting with name 'key' exists."""
        return self.dict.has_key(key)
    
    def __len__(self):
        return len(self.dict)
    
    def load(self, fp=None): #pylint:disable-msg=C0103
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
                fp = self.__fp #pylint:disable-msg=C0103
        else:
            self.__fp = fp
            
        opened = True
        #Try to open fp, if it's an openable file
        try:
            open_file = open(fp)
        except IOError:
            opened = False
        else:
            fp = open_file  #pylint:disable-msg=C0103
        
        config = ConfigParser.ConfigParser()
        config.readfp(fp)
        sections = config.sections()
        for section in sections:
            new_setting = Setting()
            new_setting.load(config, section)
            self.add_setting(section, new_setting)
                
        if opened:
            fp.close()
    
    def remove_option(self, key, option):
        """Removes an option from the specified setting.
            Raises KeyError if there is no such setting 
            with key = key."""
        if self.has_setting(key):
            self[key].remove_option(option)
        else:
            raise KeyError(self.__no_setting_err.format(key))
    
    def remove_setting(self, key):
        """Removes the setting with key = key from the dict of settings.
            Raises KeyError if there is no entry with that key."""
        if self.has_setting(key):
            return self.dict.pop(key)
        else:
            raise KeyError(self.__no_setting_err.format(key))
    
    def save(self, fp=None): # pylint: disable-msg=C0103
        """If the settings were loaded from a file and no
               filename is specified, saves to same place it was loaded from."""
        if fp is None:
            if self.__fp is None:
                raise AttributeError("No save location specified.")
            else:
                fp = self.__fp # pylint: disable-msg=C0103
        else:
            self.__fp = fp
        
        config = ConfigParser.ConfigParser()
        sections = self.dict.keys()
        for section in sections:
            self.dict[section].save(config, section)
        
        opened = True
        #Try to open fp, if it's an openable file
        try:
            open_file = open(fp, 'w')
        except IOError:
            opened = False
        else:
            fp = open_file  #pylint:disable-msg=C0103
        
        config.write(fp)
        
        if opened:
            open_file.close()
    
    def __setitem__(self, key, value):
        self.dict[key] = value
        
    def __g_settings(self):
        """Returns a list of the contained settings."""
        return self.dict.values()
    settings = property(__g_settings)
    
