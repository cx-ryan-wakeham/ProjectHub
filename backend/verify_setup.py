#!/usr/bin/env python
"""
Verification script for ProjectHub backend setup
Run this to verify all components are working correctly
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all critical imports work"""
    print("\n" + "="*60)
    print("TESTING IMPORTS")
    print("="*60)
    
    try:
        print("\n1. Importing db_ext...")
        from db_ext import db
        print("   ✓ Success")
        
        print("\n2. Importing models...")
        from models import User, Project, Task, Message, Document, Comment
        print("   ✓ Success")
        print(f"   - User.query exists: {hasattr(User, 'query')}")
        
        print("\n3. Importing Flask app...")
        from app import app
        print("   ✓ Success")
        
        print("\n4. Importing analytics...")
        from analytics import bp
        from analytics.service import AnalyticsService
        print("   ✓ Success")
        
        return True, app
    except Exception as e:
        print(f"\n   ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_routes(app):
    """Test that routes are registered"""
    print("\n" + "="*60)
    print("TESTING ROUTES")
    print("="*60)
    
    routes_to_check = [
        ('GET', '/api/v1/users', 'User list'),
        ('GET', '/api/v1/stats', 'Stats'),
        ('GET', '/api/messages', 'Messages'),
        ('GET', '/analytics/tasks/by-status', 'Analytics - Tasks by status'),
        ('GET', '/analytics/projects/summary', 'Analytics - Projects summary'),
    ]
    
    all_routes = [(str(rule.methods), rule.rule) for rule in app.url_map.iter_rules()]
    
    for method, route, description in routes_to_check:
        found = any(method in methods and route == rule for methods, rule in all_routes)
        status = "✓" if found else "✗"
        print(f"{status} {description:40} {method:10} {route}")
    
    # List all analytics routes
    print("\nAll Analytics routes:")
    for methods, rule in all_routes:
        if '/analytics' in rule:
            print(f"  - {methods:30} {rule}")

def test_database_queries(app):
    """Test that database queries work"""
    print("\n" + "="*60)
    print("TESTING DATABASE QUERIES")
    print("="*60)
    
    try:
        with app.app_context():
            from models import User, Project, Task
            
            # Test legacy query pattern
            print("\n1. Testing legacy Model.query pattern...")
            try:
                count = User.query.count()
                print(f"   ✓ User.query.count() = {count}")
            except Exception as e:
                print(f"   ✗ FAILED: {e}")
            
            # Test SQLAlchemy 2.x pattern
            print("\n2. Testing SQLAlchemy 2.x pattern...")
            try:
                from sqlalchemy import select
                from db_ext import db
                stmt = select(User)
                result = db.session.execute(stmt).scalars().all()
                print(f"   ✓ db.session.execute(select(User)) returned {len(result)} users")
            except Exception as e:
                print(f"   ✗ FAILED: {e}")
            
    except Exception as e:
        print(f"\n   ✗ Database test FAILED: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all verification tests"""
    print("\n" + "="*60)
    print("ProjectHub Backend Verification")
    print("="*60)
    
    # Test imports
    success, app = test_imports()
    if not success:
        print("\n✗ Import tests failed. Fix imports before proceeding.")
        return 1
    
    # Test routes
    test_routes(app)
    
    # Test database (requires DB connection)
    try:
        test_database_queries(app)
    except Exception as e:
        print(f"\n⚠ Database tests skipped (DB not available): {e}")
    
    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)
    print("\nIf all tests passed, the backend should work correctly.")
    print("Start the application with: python app.py")
    print("="*60 + "\n")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

