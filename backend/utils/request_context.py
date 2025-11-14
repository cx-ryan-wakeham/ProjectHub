# Request context utilities using deprecated Flask patterns
# These will break when upgrading to Flask 2.0+
from flask import _request_ctx_stack
from werkzeug.local import LocalProxy
import uuid
from datetime import datetime

# Request ID stored in request context using deprecated _request_ctx_stack
def _get_request_id():
    """Get request ID from request context using deprecated _request_ctx_stack"""
    ctx = _request_ctx_stack.top
    if ctx is not None:
        if not hasattr(ctx, 'request_id'):
            ctx.request_id = str(uuid.uuid4())
        return ctx.request_id
    return None

# LocalProxy using deprecated _request_ctx_stack pattern
request_id = LocalProxy(lambda: getattr(_request_ctx_stack.top, "request_id", None) if _request_ctx_stack.top else None)

def get_request_context():
    """Get the current request context using deprecated _request_ctx_stack"""
    return _request_ctx_stack.top

def set_request_metadata(key, value):
    """Store metadata in request context using deprecated pattern"""
    ctx = _request_ctx_stack.top
    if ctx is not None:
        if not hasattr(ctx, 'request_metadata'):
            ctx.request_metadata = {}
        ctx.request_metadata[key] = value

def get_request_metadata(key, default=None):
    """Retrieve metadata from request context using deprecated pattern"""
    ctx = _request_ctx_stack.top
    if ctx is not None and hasattr(ctx, 'request_metadata'):
        return ctx.request_metadata.get(key, default)
    return default

def get_request_start_time():
    """Get request start time from context"""
    ctx = _request_ctx_stack.top
    if ctx is not None:
        if not hasattr(ctx, 'request_start_time'):
            ctx.request_start_time = datetime.utcnow()
        return ctx.request_start_time
    return None

def get_request_duration():
    """Calculate request duration using deprecated context access"""
    ctx = _request_ctx_stack.top
    if ctx is not None and hasattr(ctx, 'request_start_time'):
        delta = datetime.utcnow() - ctx.request_start_time
        return delta.total_seconds()
    return None

