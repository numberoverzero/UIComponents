"""
Input/Output utility classes and functions
"""
import time

FMT_DATE = "%Y_%d_%m"
FMT_DATETIME = "%Y_%d_%m__%H_%M_%S"
FMT_TIME = "%H_%M_%S"

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

