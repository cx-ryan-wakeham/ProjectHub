#!/usr/bin/env python
"""Test that all imports work correctly"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    print("1. Importing db_ext...")
    from db_ext import db
    print("   ✓ db_ext imported")
    
    print("2. Importing models...")
    from models import User, Project, Task, Message, Document, Comment
    print("   ✓ models imported")
    
    print("3. Checking if User has query attribute...")
    has_query = hasattr(User, 'query')
    print(f"   User.query exists: {has_query}")
    
    print("4. Importing analytics...")
    from analytics import bp as analytics_bp
    print("   ✓ analytics imported")
    
    print("5. Importing analytics.service...")
    from analytics.service import AnalyticsService
    print("   ✓ analytics.service imported")
    
    print("6. Importing app...")
    from app import app
    print("   ✓ app imported")
    
    print("\n✓ All imports successful!")
    
except Exception as e:
    print(f"\n✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

