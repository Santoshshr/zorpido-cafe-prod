from django.core.management.base import BaseCommand
from django.db import connection
from django.utils.text import slugify
from pos.models import ExpenseCategory


class Command(BaseCommand):
    help = 'Fix missing indexes and data issues for pos app migration 0017'

    def handle(self, *args, **options):
        self.stdout.write('Checking and fixing pos migration issues...')

        # Step 1: Populate missing slugs for ExpenseCategory
        self.stdout.write('Populating missing slugs for ExpenseCategory...')
        for category in ExpenseCategory.objects.filter(slug__isnull=True):
            base_slug = slugify(category.name)
            slug = base_slug
            counter = 1
            while ExpenseCategory.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            category.slug = slug
            category.save()
            self.stdout.write(f'  Updated {category.name} with slug {slug}')

        # Step 2: Check and create missing indexes
        self.stdout.write('Checking for missing indexes...')
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
            # For other databases, you might need different queries
            self.stdout.write(self.style.WARNING('Index checking only implemented for SQLite'))
            existing = set()

        # Create missing indexes
        if 'pos_expense_date_idx' not in existing:
            cursor.execute('CREATE INDEX pos_expense_date_idx ON pos_expense (date)')
            self.stdout.write('  Created index pos_expense_date_idx')

        if 'pos_expense_cat_idx' not in existing:
            cursor.execute('CREATE INDEX pos_expense_cat_idx ON pos_expense (category_id)')
            self.stdout.write('  Created index pos_expense_cat_idx')

        # Step 3: Apply the migration
        self.stdout.write('Applying migration pos.0017...')
        from django.core.management import call_command
        call_command('migrate', 'pos', '0017', verbosity=1)

        # Step 4: Show final status
        self.stdout.write('Migration status after fix:')
        call_command('showmigrations', 'pos')

        self.stdout.write(self.style.SUCCESS('All fixes applied successfully!'))