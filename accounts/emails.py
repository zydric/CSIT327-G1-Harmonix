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
import threading

logger = logging.getLogger(__name__)


def _send_email_async(subject, message, from_email, recipient_list, html_message):
    """
    Send email in a separate thread to avoid blocking the request.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,  # Show errors for debugging
        )
        logger.info(f"Password reset email sent successfully to {recipient_list[0]}")
    except Exception as e:
        logger.error(f"Failed to send password reset email to {recipient_list[0]}: {str(e)}", exc_info=True)


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
        
        # Send email asynchronously to avoid blocking the request
        # This prevents worker timeouts in production
        email_thread = threading.Thread(
            target=_send_email_async,
            args=(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [to_email], html_message),
            daemon=True  # Thread will not prevent program from exiting
        )
        email_thread.start()
        
        logger.info(f"Password reset email queued for {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to queue password reset email for {to_email}: {str(e)}")
        # Don't raise exception - fail gracefully
        return False
