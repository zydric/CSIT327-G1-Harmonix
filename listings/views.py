from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Listing
from .forms import ListingForm
from applications.models import Application


@login_required
def listings_view(request):
    """
    Main listings page - shows different content based on user role:
    - Musicians see available opportunities they can apply to
    - Band admins see their own listings and can manage them
    """
    user = request.user
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')
    instrument_filter = request.GET.get('instrument', '')
    
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
            
        # Order by newest first
        listings = listings.order_by('-created_at')
        
        # Get unique filter options for dropdowns
        all_listings = Listing.objects.filter(is_active=True)
        
        # Get actual genres and instruments from listings
        used_genres = set()
        used_instruments = set()
        
        for listing in all_listings:
            used_genres.update(listing.genres_list)
            used_instruments.update(listing.instruments_list)
        
        # Create filter options with proper case matching
        # Convert used items to lowercase for comparison
        used_genres_lower = {g.lower() for g in used_genres}
        used_instruments_lower = {i.lower() for i in used_instruments}
        
        # Filter to only show genres/instruments that are actually used
        filter_options = {
            'genres': [choice for choice in Listing.GENRE_CHOICES if choice[0] in used_genres_lower],
            'instruments': [choice for choice in Listing.INSTRUMENT_CHOICES if choice[0] in used_instruments_lower],
        }
        
    else:  # Band admin
        # Band admins see only their own listings
        listings = Listing.objects.filter(band_admin=user).order_by('-created_at')
        filter_options = {}  # Band admins don't need filters for their own listings
    
    context = {
        'user': user,
        'listings': listings,
        'listings_count': listings.count(),
        'is_musician': user.is_musician,
        'is_band_admin': user.is_band_admin,
        'filter_options': filter_options,
        'current_filters': {
            'search': search_query,
            'genre': genre_filter,
            'instrument': instrument_filter,
        }
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
    
    # Check if current user has already applied (for musicians)
    user_has_applied = False
    user_application = None
    
    if request.user.is_musician:
        try:
            user_application = Application.objects.get(
                musician=request.user, 
                listing=listing
            )
            user_has_applied = True
        except Application.DoesNotExist:
            pass
    
    # Get all applications for this listing (for band admin who owns it)
    applications = None
    if request.user == listing.band_admin:
        applications = listing.applications.all().order_by('-created_at')
    
    context = {
        'listing': listing,
        'user': request.user,
        'user_has_applied': user_has_applied,
        'user_application': user_application,
        'applications': applications,
        'is_owner': request.user == listing.band_admin,
        'can_apply': request.user.is_musician and not user_has_applied and listing.is_active,
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
    }
    
    return render(request, 'listings/member_listing.html', context)
    