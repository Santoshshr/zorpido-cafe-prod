from django.db import migrations


def add_missing_columns(apps, schema_editor):
    """
    Adds missing columns to pos_expense table in a database-agnostic way.
    Works on SQLite, PostgreSQL, and MySQL.
    All columns are added as nullable to ensure safe ALTER TABLE operations.
    """
    conn = schema_editor.connection
    vendor = conn.vendor
    table_name = 'pos_expense'

    cursor = conn.cursor()

    try:
        # --- Check if table exists ---
        if vendor == 'sqlite':
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=%s",
                (table_name,)
            )
            if not cursor.fetchone():
                return
        elif vendor in ('postgresql', 'mysql'):
            # PostgreSQL & MySQL: information_schema.tables
            cursor.execute(
                """
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = %s AND table_name = %s
                """,
                (conn.settings_dict.get('OPTIONS', {}).get('schema', 'public') if vendor == 'postgresql' else conn.settings_dict['NAME'],
                 table_name)
            )
            if not cursor.fetchone():
                return

        # --- Get existing columns ---
        if vendor == 'sqlite':
            cursor.execute(f"PRAGMA table_info('{table_name}')")
            existing = {row[1] for row in cursor.fetchall()}  # name is index 1
        elif vendor == 'postgresql':
            cursor.execute(
                """
                SELECT column_name FROM information_schema.columns
                WHERE table_name = %s
                """,
                (table_name,)
            )
            existing = {row[0] for row in cursor.fetchall()}
        elif vendor == 'mysql':
            cursor.execute(
                """
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                """,
                (conn.settings_dict['NAME'], table_name)
            )
            existing = {row[0] for row in cursor.fetchall()}

        # --- Columns to add ---
        to_add = {
            'updated_at': "datetime",
            'created_by_id': "integer",
            'description': "text",
            'date': "date",
            'category_id': "integer",
            'created_at': "datetime",
            'amount': "numeric",
        }

        for col, col_type in to_add.items():
            if col not in existing:
                sql = f"ALTER TABLE {table_name} ADD COLUMN {col} {col_type}"
                try:
                    cursor.execute(sql)
                except Exception:
                    # best-effort: ignore errors for idempotency
                    pass

    finally:
        cursor.close()


def noop(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0011_add_expenses'),
    ]

    operations = [
        migrations.RunPython(add_missing_columns, reverse_code=noop),
    ]
