# Jinja2 template filters using deprecated contextfilter decorator
# These will break when upgrading to Jinja2 3.0+ (contextfilter replaced with pass_context)
from jinja2 import contextfilter
from datetime import datetime
import hashlib

@contextfilter
def format_datetime(context, value, format='%Y-%m-%d %H:%M:%S'):
    """Format datetime using deprecated contextfilter decorator"""
    if value is None:
        return ''
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    return value.strftime(format)

@contextfilter
def user_display_name(context, user):
    """Get user display name from context"""
    if isinstance(user, dict):
        return user.get('username', user.get('email', 'Unknown'))
    return getattr(user, 'username', getattr(user, 'email', 'Unknown'))

@contextfilter
def truncate(context, value, length=50):
    """Truncate string with ellipsis"""
    if not value:
        return ''
    if len(value) <= length:
        return value
    return value[:length] + '...'

@contextfilter
def md5_hash(context, value):
    """Generate MD5 hash (for demonstration purposes)"""
    if not value:
        return ''
    return hashlib.md5(str(value).encode()).hexdigest()

@contextfilter
def request_id_filter(context):
    """Get request ID from context using deprecated pattern"""
    from utils.request_context import get_request_context
    ctx = get_request_context()
    if ctx and hasattr(ctx, 'request_id'):
        return ctx.request_id
    return 'N/A'

@contextfilter
def format_file_size(context, size_bytes):
    """Format file size in human-readable format"""
    if not size_bytes:
        return '0 B'
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

@contextfilter
def role_badge(context, role):
    """Generate role badge HTML"""
    role_colors = {
        'admin': 'danger',
        'project_manager': 'primary',
        'team_member': 'secondary'
    }
    color = role_colors.get(role, 'secondary')
    return f'<span class="badge badge-{color}">{role}</span>'

