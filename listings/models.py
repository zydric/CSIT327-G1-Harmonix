from django.db import models
from django.conf import settings
from django.utils import timezone
from harmonix.constants import GENRE_CHOICES, INSTRUMENT_CHOICES


class Listing(models.Model):
    # Use shared choices from constants
    GENRE_CHOICES = GENRE_CHOICES
    INSTRUMENT_CHOICES = INSTRUMENT_CHOICES
    # Basic Info
    title = models.CharField(max_length=200, help_text="e.g., 'Lead Guitarist Needed'")
    band_name = models.CharField(max_length=100, help_text="Name of the band posting this opportunity")
    description = models.TextField(help_text="Detailed description of the opportunity and requirements")
    
    # Who posted it (must be a band admin)
    band_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'band'},
        related_name='listings',
        help_text="Band admin who created this listing"
    )
    
    # Requirements
    instruments_needed = models.CharField(
        max_length=200, 
        help_text="Comma-separated list: 'Guitar, Bass, Drums'"
    )
    genres = models.CharField(
        max_length=200,
        help_text="Comma-separated list: 'Rock, Alternative, Jazz'"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this listing is currently accepting applications"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest first
        verbose_name = "Band Listing"
        verbose_name_plural = "Band Listings"
    
    def __str__(self):
        return f"{self.title} - {self.band_name}"
    
    @property
    def posted_date_display(self):
        """Returns formatted date like 'Posted Jan 15, 2024'"""
        return f"Posted {self.created_at.strftime('%b %d, %Y')}"
    
    @property
    def instruments_list(self):
        """Returns list of instruments from comma-separated string, converted to display format"""
        from harmonix.constants import INSTRUMENT_DICT
        instruments = [instrument.strip() for instrument in self.instruments_needed.split(',') if instrument.strip()]
        # Convert lowercase keys to display labels (e.g., 'guitar' -> 'Guitar')
        return [INSTRUMENT_DICT.get(inst.lower(), inst.capitalize()) for inst in instruments]
    
    @property
    def genres_list(self):
        """Returns list of genres from comma-separated string, converted to display format"""
        from harmonix.constants import GENRE_DICT
        genres = [genre.strip() for genre in self.genres.split(',') if genre.strip()]
        # Convert lowercase keys to display labels (e.g., 'rock' -> 'Rock')
        return [GENRE_DICT.get(genre.lower(), genre.capitalize()) for genre in genres]
    
    @property
    def application_count(self):
        """Returns number of applications for this listing"""
        return self.applications.count()
    
    def is_applied_by(self, user):
        """Check if a specific user has already submitted (non-draft) application to this listing"""
        if not user.is_authenticated or user.role != 'musician':
            return False
        return self.applications.filter(musician=user).exclude(status='draft').exists()
    
    def has_draft_by(self, user):
        """Check if a specific user has a draft application to this listing"""
        if not user.is_authenticated or user.role != 'musician':
            return False
        return self.applications.filter(musician=user, status='draft').exists()
