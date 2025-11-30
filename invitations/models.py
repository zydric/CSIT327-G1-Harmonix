from django.db import models
from django.conf import settings
from django.utils import timezone


class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    # Who's inviting (band admin)
    band_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_invitations',
        limit_choices_to={'role': 'band'}
    )
    
    # Who's being invited (musician)
    musician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_invitations',
        limit_choices_to={'role': 'musician'}
    )
    
    # Which listing this invitation is for
    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    
    # Optional message from band admin
    message = models.TextField(blank=True, null=True, help_text="Optional message from band admin to musician")
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['band_admin', 'musician', 'listing']  # Prevent duplicate invitations
    
    def __str__(self):
        return f"Invitation from {self.band_admin.username} to {self.musician.username} for {self.listing.title}"
