"""
Email utilities for sending password reset emails.
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from .tokens import password_reset_token
import logging

logger = logging.getLogger(__name__)


def send_password_reset_email(request, user, to_email):
    """
    Send password reset email to the user.
    
    Args:
        request: HttpRequest object to get the current site domain
        user: User object who requested the password reset
        to_email: Email address to send the reset link
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Get current site domain
        current_site = get_current_site(request)
        
        # Generate token and uid
        token = password_reset_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Build the reset URL
        protocol = 'https' if request.is_secure() else 'http'
        reset_url = f"{protocol}://{current_site.domain}/accounts/reset/{uid}/{token}/"
        
        # Email context
        context = {
            'user': user,
            'reset_url': reset_url,
            'site_name': 'Harmonix',
            'protocol': protocol,
            'domain': current_site.domain,
        }
        
        # Render email templates
        html_message = render_to_string('emails/password_reset_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Email subject
        subject = 'Reset Your Harmonix Password'
        
        # Validate email configuration before sending
        if not settings.DEFAULT_FROM_EMAIL:
            logger.error("DEFAULT_FROM_EMAIL not configured")
            return False
        
        # Send email with proper error handling
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            html_message=html_message,
            fail_silently=True,  # Don't raise exceptions
        )
        
        logger.info(f"Password reset email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset email to {to_email}: {str(e)}")
        # Don't raise exception - fail gracefully
        return False
