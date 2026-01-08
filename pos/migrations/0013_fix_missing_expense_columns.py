"""Add missing columns to pos_expense table if they were created out-of-sync.

This migration is defensive: it inspects the database table schema and adds
columns that exist on the model but are missing in the database. It is
designed to help recover from a previous inconsistent migration state.

Database-agnostic version that works on SQLite, PostgreSQL, and MySQL.
Columns added are nullable so ALTER TABLE succeeds.
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
        ('pos', '0012_rename_pos_expense_date_idx_pos_expense_date_467b66_idx_and_more'),
    ]

    operations = [
        migrations.RunPython(add_missing_columns, reverse_code=noop),
    ]
