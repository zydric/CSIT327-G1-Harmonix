from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample listings for testing'

    def handle(self, *args, **options):
        # Create or get a test band user
        band_user, created = User.objects.get_or_create(
            username='electric_storm',
            defaults={
                'email': 'band@electricstorm.com',
                'role': 'band',
                'location': 'Los Angeles, CA',
                'genres': 'Rock',
            }
        )
        if created:
            band_user.set_password('testpass123')
            band_user.save()
            self.stdout.write(f'Created band user: {band_user.username}')

        # Create another band user
        jazz_band, created = User.objects.get_or_create(
            username='smooth_cats',
            defaults={
                'email': 'band@smoothcats.com',
                'role': 'band',
                'location': 'New York, NY',
                'genres': 'Jazz',
            }
        )
        if created:
            jazz_band.set_password('testpass123')
            jazz_band.save()
            self.stdout.write(f'Created band user: {jazz_band.username}')

        # Create indie band
        indie_band, created = User.objects.get_or_create(
            username='neon_dreams',
            defaults={
                'email': 'band@neondreams.com',
                'role': 'band',
                'location': 'Portland, OR',
                'genres': 'Indie',
            }
        )
        if created:
            indie_band.set_password('testpass123')
            indie_band.save()
            self.stdout.write(f'Created band user: {indie_band.username}')

        # Sample listings data matching your mockups
        sample_listings = [
            {
                'title': 'Lead Guitarist Needed',
                'band_name': 'Electric Storm',
                'description': 'We are looking for a skilled lead guitarist to complete our rock band. Must be available for weekend gigs and weekly rehearsals.',
                'band_admin': band_user,
                'instruments_needed': 'Guitar',
                'genres': 'Rock',
            },
            {
                'title': 'Jazz Bassist for Regular Venue',
                'band_name': 'Smooth Cats',
                'description': 'Established jazz trio seeking a bassist for regular performances at upscale venues. Professional attitude required.',
                'band_admin': jazz_band,
                'instruments_needed': 'Bass',
                'genres': 'Jazz',
            },
            {
                'title': 'Indie Band Seeks Drummer',
                'band_name': 'Neon Dreams',
                'description': 'Creative indie band looking for a drummer who can bring energy and unique rhythms to our sound.',
                'band_admin': indie_band,
                'instruments_needed': 'Drums',
                'genres': 'Indie',
            },
            {
                'title': 'Vocalist for Rock Band',
                'band_name': 'Electric Storm',
                'description': 'Rock band seeking powerful vocalist with stage presence. Experience with classic and modern rock preferred.',
                'band_admin': band_user,
                'instruments_needed': 'Vocals',
                'genres': 'Rock',
            },
            {
                'title': 'Pianist for Jazz Ensemble',
                'band_name': 'Smooth Cats', 
                'description': 'Looking for a skilled pianist to join our jazz ensemble. Must be comfortable with improvisation.',
                'band_admin': jazz_band,
                'instruments_needed': 'Piano',
                'genres': 'Jazz',
            },
        ]

        # Create listings if they don't exist
        for listing_data in sample_listings:
            listing, created = Listing.objects.get_or_create(
                title=listing_data['title'],
                band_admin=listing_data['band_admin'],
                defaults=listing_data
            )
            if created:
                self.stdout.write(f'Created listing: {listing.title}')
            else:
                self.stdout.write(f'Listing already exists: {listing.title}')

        # Create a test musician user
        musician_user, created = User.objects.get_or_create(
            username='alexdrums',
            defaults={
                'email': 'alex@example.com',
                'role': 'musician',
                'location': 'Los Angeles, CA',
                'instruments': 'Drums, Percussion',
                'genres': 'Rock, Jazz',
            }
        )
        if created:
            musician_user.set_password('testpass123')
            musician_user.save()
            self.stdout.write(f'Created musician user: {musician_user.username}')

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data!')
        )