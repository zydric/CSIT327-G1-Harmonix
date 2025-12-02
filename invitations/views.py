from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.models import User
from listings.models import Listing
from .models import Invitation
import datetime
from datetime import datetime, timedelta

@login_required
def band_admin_invite_musicians(request):
    """Display all musicians for band admins to invite (Band Admin View)"""
    
    # Only band admins can access this page
    if not request.user.is_band_admin:
        messages.error(request, "Access denied. Only band admins can invite musicians.")
        return redirect('listings:feed')
    
    # Get all musicians - prioritize available musicians
    musicians = User.objects.filter(role='musician').order_by('-availability', 'username')
    
    # Get band admin's active listings for the dropdown
    active_listings = Listing.objects.filter(band_admin=request.user, is_active=True)
    
    context = {
        'musicians': musicians,
        'active_listings': active_listings,
    }
    
    return render(request, 'invitations/band_admin_invite.html', context)


@login_required
def musician_received_invitations(request):
    """Display invitations received by musician (Musician View)"""
    
    # Only musicians can access this page
    if not request.user.is_musician:
        messages.error(request, "Access denied. Only musicians can view invitations.")
        return redirect('listings:feed')
    
    # Get all invitations for this musician
    invitations = Invitation.objects.filter(musician=request.user).select_related('band_admin', 'listing')
    
    context = {
        'invitations': invitations,
    }
    
    return render(request, 'invitations/musician_invitations.html', context)


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
        message = data.get('message', '').strip()
        
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
            listing=listing,
            message=message if message else None
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Invitation sent to {musician.username} for "{listing.title}"!'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

"""
FOR TREASURE:
In the frontend it can be entered as 
{% for inv in invitations %}

{{ inv.get_status_display }}
{{ inv.musician.username }}
{{ inv.listing.title }}
{{ inv.listing.description }}

{% endfor %}
refer to models.py in the invitations folder and listings folder for more details
"""
@login_required
@csrf_exempt
def band_sent_invitations(request):
    """Display invitations sent by band admins (Band Admin View)"""
    
    # Only band admins can access this page
    if not request.user.is_band_admin:
        messages.error(request, "Access denied. Only band admins can view sent invitations.")
        return redirect('listings:feed')
    
    # Get all invitations sent by this band admin
    invitations = Invitation.objects.filter(band_admin=request.user).select_related('musician', 'listing')
    
    context = {
        'invitations': invitations,
    }
    #Change the html here according to your own page
    return render(request, 'invitations/band_sent_invites.html', context)

@login_required
@csrf_exempt
def respond_to_invitation(request):
    """Handle musician's response to invitation (accept/decline)"""
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    
    # Only musicians can respond to invitations
    if not request.user.is_musician:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        invitation_id = data.get('invitation_id')
        response = data.get('response')  # 'accepted' or 'declined'
        
        if response not in ['accepted', 'declined']:
            return JsonResponse({'error': 'Invalid response'}, status=400)
        
        # Get the invitation
        invitation = get_object_or_404(Invitation, id=invitation_id, musician=request.user, status='pending')
        
        # Update the invitation status
        invitation.status = response
        invitation.save()
        
        action = 'accepted' if response == 'accepted' else 'declined'
        
        return JsonResponse({
            'success': True,
            'message': f'You have {action} the invitation for "{invitation.listing.title}"!'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_listing_details(request, listing_id):
    """Get detailed information about a listing for the modal"""
    
    try:
        listing = get_object_or_404(Listing, id=listing_id, is_active=True)
        
        data = {
            'id': listing.id,
            'title': listing.title,
            'band_name': listing.band_name,
            'band_admin': listing.band_admin.username,
            'description': listing.description,
            'instruments_needed': listing.instruments_list,
            'genres': listing.genres_list,
            'location': listing.band_admin.location or 'Not specified',
            'posted_date': listing.posted_date_display,
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def band_sent_invites(request):
    # --- MOCK DATA START ---
    # We create a list of dictionaries that look exactly like your database models
    mock_invitations = [
        {
            'id': 1,
            'status': 'pending',
            'created_at': datetime.now() - timedelta(days=2), # Sent 2 days ago
            'message': "We love your drumming style! Would you be interested in jamming with us this weekend? We have a gig coming up at the Roxy.",
            'listing': {
                'title': 'Indie Rock Drummer Needed'
            },
            'recipient': {
                'username': 'alexdrums',
                'get_full_name': 'Alex Martinez', # In a dict, we just put the string here
                'profile': {
                    'location': 'Los Angeles, CA',
                    'instrument': 'Drums, Percussion'
                }
            }
        },
        {
            'id': 2,
            'status': 'accepted',
            'created_at': datetime.now() - timedelta(days=10), # Sent 10 days ago
            'message': "Hey Sarah! We are looking for a synth player for our pop cover band. Check out our profile!",
            'listing': {
                'title': 'Synth Pop Keys Needed'
            },
            'recipient': {
                'username': 'sarahkeys',
                'get_full_name': 'Sarah Jenkins',
                'first_name': 'Sarah', # Needed for the 'accepted' footer message
                'profile': {
                    'location': 'San Diego, CA',
                    'instrument': 'Piano, Synthesizer'
                }
            }
        }
    ]
    # --- MOCK DATA END ---

    return render(request, 'invitations/band_sent_invites.html', {
        'invitations': mock_invitations
    })