# Generated manually to fix created_at field issue

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        # First, add the correct created_at column
        migrations.RunSQL(
            "ALTER TABLE applications_application ADD COLUMN created_at_temp timestamp with time zone DEFAULT NOW();",
            reverse_sql="ALTER TABLE applications_application DROP COLUMN created_at_temp;"
        ),
        
        # Copy data from applied_at to created_at_temp
        migrations.RunSQL(
            "UPDATE applications_application SET created_at_temp = applied_at;",
            reverse_sql=""
        ),
        
        # Drop the incorrect applied_at column
        migrations.RunSQL(
            "ALTER TABLE applications_application DROP COLUMN applied_at;",
            reverse_sql="ALTER TABLE applications_application ADD COLUMN applied_at timestamp with time zone;"
        ),
        
        # Rename created_at_temp to created_at
        migrations.RunSQL(
            "ALTER TABLE applications_application RENAME COLUMN created_at_temp TO created_at;",
            reverse_sql="ALTER TABLE applications_application RENAME COLUMN created_at TO created_at_temp;"
        ),
        
        # Set NOT NULL constraint
        migrations.RunSQL(
            "ALTER TABLE applications_application ALTER COLUMN created_at SET NOT NULL;",
            reverse_sql="ALTER TABLE applications_application ALTER COLUMN created_at DROP NOT NULL;"
        ),
    ]