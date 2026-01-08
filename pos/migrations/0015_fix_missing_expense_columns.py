"""Fallback migration copy in case earlier renames left duplicated numbers.

This file mirrors the earlier fix and is safe if the other copy remains.
Database-agnostic version that works on SQLite, PostgreSQL, and MySQL.
"""
from django.db import migrations


def add_missing_columns(apps, schema_editor):
    conn = schema_editor.connection
    table_name = 'pos_expense'
    vendor = conn.vendor
    
    try:
        cursor = conn.cursor()
        
        # Check if table exists
        if vendor == 'sqlite3':
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=%s", (table_name,))
        elif vendor == 'postgresql':
            cursor.execute("SELECT tablename FROM pg_tables WHERE tablename = %s", (table_name,))
        elif vendor == 'mysql':
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name = %s AND table_schema = DATABASE()", (table_name,))
        else:
            # Unknown database, skip
            return
            
        if not cursor.fetchone():
            return
            
        # Get existing columns
        if vendor == 'sqlite3':
            cursor.execute(f"PRAGMA table_info('{table_name}')")
            existing = {row[1] for row in cursor.fetchall()}
        elif vendor == 'postgresql':
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s AND table_schema = 'public'", (table_name,))
            existing = {row[0] for row in cursor.fetchall()}
        elif vendor == 'mysql':
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s AND table_schema = DATABASE()", (table_name,))
            existing = {row[0] for row in cursor.fetchall()}
        else:
            return
            
        # Columns to add with database-agnostic SQL
        to_add = {
            'updated_at': f"ALTER TABLE {table_name} ADD COLUMN updated_at TIMESTAMP NULL",
            'created_by_id': f"ALTER TABLE {table_name} ADD COLUMN created_by_id INTEGER NULL",
            'description': f"ALTER TABLE {table_name} ADD COLUMN description TEXT NULL",
            'date': f"ALTER TABLE {table_name} ADD COLUMN date DATE NULL",
            'category_id': f"ALTER TABLE {table_name} ADD COLUMN category_id INTEGER NULL",
            'created_at': f"ALTER TABLE {table_name} ADD COLUMN created_at TIMESTAMP NULL",
            'amount': f"ALTER TABLE {table_name} ADD COLUMN amount DECIMAL(10,2) NULL",
        }
        
        for col, sql in to_add.items():
            if col not in existing:
                try:
                    cursor.execute(sql)
                except Exception:
                    # Ignore errors (column might already exist or other issues)
                    pass
    finally:
        try:
            cursor.close()
        except Exception:
            pass


def noop(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0014_fix_missing_expense_columns'),
    ]

    operations = [
        migrations.RunPython(add_missing_columns, reverse_code=noop),
    ]
