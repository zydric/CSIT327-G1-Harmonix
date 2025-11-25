"""
Token generator for password reset functionality.
Uses Django's default password reset token generator for security.
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for password reset.
    Inherits from Django's PasswordResetTokenGenerator for security best practices.
    """
    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's primary key, password, and timestamp.
        This ensures tokens become invalid after password change.
        """
        return (
            str(user.pk) + str(timestamp) + str(user.password)
        )


# Create a single instance to use throughout the app
password_reset_token = AccountActivationTokenGenerator()
