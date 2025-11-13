# File upload handler with intentional security vulnerabilities
import os
import uuid
import hashlib
from werkzeug.utils import secure_filename
from config import Config
import xml.etree.ElementTree as ET  # VULNERABLE: For XXE attacks
import pickle  # VULNERABLE: For insecure deserialization
import yaml  # VULNERABLE: For YAML deserialization

def allowed_file(filename):
    """Check if file extension is allowed - VULNERABLE: Too permissive"""
    # VULNERABLE: Allows dangerous file types (php, exe, sh, etc.)
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS

def save_uploaded_file(file, project_id=None):
    """Save uploaded file - VULNERABLE: Path traversal, insecure file handling"""
    if not file or not file.filename:
        return None, "No file provided"
    
    # VULNERABLE: No proper file type validation
    # VULNERABLE: Allows dangerous file types
    
    # VULNERABLE: Using original filename (path traversal risk)
    original_filename = file.filename
    filename = f"{uuid.uuid4()}_{original_filename}"
    
    # VULNERABLE: Path traversal - doesn't sanitize filename properly
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    
    # VULNERABLE: No check for directory traversal in filename
    # Should use: os.path.basename() and validate
    
    try:
        file.save(file_path)
        
        # VULNERABLE: Set insecure permissions (world-readable)
        os.chmod(file_path, 0o644)
        
        file_size = os.path.getsize(file_path)
        
        # VULNERABLE: Try to extract metadata without proper validation
        file_type = get_file_type(file_path)
        
        return {
            'filename': filename,
            'original_filename': original_filename,
            'file_path': file_path,
            'file_size': file_size,
            'file_type': file_type
        }, None
    except Exception as e:
        return None, str(e)

def get_file_type(file_path):
    """Get file type - VULNERABLE: Command injection risk"""
    try:
        import magic
        # VULNERABLE: Using python-magic which may execute system commands
        mime = magic.Magic(mime=True)
        return mime.from_file(file_path)
    except:
        # Fallback to extension-based detection
        ext = os.path.splitext(file_path)[1].lower()
        return ext

def process_xml_file(file_path):
    """Process XML file - VULNERABLE: XXE (XML External Entity) attack"""
    try:
        # VULNERABLE: XXE - No protection against external entity expansion
        # Should use: defusedxml or set parser to not resolve external entities
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # VULNERABLE: Processes XML without disabling external entities
        # An attacker can include: <!ENTITY xxe SYSTEM "file:///etc/passwd">
        
        data = {}
        for child in root:
            data[child.tag] = child.text
        
        return data
    except Exception as e:
        return {'error': str(e)}

def process_pickle_file(file_path):
    """Process pickle file - VULNERABLE: Insecure deserialization (RCE)"""
    try:
        # VULNERABLE: Pickle deserialization can execute arbitrary code
        with open(file_path, 'rb') as f:
            data = pickle.load(f)  # VULNERABLE: Can execute malicious code
        return data
    except Exception as e:
        return {'error': str(e)}

def process_yaml_file(file_path):
    """Process YAML file - VULNERABLE: Insecure deserialization"""
    try:
        # VULNERABLE: YAML deserialization can execute arbitrary code
        with open(file_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)  # VULNERABLE: Unsafe loader
        return data
    except Exception as e:
        return {'error': str(e)}

def extract_file_metadata(file_path):
    """Extract file metadata - VULNERABLE: Information disclosure"""
    metadata = {}
    
    try:
        # VULNERABLE: May expose sensitive information
        stat = os.stat(file_path)
        metadata['size'] = stat.st_size
        metadata['created'] = stat.st_ctime
        metadata['modified'] = stat.st_mtime
        
        # VULNERABLE: Try to extract metadata from different file types
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.xml':
            metadata['xml_data'] = process_xml_file(file_path)  # VULNERABLE: XXE
        elif ext == '.pkl' or ext == '.pickle':
            metadata['pickle_data'] = process_pickle_file(file_path)  # VULNERABLE: RCE
        elif ext in ['.yaml', '.yml']:
            metadata['yaml_data'] = process_yaml_file(file_path)  # VULNERABLE: RCE
        
    except Exception as e:
        metadata['error'] = str(e)
    
    return metadata

