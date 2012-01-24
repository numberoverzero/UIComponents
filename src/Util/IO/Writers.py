""""
Various file writers with performance profiles for specific implementations
"""

import Util.IO
import Util.Time
import functools

class BufferedWriter(object):
    """
    Writes lines to memory, dumps to file when buffer is full.
    
    Use neg buffer_size for full-file buffering.
    Use buffer_size = 0 for immediate writing.
    """
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

class Logger(object):
    """
    Used for logging info to a logfile.
    
    To log execution of something, you can do any of the following:
        - use the log_func_time decorator
        - 1) call your_logger.start()
          2) execute the code
          3) call your_logger.stop()
          4) call your_logger.log_message_with_elapsed("message")
        - log_message_with_time to simply log the current time and a statement
        - log_message to log without any timing information
    """
    
    def __init__(self, filename):
        self.filename = filename
        self.next_tid = [0, 0]
        self.time_start = {}
        self.time_end = {}
        self.last_tid = None
        
    def start(self, tid=None):
        """Start a timer.  tid is a timer id.
            Leaving tid blank gives you the next timer, which is a good idea
            for logging sequential events."""
        if tid is None:
            tid = self.next_tid[0]
            self.next_tid[0] += 1
            self.next_tid[1] = self.next_tid[0]
        self.time_start[tid] = Util.Time.time.time()
        return tid

    def stop(self, tid=None):
        """stop a timer.  tid is a timer id.
            Leaving tid blank uses the next timer, which is a good idea
            for logging sequential events."""
        if tid is None:
            for ptid in xrange(self.next_tid[1] - 1, -1, -1):
                if ptid not in self.time_end:
                    tid = ptid
                    break
            if tid is None:
                tid = self.next_tid[1]
            self.next_tid[1] -= 1
        self.time_end[tid] = Util.Time.time.time()
        self.last_tid = tid
        return tid

    def log_message(self, msg, out = False):
        """Log a message."""
        with open(self.filename, 'a') as log:
            log.write(msg+'\n')
            if out: 
                print msg

    def log_message_with_time(self, msg, out = False):
        """Log a message, prepended with the time."""
        now = Util.Time.log_fmt_time()
        self.log_message(now + " " + msg, out)

    def log_message_with_elapsed(self, msg, out = False, tid = None):
        """Log a message, with elapsed time appended.
            If no tid is provided, uses the last tid from stop() 
                as time information."""
        if tid is None:
            tid = self.last_tid
        try:
            dtime = self.time_end[tid] - self.time_start[tid]
        except: #pylint:disable-msg=W0702
            dtime = 0
            
        hrs, mins, sec, msec = Util.Time.split_time(dtime)
        msg += " ({:02}:{:02}:{:02}::{:03})".format(hrs, mins, sec, msec)
        
        self.log_message(msg, out)

    def log_func_time(self, func):
        """Wrapper for logging a function's execution time 
            every time it is run."""
        
        @functools.wraps(func)
        def wrapper(*arg, **kwargs): #pylint:disable-msg=C0111
            tid = func.func_name
            self.start(tid)
            res = func(*arg, **kwargs)
            self.stop(tid)
            msg = "{} complete".format(tid)
            self.log_message_with_elapsed(msg, tid)
            return res
        return wrapper

def make_log(name, use_date = True):
    """Make a logfile with name "{name}_{datetime}" if use_date
        otherwise makes a log file with name "{name}".
        name should be the FULL PATH (without extension)"""
    now = Util.Time.file_fmt_datetime()
    ext = '.log'

    if use_date:
        filename = name + "_" + now
    else:
        filename = name
    
    filename += ext
        
    Util.IO.ensfile(filename)
    return Logger(filename)