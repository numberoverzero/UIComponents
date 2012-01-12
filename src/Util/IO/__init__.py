"""
Input/Output utility classes and functions
"""
import time

def file_fmt_date(date_ = None):
    """Returns the date in MM_DD_YYYY format.
        Uses localtime if called without args.
        Make sure the passed arg has a strformat method."""
    fmt = "%Y_%d_%m"
    if not date_: 
        date_ = time.localtime()
    return time.strftime(fmt, date_)

def file_fmt_time(time_ = None):
    """Returns the time in HH_MM_SS format.
        Uses localtime if called without args.
        Make sure the passed arg has a strformat method."""
    fmt = "%H_%M_%S"
    if not time_: 
        time_ = time.localtime()
    return time.strftime(fmt, time_)

def file_fmt_datetime(datetime_ = None):
    """Returns the date and time in MM_DD_YYYY__HH_MM_SS format.
        Uses localtime if called without args.
        Make sure the passed arg has a strformat method."""
    fmt = "%Y_%d_%m__%H_%M_%S"
    if not datetime_: 
        datetime_ = time.localtime()
    return time.strftime(fmt, datetime_)