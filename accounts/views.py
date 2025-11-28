from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from harmonix.constants import GENRE_CHOICES, INSTRUMENT_CHOICES


# REST FRAMEWORKS (Imports are not used in these views)
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

from .models import User

def band_profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        # Get form data
        new_username = request.POST.get('username', '').strip()
        new_location = request.POST.get('location', '').strip()
        new_genres = request.POST.get('genres', '').strip()

        # Validate username if it changed
        if new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'This username is already taken.')
                return render(request, 'accounts/band_profile.html', {'user': user})
        
        # Validate location format if provided
        if new_location and not is_valid_location_format(new_location):
            messages.error(request, 'Please enter location in the format: City, Country (e.g., Cebu, Philippines)')
            return render(request, 'accounts/band_profile.html', {'user': user})

        try:
            # Update user fields
            user.username = new_username
            user.location = new_location
            user.genres = new_genres
            user.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:band_profile')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    context = {
        'user': user,
        'genre_choices': GENRE_CHOICES,
    }
    return render(request, 'accounts/band_profile.html', context)

# ============================
# Validation Helper Functions
# ============================
def validate_registration_data(username, email, password1, password2, role, selected_instruments, selected_genres):
    """
    Comprehensive validation for registration data.
    Returns a dictionary with field-specific errors and general errors.
    """
    field_errors = {}
    
    # Username validation
    if not username:
        field_errors['username'] = "Username is required."
    elif len(username) < 3:
        field_errors['username'] = "Username must be at least 3 characters long."
    elif len(username) > 30:
        field_errors['username'] = "Username cannot exceed 30 characters."
    elif not re.match(r'^[a-zA-Z0-9_]+$', username):
        field_errors['username'] = "Username can only contain letters, numbers, and underscores."
    elif User.objects.filter(username=username).exists():
        field_errors['username'] = "This username is already taken."
    
    # Email validation
    if not email:
        field_errors['email'] = "Email is required."
    else:
        try:
            validate_email(email)
        except ValidationError:
            field_errors['email'] = "Please enter a valid email address."
        
        if User.objects.filter(email=email).exists():
            field_errors['email'] = "An account with this email already exists."
    
    # Enhanced password validation
    if not password1:
        field_errors['password1'] = "Password is required."
    elif len(password1) < 8:
        field_errors['password1'] = "Password must be at least 8 characters long."
    elif len(password1) > 128:
        field_errors['password1'] = "Password cannot exceed 128 characters."
    else:
        # Check password strength requirements
        password_issues = []
        if not re.search(r'[a-z]', password1):
            password_issues.append("lowercase letter")
        if not re.search(r'[A-Z]', password1):
            password_issues.append("uppercase letter")
        if not re.search(r'[0-9]', password1):
            password_issues.append("number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            password_issues.append("special character")
        
        if password_issues:
            if len(password_issues) == 1:
                field_errors['password1'] = f"Password must contain at least one {password_issues[0]}."
            else:
                field_errors['password1'] = f"Password must contain at least one: {', '.join(password_issues)}."
        
        # Check for common weak passwords
        weak_passwords = ['password', '12345678', 'qwerty123', 'admin123', 'welcome123']
        if password1.lower() in weak_passwords:
            field_errors['password1'] = "This password is too common. Please choose a stronger password."
    
    # Password confirmation
    if password1 != password2:
        field_errors['password2'] = "Passwords do not match."
    
    # Role validation
    if not role:
        field_errors['role'] = "Please select a role (Musician or Band)."
    elif role not in ['musician', 'band']:
        field_errors['role'] = "Please select a valid role."
    
    # Role-specific validation
    if role == 'musician':
        if not selected_instruments:
            field_errors['instruments'] = "Musicians must select at least one instrument."
        if not selected_genres:
            field_errors['genres'] = "Musicians must select at least one musical genre."
    elif role == 'band':
        if not selected_genres:
            field_errors['genres'] = "Bands must select at least one musical genre."
    
    return field_errors

# ============================
# Registration View
# ============================
@csrf_protect
def register(request):
    if request.method == 'POST':
        # --- Get form data ---
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        role = request.POST.get('role', '')
        
        # Get multi-select values
        selected_instruments = request.POST.getlist('instruments')  # getlist for multiple values
        selected_genres = request.POST.getlist('genres')  # getlist for multiple values

        # --- Comprehensive Validation ---
        field_errors = validate_registration_data(
            username, email, password1, password2, role, 
            selected_instruments, selected_genres
        )
        
        if field_errors:
            # Add field-specific errors to messages for display
            for field, error in field_errors.items():
                messages.error(request, error)
            
            return render(request, 'accounts/register.html', {
                'genre_choices': GENRE_CHOICES,
                'instrument_choices': INSTRUMENT_CHOICES,
                'selected_instruments': selected_instruments,
                'selected_genres': selected_genres,
                'username': username,
                'email': email,
                'role': role,
                'field_errors': field_errors,
            })

        # --- Create user ---
        try:
            # Convert lists to comma-separated strings
            instruments_str = ', '.join(filter(None, selected_instruments)) if selected_instruments else ''
            genres_str = ', '.join(filter(None, selected_genres)) if selected_genres else ''
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                role=role
            )
            
            # Set instruments and genres if provided
            if instruments_str:
                user.instruments = instruments_str
            if genres_str:
                user.genres = genres_str
            user.save()
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('accounts:login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'accounts/register.html', {
                'genre_choices': GENRE_CHOICES,
                'instrument_choices': INSTRUMENT_CHOICES,
                'selected_instruments': selected_instruments,
                'selected_genres': selected_genres,
                'username': username,
                'email': email,
                'role': role,
                'field_errors': {},
            })

    # Handle GET request
    return render(request, 'accounts/register.html', {
        'genre_choices': GENRE_CHOICES,
        'instrument_choices': INSTRUMENT_CHOICES,
        'selected_instruments': [],
        'selected_genres': [],
        'field_errors': {},
    })


# ============================
# Login View
# ============================
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login successful
            auth_login(request, user)
            
            # Redirect to 'next' page or default to 'listings:feed'
            next_page = request.GET.get('next', 'listings:feed')
            return redirect(next_page)
        else:
            # Login failed
            messages.error(request, 'Invalid username or password!')

    # Handle GET request
    return render(request, 'accounts/login.html')


# ============================
# Logout View
# ============================
@never_cache  # Prevents caching of the logout page
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# ============================
# Profile View
# ============================
def is_valid_location_format(location):
    """
    Validate location format: City, Country
    """
    if not location or location.strip() == '':
        return True  # Empty is okay
    
    # Check for "City, Country" format
    parts = location.split(',')
    if len(parts) != 2:
        return False
    
    city = parts[0].strip()
    country = parts[1].strip()
    
    # Both parts should be non-empty and contain only valid characters
    valid_name_pattern = re.compile(r'^[a-zA-Z\s\-.\'()]+$')
    
    return (city and country and 
            valid_name_pattern.match(city) and 
            valid_name_pattern.match(country))

@login_required
@csrf_protect
def musician_profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        # Get form data
        new_username = request.POST.get('username', '').strip()
        new_location = request.POST.get('location', '').strip()
        new_instruments = request.POST.get('instruments', '').strip()
        new_genres = request.POST.get('genres', '').strip()

        # Validate username if it changed
        if new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'This username is already taken.')
                return render(request, 'accounts/musician_profile.html', {'user': user})
        
        # Validate location format if provided
        if new_location and not is_valid_location_format(new_location):
            messages.error(request, 'Please enter location in the format: City, Country (e.g., Cebu, Philippines)')
            return render(request, 'accounts/musician_profile.html', {'user': user})

        try:
            # Update user fields
            user.username = new_username
            user.location = new_location
            user.instruments = new_instruments
            user.genres = new_genres
            user.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:musician_profile')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    context = {
        'user': user,
        'genre_choices': GENRE_CHOICES,
        'instrument_choices': INSTRUMENT_CHOICES,
    }
    return render(request, 'accounts/musician_profile.html', context)


@login_required
def view_profile(request, username):
    """
    View another user's profile
    """
    from django.shortcuts import get_object_or_404
    
    profile_user = get_object_or_404(User, username=username)
    
    context = {
        'profile_user': profile_user,
        'user': request.user,
        'is_own_profile': request.user == profile_user,
    }
    
    return render(request, 'accounts/view_profile.html', context)


# ============================
# Password Reset Views
# ============================

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .forms import PasswordResetRequestForm, SetPasswordForm
from .emails import send_password_reset_email
from .tokens import password_reset_token


@csrf_protect
def password_reset_request(request):
    """
    Handle password reset request.
    User enters their email address to receive reset link.
    """
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Security: Always redirect to success page regardless of whether email exists
            # This prevents user enumeration attacks
            try:
                user = User.objects.get(email=email, is_active=True)
                # Send password reset email
                send_password_reset_email(request, user, email)
            except User.DoesNotExist:
                # Don't reveal that the user doesn't exist
                pass
            
            # Redirect to success page without using messages framework
            return redirect('accounts:password_reset_done')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_done(request):
    """
    Show confirmation that password reset email has been sent.
    """
    return render(request, 'accounts/password_reset_done.html')


@csrf_protect
def password_reset_confirm(request, uidb64, token):
    """
    Handle password reset confirmation with token validation.
    User clicks link from email and sets new password.
    """
    try:
        # Decode user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Validate token
    if user is not None and password_reset_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                # Redirect to success page without using messages framework
                return redirect('accounts:password_reset_complete')
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'accounts/password_reset_confirm.html', {
            'form': form,
            'validlink': True,
        })
    else:
        # Invalid or expired token - render template with validlink=False
        return render(request, 'accounts/password_reset_confirm.html', {
            'validlink': False,
        })


def password_reset_complete(request):
    """
    Show confirmation that password has been reset successfully.
    """
    return render(request, 'accounts/password_reset_complete.html')