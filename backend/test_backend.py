#!/usr/bin/env python
"""Test backend functionality"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("BACKEND DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: Import db_ext
print("\n[TEST 1] Importing db_ext...")
try:
    from db_ext import db
    print("✓ PASS: db_ext imported successfully")
    print(f"  db type: {type(db)}")
except Exception as e:
    print(f"✗ FAIL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Import models
print("\n[TEST 2] Importing models...")
try:
    from models import User, Project, Task, Message, Document, Comment
    print("✓ PASS: All models imported successfully")
    print(f"  User has 'query': {hasattr(User, 'query')}")
    print(f"  Project has 'query': {hasattr(Project, 'query')}")
except Exception as e:
    print(f"✗ FAIL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Import app
print("\n[TEST 3] Importing Flask app...")
try:
    from app import app
    print("✓ PASS: Flask app imported successfully")
except Exception as e:
    print(f"✗ FAIL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Check if app can create context
print("\n[TEST 4] Testing app context...")
try:
    with app.app_context():
        print("✓ PASS: App context created successfully")
except Exception as e:
    print(f"✗ FAIL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Import analytics
print("\n[TEST 5] Importing analytics module...")
try:
    from analytics import bp as analytics_bp
    from analytics.service import AnalyticsService
    print("✓ PASS: Analytics module imported successfully")
except Exception as e:
    print(f"✗ FAIL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Check registered blueprints
print("\n[TEST 6] Checking registered blueprints...")
try:
    blueprints = list(app.blueprints.keys())
    print(f"✓ PASS: Found {len(blueprints)} blueprints")
    for bp_name in blueprints:
        print(f"  - {bp_name}")
    
    if 'analytics' in blueprints:
        print("  ✓ Analytics blueprint registered")
    else:
        print("  ✗ WARNING: Analytics blueprint NOT found")
except Exception as e:
    print(f"✗ FAIL: {e}")
    import traceback
    traceback.print_exc()

# Test 7: List all routes
print("\n[TEST 7] Checking API routes...")
try:
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.methods} {rule.rule}")
    
    print(f"✓ PASS: Found {len(routes)} routes")
    
    # Check for key routes
    key_routes = ['/api/v1/users', '/api/v1/stats', '/api/messages', '/analytics/tasks/by-status']
    for route in key_routes:
        found = any(route in r for r in routes)
        status = "✓" if found else "✗"
        print(f"  {status} {route}")
        
except Exception as e:
    print(f"✗ FAIL: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)

