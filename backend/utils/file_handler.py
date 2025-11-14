# File upload handler
import os
import uuid
import hashlib
from werkzeug.utils import secure_filename
from config import Config
import xml.etree.ElementTree as ET
import pickle
try:
    import yaml
except ImportError:
    yaml = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS

def save_uploaded_file(file, project_id=None):
    """Save uploaded file"""
    if not file or not file.filename:
        return None, "No file provided"
    
    original_filename = file.filename
    filename = f"{uuid.uuid4()}_{original_filename}"
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    
    try:
        file.save(file_path)
        os.chmod(file_path, 0o644)
        file_size = os.path.getsize(file_path)
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
    """Get file type"""
    try:
        import magic
        mime = magic.Magic(mime=True)
        return mime.from_file(file_path)
    except:
        ext = os.path.splitext(file_path)[1].lower()
        return ext

def process_xml_file(file_path):
    """Process XML file"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = {}
        for child in root:
            data[child.tag] = child.text
        return data
    except Exception as e:
        return {'error': str(e)}

def process_pickle_file(file_path):
    """Process pickle file"""
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data
    except Exception as e:
        return {'error': str(e)}

def process_yaml_file(file_path):
    """Process YAML file"""
    if yaml is None:
        return {'error': 'YAML library not installed'}
    try:
        with open(file_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)
        return data
    except Exception as e:
        return {'error': str(e)}

def extract_file_metadata(file_path):
    """Extract file metadata"""
    metadata = {}
    
    try:
        stat = os.stat(file_path)
        metadata['size'] = stat.st_size
        metadata['created'] = stat.st_ctime
        metadata['modified'] = stat.st_mtime
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.xml':
            metadata['xml_data'] = process_xml_file(file_path)
        elif ext == '.pkl' or ext == '.pickle':
            metadata['pickle_data'] = process_pickle_file(file_path)
        elif ext in ['.yaml', '.yml']:
            metadata['yaml_data'] = process_yaml_file(file_path)
        
    except Exception as e:
        metadata['error'] = str(e)
    
    return metadata

