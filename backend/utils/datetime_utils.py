# Datetime utilities
from datetime import datetime

def get_utc_now():
    """Get current UTC time"""
    return datetime.utcnow()

def get_utc_timestamp():
    """Get UTC timestamp"""
    return datetime.utcnow().timestamp()

def format_utc_datetime(dt=None):
    """Format UTC datetime"""
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat()

