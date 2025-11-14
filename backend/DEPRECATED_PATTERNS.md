# Deprecated Patterns Introduced for Upgrade Testing

This document lists the deprecated Flask/Jinja2 patterns intentionally introduced into the codebase. These patterns will **break** when upgrading to:
- Flask 2.0+ (removes `_request_ctx_stack`)
- Jinja2 3.0+ (replaces `contextfilter` with `pass_context`)

## Purpose

These patterns are intentionally introduced to create technical debt that will require refactoring during upgrades. This serves as a learning exercise for handling breaking changes in dependencies.

## Deprecated Patterns Used

### 1. `_request_ctx_stack` (Flask)

**Location**: `backend/utils/request_context.py`

**Pattern**:
```python
from flask import _request_ctx_stack

ctx = _request_ctx_stack.top
```

**Usage**:
- Request ID tracking
- Request metadata storage
- Request duration calculation
- Context access in utilities

**Breaking Change**: Removed in Flask 2.2. Must migrate to `g` object or `has_request_context()`.

**Files Using This**:
- `backend/utils/request_context.py` - Core utility module
- `backend/app.py` - Request initialization
- `backend/utils/logger.py` - Logging with request context
- `backend/routes/api.py` - Route handlers

### 2. `LocalProxy` with `_request_ctx_stack` (Flask)

**Location**: `backend/utils/request_context.py`

**Pattern**:
```python
from werkzeug.local import LocalProxy
from flask import _request_ctx_stack

request_id = LocalProxy(lambda: getattr(_request_ctx_stack.top, "request_id", None))
```

**Usage**:
- Thread-local request ID access
- Request-scoped variables

**Breaking Change**: Must use Flask's `g` object instead.

**Files Using This**:
- `backend/utils/request_context.py`
- `backend/utils/logger.py`

### 3. `@contextfilter` (Jinja2)

**Location**: `backend/utils/jinja_filters.py`

**Pattern**:
```python
from jinja2 import contextfilter

@contextfilter
def my_filter(context, value):
    return process(context, value)
```

**Usage**:
- Custom template filters that need context
- Date/time formatting
- User display name formatting
- Request ID in templates
- File size formatting
- Role badge generation

**Breaking Change**: Replaced with `@pass_context` in Jinja2 3.0+.

**Files Using This**:
- `backend/utils/jinja_filters.py` - All filter definitions
- `backend/app.py` - Filter registration
- `backend/templates/error.html` - Template usage
- `backend/templates/admin.html` - Template usage

## Integration Points

### Request Context Initialization
- **File**: `backend/app.py`
- **Function**: `init_request_context()`
- Uses `_request_ctx_stack.top` to initialize request metadata

### Logging System
- **File**: `backend/utils/logger.py`
- All logging functions use `request_id` LocalProxy
- Access request context for IP addresses and metadata

### Template System
- **Files**: `backend/templates/*.html`
- All templates use filters decorated with `@contextfilter`
- Error pages and admin dashboard rely on deprecated filters

### API Routes
- **File**: `backend/routes/api.py`
- Example route (`get_users`) demonstrates deprecated pattern usage

## Migration Path (For Future Reference)

When upgrading Flask:
1. Replace `_request_ctx_stack.top` with `g` object
2. Replace `LocalProxy` with `g` attributes
3. Use `has_request_context()` for context checks

When upgrading Jinja2:
1. Replace `@contextfilter` with `@pass_context`
2. Update filter signatures to use `pass_context` pattern
3. Update filter calls in templates if needed

## Testing

To verify these patterns work with current versions:
- Flask 1.1.4: ✅ Works
- Jinja2 2.11.3: ✅ Works

To test breaking changes:
- Upgrade to Flask 2.0+: ❌ Will break
- Upgrade to Jinja2 3.0+: ❌ Will break

