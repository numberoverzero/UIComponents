"""
Input/Output utility classes and functions
"""
import os
import os.path
import Readers
import Writers

def bufcount(filename):
    """Counts the number of lines in a file quickly.
    
        Code from (with minor change):
        http://stackoverflow.com/
        questions/845058/how-to-get-line-count-cheaply-in-python
    """
    
    with open(filename) as fname:                  
        lines = 0
        buf_size = 1024 * 1024
        read_f = fname.read # loop optimization
    
        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)
    return lines

def ensdir(path):
    """Ensures that the folder exists.  
        If the folder does not, trys to create it.
        Raises IOError if the folder can't be created."""
    if not os.path.exists(path):
        os.mkdir(path)

def ensfile(filename):
    """Ensures that the file exists.
        If the file does not, trys to create it.
        Raises IOError if the file can't be created."""
    path = os.path.split(filename)[0]
    ensdir(path)
    if not os.path.exists(filename):
        open(filename, 'w').close()
