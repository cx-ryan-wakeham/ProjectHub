# Logging configuration with intentional vulnerabilities
import logging
import sys
from config import Config

def setup_logger(app):
    """Setup logging with intentional vulnerabilities for security testing"""
    
    # VULNERABLE: No log sanitization - allows log injection
    # VULNERABLE: Logs sensitive information (passwords, tokens, etc.)
    
    logger = logging.getLogger('projecthub')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # File handler
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Formatter - VULNERABLE: Includes user input without sanitization
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # VULNERABLE: Log sensitive configuration
    logger.info(f"Application started with JWT secret: {Config.JWT_SECRET_KEY}")
    logger.info(f"Database URL: {Config.DATABASE_URL}")
    logger.info(f"AWS Access Key: {Config.AWS_ACCESS_KEY_ID}")
    
    return logger

def log_user_action(user_id, action, details=None):
    """Log user actions - VULNERABLE: No sanitization of user input"""
    logger = logging.getLogger('projecthub')
    
    # VULNERABLE: Logging user input without sanitization (log injection)
    # VULNERABLE: Logging sensitive information
    log_message = f"User {user_id} performed action: {action}"
    if details:
        # VULNERABLE: Details may contain sensitive data or injection attempts
        log_message += f" - Details: {details}"
    
    logger.info(log_message)

def log_login_attempt(username, password, success=False):
    """Log login attempts - VULNERABLE: Logs passwords in plain text"""
    logger = logging.getLogger('projecthub')
    
    # VULNERABLE: Logging password in plain text
    status = "SUCCESS" if success else "FAILED"
    logger.warning(f"Login attempt - Username: {username}, Password: {password}, Status: {status}")

def log_api_request(user_id, endpoint, request_data):
    """Log API requests - VULNERABLE: Logs sensitive request data"""
    logger = logging.getLogger('projecthub')
    
    # VULNERABLE: Logging request data which may contain sensitive information
    logger.info(f"API Request - User: {user_id}, Endpoint: {endpoint}, Data: {request_data}")

