from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.models import User
from listings.models import Listing
from .models import Invitation


@login_required
def invites_page(request):
    """Display all musicians for band admins to invite"""
    
    # Only band admins can access this page
    if not request.user.is_band_admin:
        messages.error(request, "Access denied. Only band admins can invite musicians.")
        return redirect('listings:feed')
    
    # Get all musicians
    musicians = User.objects.filter(role='musician').order_by('username')
    
    # Get band admin's active listings for the dropdown
    active_listings = Listing.objects.filter(band_admin=request.user, is_active=True)
    
    context = {
        'musicians': musicians,
        'active_listings': active_listings,
    }
    
    return render(request, 'invitations/invite_musicians.html', context)


@login_required
@csrf_exempt
def send_invitation(request):
    """Send invitation to a musician for a specific listing"""
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    
    # Only band admins can send invitations
    if not request.user.is_band_admin:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        musician_id = data.get('musician_id')
        listing_id = data.get('listing_id')
        
        # Validate musician
        musician = get_object_or_404(User, id=musician_id, role='musician')
        
        # Validate listing belongs to the current band admin
        listing = get_object_or_404(Listing, id=listing_id, band_admin=request.user, is_active=True)
        
        # Check if invitation already exists
        existing_invitation = Invitation.objects.filter(
            band_admin=request.user,
            musician=musician,
            listing=listing
        ).first()
        
        if existing_invitation:
            return JsonResponse({
                'error': f'You have already invited {musician.username} for this listing.'
            }, status=400)
        
        # Create the invitation
        invitation = Invitation.objects.create(
            band_admin=request.user,
            musician=musician,
            listing=listing
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Invitation sent to {musician.username} for "{listing.title}"!'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
