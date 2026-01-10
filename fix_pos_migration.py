#!/usr/bin/env python
"""
Standalone script to fix pos migration 0017 issues.
Run this script from your Django project root directory.
"""

import os
import sys
import django
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zorpido_config.settings')
django.setup()

from django.db import connection
from django.utils.text import slugify
from django.core.management import call_command
from pos.models import ExpenseCategory


def main():
    print('Checking and fixing pos migration issues...')

    # Step 1: Populate missing slugs for ExpenseCategory
    print('Populating missing slugs for ExpenseCategory...')
    for category in ExpenseCategory.objects.filter(slug__isnull=True):
        base_slug = slugify(category.name)
        slug = base_slug
        counter = 1
        while ExpenseCategory.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        category.slug = slug
        category.save()
        print(f'  Updated {category.name} with slug {slug}')

    # Step 2: Check and create missing indexes
    print('Checking for missing indexes...')
    cursor = connection.cursor()

    # Check existing indexes
    if connection.vendor == 'sqlite':
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND tbl_name='pos_expense'
            AND name IN ('pos_expense_date_idx', 'pos_expense_cat_idx')
        """)
        existing = {row[0] for row in cursor.fetchall()}
    else:
        print('WARNING: Index checking only implemented for SQLite')
        existing = set()

    # Create missing indexes
    if 'pos_expense_date_idx' not in existing:
        cursor.execute('CREATE INDEX pos_expense_date_idx ON pos_expense (date)')
        print('  Created index pos_expense_date_idx')

    if 'pos_expense_cat_idx' not in existing:
        cursor.execute('CREATE INDEX pos_expense_cat_idx ON pos_expense (category_id)')
        print('  Created index pos_expense_cat_idx')

    # Step 3: Apply the migration
    print('Applying migration pos.0017...')
    call_command('migrate', 'pos', '0017', verbosity=1)

    # Step 4: Show final status
    print('Migration status after fix:')
    call_command('showmigrations', 'pos')

    print('All fixes applied successfully!')


if __name__ == '__main__':
    main()