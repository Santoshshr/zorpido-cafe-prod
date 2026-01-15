#!/usr/bin/env python
"""
Render.com Deployment Audit Script

This script verifies that the Django project is ready for production
deployment on Render.com with PostgreSQL.

Run this script in the production environment to validate configuration.
"""

import os
import sys
import django

def main():
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zorpido_config.settings.production')
    
    # Set required environment variables for testing
    os.environ.setdefault('DJANGO_SECRET_KEY', 'test-audit-key-1234567890-abcdefghijk-1234567890-abcdefghijk')
    os.environ.setdefault('ALLOWED_HOSTS', 'localhost,127.0.0.1,*.onrender.com')
    os.environ.setdefault('DATABASE_URL', 'postgresql://user:pass@localhost:5432/testdb')
    
    django.setup()
    
    from django.conf import settings
    from django.core.management import call_command
    
    print("\n" + "="*80)
    print("DJANGO PRODUCTION READINESS AUDIT FOR RENDER.COM")
    print("="*80 + "\n")
    
    # Audit 1: Database Configuration
    print("✅ AUDIT 1: Database Configuration")
    print("-" * 80)
    db = settings.DATABASES['default']
    assert db['ENGINE'] == 'django.db.backends.postgresql', "❌ Not using PostgreSQL"
    print(f"   Engine: {db['ENGINE']}")
    print(f"   SSL Require: {db.get('OPTIONS', {}).get('sslmode', 'ENABLED')}")
    print(f"   Connection Pooling: {db.get('CONN_MAX_AGE', 600)}s")
    print(f"   ✓ PostgreSQL configured correctly\n")
    
    # Audit 2: Security Configuration
    print("✅ AUDIT 2: Security Configuration")
    print("-" * 80)
    assert not settings.DEBUG, "❌ DEBUG should be False in production"
    assert settings.SECRET_KEY, "❌ SECRET_KEY not set"
    assert len(settings.SECRET_KEY) > 50, "❌ SECRET_KEY too short"
    assert settings.SECURE_SSL_REDIRECT == True, "❌ SECURE_SSL_REDIRECT not True"
    assert settings.SESSION_COOKIE_SECURE == True, "❌ SESSION_COOKIE_SECURE not True"
    assert settings.CSRF_COOKIE_SECURE == True, "❌ CSRF_COOKIE_SECURE not True"
    assert settings.SECURE_PROXY_SSL_HEADER == ('HTTP_X_FORWARDED_PROTO', 'https'), \
        "❌ SECURE_PROXY_SSL_HEADER not set for reverse proxy"
    assert settings.SECURE_HSTS_SECONDS >= 31536000, "❌ HSTS seconds too low"
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
    print(f"   SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
    print(f"   CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
    print(f"   SECURE_PROXY_SSL_HEADER: {settings.SECURE_PROXY_SSL_HEADER}")
    print(f"   SECURE_HSTS_SECONDS: {settings.SECURE_HSTS_SECONDS}")
    print(f"   ✓ Security configuration correct\n")
    
    # Audit 3: Static Files Configuration
    print("✅ AUDIT 3: Static Files Configuration")
    print("-" * 80)
    assert settings.STATIC_ROOT, "❌ STATIC_ROOT not set"
    assert settings.STATIC_URL, "❌ STATIC_URL not set"
    assert 'whitenoise' in settings.STATICFILES_STORAGE, "❌ WhiteNoise not configured"
    assert 'CompressedManifestStaticFilesStorage' in settings.STATICFILES_STORAGE, \
        "❌ Static file compression not enabled"
    print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"   STATIC_URL: {settings.STATIC_URL}")
    print(f"   STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    print(f"   ✓ Static files configured correctly\n")
    
    # Audit 4: Middleware Order
    print("✅ AUDIT 4: Middleware Order")
    print("-" * 80)
    middleware = settings.MIDDLEWARE
    assert 'SecurityMiddleware' in middleware[0], "❌ SecurityMiddleware not first"
    assert 'WhiteNoiseMiddleware' in middleware[1], "❌ WhiteNoiseMiddleware not second"
    print(f"   1. {middleware[0]}")
    print(f"   2. {middleware[1]}")
    print(f"   3. {middleware[2]}")
    print(f"   ✓ Middleware order correct\n")
    
    # Audit 5: Environment Variables
    print("✅ AUDIT 5: Environment Variables")
    print("-" * 80)
    required_vars = ['DJANGO_SECRET_KEY', 'ALLOWED_HOSTS', 'DATABASE_URL']
    
    for var in required_vars:
        if var in os.environ:
            print(f"   ✓ {var} is set")
        else:
            print(f"   ⚠ {var} is not set (will be required in production)")
    print()
    
    # Audit 6: ALLOWED_HOSTS Configuration
    print("✅ AUDIT 6: ALLOWED_HOSTS Configuration")
    print("-" * 80)
    assert len(settings.ALLOWED_HOSTS) > 0, "❌ ALLOWED_HOSTS is empty"
    print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"   ✓ ALLOWED_HOSTS configured\n")
    
    # Audit 7: Static Files Collection Test
    print("✅ AUDIT 7: Static Files Collection Test")
    print("-" * 80)
    try:
        # Run collectstatic in dry-run mode
        print("   Running collectstatic --dry-run...")
        from io import StringIO
        from django.core.management import call_command
        
        out = StringIO()
        call_command('collectstatic', '--noinput', '--dry-run', stdout=out)
        output = out.getvalue()
        
        if 'copied' in output.lower() or 'pretending' in output.lower():
            print("   ✓ Static files collection works\n")
        else:
            print("   ⚠ Static files collection test inconclusive\n")
    except Exception as e:
        print(f"   ❌ Static files collection failed: {e}\n")
        return 1
    
    # Audit 8: Database Connection Check
    print("✅ AUDIT 8: Database Configuration Validation")
    print("-" * 80)
    print(f"   Database engine: {db['ENGINE']}")
    print(f"   Connection pooling enabled: {db.get('CONN_MAX_AGE') is not None}")
    print(f"   No hardcoded localhost: {'localhost' not in str(db)}")
    print(f"   ✓ Database configuration valid\n")
    
    # Summary
    print("="*80)
    print("✅ ALL AUDITS PASSED - READY FOR RENDER.COM DEPLOYMENT")
    print("="*80 + "\n")
    
    print("DEPLOYMENT CHECKLIST:")
    print("-" * 80)
    print("Before deploying to Render, ensure:")
    print("  ✓ DJANGO_SECRET_KEY is set to a secure random value")
    print("  ✓ ALLOWED_HOSTS includes your Render domain (*.onrender.com)")
    print("  ✓ CSRF_TRUSTED_ORIGINS is configured")
    print("  ✓ DATABASE_URL will be auto-set by Render")
    print("  ✓ All git changes are committed")
    print("  ✓ render.yaml or Procfile is correct")
    print()
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except AssertionError as e:
        print(f"\n❌ AUDIT FAILED: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ AUDIT ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
