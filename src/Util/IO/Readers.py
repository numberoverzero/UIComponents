""""
Various file readers with performance profiles for specific implementations
"""

import os.path

class FullBufferedRead(object):
    """Reads an entire file into memory,
        allowing line-indexed searching.
        First index is 0, NOT 1"""
    def __init__(self, filename):
        self._lines = []
        self._is_loaded = False
        self._filename = filename
        self.reload_file()
    
    def clear(self):
        """Clear the file from memory"""
        self._lines = None
        self._is_loaded = False
        
    def __getitem__(self, key):
        """Returns the line at the specified index"""
        if not self._is_loaded:
            err = "Error: tried to read a line on an unloaded file."
            raise IOError(err)
        else:
            return self._lines[key]
    
    def __len__(self):
        """Returns the number of lines in the file"""
        if not self._is_loaded:
            return 0
        else:
            return len(self._lines)
    
    def _load_file(self):
        """Load the file into memory."""
        
        #Clear out any existing data
        self._lines = []
        
        #Load the file
        with open(self._filename, 'r', 8 << 10) as open_file:
            for line in open_file:
                self._lines.append(line)
        
        self._is_loaded = True
        
    def reload_file(self):
        """Reload the file into memory."""
        err_msg = None
        if (not hasattr(self, '_filename') 
            or self._filename is None):
            err_msg = "No file specified"
        elif not os.path.isfile(self._filename):
            err_msg = "File not found. ({})".format(self._filename)
        
        if err_msg:
            raise IOError(err_msg)
        else:
            self._load_file()
        
            