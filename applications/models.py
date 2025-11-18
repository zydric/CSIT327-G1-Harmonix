from django.db import models
from django.conf import settings
from django.utils import timezone


class Application(models.Model):
    """
    Model representing a musician's application to join a band listing
    """
    # Who applied (must be a musician)
    musician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'musician'},
        related_name='applications'
    )
    
    # What listing they applied to
    listing = models.ForeignKey(
        'listings.Listing',  # String reference to avoid circular imports
        on_delete=models.CASCADE,
        related_name='applications'
    )
    
    # Application details
    message = models.TextField(
        help_text="Cover letter or application message from the musician",
        blank=True
    )
    
    # Status tracking
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Prevent duplicate applications from same musician to same listing
        unique_together = ['musician', 'listing']
        ordering = ['-created_at']
        verbose_name = "Application"
        verbose_name_plural = "Applications"
    
    def __str__(self):
        return f"{self.musician.username} -> {self.listing.title} ({self.status})"
    
    @property
    def application_date_display(self):
        """Returns formatted date like 'Applied Jan 15, 2024'"""
        return f"Applied {self.created_at.strftime('%b %d, %Y')}"