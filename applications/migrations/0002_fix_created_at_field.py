# Generated manually to fix created_at field issue
# This migration is a no-op because the created_at field already exists correctly
# from the initial migration. Making it empty for SQLite compatibility.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        # No operations needed - created_at field already exists correctly
    ]