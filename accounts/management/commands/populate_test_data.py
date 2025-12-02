from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing
from applications.models import Application
from invitations.models import Invitation
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with test data (musicians and band admins with listings)'

    def handle(self, *args, **kwargs):
        # Clear all data except superuser
        self.stdout.write('Clearing existing data...')
        
        # Delete in correct order to handle foreign key constraints
        Invitation.objects.all().delete()
        Application.objects.all().delete()
        Listing.objects.all().delete()
        
        # Delete notifications if the table exists
        from django.db import connection
        with connection.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM notifications_notification")
                self.stdout.write('Deleted notifications')
            except Exception as e:
                self.stdout.write(f'Note: Could not delete notifications: {e}')
        
        User.objects.filter(is_superuser=False).delete()

        # Define test data
        locations = [
            'Los Angeles, CA',
            'New York, NY',
            'Nashville, TN',
            'Austin, TX',
            'Seattle, WA',
            'Chicago, IL',
            'Portland, OR',
            'Denver, CO'
        ]

        genres = [
            'Rock', 'Jazz', 'Blues', 'Classical', 'Electronic',
            'Hip Hop', 'Country', 'R&B', 'Pop', 'Metal'
        ]

        instruments = [
            'Guitar', 'Bass', 'Drums', 'Keyboard', 'Vocals',
            'Saxophone', 'Trumpet', 'Violin', 'Cello', 'Flute'
        ]

        # Create 6 musicians
        self.stdout.write('Creating musicians...')
        musicians_data = [
            {
                'username': 'alex_guitar',
                'email': 'alex@example.com',
                'bio': 'Professional guitarist with 10+ years of experience in rock and blues. Toured with several indie bands and love collaborating on new projects.',
                'instruments': ['Guitar', 'Vocals'],
                'genres': ['Rock', 'Blues', 'Alternative'],
                'location': 'Los Angeles, CA'
            },
            {
                'username': 'sarah_drums',
                'email': 'sarah@example.com',
                'bio': 'Versatile drummer specializing in jazz and funk. Studied at Berklee College of Music and performed at numerous festivals worldwide.',
                'instruments': ['Drums', 'Percussion'],
                'genres': ['Jazz', 'Funk', 'R&B'],
                'location': 'New York, NY'
            },
            {
                'username': 'mike_bass',
                'email': 'mike@example.com',
                'bio': 'Bass player with a passion for metal and hard rock. Available for studio sessions and live performances.',
                'instruments': ['Bass'],
                'genres': ['Metal', 'Rock', 'Punk'],
                'location': 'Seattle, WA'
            },
            {
                'username': 'emma_vocals',
                'email': 'emma@example.com',
                'bio': 'Lead vocalist with range from pop to soul. Former contestant on singing competitions and looking to join a serious band.',
                'instruments': ['Vocals', 'Piano'],
                'genres': ['Pop', 'Soul', 'R&B'],
                'location': 'Nashville, TN'
            },
            {
                'username': 'carlos_keys',
                'email': 'carlos@example.com',
                'bio': 'Keyboard player and producer. Skilled in electronic music production and live performances with various synthesizers.',
                'instruments': ['Keyboard', 'Synthesizer'],
                'genres': ['Electronic', 'Pop', 'Jazz'],
                'location': 'Austin, TX'
            },
            {
                'username': 'lisa_violin',
                'email': 'lisa@example.com',
                'bio': 'Classically trained violinist open to fusion and experimental projects. Experienced in both classical orchestras and modern bands.',
                'instruments': ['Violin', 'Viola'],
                'genres': ['Classical', 'Rock', 'Alternative'],
                'location': 'Chicago, IL'
            }
        ]

        musicians = []
        for data in musicians_data:
            musician = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='testpass123',
                role='musician'
            )
            # Set additional fields
            musician.bio = data['bio']
            musician.instruments = ', '.join(data['instruments'])
            musician.genres = ', '.join(data['genres'])
            musician.location = data['location']
            musician.save()
            
            musicians.append(musician)
            self.stdout.write(f'Created musician: {musician.username}')

        # Create 4 band admins with listings
        self.stdout.write('\nCreating band admins and listings...')
        
        bands_data = [
            {
                'username': 'imagine_dragons_official',
                'email': 'imaginedragons@example.com',
                'band_name': 'Imagine Dragons',
                'bio': 'Grammy-winning alternative rock band looking to expand our sound with talented musicians.',
                'location': 'Las Vegas, NV',
                'listings': [
                    {
                        'title': 'Lead Guitarist Needed',
                        'description': 'We are searching for an experienced lead guitarist to join our touring lineup. Must be comfortable with alternative rock and able to handle complex riffs and solos.',
                        'instruments': ['Guitar'],
                        'genres': ['Rock', 'Alternative', 'Pop'],
                        'show_current_lineup': True,
                        'current_lineup': 'Dan Reynolds (Vocals), Wayne Sermon (Guitar), Ben McKee (Bass), Daniel Platzman (Drums)'
                    }
                ]
            },
            {
                'username': 'coldplay_band',
                'email': 'coldplay@example.com',
                'band_name': 'Coldplay',
                'bio': 'British rock band seeking new members for upcoming world tour and album production.',
                'location': 'London, UK',
                'listings': [
                    {
                        'title': 'Touring Keyboardist',
                        'description': 'Looking for a talented keyboard player for our upcoming tour. Should be proficient in various keyboard instruments and comfortable with electronic elements.',
                        'instruments': ['Keyboard', 'Piano'],
                        'genres': ['Rock', 'Pop', 'Alternative'],
                        'show_current_lineup': False,
                        'current_lineup': ''
                    },
                    {
                        'title': 'Backup Vocalist',
                        'description': 'Seeking backup vocalist with strong harmonizing skills. Experience with large venue performances preferred. Must be available for rehearsals and touring.',
                        'instruments': ['Vocals'],
                        'genres': ['Rock', 'Pop'],
                        'show_current_lineup': True,
                        'current_lineup': 'Chris Martin (Vocals/Piano), Jonny Buckland (Guitar), Guy Berryman (Bass), Will Champion (Drums)'
                    }
                ]
            },
            {
                'username': 'the_beatles_revival',
                'email': 'beatles@example.com',
                'band_name': 'The Beatles Revival',
                'bio': 'Tribute band dedicated to recreating the magic of The Beatles. Looking for passionate musicians who love classic rock.',
                'location': 'Liverpool, UK',
                'listings': [
                    {
                        'title': 'Bass Player Wanted',
                        'description': 'Join our Beatles tribute band as bass player. Must know Beatles catalog and be able to perform live shows regularly. Great opportunity for fans of classic rock.',
                        'instruments': ['Bass'],
                        'genres': ['Rock', 'Pop', 'Classic Rock'],
                        'show_current_lineup': True,
                        'current_lineup': 'John (Rhythm Guitar/Vocals), Paul (Bass/Vocals - leaving), George (Lead Guitar), Ringo (Drums)'
                    }
                ]
            },
            {
                'username': 'linkin_park_crew',
                'email': 'linkinpark@example.com',
                'band_name': 'Linkin Park',
                'bio': 'Nu-metal pioneers looking for musicians to help us create our next chapter. Seeking dedicated and creative individuals.',
                'location': 'Los Angeles, CA',
                'listings': [
                    {
                        'title': 'Drummer Position Open',
                        'description': 'We need a powerful drummer who can handle both heavy rock beats and electronic elements. Studio and touring experience required for this full-time position.',
                        'instruments': ['Drums'],
                        'genres': ['Rock', 'Metal', 'Alternative'],
                        'show_current_lineup': False,
                        'current_lineup': ''
                    },
                    {
                        'title': 'DJ and Producer',
                        'description': 'Seeking DJ/producer to add electronic elements to our sound. Must be skilled in turntablism and music production. Experience with live performances essential.',
                        'instruments': ['Turntables', 'Keyboard'],
                        'genres': ['Rock', 'Electronic', 'Hip Hop'],
                        'show_current_lineup': True,
                        'current_lineup': 'Mike Shinoda (Vocals/Keyboards), Brad Delson (Guitar), Dave Farrell (Bass), Rob Bourdon (Drums), Joe Hahn (DJ - leaving)'
                    }
                ]
            }
        ]

        for band_data in bands_data:
            # Create band admin
            band_admin = User.objects.create_user(
                username=band_data['username'],
                email=band_data['email'],
                password='testpass123',
                role='band'
            )
            # Set additional fields
            band_admin.bio = band_data['bio']
            band_admin.location = band_data['location']
            band_admin.save()
            
            self.stdout.write(f'Created band admin: {band_admin.username}')

            # Create listings for this band
            for listing_data in band_data['listings']:
                listing = Listing.objects.create(
                    band_admin=band_admin,
                    band_name=band_data['band_name'],
                    title=listing_data['title'],
                    description=listing_data['description'],
                    instruments_needed=', '.join(listing_data['instruments']),
                    genres=', '.join(listing_data['genres']),
                    location=band_data['location'],
                    current_lineup=listing_data['current_lineup'] if listing_data['show_current_lineup'] else '',
                    is_active=True
                )
                self.stdout.write(f'  - Created listing: {listing.title}')

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully populated database with:'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(musicians)} musicians'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(bands_data)} band admins'))
        self.stdout.write(self.style.SUCCESS(f'  - {Listing.objects.count()} listings'))
