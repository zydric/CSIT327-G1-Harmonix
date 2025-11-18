from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import User
from listings.models import Listing
from applications.models import Application


class Command(BaseCommand):
    help = 'Deletes all test data except the superuser (harmonix_admin)'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Get the superuser to preserve
                superuser = User.objects.filter(username='harmonix_admin', is_superuser=True).first()
                
                if not superuser:
                    self.stdout.write(self.style.WARNING('Superuser "harmonix_admin" not found. Please ensure it exists.'))
                    return
                
                # Count records before deletion
                apps_count = Application.objects.count()
                listings_count = Listing.objects.count()
                users_count = User.objects.exclude(id=superuser.id).count()
                
                self.stdout.write(f'\nFound {apps_count} applications')
                self.stdout.write(f'Found {listings_count} listings')
                self.stdout.write(f'Found {users_count} users (excluding superuser)')
                
                # Step 1: Delete all applications
                Application.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'✓ Deleted {apps_count} applications'))
                
                # Step 2: Delete all listings
                Listing.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'✓ Deleted {listings_count} listings'))
                
                # Step 3: Delete all users EXCEPT the superuser
                User.objects.exclude(id=superuser.id).delete()
                self.stdout.write(self.style.SUCCESS(f'✓ Deleted {users_count} users'))
                
                self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully reset test data!'))
                self.stdout.write(self.style.SUCCESS(f'✓ Preserved superuser: {superuser.username}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            raise
