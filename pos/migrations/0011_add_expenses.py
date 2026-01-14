"""Create ExpenseCategory and Expense models."""
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0010_alter_expensecategory_options_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "DROP TABLE IF EXISTS pos_expense",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AddField(
            model_name='expensecategory',
            name='name',
            field=models.CharField(max_length=120, unique=True, default='Default Category'),
        ),
        migrations.AddField(
            model_name='expensecategory',
            name='slug',
            field=models.SlugField(max_length=140, unique=True, default='default-category'),
        ),
        migrations.AddField(
            model_name='expensecategory',
            name='created_at',
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.AlterModelOptions(
            name='expensecategory',
            options={'ordering': ['name'], 'verbose_name': 'Expense Category', 'verbose_name_plural': 'Expense Categories'},
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateField(db_index=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='expenses', to='pos.expensecategory')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_expenses', to='users.user')),
            ],
            options={
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='expense',
            index=models.Index(fields=['date'], name='pos_expense_date_idx'),
        ),
        migrations.AddIndex(
            model_name='expense',
            index=models.Index(fields=['category'], name='pos_expense_cat_idx'),
        ),
    ]
