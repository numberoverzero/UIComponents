""""
Various file writers with performance profiles for specific implementations
"""

class BufferedWriter(object):
    """Writes lines to memory, then when it hits the buffer limit,
        writes memory to file.  Use neg BufferSize for full-file buffering.
        Use BufferSize = 0 for immediate writing."""
    def __init__(self, filename, buffer_size = -1):
        self._filename = filename
        self._buffer_size = buffer_size
        self._data = ""
    
    def _g_buffer_size(self):
        """Get buffer size"""
        return self._buffer_size
    def _s_buffer_size(self, value):
        """Set buffer size"""
        self._buffer_size = value
        self._check_buffer()
    BufferSize = property(_g_buffer_size, _s_buffer_size) 
    
    def _check_buffer(self, write_on_full = True):
        """Check the buffer for overflow, write memory to file if full."""
        was_full = is_full = False
        if (self.CurrentBufferSize >= self.BufferSize 
            and self.BufferSize >= 0):
            was_full = is_full = True
            if write_on_full:
                self._write_data_to_file()
                is_full = False
        return was_full, is_full
    
    def close(self):
        """Close the file, writing anything still in memory to file."""
        if self._data:
            self._write_data_to_file()
        self._buffer_size = None
        self._filename = None
        self._data = None
    
    def _g_c_buffer_size(self):
        """Get current buffer size"""
        return len(self._data)
    CurrentBufferSize = property(_g_c_buffer_size)
    
    def force_write_to_file(self):
        """Write memory to file, regardless of buffer size."""
        self._write_data_to_file()
   
    def __len__(self):
        """Same as CurrentBufferSize"""
        return len(self._data)
    
    def _write(self, data):
        """Write to memory, check for overflow"""
        self._data += data
        self._check_buffer()
    
    def _write_data_to_file(self):
        """Write memory to file, clear memory"""
        with open(self._filename, 'a', 8 << 10) as writefile:
            writefile.write(self._data)
        self._data = ""
             
    def write(self, data):
        """Write data to the buffer"""
        self._write(data)
        
    def writeln(self, data):
        """Write data to the buffer, appending a line return."""
        self._write(data + "\n")
