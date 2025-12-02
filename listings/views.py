from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Listing
from .forms import ListingForm
from applications.models import Application
from harmonix.constants import GENRE_CHOICES, INSTRUMENT_CHOICES
from django.core.paginator import Paginator


@login_required
def listings_view(request):
    """
    Main listings page - shows different content based on user role:
    - Musicians see available opportunities they can apply to
    - Band admins see their own listings and can manage them
    """
    user = request.user
    
    # Get filter and sort parameters
    search_query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')
    instrument_filter = request.GET.get('instrument', '')
    location_filter = request.GET.get('location', '')
    sort_by = request.GET.get('sort', 'newest')  # Default to newest
    
    if user.is_musician:
        # Musicians see all active listings
        listings = Listing.objects.filter(is_active=True)
        
        # Apply filters
        if search_query:
            listings = listings.filter(
                Q(title__icontains=search_query) |
                Q(band_name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if genre_filter:
            # Convert filter value to proper case for matching
            genre_display = dict(Listing.GENRE_CHOICES).get(genre_filter, genre_filter)
            listings = listings.filter(genres__icontains=genre_display)
            
        if instrument_filter:
            # Convert filter value to proper case for matching
            instrument_display = dict(Listing.INSTRUMENT_CHOICES).get(instrument_filter, instrument_filter)
            listings = listings.filter(instruments_needed__icontains=instrument_display)
        
        if location_filter:
            listings = listings.filter(location__icontains=location_filter)

        # Apply sorting
        if sort_by == 'oldest':
            listings = listings.order_by('created_at')
        elif sort_by == 'positions':
            # Sort by number of instruments (most positions first)
            # This requires fetching all and sorting in Python since we can't easily do this in SQL
            listings_list = list(listings)
            listings_list.sort(key=lambda x: len(x.instruments_list), reverse=True)
            # Convert back to queryset for pagination
            from django.db.models.query import QuerySet
            # For pagination to work, we need to use the list directly
            listings = listings_list
        else:  # Default to newest
            listings = listings.order_by('-created_at')
        
        # Show all genres and instruments from constants in filters
        filter_options = {
            'genres': GENRE_CHOICES,
            'instruments': INSTRUMENT_CHOICES,
        }
        
    else:  # Band admin
        # Band admins see only their own listings
        listings = Listing.objects.filter(band_admin=user)
        
        # Apply sorting for band admins too
        if sort_by == 'oldest':
            listings = listings.order_by('created_at')
        else:  # Default to newest
            listings = listings.order_by('-created_at')
            
        filter_options = {}  # Band admins don't need filters for their own listings

    # Apply pagination for both musicians and band admins
    paginator = Paginator(listings, 4)  # Show 4 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user': user,
        'listings': page_obj,  # Use paginated listings
        'listings_count': paginator.count,  # Total count for display
        'is_musician': user.is_musician,
        'is_band_admin': user.is_band_admin,
        'filter_options': filter_options,
        'current_filters': {
            'search': search_query,
            'genre': genre_filter,
            'instrument': instrument_filter,
            'location': location_filter,
            'sort': sort_by,
        },
        'page_obj': page_obj,  # Add page object for pagination controls
    }
    
    return render(request, 'listings/listings_feed.html', context)


@login_required
def create_listing(request):
    """
    Create a new listing - only accessible to band admins
    """
    # Check if user is a band admin
    if not request.user.is_band_admin:
        messages.error(request, "Only band admins can create listings.")
        return redirect('listings:feed')
    
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.band_admin = request.user  # Set the current user as the band admin
            listing.save()
            
            messages.success(request, f'Listing "{listing.title}" has been created successfully!')
            return redirect('listings:detail', pk=listing.pk)
        else:
            messages.error(request, "Please fix the errors below and try again.")
    else:
        form = ListingForm()
    
    context = {
        'form': form,
        'user': request.user,
    }
    
    return render(request, 'listings/create_listing.html', context)


@login_required
def listing_detail(request, pk):
    """
    Show detailed view of a specific listing
    """
    listing = get_object_or_404(Listing, pk=pk)
    
    # Determine back URL based on referer or query param
    back_url = request.GET.get('from')
    back_label = "Back to Listings"
    
    if not back_url:
        referer = request.META.get('HTTP_REFERER', '')
        if 'dashboard' in referer:
            back_url = 'musician_dashboard' if request.user.is_musician else 'band_admin_dashboard'
            back_label = "Back to Dashboard"
        elif 'invitations' in referer:
            if request.user.is_musician:
                back_url = 'invitations:musician_invitations'
                back_label = "Back to Invitations"
            else:
                back_url = 'invitations:band_sent_invites'
                back_label = "Back to Invitations"
        else:
            back_url = 'listings:feed'
    else:
        # If 'from' param is provided, set appropriate label
        if back_url in ['musician_dashboard', 'band_admin_dashboard']:
            back_label = "Back to Dashboard"
        elif 'invitations' in back_url:
            back_label = "Back to Invitations"
    
    # Check if current user has already applied (for musicians)
    # Note: Draft applications don't count as "applied"
    user_has_applied = False
    user_application = None
    pending_invitation = None
    
    if request.user.is_musician:
        try:
            user_application = Application.objects.get(
                musician=request.user, 
                listing=listing,
                status__in=['pending', 'accepted', 'rejected']  # Exclude drafts
            )
            user_has_applied = True
        except Application.DoesNotExist:
            pass
        
        # Check if user has a pending invitation for this listing
        from invitations.models import Invitation
        try:
            pending_invitation = Invitation.objects.get(
                musician=request.user,
                listing=listing,
                status='pending'
            )
        except Invitation.DoesNotExist:
            pass
    
    # Get all applications for this listing (for band admin who owns it)
    # Exclude draft applications from the list
    applications = None
    if request.user == listing.band_admin:
        applications = listing.applications.exclude(status='draft').order_by('-created_at')
    
    context = {
        'listing': listing,
        'user': request.user,
        'user_has_applied': user_has_applied,
        'user_application': user_application,
        'pending_invitation': pending_invitation,
        'applications': applications,
        'is_owner': request.user == listing.band_admin,
        'can_apply': request.user.is_musician and not user_has_applied and listing.is_active and not pending_invitation,
        'back_url': back_url,
        'back_label': back_label,
    }
    
    return render(request, 'listings/listing_detail.html', context)


@login_required
def edit_listing(request, pk):
    """
    Edit an existing listing - only accessible to the band admin who created it
    """
    listing = get_object_or_404(Listing, pk=pk)
    
    # Check if user is the owner of this listing
    if request.user != listing.band_admin:
        messages.error(request, "You can only edit your own listings.")
        return redirect('listings:detail', pk=listing.pk)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            listing = form.save()
            messages.success(request, f'Listing "{listing.title}" has been updated successfully!')
            return redirect('listings:detail', pk=listing.pk)
        else:
            messages.error(request, "Please fix the errors below and try again.")
    else:
        form = ListingForm(instance=listing)
    
    context = {
        'form': form,
        'listing': listing,
        'user': request.user,
        'is_editing': True,
    }
    
    return render(request, 'listings/edit_listing.html', context)


@login_required
def delete_listing(request, pk):
    """
    Delete a listing - only accessible to the band admin who created it
    """
    listing = get_object_or_404(Listing, pk=pk)
    
    # Check if user is the owner of this listing
    if request.user != listing.band_admin:
        messages.error(request, "You can only delete your own listings.")
        return redirect('listings:detail', pk=listing.pk)
    
    if request.method == 'POST':
        listing_title = listing.title
        listing.delete()
        messages.success(request, f'Listing "{listing_title}" has been deleted successfully.')
        return redirect('listings:feed')
    
    # If not POST, redirect back to listing detail
    return redirect('listings:detail', pk=listing.pk)

@login_required
def member_listing_view(request):
    """
    View for band admins to see their own listings and applications
    """
    # Check if user is a band admin
    if not request.user.is_band_admin:
        messages.error(request, "Only band admins can access this page.")
        return redirect('listings:feed')
    
    # Get all listings for the current band admin
    listings = Listing.objects.filter(band_admin=request.user).order_by('-created_at')
    
    context = {
        'user': request.user,
        'listings': listings,
        'genre_choices': GENRE_CHOICES,
        'instrument_choices': INSTRUMENT_CHOICES,
    }
    
    return render(request, 'listings/member_listing.html', context)
    