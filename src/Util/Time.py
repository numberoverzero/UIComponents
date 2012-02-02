"""
Functions related to displaying and comparing times
"""

import time
from math import floor

FMT_DATE = "%Y_%d_%m"
FMT_DATETIME = "%Y_%d_%m__%H_%M_%S"
FMT_TIME = "%H_%M_%S"
FMT_LOG_TIME = "%H:%M:%S"

def combine_time(hrs, mins, sec, ms): #pylint:disable-msg=C0103
    """Combines a time in hours, minutes, seconds, and ms into seconds"""
    return hrs * 3600 + mins * 60 + sec + ms / 1000.0

def _file_fmt(fmt, value):
    """Applies current time if no time provided,
        uses fmt as formatting string"""
    if not value: 
        value = time.localtime()
    return time.strftime(fmt, value)

def file_fmt_date(date_ = None):
    """Returns the date in MM_DD_YYYY format.
        Uses localtime if called without args.
        Make sure the passed arg has a strformat method."""
    fmt = FMT_DATE
    return _file_fmt(fmt, date_)

def file_fmt_datetime(datetime_ = None):
    """Returns the date and time in MM_DD_YYYY__HH_MM_SS format.
        Uses localtime if called without args.
        Make sure the passed arg has a strformat method."""
    fmt = FMT_DATETIME
    return _file_fmt(fmt, datetime_)

def file_fmt_time(time_ = None):
    """Returns the time in HH_MM_SS format.
        Uses localtime if called without args.
        Make sure the passed arg has a strformat method."""
    fmt = FMT_TIME
    return _file_fmt(fmt, time_)

def log_fmt_time(time_ = None):
    """Returns the time in HH:MM:SS format.
        Uses localtime if called without args.
        Make sure the passed arg has a strformat method."""
    fmt = FMT_LOG_TIME
    return _file_fmt(fmt, time_)

def split_time(sec):
    """Splits a time in seconds into hours, minutes, seconds, ms."""
    
    msec = 1000*sec - 1000*floor(sec)
    
    hrs, sec = divmod(sec, 3600)
    mins, sec = divmod(sec, 60)
    
    return int(hrs), int(mins), int(sec), int(msec)
