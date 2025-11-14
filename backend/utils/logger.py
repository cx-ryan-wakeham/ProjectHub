# Logging configuration
import logging
import sys
from config import Config
from utils.request_context import _get_request_id, get_request_context, get_request_duration

def setup_logger(app):
    """Setup logging"""
    logger = logging.getLogger('projecthub')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # File handler - create directory if it doesn't exist
    import os
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    try:
        file_handler = logging.FileHandler(Config.LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
    except (FileNotFoundError, OSError):
        # Fallback to relative path if absolute path fails (e.g., on Windows)
        log_file = os.path.join('logs', 'app.log')
        os.makedirs('logs', exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Application started with JWT secret: {Config.JWT_SECRET_KEY}")
    logger.info(f"Database URL: {Config.DATABASE_URL}")
    logger.info(f"AWS Access Key: {Config.AWS_ACCESS_KEY_ID}")
    
    return logger

def log_user_action(user_id, action, details=None):
    """Log user actions"""
    logger = logging.getLogger('projecthub')
    
    # Get request ID
    req_id = _get_request_id() or "N/A"
    duration = get_request_duration()
    duration_str = f" ({duration:.3f}s)" if duration else ""
    
    log_message = f"[{req_id}] User {user_id} performed action: {action}{duration_str}"
    if details:
        log_message += f" - Details: {details}"
    
    logger.info(log_message)

def log_login_attempt(username, password, success=False):
    """Log login attempts"""
    logger = logging.getLogger('projecthub')
    
    # Get request ID
    req_id = _get_request_id() or "N/A"
    ctx = get_request_context()
    ip_address = ctx.request.remote_addr if ctx and hasattr(ctx, 'request') and ctx.request else "unknown"
    
    status = "SUCCESS" if success else "FAILED"
    logger.warning(f"[{req_id}] Login attempt from {ip_address} - Username: {username}, Password: {password}, Status: {status}")

def log_api_request(user_id, endpoint, request_data):
    """Log API requests"""
    logger = logging.getLogger('projecthub')
    
    # Get request ID
    req_id = _get_request_id() or "N/A"
    duration = get_request_duration()
    duration_str = f" ({duration:.3f}s)" if duration else ""
    
    logger.info(f"[{req_id}] API Request{duration_str} - User: {user_id}, Endpoint: {endpoint}, Data: {request_data}")

