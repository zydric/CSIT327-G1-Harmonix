from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from .models import Application
from listings.models import Listing


@login_required
def apply_to_listing(request, pk):
    """
    Handle musician applications to band listings (both draft and submit)
    """
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    
    # Only musicians can apply
    if not request.user.is_musician:
        messages.error(request, "Only musicians can apply to listings.")
        return redirect('listings:detail', pk=listing.pk)
    
    # Check if already submitted a non-draft application
    existing_submitted = Application.objects.filter(
        musician=request.user, 
        listing=listing, 
        status__in=['pending', 'accepted', 'rejected']
    ).exists()
    
    if existing_submitted:
        messages.warning(request, "You have already applied to this listing.")
        return redirect('listings:detail', pk=listing.pk)
    
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        action = request.POST.get('action', 'submit')  # 'draft' or 'submit'
        
        # Get or create draft application
        existing_draft = Application.objects.filter(
            musician=request.user, 
            listing=listing, 
            status='draft'
        ).first()
        
        if action == 'draft':
            if existing_draft:
                # Update existing draft
                existing_draft.message = message
                existing_draft.save()
            else:
                # Create new draft
                Application.objects.create(
                    musician=request.user,
                    listing=listing,
                    message=message,
                    status='draft'
                )
            messages.success(request, f"Your draft application to '{listing.title}' has been saved!")
            
            # Check if redirect parameter is provided for draft saves too
            redirect_to = request.POST.get('redirect_to', 'listing')
            if redirect_to == 'my_applications':
                return redirect('applications:my_applications')
        else:
            # Submit application (change draft to pending or create new)
            if existing_draft:
                existing_draft.message = message
                existing_draft.status = 'pending'
                existing_draft.save()
            else:
                Application.objects.create(
                    musician=request.user,
                    listing=listing,
                    message=message,
                    status='pending'
                )
            messages.success(request, f"Your application to '{listing.title}' has been submitted!")
        
        # Check if redirect parameter is provided
        redirect_to = request.POST.get('redirect_to', 'listing')
        if redirect_to == 'my_applications':
            return redirect('applications:my_applications')
        else:
            return redirect('listings:detail', pk=listing.pk)
    
    # GET request - redirect to listing detail (applications are handled via modal)
    return redirect('listings:detail', pk=listing.pk)


@login_required
def update_application_status(request, pk):
    """
    Update application status (accept/reject) - only for band admins
    """
    application = get_object_or_404(Application, pk=pk)
    
    # Check if user is the band admin who owns this listing
    if request.user != application.listing.band_admin:
        return HttpResponseForbidden("You can only manage applications to your own listings.")
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['accepted', 'rejected']:
            old_status = application.get_status_display()
            application.status = new_status
            application.save()
            
            status_display = application.get_status_display()
            messages.success(
                request, 
                f"Application from {application.musician.username} has been {status_display.lower()}."
            )
        else:
            messages.error(request, "Invalid status provided.")
    
    # Redirect to 'next' parameter if provided, otherwise to my_applications
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('applications:my_applications')


@login_required
def withdraw_application(request, pk):
    """
    Allow musicians to withdraw their pending applications
    """
    application = get_object_or_404(Application, pk=pk)
    
    # Check if user owns this application
    if request.user != application.musician:
        return HttpResponseForbidden("You can only withdraw your own applications.")
    
    # Only pending applications and drafts can be withdrawn
    if application.status not in ['pending', 'draft']:
        messages.error(request, "Only pending applications and drafts can be withdrawn.")
        return redirect('applications:my_applications')
    
    if request.method == 'POST':
        listing_title = application.listing.title
        application.delete()
        messages.success(request, f"Your application to '{listing_title}' has been withdrawn.")
        return redirect('applications:my_applications')
    
    # If not POST, redirect back
    return redirect('applications:my_applications')


@login_required 
def my_applications(request):
    """
    Show musician's applications or band admin's received applications
    """
    if request.user.is_musician:
        # Show applications made by this musician
        applications = Application.objects.filter(musician=request.user).order_by('-created_at')
        context = {
            'applications': applications,
            'user': request.user,
        }
        return render(request, 'applications/my_applications.html', context)
    else:
        # Show applications to this band's listings (exclude drafts)
        applications = Application.objects.filter(
            listing__band_admin=request.user
        ).exclude(status='draft').order_by('-created_at')
        context = {
            'applications': applications,
            'user': request.user,
        }
        return render(request, 'applications/received_applications.html', context)


@login_required
def get_draft_application(request, listing_pk):
    """
    Get draft application for a specific listing (AJAX endpoint)
    """
    if not request.user.is_musician:
        return JsonResponse({'error': 'Only musicians can access drafts'}, status=403)
    
    try:
        listing = get_object_or_404(Listing, pk=listing_pk)
        draft = Application.objects.filter(
            musician=request.user,
            listing=listing,
            status='draft'
        ).first()
        
        if draft:
            return JsonResponse({
                'exists': True,
                'message': draft.message,
                'application_id': draft.pk
            })
        else:
            return JsonResponse({'exists': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)